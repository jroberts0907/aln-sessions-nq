# ALN Sessions: Asia Engulfs London -> NY breaks London high

Data: NQ.v.0 ohlcv-1m, 2016-01-04 to 2025-12-31
Sessions (New York time): Asia 20:00-02:00, London 02:00-08:00, NY 08:00-16:00
Engulf rule: strict (>, <)

Trading days found: 2582; valid: 2574 (dropped 8 incomplete, 0 with a contract roll inside the window)
Pattern frequency: 6.6%  (169/2574, 95% CI 5.7-7.6%)   (NQStats: 6.9%)

## Headline

P(NY breaks London high | Asia engulfs London) = **82.2%  (139/169, 95% CI 75.8-87.3%)**  (NQStats: 81.1%)
P(NY breaks London high | not engulfed) = 74.6%  (1794/2405, 95% CI 72.8-76.3%)
Difference p-value (two-proportion z-test): 0.0261

### Asia engulfs London days

- Breaks London high: **82.2%  (139/169, 95% CI 75.8-87.3%)**
- Breaks London low: 74.6%  (126/169, 95% CI 67.5-80.5%)
- Breaks both: 56.8%  (96/169, 95% CI 49.3-64.0%)
- Breaks neither: 0.0%  (0/169, 95% CI 0.0-2.2%)
- High broken first: 53.8%  (91/169, 95% CI 46.3-61.2%)
  - ...then low also breaks: 52.7%  (48/91, 95% CI 42.6-62.7%)
- Low broken first: 45.6%  (77/169, 95% CI 38.2-53.1%)
  - ...then high also breaks: 61.0%  (47/77, 95% CI 49.9-71.2%)
- Both in the same 1-min bar (order unknown): 1

### All valid days (base rate)

- Breaks London high: **75.1%  (1933/2574, 95% CI 73.4-76.7%)**
- Breaks London low: 70.2%  (1807/2574, 95% CI 68.4-71.9%)
- Breaks both: 46.2%  (1189/2574, 95% CI 44.3-48.1%)
- Breaks neither: 0.9%  (23/2574, 95% CI 0.6-1.3%)
- High broken first: 53.6%  (1380/2574, 95% CI 51.7-55.5%)
  - ...then low also breaks: 46.1%  (636/1380, 95% CI 43.5-48.7%)
- Low broken first: 44.9%  (1156/2574, 95% CI 43.0-46.8%)
  - ...then high also breaks: 46.5%  (538/1156, 95% CI 43.7-49.4%)
- Both in the same 1-min bar (order unknown): 15

## By year (pattern days)

| Year | Pattern days | Breaks London high | Base rate (all days) |
|---|---|---|---|
| 2016 | 13 | 76.9%  (10/13, 95% CI 49.7-91.8%) | 70.5%  (182/258, 95% CI 64.7-75.8%) |
| 2017 | 29 | 82.8%  (24/29, 95% CI 65.5-92.4%) | 79.8%  (205/257, 95% CI 74.4-84.2%) |
| 2018 | 21 | 95.2%  (20/21, 95% CI 77.3-99.2%) | 75.1%  (193/257, 95% CI 69.5-80.0%) |
| 2019 | 19 | 68.4%  (13/19, 95% CI 46.0-84.6%) | 75.6%  (195/258, 95% CI 70.0-80.4%) |
| 2020 | 27 | 77.8%  (21/27, 95% CI 59.2-89.4%) | 74.2%  (190/256, 95% CI 68.5-79.2%) |
| 2021 | 15 | 86.7%  (13/15, 95% CI 62.1-96.3%) | 75.2%  (194/258, 95% CI 69.6-80.1%) |
| 2022 | 8 | 75.0%  (6/8, 95% CI 40.9-92.9%) | 69.8%  (180/258, 95% CI 63.9-75.0%) |
| 2023 | 5 | 80.0%  (4/5, 95% CI 37.6-96.4%) | 77.8%  (200/257, 95% CI 72.4-82.5%) |
| 2024 | 13 | 92.3%  (12/13, 95% CI 66.7-98.6%) | 76.1%  (197/259, 95% CI 70.5-80.9%) |
| 2025 | 19 | 84.2%  (16/19, 95% CI 62.4-94.5%) | 77.0%  (197/256, 95% CI 71.4-81.7%) |
