"""Turn 1-minute NQ bars into one row per trading day with Asia / London / NY
ranges, the "Asia engulfs London" flag, and whether/when NY broke London's levels.

Like Gabe's HourStat, levels come from slicing the 1-min bars into time windows
(here sessions instead of clock hours) and taking max(High) / min(Low).
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SESSIONS = {"asia": config.ASIA, "london": config.LONDON, "ny": config.NY}


def _minutes(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


# ---------------------------------------------------------------- loading ---

def load_raw(raw_dir: Path | None = None) -> pd.DataFrame:
    """Read every data/raw/*.dbn.zst file into one DataFrame indexed by
    New York time. Columns: open, high, low, close, volume, instrument_id."""
    import databento as db

    raw_dir = raw_dir or ROOT / config.RAW_DIR
    files = sorted(raw_dir.glob("*.dbn.zst"))
    if not files:
        sys.exit(f"No .dbn.zst files in {raw_dir}. Run src/download.py first.")
    frames = [db.DBNStore.from_file(f).to_df() for f in files]
    df = pd.concat(frames)
    return prepare(df)


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    """Databento timestamps are UTC bar-open times. Convert to New York time
    (handles daylight saving), drop duplicate minutes from overlapping files."""
    df = df[~df.index.duplicated(keep="first")].sort_index()
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    df.index = df.index.tz_convert(config.TZ)
    return df[["open", "high", "low", "close", "volume", "instrument_id"]]


# ------------------------------------------------------------- labelling ---

def label_sessions(df: pd.DataFrame) -> pd.DataFrame:
    """Add `session` (asia/london/ny/None) and `day` (the NY trading date the
    bar belongs to; Asia's evening bars roll forward to the next date)."""
    mod = df.index.hour * 60 + df.index.minute
    cal_date = pd.Series(df.index.date, index=df.index)
    session = pd.Series(None, index=df.index, dtype="object")
    day = pd.Series(pd.NaT, index=df.index, dtype="datetime64[ns]")

    for name, (start, end) in SESSIONS.items():
        s, e = _minutes(start), _minutes(end)
        if s < e:
            mask = (mod >= s) & (mod < e)
            shift = pd.Series(False, index=df.index)
        else:  # wraps midnight, e.g. Asia 20:00-02:00
            mask = (mod >= s) | (mod < e)
            shift = pd.Series(mod >= s, index=df.index)
        session[mask] = name
        d = pd.to_datetime(cal_date[mask]) + pd.to_timedelta(shift[mask].astype(int), unit="D")
        day[mask] = d

    out = df.copy()
    out["session"] = session
    out["day"] = day
    return out.dropna(subset=["session"])


# ------------------------------------------------------------ day table ---

def _first_time(bars: pd.DataFrame, cond: pd.Series):
    hits = bars.index[cond.to_numpy()]
    return hits[0] if len(hits) else pd.NaT


def build_days(df: pd.DataFrame) -> pd.DataFrame:
    """One row per trading day. Days with an incomplete session or a contract
    roll inside the Asia->NY window are kept but flagged `valid = False`."""
    bars = label_sessions(df)

    agg = bars.groupby(["day", "session"]).agg(
        high=("high", "max"), low=("low", "min"), bars=("high", "size"))
    wide = agg.unstack("session")
    wide.columns = [f"{sess}_{field}" for field, sess in wide.columns]
    wide = wide.reindex(columns=[f"{s}_{f}" for s in SESSIONS for f in ("high", "low", "bars")])

    instruments = bars.groupby("day")["instrument_id"].nunique()
    wide["roll_in_window"] = instruments.reindex(wide.index).fillna(0) > 1

    complete = pd.Series(True, index=wide.index)
    for name, need in config.MIN_BARS.items():
        complete &= wide[f"{name}_bars"].fillna(0) >= need
    wide["complete"] = complete
    wide["valid"] = complete & ~wide["roll_in_window"]

    # Pattern: Asia engulfs London
    if config.STRICT_ENGULF:
        engulf = (wide["asia_high"] > wide["london_high"]) & (wide["asia_low"] < wide["london_low"])
    else:
        engulf = (wide["asia_high"] >= wide["london_high"]) & (wide["asia_low"] <= wide["london_low"])
    wide["asia_engulfs_london"] = engulf.fillna(False).astype(bool)

    # NY outcome: did NY trade strictly beyond London's high / low, and when first?
    wide["ny_break_high"] = wide["ny_high"] > wide["london_high"]
    wide["ny_break_low"] = wide["ny_low"] < wide["london_low"]

    ny = bars[bars["session"] == "ny"]
    t_high, t_low = {}, {}
    for d, g in ny.groupby("day"):
        lh, ll = wide.at[d, "london_high"], wide.at[d, "london_low"]
        if pd.isna(lh):
            continue
        t_high[d] = _first_time(g, g["high"] > lh)
        t_low[d] = _first_time(g, g["low"] < ll)
    wide["t_break_high"] = pd.Series(t_high, dtype="object").reindex(wide.index)
    wide["t_break_low"] = pd.Series(t_low, dtype="object").reindex(wide.index)

    def first(row):
        th, tl = row["t_break_high"], row["t_break_low"]
        if pd.isna(th) and pd.isna(tl):
            return "neither"
        if pd.isna(tl) or (not pd.isna(th) and th < tl):
            return "high"
        if pd.isna(th) or tl < th:
            return "low"
        return "same_bar"  # both broken inside one 1-min bar; order unknowable
    wide["first_break"] = wide.apply(first, axis=1)

    wide.index.name = "day"
    return wide
