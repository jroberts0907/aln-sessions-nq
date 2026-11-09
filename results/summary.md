# ALN Sessions: Asia Engulfs London -> NY breaks London high

Data: NQ.v.0 ohlcv-1m, 2020-12-31 to 2026-11-05
Sessions (New York time): Asia 20:00-02:00, London 02:00-08:00, NY 08:00-16:00
Engulf rule: strict (>, <)

Trading days found: 1513; valid: 1508 (dropped 5 incomplete, 0 with a contract roll inside the window)
Pattern frequency: 5.7%  (86/1508, 95% CI 4.6-7.0%)   (NQStats: 6.9%)

## Headline

P(NY breaks London high | Asia engulfs London) = **79.1%  (68/86, 95% CI 69.3-86.3%)**  (NQStats: 81.1%)
P(NY breaks London high | not engulfed) = 74.5%  (1060/1422, 95% CI 72.2-76.7%)
Difference p-value (two-proportion z-test): 0.3477

### Asia engulfs London days

- Breaks London high: **79.1%  (68/86, 95% CI 69.3-86.3%)**
- Breaks London low: 69.8%  (60/86, 95% CI 59.4-78.5%)
- Breaks both: 48.8%  (42/86, 95% CI 38.6-59.2%)
- Breaks neither: 0.0%  (0/86, 95% CI 0.0-4.3%)
- High broken first: 51.2%  (44/86, 95% CI 40.8-61.4%)
  - ...then low also breaks: 40.9%  (18/44, 95% CI 27.7-55.6%)
- Low broken first: 47.7%  (41/86, 95% CI 37.4-58.1%)
  - ...then high also breaks: 56.1%  (23/41, 95% CI 41.0-70.1%)
- Both in the same 1-min bar (order unknown): 1

### All valid days (base rate)

- Breaks London high: **74.8%  (1128/1508, 95% CI 72.5-76.9%)**
- Breaks London low: 70.8%  (1067/1508, 95% CI 68.4-73.0%)
- Breaks both: 46.2%  (697/1508, 95% CI 43.7-48.7%)
- Breaks neither: 0.7%  (10/1508, 95% CI 0.4-1.2%)
- High broken first: 53.4%  (806/1508, 95% CI 50.9-56.0%)
  - ...then low also breaks: 46.5%  (375/806, 95% CI 43.1-50.0%)
- Low broken first: 45.0%  (678/1508, 95% CI 42.5-47.5%)
  - ...then high also breaks: 45.4%  (308/678, 95% CI 41.7-49.2%)
- Both in the same 1-min bar (order unknown): 14

## By year (pattern days)

| Year | Pattern days | Breaks London high | Base rate (all days) |
|---|---|---|---|
| 2020 | 0 | n/a (n=0) | 100.0%  (1/1, 95% CI 20.7-100.0%) |
| 2021 | 15 | 86.7%  (13/15, 95% CI 62.1-96.3%) | 75.2%  (194/258, 95% CI 69.6-80.1%) |
| 2022 | 8 | 75.0%  (6/8, 95% CI 40.9-92.9%) | 69.8%  (180/258, 95% CI 63.9-75.0%) |
| 2023 | 5 | 80.0%  (4/5, 95% CI 37.6-96.4%) | 77.8%  (200/257, 95% CI 72.4-82.5%) |
| 2024 | 13 | 92.3%  (12/13, 95% CI 66.7-98.6%) | 76.1%  (197/259, 95% CI 70.5-80.9%) |
| 2025 | 19 | 84.2%  (16/19, 95% CI 62.4-94.5%) | 77.0%  (197/256, 95% CI 71.4-81.7%) |
| 2026 | 26 | 65.4%  (17/26, 95% CI 46.2-80.6%) | 72.6%  (159/219, 95% CI 66.3-78.1%) |
