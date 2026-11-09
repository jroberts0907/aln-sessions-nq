"""Compute the "Asia engulfs London -> NY breaks London high" statistics.

    python src/analyze.py

Writes results/days.csv (one row per trading day, every input to every number)
and results/summary.md. Beyond replicating the NQStats figures, it reports the
same probabilities on ALL valid days (the base rate) and on non-pattern days:
81.1% only means something if it's measurably different from how often NY
breaks London's high anyway.
"""
import math
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config  # noqa: E402
from sessions import build_days, load_raw  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """95% Wilson score interval for a proportion k/n."""
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return centre - half, centre + half


def two_prop_p(k1: int, n1: int, k2: int, n2: int) -> float:
    """Two-sided p-value, two-proportion z-test (pooled)."""
    if min(n1, n2) == 0:
        return float("nan")
    p = (k1 + k2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    if se == 0:
        return float("nan")
    z = (k1 / n1 - k2 / n2) / se
    return math.erfc(abs(z) / math.sqrt(2))


def rate(mask: pd.Series) -> str:
    k, n = int(mask.sum()), len(mask)
    if n == 0:
        return "n/a (n=0)"
    lo, hi = wilson(k, n)
    return f"{100 * k / n:.1f}%  ({k}/{n}, 95% CI {100 * lo:.1f}-{100 * hi:.1f}%)"


def block(days: pd.DataFrame, title: str) -> list[str]:
    bh, bl = days["ny_break_high"], days["ny_break_low"]
    fb = days["first_break"]
    hf, lf = days[fb == "high"], days[fb == "low"]
    return [
        f"### {title}",
        "",
        f"- Breaks London high: **{rate(bh)}**",
        f"- Breaks London low: {rate(bl)}",
        f"- Breaks both: {rate(bh & bl)}",
        f"- Breaks neither: {rate(~bh & ~bl)}",
        f"- High broken first: {rate(fb == 'high')}",
        f"  - ...then low also breaks: {rate(hf['ny_break_low'])}",
        f"- Low broken first: {rate(fb == 'low')}",
        f"  - ...then high also breaks: {rate(lf['ny_break_high'])}",
        f"- Both in the same 1-min bar (order unknown): {int((fb == 'same_bar').sum())}",
        "",
    ]


def summarize(all_days: pd.DataFrame) -> str:
    start, end = pd.Timestamp(config.STUDY_START), pd.Timestamp(config.STUDY_END)
    days = all_days[(all_days.index >= start) & (all_days.index <= end)]
    valid = days[days["valid"]]
    pat = valid[valid["asia_engulfs_london"]]
    rest = valid[~valid["asia_engulfs_london"]]
    k1, n1 = int(pat["ny_break_high"].sum()), len(pat)
    k2, n2 = int(rest["ny_break_high"].sum()), len(rest)

    lines = [
        "# ALN Sessions: Asia Engulfs London -> NY breaks London high",
        "",
        f"Data: {config.SYMBOL} {config.SCHEMA}, {valid.index.min():%Y-%m-%d} to "
        f"{valid.index.max():%Y-%m-%d}",
        f"Sessions (New York time): Asia {config.ASIA[0]}-{config.ASIA[1]}, "
        f"London {config.LONDON[0]}-{config.LONDON[1]}, NY {config.NY[0]}-{config.NY[1]}",
        f"Engulf rule: {'strict (>, <)' if config.STRICT_ENGULF else 'inclusive (>=, <=)'}",
        "",
        f"Trading days found: {len(days)}; valid: {len(valid)} "
        f"(dropped {int((~days['complete']).sum())} incomplete, "
        f"{int((days['complete'] & days['roll_in_window']).sum())} with a contract roll inside the window)",
        f"Pattern frequency: {rate(valid['asia_engulfs_london'])}   (NQStats: 6.9%)",
        "",
        "## Headline",
        "",
        f"P(NY breaks London high | Asia engulfs London) = **{rate(pat['ny_break_high'])}**  "
        "(NQStats: 81.1%)",
        f"P(NY breaks London high | not engulfed) = {rate(rest['ny_break_high'])}",
        f"Difference p-value (two-proportion z-test): {two_prop_p(k1, n1, k2, n2):.4f}",
        "",
        *block(pat, "Asia engulfs London days"),
        *block(valid, "All valid days (base rate)"),
        "## By year (pattern days)",
        "",
        "| Year | Pattern days | Breaks London high | Base rate (all days) |",
        "|---|---|---|---|",
    ]
    for year, g in valid.groupby(valid.index.year):
        gp = g[g["asia_engulfs_london"]]
        lines.append(f"| {year} | {len(gp)} | {rate(gp['ny_break_high'])} | {rate(g['ny_break_high'])} |")

    later = all_days[all_days["valid"] & (all_days.index > end)]
    if len(later):
        later_pat = later[later["asia_engulfs_london"]]
        combined = all_days[all_days["valid"] & (all_days.index >= start)]
        combined_pat = combined[combined["asia_engulfs_london"]]
        lines += [
            "",
            "## After the study window",
            "",
            f"Not included in the headline. {later.index.min():%Y-%m-%d} to {later.index.max():%Y-%m-%d}:",
            "",
            f"- Pattern frequency: {rate(later['asia_engulfs_london'])}",
            f"- Breaks London high, pattern days: {rate(later_pat['ny_break_high'])}",
            f"- Breaks London high, all days: {rate(later['ny_break_high'])}",
            f"- Study window plus this period, pattern days: {rate(combined_pat['ny_break_high'])}",
        ]
    return "\n".join(lines) + "\n"


def main() -> None:
    days = build_days(load_raw())
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    days.to_csv(out / "days.csv")
    text = summarize(days)
    (out / "summary.md").write_text(text, encoding="utf-8")
    print(text)
    print(f"Wrote {out / 'days.csv'} and {out / 'summary.md'}")


if __name__ == "__main__":
    main()
