"""Out-of-sample checks: the same rules as the study, applied to the years before
(2011-2015) and after (2026 to date) the 2016-2025 study window.

Not part of the headline result. Nothing in config.py changes except the date range
used here, and only aggregate statistics are written (no per-day levels).

    python src/out_of_sample.py     # needs data/raw/ with 2011-2026 files
    -> results/out_of_sample.md
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from analyze import rate, two_prop_p  # noqa: E402
from sessions import build_days, load_raw  # noqa: E402


def _stats(d):
    pat, rest = d[d["asia_engulfs_london"]], d[~d["asia_engulfs_london"]]
    k1, n1 = int(pat["ny_break_high"].sum()), len(pat)
    k2, n2 = int(rest["ny_break_high"].sum()), len(rest)
    gap = 100 * (k1 / n1 - k2 / n2) if n1 and n2 else float("nan")
    return pat, rest, gap, two_prop_p(k1, n1, k2, n2)


def _row(label, d):
    pat, rest, gap, p = _stats(d)
    return (f"| {label} | {len(d):,} | {rate(d['asia_engulfs_london'])} | **{rate(pat['ny_break_high'])}** "
            f"| {rate(rest['ny_break_high'])} | {gap:+.1f} pts | {p:.3f} |")


def main():
    days = build_days(load_raw()).loc["2011-01-01":]
    valid = days[days["valid"]]
    last = valid.index.max()
    head = ("| Sample | Valid days | Pattern frequency | NY breaks London high, pattern days "
            "| NY breaks London high, other days | Gap | p-value |\n|---|---|---|---|---|---|---|")
    lines = [
        "# Out-of-sample checks: before and after the study window",
        "",
        f"Not part of the headline. Data through {last:%Y-%m-%d}. Same session definitions and rules as the study.",
        f"Trading days found: {len(days):,}; valid: {len(valid):,}; dropped incomplete: "
        f"{int((~days['complete']).sum())}; dropped for a contract roll in the window: "
        f"{int((days['complete'] & days['roll_in_window']).sum())}.",
        "",
        "## Samples",
        "",
        head,
        _row("2011-2015 (before NQStats' window)", valid.loc["2011":"2015"]),
        _row("2016-2025 (study window)", valid.loc["2016":"2025"]),
        _row(f"2026 through {last:%b %d}", valid.loc["2026":]),
        _row(f"2016 through {last:%Y-%m-%d} (study window plus 2026)", valid.loc["2016":]),
        _row("2011-2025 (15 full years)", valid.loc["2011":"2025"]),
        _row(f"2011 through {last:%Y-%m-%d} (everything)", valid),
        "",
        "NQStats (2016-2025): 81.1% of 175 pattern days (6.9% of 2,542 sessions).",
        "",
        "## By year",
        "",
        "| Year | Pattern days | NY breaks London high, pattern days | Base rate (all valid days) | Dropped days |",
        "|---|---|---|---|---|",
    ]
    for year, g in days.groupby(days.index.year):
        v = g[g["valid"]]
        pat = v[v["asia_engulfs_london"]]
        lines.append(f"| {year} | {len(pat)} | {rate(pat['ny_break_high'])} | {rate(v['ny_break_high'])} "
                     f"| {int((~g['valid']).sum())} |")

    out = ROOT / "results" / "out_of_sample.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
