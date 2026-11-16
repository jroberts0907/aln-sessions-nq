# ALN Sessions: Does NY Break London's High When Asia Engulfs London?

Undergraduate research under Dr. Steve Rubin (FMU). This repo independently tests
one claim from the NQStats 10-year *ALN Sessions* study (2016–2025) on E-mini Nasdaq-100 (NQ) futures:

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
- **95% Wilson confidence intervals** on every percentage. Even over ten years the pattern has only 169 days, so the intervals are a few points wide.
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
python -m pytest tests             # synthetic-data checks, plus a check that the raw
                                   # data reproduces the published results (skipped
                                   # if data/raw/ is missing)
```

Raw data is **not** included (Databento license). `results/days.csv` is also left out of
this repo because it holds per-day levels derived from that data. Running `analyze.py`
generates it locally, with one row per trading day and every level and timestamp that the
statistics come from.

## Results

NQ 1-minute bars for ten full calendar years, 2016 through 2025, the same window as the
NQStats study, using the session definitions above. 2,574 of 2,582 trading days were valid;
8 were dropped as incomplete (early closes such as 2018-12-05 and Good Friday, and three
days in the March 2020 crash when trading halted at price limits overnight). No contract
roll fell inside a session window. Full output is in [`results/summary.md`](results/summary.md).

| | This study | NQStats |
|---|---|---|
| Sessions | 2,574 | 2,542 |
| Pattern frequency | 6.6% (169/2,574, 95% CI 5.7–7.6%) | 6.9% (175) |
| NY breaks London high, Asia engulfs London days | **82.2%** (139/169, 95% CI 75.8–87.3%) | 81.1% |
| NY breaks London low, Asia engulfs London days | 74.6% (126/169) | 74.9% |
| NY breaks both | 56.8% (96/169) | 56.0% |
| NY breaks neither | 0 days | 0 days |
| NY breaks London high, all other days | 74.6% (1,794/2,405, 95% CI 72.8–76.3%) | not compared |

The NQStats figures replicate closely: every one falls inside this study's confidence
interval. NY breaks London's high on about 75% of all days, so the useful figure is the
7.6-point gap between pattern and non-pattern days. Over ten years that gap is significant
at the 0.05 level (two-proportion z-test, p = 0.026), though it is a modest edge over the
base rate, not an 81% edge.

| Year | Pattern days | Breaks London high (pattern days) | Base rate (all valid days) |
|---|---|---|---|
| 2016 | 13 | 76.9% (10/13) | 70.5% (182/258) |
| 2017 | 29 | 82.8% (24/29) | 79.8% (205/257) |
| 2018 | 21 | 95.2% (20/21) | 75.1% (193/257) |
| 2019 | 19 | 68.4% (13/19) | 75.6% (195/258) |
| 2020 | 27 | 77.8% (21/27) | 74.2% (190/256) |
| 2021 | 15 | 86.7% (13/15) | 75.2% (194/258) |
| 2022 | 8 | 75.0% (6/8) | 69.8% (180/258) |
| 2023 | 5 | 80.0% (4/5) | 77.8% (200/257) |
| 2024 | 13 | 92.3% (12/13) | 76.1% (197/259) |
| 2025 | 19 | 84.2% (16/19) | 77.0% (197/256) |

Yearly samples are small, so individual years should be read with caution. The rate varies
from year to year: in 2019 it was below the base rate.

**Earlier five-year run.** An earlier version of this study used only 2021–2025: 85.0% (51/60,
95% CI 73.9–91.9%) against 74.7% on other days, p = 0.07. Sixty pattern days was too few to
compare with NQStats' 175, so the window was widened to match theirs.
