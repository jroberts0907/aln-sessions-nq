# ALN Sessions: Asia Engulfs London -> NY breaks London high

Data: NQ.v.0 ohlcv-1m, 2021-01-04 to 2025-12-31
Sessions (New York time): Asia 20:00-02:00, London 02:00-08:00, NY 08:00-16:00
Engulf rule: strict (>, <)

Trading days found: 1292; valid: 1288 (dropped 4 incomplete, 0 with a contract roll inside the window)
Pattern frequency: 4.7%  (60/1288, 95% CI 3.6-6.0%)   (NQStats: 6.9%)

## Headline

P(NY breaks London high | Asia engulfs London) = **85.0%  (51/60, 95% CI 73.9-91.9%)**  (NQStats: 81.1%)
P(NY breaks London high | not engulfed) = 74.7%  (917/1228, 95% CI 72.2-77.0%)
Difference p-value (two-proportion z-test): 0.0707

### Asia engulfs London days

- Breaks London high: **85.0%  (51/60, 95% CI 73.9-91.9%)**
- Breaks London low: 66.7%  (40/60, 95% CI 54.1-77.3%)
- Breaks both: 51.7%  (31/60, 95% CI 39.3-63.8%)
- Breaks neither: 0.0%  (0/60, 95% CI -0.0-6.0%)
- High broken first: 58.3%  (35/60, 95% CI 45.7-69.9%)
  - ...then low also breaks: 42.9%  (15/35, 95% CI 28.0-59.1%)
- Low broken first: 40.0%  (24/60, 95% CI 28.6-52.6%)
  - ...then high also breaks: 62.5%  (15/24, 95% CI 42.7-78.8%)
- Both in the same 1-min bar (order unknown): 1

### All valid days (base rate)

- Breaks London high: **75.2%  (968/1288, 95% CI 72.7-77.4%)**
- Breaks London low: 71.3%  (918/1288, 95% CI 68.7-73.7%)
- Breaks both: 47.0%  (606/1288, 95% CI 44.3-49.8%)
- Breaks neither: 0.6%  (8/1288, 95% CI 0.3-1.2%)
- High broken first: 54.0%  (696/1288, 95% CI 51.3-56.7%)
  - ...then low also breaks: 48.0%  (334/696, 95% CI 44.3-51.7%)
- Low broken first: 44.3%  (570/1288, 95% CI 41.6-47.0%)
  - ...then high also breaks: 45.3%  (258/570, 95% CI 41.2-49.4%)
- Both in the same 1-min bar (order unknown): 14

## By year (pattern days)

| Year | Pattern days | Breaks London high | Base rate (all days) |
|---|---|---|---|
| 2021 | 15 | 86.7%  (13/15, 95% CI 62.1-96.3%) | 75.2%  (194/258, 95% CI 69.6-80.1%) |
| 2022 | 8 | 75.0%  (6/8, 95% CI 40.9-92.9%) | 69.8%  (180/258, 95% CI 63.9-75.0%) |
| 2023 | 5 | 80.0%  (4/5, 95% CI 37.6-96.4%) | 77.8%  (200/257, 95% CI 72.4-82.5%) |
| 2024 | 13 | 92.3%  (12/13, 95% CI 66.7-98.6%) | 76.1%  (197/259, 95% CI 70.5-80.9%) |
| 2025 | 19 | 84.2%  (16/19, 95% CI 62.4-94.5%) | 77.0%  (197/256, 95% CI 71.4-81.7%) |

## After the study window

Not included in the headline. 2026-01-02 to 2026-11-05:

- Pattern frequency: 11.9%  (26/219, 95% CI 8.2-16.8%)
- Breaks London high, pattern days: 65.4%  (17/26, 95% CI 46.2-80.6%)
- Breaks London high, all days: 72.6%  (159/219, 95% CI 66.3-78.1%)
- Study window plus this period, pattern days: 79.1%  (68/86, 95% CI 69.3-86.3%)
