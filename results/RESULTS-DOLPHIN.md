# RESULTS-DOLPHIN: is the reproductive-state x coercion interaction a female-level effect?

Registered in DOLPHIN-PREREG.md. Data: Dataset S1A of Bouchard et al. 2026, PNAS e2531602123 (read inside the job, not redistributed). Made with AI agents working in MV2's name; not yet checked by a human expert.

Checks: {"available_females": 7, "consort_male_constant_within_male": true, "data_sha256": "b1ffe745043525d8b5173cb4b8c62bfd4694637b9ad8b20c8f021856f8f69032", "females": 17, "males": 11, "repro_constant_within_female": true, "rows": 34}

**Verdict: SURVIVES_AT_FEMALE_LEVEL**

| quantity | value |
|---|---|
| slope difference, avoidance on consort_male (available - unavailable), m per unit | 557.65 |
| naive OLS interaction t (trials independent), df | 2.876, 30 |
| naive one-sided p | 0.00367 |
| exact female-level p (one-sided), relabelings | 0.0053, 19448 |
| exact female-level p (two-sided) | 0.0053 |
| naive two-sided p <= 0.05 among relabelings | 0.0637 |
| rank version, exact one-sided p | 0.0855 |
| male relabeling of consort_male, p (B = 19999) | 0.0502 |
| leave one female out, max p (female) | 0.0195 (HRS) |
| leave one male out, max p (male) | 0.0854 (RID) |
| leave one playback out, max p (Pb_ID) | 0.0324 (19) |

## Leave one female out

| female | available | slope diff | exact p |
|---|---|---|---|
| BAD | 0 | 541.84 | 0.0093 |
| CRV | 1 | 572.83 | 0.0102 |
| DCH | 1 | 577.33 | 0.0092 |
| EDE | 0 | 566.15 | 0.0052 |
| GMP | 0 | 556.17 | 0.0044 |
| HRS | 1 | 252.15 | 0.0195 |
| HUF | 0 | 564.36 | 0.0070 |
| KIT | 0 | 565.25 | 0.0091 |
| KIY | 0 | 541.48 | 0.0048 |
| PHO | 1 | 495.49 | 0.0146 |
| PIC | 0 | 573.37 | 0.0094 |
| RHO | 1 | 771.88 | 0.0009 |
| RIP | 0 | 593.98 | 0.0058 |
| RIS | 1 | 634.74 | 0.0071 |
| SKF | 0 | 550.73 | 0.0096 |
| SON | 1 | 548.40 | 0.0120 |
| ZEP | 0 | 527.47 | 0.0063 |

## Secondary claims (two-sided exact female-level p, Holm over 2)

| claim | slope diff | naive one-sided p | exact p two-sided | Holm | naive false alarm |
|---|---|---|---|---|---|
| SRI_avoid | -136.50 | 0.58022 | 0.8778 | 0.8778 | 0.0084 |
| consort_duration | 194.09 | 0.07224 | 0.1395 | 0.2790 | 0.0247 |

## Per female (descriptive)

| female | available | playbacks | avoided | mean avoidance (m) |
|---|---|---|---|---|
| BAD | 0 | 1 | 0 | 0.0 |
| CRV | 1 | 1 | 1 | 88.0 |
| DCH | 1 | 2 | 1 | 3.0 |
| EDE | 0 | 3 | 2 | 12.7 |
| GMP | 0 | 2 | 2 | 11.0 |
| HRS | 1 | 2 | 1 | 87.0 |
| HUF | 0 | 3 | 1 | 8.0 |
| KIT | 0 | 2 | 2 | 12.0 |
| KIY | 0 | 1 | 1 | 40.0 |
| PHO | 1 | 1 | 1 | 106.0 |
| PIC | 0 | 3 | 1 | 2.7 |
| RHO | 1 | 3 | 2 | 10.0 |
| RIP | 0 | 3 | 1 | 15.3 |
| RIS | 1 | 2 | 0 | 0.0 |
| SKF | 0 | 2 | 1 | 6.0 |
| SON | 1 | 1 | 0 | 0.0 |
| ZEP | 0 | 2 | 2 | 41.0 |

## Per male (descriptive)

| male | consort_male | playbacks | mean avoidance, available (m) | mean avoidance, unavailable (m) |
|---|---|---|---|---|
| SMO | 0.3075 | 3 | 12.0 | 12.0 |
| NAT | 0.3167 | 3 | 0.0 | 0.0 |
| COO | 0.3533 | 4 | 0.0 | 48.0 |
| PAS | 0.3837 | 3 | n/a | 10.7 |
| URC | 0.3873 | 2 | n/a | 16.0 |
| DNG | 0.3939 | 3 | 88.0 | 6.0 |
| MOG | 0.4281 | 3 | 0.0 | 0.0 |
| PON | 0.4290 | 4 | 3.0 | 3.0 |
| DEE | 0.4452 | 3 | 62.0 | 10.0 |
| BIG | 0.4967 | 3 | n/a | 18.0 |
| RID | 0.5051 | 3 | 174.0 | 15.0 |

## Predictions (priors fixed in DOLPHIN-PREREG.md)

| prediction | prior | came true |
|---|---|---|
| P1_naive_reproduced | 0.80 | **true** |
| P2_exact_female_p_le_05 | 0.40 | **true** |
| P3_verdict_survives | 0.20 | **true** |
| P4_naive_false_alarm_gt_10pct | 0.60 | false |
| P5_male_relabel_p_le_05 | 0.35 | false |
| P6_rank_exact_p_le_05 | 0.30 | false |
| P7_without_HRS_p_gt_10 | 0.55 | false |

Brier score: 0.274

