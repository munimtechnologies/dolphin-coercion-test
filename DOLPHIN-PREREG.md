# DOLPHIN-PREREG: do available females really avoid coercive males more, female by female?

Pre-registered 2026-11-22 by MV2 of Munim, Inc. (mv2@munimtech.com). Made with AI agents
working in MV2's name; not yet checked by a human expert. Code Apache-2.0, text CC BY 4.0.

**What was seen before registration.** The 34 rows of Dataset S1A were read by eye to fix the
design: reproductive state never changes within a female (7 of 17 females are "available" in
all their playbacks), and coercion score (`consort_male`) never changes within a male (11
males). We also saw that the largest avoidance (174 m, playback 19, female HRS, male RID) sits at
the highest coercion score, which is why leave-one-out checks and prediction P7 are registered.
No slope, model or test statistic was computed before this file was written.

## 1. The claim

Bouchard, Allen, Sorensen, Kruetzen, Marfurt, Connor & King (2026), "Female dolphins use
individual vocal labels to track coercive males", PNAS 123(24): e2531602123 (with a PNAS
commentary, "Dolphins use names to remember whom to avoid", e2617174123). Thirty-four playbacks of
male signature whistles to 17 wild female bottlenose dolphins at Shark Bay. The headline: females
that were reproductively available moved away further from (and responded longer to) the
whistles of males who consort, and so coerce, at higher rates. In the authors' R script
(Software S1) avoidance distance is modelled by `lmer` with 10 predictors and two interactions
(`consort_male * fem_repro`, `SRI * fem_repro`) plus random intercepts for female and male,
followed by `dredge` model selection and averaging of all models within 2 AICc; the figure
reports p < 0.001 for the consortship-by-state slope, p = 0.003 for SRI and p = 0.01 for
response duration.

## 2. Why it needs this test

Because reproductive state is a property of the female in these data, the state-by-coercion
interaction compares the slopes of 7 females with the slopes of 10 others. A random female
intercept does not protect a between-female slope difference: if one or two females happen to
respond strongly to one high-ranked male, the trial-level interaction can look strong with 34
trials although the evidence rests on very few females. Model selection by `dredge` over the subsets of 12
terms (up to 2^12 candidate models) with 34 observations adds a further, unmeasured, selection step. The clean question: if
the "available" label were given to 7 of the 17 females at random, how often would the
interaction be as large as observed? All C(17, 7) = 19,448 labelings can be enumerated exactly.

No re-analysis or critique of this paper was found (web search 2026-11-22: paper, PubMed record,
PNAS commentary, Phys.org coverage).

## 3. Data

Dataset S1A of the paper's supplement (`pnas.2531602123.sd01.xlsx`, sheet "Dataset S1A", 15,978
bytes, sha256 f07dc49dfb7c04489a179dac1522dfd1a874d2a843ee25fa1a8baf45b9aab39c), converted to CSV
without edits. The job reads the CSV in its sealed work folder and records its sha256 (line
endings normalised). The data are **not** redistributed in this repository; get them from the
PNAS supplement. Checks: 34 rows, 17 females, 11 males, 7 available females, state constant within
female; otherwise DATA_MISMATCH and nothing is graded.

## 4. Statistic

For a given set A of "available" females: S = OLS slope of `Dist_avoid` on `consort_male` among
playbacks to females in A minus the same slope among the other females (each group with its own
intercept; the interaction coefficient of `Dist_avoid ~ consort_male * state`). The paper's
direction is S > 0.

## 5. Tests

* **T0, naive (reproduction of direction).** The OLS t of the interaction with the 34 playbacks
  as independent (df 30), one-sided. This is a stand-in for the paper's model, not a re-fit.
* **T1, PRIMARY: exact female-level test.** S for all 19,448 choices of 7 females;
  p = share of labelings with S at least the observed (observed labeling included). One-sided.
  The two-sided share (|S| at least |S_obs|) is also reported.
* **T2, calibration of T0.** Share of the 19,448 labelings in which the naive two-sided p is
  <= 0.05: the false-alarm rate of trial-level inference when the label is random at female level.
* **T3, rank version.** T1 with `Dist_avoid` replaced by its mid-ranks over the 34 playbacks.
* **T4, male relabeling.** The 11 males' `consort_male` values permuted among males (19,999
  random permutations, seed 20261122), state labels fixed: is it the coercion score, or which
  males were played?
* **T5, robustness.** T1 again after leaving out each female (exact over her remaining
  co-labelings), each male, and each single playback; max p and the unit that gives it.
* **Secondary (two-sided T1, Holm over the two):** `Dist_avoid` on `SRI` x state (paper p 0.003),
  and `Resp_dur` on `consort_male` x state (paper p 0.01), each with its T2 rate.
* Descriptive: per female (state, playbacks, playbacks with avoidance, mean avoidance) and per male
  (coercion score, mean avoidance by female state).

## 6. Verdict (in this order)

1. DATA_MISMATCH: any check of section 3 fails.
2. SURVIVES_AT_FEMALE_LEVEL: T1 p <= 0.05 and the max leave-one-female-out p <= 0.10 and the max
   leave-one-male-out p <= 0.10.
3. FRAGILE_AT_FEMALE_LEVEL: T1 p <= 0.05 otherwise.
4. NOT_SUPPORTED_AT_FEMALE_LEVEL: T1 p > 0.05.

Readings fixed now. SURVIVES: the headline holds when females, not playbacks, are the units; we
will say so plainly. FRAGILE: the effect is real in these data but rests on one female or one male.
NOT_SUPPORTED: with females as units the data cannot distinguish the available females' response
from a chance split of 17 females; this does not show that females do not track males, only that
the published p values do not measure it. The leave-one-playback-out result is exploratory.

## 7. Predictions (priors, Brier score)

| id | prediction | prior |
|---|---|---|
| P1 | T0: S > 0 and naive one-sided p <= 0.05 | 0.80 |
| P2 | T1 one-sided p <= 0.05 | 0.40 |
| P3 | verdict SURVIVES_AT_FEMALE_LEVEL | 0.20 |
| P4 | T2 false-alarm rate > 0.10 | 0.60 |
| P5 | T4 p <= 0.05 | 0.35 |
| P6 | T3 p <= 0.05 | 0.30 |
| P7 | T1 without female HRS: p > 0.10 | 0.55 |

## 8. Limits known now

* Simple slopes replace the paper's 10-covariate mixed model and model averaging; the covariates
  (group size, familiarity, association) are not adjusted for. The test asks whether the core
  contrast is carried by females, not whether the full model is right.
* With 7 of 17 females the smallest possible p is 1/19,448; power is limited, and a non-significant
  T1 is not evidence of no effect.
* Female state is recorded per female, not per playback, in the shared data.
* Videos and metadata of the playbacks are available only from the authors and are not used.

## 9. Process

`gate.py` makes the job wait until this file, `dolphin_test.py` and `test_dolphin_test.py` are
public on GitHub main and identical to its copies; then the unit tests run; then
`python dolphin_test.py --data data/Dataset_S1A.csv --out-dir /out`. Outputs: `dolphin_results.json`
and `RESULTS-DOLPHIN.md`, committed unchanged. Any later change is a dated amendment.
