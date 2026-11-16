"""Regression check against the committed results, using the real Databento files.

Rebuilds every statistic from data/raw/ and compares it to results/summary.md as
committed, so a re-download (new laptop, restored backup) can be confirmed to
reproduce the published study. Skipped when the licensed raw data isn't present.

    python -m pytest tests/test_results_regression.py -v
"""
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import config  # noqa: E402
from analyze import summarize  # noqa: E402
from sessions import build_days, load_raw  # noqa: E402

STUDY_YEARS = range(2016, 2026)
RAW = ROOT / config.RAW_DIR
HAVE_DATA = all((RAW / f"NQ_{config.SCHEMA}_{y}.dbn.zst").exists() for y in STUDY_YEARS)

pytestmark = pytest.mark.skipif(not HAVE_DATA, reason="raw Databento files for 2016-2025 not in data/raw/")

# Figures published in README.md / results/summary.md
EXPECTED = {
    "trading_days": 2582,
    "valid_days": 2574,
    "pattern_days": 169,
    "pattern_break_high": 139,
    "rest_days": 2405,
    "rest_break_high": 1794,
    "all_break_high": 1933,
}
EXPECTED_BY_YEAR = {  # year: (pattern days, pattern breaks high, valid days, all breaks high)
    2016: (13, 10, 258, 182),
    2017: (29, 24, 257, 205),
    2018: (21, 20, 257, 193),
    2019: (19, 13, 258, 195),
    2020: (27, 21, 256, 190),
    2021: (15, 13, 258, 194),
    2022: (8, 6, 258, 180),
    2023: (5, 4, 257, 200),
    2024: (13, 12, 259, 197),
    2025: (19, 16, 256, 197),
}
EXPECTED_INVALID = {"2018-12-05", "2020-03-16", "2020-03-17", "2020-03-18",
                    "2021-04-02", "2023-04-07", "2025-01-09", "2025-11-28"}


@pytest.fixture(scope="module")
def days():
    all_days = build_days(load_raw())
    return all_days


@pytest.fixture(scope="module")
def study(days):
    return days.loc[config.STUDY_START:config.STUDY_END]


def test_headline_counts(study):
    valid = study[study["valid"]]
    pat = valid[valid["asia_engulfs_london"]]
    rest = valid[~valid["asia_engulfs_london"]]
    got = {
        "trading_days": len(study),
        "valid_days": len(valid),
        "pattern_days": len(pat),
        "pattern_break_high": int(pat["ny_break_high"].sum()),
        "rest_days": len(rest),
        "rest_break_high": int(rest["ny_break_high"].sum()),
        "all_break_high": int(valid["ny_break_high"].sum()),
    }
    assert got == EXPECTED


def test_by_year(study):
    valid = study[study["valid"]]
    for year, exp in EXPECTED_BY_YEAR.items():
        v = valid[valid.index.year == year]
        p = v[v["asia_engulfs_london"]]
        got = (len(p), int(p["ny_break_high"].sum()), len(v), int(v["ny_break_high"].sum()))
        assert got == exp, f"{year}: got {got}, expected {exp}"


def test_same_days_excluded(study):
    invalid = {d.strftime("%Y-%m-%d") for d in study.index[~study["valid"]]}
    assert invalid == EXPECTED_INVALID
    assert not study["roll_in_window"].any()


def test_summary_matches_committed(days):
    """Every line of the committed summary.md up to the post-study (2026) section
    must be reproduced exactly. The 2026 section is excluded because it needs a
    2026 download, which is outside the study window."""
    committed = (ROOT / "results" / "summary.md").read_text(encoding="utf-8")
    marker = "\n## After the study window"
    study_only = days.loc[:config.STUDY_END]
    fresh = summarize(study_only)
    assert fresh.split(marker)[0].rstrip() == committed.split(marker)[0].rstrip()
