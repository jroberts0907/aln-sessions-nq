# ALN Sessions: Does NY Break London's High When Asia Engulfs London?

Undergraduate research under Dr. Steve Rubin (FMU). This repo independently tests
one claim from the NQStats 10-year *ALN Sessions* study on E-mini Nasdaq-100 (NQ) futures:

> **Asia Engulfs London:** Asia's high is above London's high and Asia's low is below
> London's low. On these days, NQStats reports that the New York session **breaks
> London's high 81.1%** of the time (n = 175, 6.9% of sessions).

Method follows [Gabe Gonzalez's HourStat project](https://github.com/ElAmoen3D/HourStat-TradingProject):
take 1-minute NQ bars from Databento and slice them into time windows. Here the windows
are sessions instead of clock hours.

## Definitions (New York time, editable in `src/config.py`)

| Session | Window | Notes |
|---|---|---|
| Asia | 20:00 – 02:00 | starts the evening *before* the NY day it belongs to |
| London | 02:00 – 08:00 | |
| New York | 08:00 – 16:00 | NQStats convention. A 09:30 open is a planned robustness check |

- **Engulf:** `asia_high > london_high` and `asia_low < london_low`
- **Break high:** any NY 1-min bar trades strictly above `london_high`
- **First break:** the earlier of the first bar above `london_high` and the first bar below `london_low`. If both happen inside the same 1-minute bar, the order can't be known, so the day is reported as `same_bar` and kept out of the first-break percentages.

## What's different from just re-counting

- **Base rate.** The script also reports how often NY breaks London's high on *every* day and on non-pattern days, and tests whether the difference is significant. 81.1% is only interesting if it beats the unconditional rate.
- **95% Wilson confidence intervals** on every percentage. The five-year study window has 60 pattern days, so the intervals are wide.
- **Contract rolls.** `NQ.v.0` switches contracts by volume. Any day with a roll inside the Asia→NY window is flagged and excluded, because the levels would come from two different contracts.
- **Incomplete sessions** (holidays, outages) are excluded. The threshold is in `config.MIN_BARS`.
- **Timezones.** Databento timestamps are UTC. Everything is converted to `America/New_York`, so daylight saving time is handled correctly.

## Running

```bash
pip install -r requirements.txt
cp .env.example .env.local         # paste your Databento API key (git-ignored)

python src/download.py 2024        # shows the estimated cost, downloads nothing
python src/download.py 2024 --download
#   check your remaining credit in the Databento portal, then repeat for 2025, 2023, ...

python src/analyze.py              # -> results/summary.md, results/days.csv
python -m pytest tests             # synthetic-data checks
```

Raw data is **not** included (Databento license). `results/days.csv` is also left out of
this repo because it holds per-day levels derived from that data. Running `analyze.py`
generates it locally, with one row per trading day and every level and timestamp that the
statistics come from.

## Results

NQ 1-minute bars for five full calendar years, 2021 through 2025, using the session
definitions above. 1,288 of 1,292 trading days were valid; 4 were dropped as incomplete.
No contract roll fell inside a session window. Full output is in
[`results/summary.md`](results/summary.md).

| | This study | NQStats |
|---|---|---|
| NY breaks London high, Asia engulfs London days | **85.0%** (51/60, 95% CI 73.9–91.9%) | 81.1% (n = 175) |
| Pattern frequency | 4.7% (60/1,288, 95% CI 3.6–6.0%) | 6.9% |
| NY breaks London high, all other days | 74.7% (917/1,228, 95% CI 72.2–77.0%) | not compared |

The 81.1% figure falls inside this study's confidence interval, so the rate replicates. The
pattern occurred less often here than NQStats reports: 6.9% is outside this study's interval.
NY breaks London's high on about 75% of all days, so the useful figure is the 10.3-point gap
between pattern and non-pattern days. That gap does not reach significance at the 0.05 level
(two-proportion z-test, p = 0.07).

**The result depends on the window.** The five-year window was chosen after the 2026 data had
been examined, and 2026 is weaker. Through 2026-11-05, 2026 has 26 pattern days and NY broke
London's high on 65.4% of them (17/26, 95% CI 46.2–80.6%), against a 72.6% base rate that
year. The pattern was also more frequent in 2026, at 11.9% of days. Including 2026, the rate
is 79.1% (68/86, 95% CI 69.3–86.3%) and the gap over non-pattern days falls to about 4.6
points (p = 0.35).

| Year | Pattern days | Breaks London high (pattern days) | Base rate (all valid days) |
|---|---|---|---|
| 2021 | 15 | 86.7% (13/15) | 75.2% (194/258) |
| 2022 | 8 | 75.0% (6/8) | 69.8% (180/258) |
| 2023 | 5 | 80.0% (4/5) | 77.8% (200/257) |
| 2024 | 13 | 92.3% (12/13) | 76.1% (197/259) |
| 2025 | 19 | 84.2% (16/19) | 77.0% (197/256) |
| 2026 through Nov 5 (outside the study window) | 26 | 65.4% (17/26) | 72.6% (159/219) |

Yearly samples are small, so individual years should be read with caution.
