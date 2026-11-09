"""Synthetic-data checks for session slicing and break detection.
Run:  python -m pytest tests   (or just  python tests/test_sessions.py)"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from analyze import wilson  # noqa: E402
from sessions import build_days, prepare  # noqa: E402

TZ = "America/New_York"


def make_day(day: str, asia, london, ny_events, instrument=1, ny_instrument=None):
    """One trading day of flat 1-min bars. asia/london = (low, high) ranges,
    printed once each mid-session. ny_events = {"HH:MM": (low, high)}."""
    d = pd.Timestamp(day, tz=TZ)
    idx = pd.date_range(d - pd.Timedelta(hours=4), d + pd.Timedelta(hours=16),
                        freq="1min", inclusive="left")  # prev 20:00 -> 16:00
    mid = (london[0] + london[1]) / 2
    df = pd.DataFrame({"open": mid, "high": mid, "low": mid, "close": mid,
                       "volume": 1, "instrument_id": instrument}, index=idx)
    df.loc[d - pd.Timedelta(hours=1), ["low", "high"]] = asia          # 23:00 prev day
    df.loc[d + pd.Timedelta(hours=5), ["low", "high"]] = london        # 05:00
    for t, (lo, hi) in ny_events.items():
        h, m = map(int, t.split(":"))
        df.loc[d + pd.Timedelta(hours=h, minutes=m), ["low", "high"]] = (lo, hi)
    if ny_instrument is not None:
        df.loc[df.index >= d + pd.Timedelta(hours=8), "instrument_id"] = ny_instrument
    df.index = df.index.tz_convert("UTC")  # what Databento delivers
    return df


def run(*frames):
    return build_days(prepare(pd.concat(frames)))


def test_engulf_and_break_order():
    # EST day and an EDT day, to catch timezone/DST mistakes
    a = make_day("2025-03-04", asia=(100, 200), london=(120, 180),
                 ny_events={"09:00": (150, 185), "10:00": (110, 150)})
    b = make_day("2025-03-11", asia=(130, 170), london=(120, 180),
                 ny_events={"08:30": (115, 150)})
    days = run(a, b)
    r1, r2 = days.loc["2025-03-04"], days.loc["2025-03-11"]

    assert r1["valid"] and r1["asia_engulfs_london"]
    assert (r1["asia_high"], r1["asia_low"]) == (200, 100)
    assert (r1["london_high"], r1["london_low"]) == (180, 120)
    assert r1["ny_break_high"] and r1["ny_break_low"]
    assert r1["first_break"] == "high"
    assert r1["t_break_high"] == pd.Timestamp("2025-03-04 09:00", tz=TZ)

    assert r2["valid"] and not r2["asia_engulfs_london"]   # London engulfs Asia
    assert not r2["ny_break_high"] and r2["ny_break_low"]
    assert r2["first_break"] == "low"


def test_same_bar_and_roll():
    a = make_day("2025-06-10", asia=(100, 200), london=(120, 180),
                 ny_events={"09:30": (110, 190)})
    b = make_day("2025-06-11", asia=(100, 200), london=(120, 180),
                 ny_events={}, ny_instrument=2)
    days = run(a, b)
    assert days.loc["2025-06-10", "first_break"] == "same_bar"
    assert days.loc["2025-06-11", "roll_in_window"]
    assert not days.loc["2025-06-11", "valid"]
    assert days.loc["2025-06-11", "first_break"] == "neither"


def test_wilson():
    lo, hi = wilson(81, 100)
    assert 0.72 < lo < 0.73 and 0.87 < hi < 0.88


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
