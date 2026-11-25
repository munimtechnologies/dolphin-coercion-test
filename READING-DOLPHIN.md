# READING-DOLPHIN: does the dolphin coercion effect hold with females as the units?

MV2, Munim, Inc. (mv2@munimtech.com), 2026-11-25. Made with AI agents working in MV2's name; no
human expert has checked it yet. Text CC BY 4.0. Every number below comes from
[results/dolphin_results.json](results/dolphin_results.json) and
[results/RESULTS-DOLPHIN.md](results/RESULTS-DOLPHIN.md), written unchanged by job
dolphin-coercion-v1 (run 2026-11-25 12:00-12:09 UTC; unit tests passed; gate.py checked the plan
and code against GitHub main before computing). Plan: [DOLPHIN-PREREG.md](DOLPHIN-PREREG.md),
public 2026-11-22.

Claim under test: Bouchard, Allen, Sorensen, Kruetzen, Marfurt, Connor and King (2026), "Female
dolphins use individual vocal labels to track coercive males", PNAS 123(24): e2531602123:
reproductively available females move away further from the signature whistles of males who
consort (and so coerce) more often. Data: Dataset S1A of the paper's supplement (34 playbacks,
17 females, 11 males), read inside the job and not redistributed here.

## Registered verdict: SURVIVES_AT_FEMALE_LEVEL

In these data reproductive state is a property of the female (7 "available" females, 10 others),
so the key interaction compares two groups of females, not 34 independent trials. We computed the
interaction (the slope of avoidance distance on the male's consort score, available minus
unavailable) for **all 19,448 ways** of calling 7 of the 17 females "available".

| quantity | value |
|---|---|
| observed slope difference (m per unit of consort score) | 557.65 |
| exact female-level p, one-sided (19,448 labelings) | 0.0053 |
| naive trial-level t (df 30), one-sided p | 2.876, 0.0037 |
| naive two-sided p <= 0.05 among the 19,448 labelings (false-alarm rate) | 0.064 |
| leave one female out: largest p (female HRS) | 0.0195 |
| leave one male out: largest p (male RID) | 0.0854 |
| leave one playback out: largest p (playback 19) | 0.0324 |
| rank version, exact one-sided p | 0.0855 |
| male relabeling of the consort score (19,999 permutations), p | 0.0502 |

The verdict rule (exact p <= 0.05, every leave-one-female-out p <= 0.10, every leave-one-male-out
p <= 0.10) is met. **The headline holds with females, not playbacks, as the units.** Before the
run we gave this verdict a probability of only 0.20.

## What qualifies it

- **It rests on the size of a few long avoidances.** With avoidance distances replaced by ranks the
  exact p is 0.0855. Three females never moved away (0 m), and three available females have mean
  avoidances of 87 to 106 m, against at most 41 m for any unavailable female.
- **Which males were played is nearly as good an explanation as their consort score.** Shuffling
  the consort scores among the 11 males gives p = 0.0502, just above 0.05. Each male's whistle was
  played only 2 to 4 times.
- **The trial-level analysis was not badly miscalibrated here.** With the label randomised at the
  female level, the naive trial-level test fired in 6.4% of labelings at a nominal 5%. Our worry
  that 34 trials overstate 17 females was mostly unfounded for this contrast.
- **The two secondary effects do not hold at the female level.** Our registered female-level
  versions of them: association (SRI) by state on avoidance, slope difference -136.5, exact
  two-sided p 0.878; consort score by state on response duration, slope difference 194.1, exact
  two-sided p 0.140 (Holm-adjusted 0.279). The paper reports p = 0.003 and p = 0.01 from its
  model-averaged mixed models.

## Predictions (priors fixed in DOLPHIN-PREREG.md)

| id | prediction | prior | outcome | Brier |
|---|---|---|---|---|
| P1 | naive interaction positive, one-sided p <= 0.05 | 0.80 | true | 0.040 |
| P2 | exact female-level p <= 0.05 | 0.40 | true | 0.360 |
| P3 | verdict SURVIVES_AT_FEMALE_LEVEL | 0.20 | true | 0.640 |
| P4 | naive false-alarm rate > 0.10 | 0.60 | false | 0.360 |
| P5 | male relabeling p <= 0.05 | 0.35 | false | 0.123 |
| P6 | rank version p <= 0.05 | 0.30 | false | 0.090 |
| P7 | without female HRS, p > 0.10 | 0.55 | false | 0.303 |

Mean Brier score 0.274. We expected the effect to rest on one female (HRS, who gave the largest
single avoidance, 174 m, to the most coercive male); it does not (without her, p = 0.0195).

## Limits

- Simple slopes replace the paper's mixed model with 10 covariates and AICc model averaging; group
  size, familiarity and association are not adjusted for. The test asks whether the core contrast
  is carried by females, not whether the full model is right.
- 17 females and 11 males; the smallest possible exact p is 1/19,448.
- The secondary tests are our stand-ins for the paper's results, not refits of its models.
- This was done with AI agents working in MV2's name and has not been checked by a human expert.
