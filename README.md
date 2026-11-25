# dolphin-coercion-test

An open, pre-registered test of the headline of Bouchard et al. (2026), "Female dolphins use
individual vocal labels to track coercive males" (PNAS 123(24): e2531602123): reproductively
available females avoid the whistles of frequently consorting (coercive) males more.

In the published data, reproductive state never changes within a female, so the key interaction
compares 7 females with 10 others. This test enumerates all 19,448 ways of calling 7 of the 17
females "available", keeping each female's playbacks together, and asks how often the
interaction is as strong as observed. It also measures how often the usual trial-level test
reports significance when the label is random at female level, and checks single females,
single males and single playbacks.

## Result (2026-11-25): SURVIVES_AT_FEMALE_LEVEL ([READING-DOLPHIN.md](READING-DOLPHIN.md))

- Exact female-level p = 0.0053 (19,448 labelings); no single female or male removes it
  (largest leave-one-out p 0.0195 and 0.0854).
- Qualified: the rank version gives p = 0.0855, and shuffling consort scores among males gives
  p = 0.0502. The two secondary effects (association and response duration) are not significant
  at the female level (p 0.878 and 0.140).
- The naive trial-level test's false-alarm rate was 6.4%, close to nominal.
- Brier score of our registered predictions: 0.274 (we expected the effect to fail).

## Files

- Plan, predictions and priors: [DOLPHIN-PREREG.md](DOLPHIN-PREREG.md) (fixed before any statistic)
- Code: [dolphin_test.py](dolphin_test.py) (standard library only), tests:
  [test_dolphin_test.py](test_dolphin_test.py)
- Results, unchanged job output: [results/dolphin_results.json](results/dolphin_results.json),
  [results/RESULTS-DOLPHIN.md](results/RESULTS-DOLPHIN.md)
- Data: Dataset S1A of the paper's supplement at
  [pnas.org](https://www.pnas.org/doi/10.1073/pnas.2531602123). Not redistributed here;
  save sheet "Dataset S1A" as CSV and pass its path.

```
python -m unittest -v test_dolphin_test
python dolphin_test.py --data Dataset_S1A.csv --out-dir out
```

Part of MV2's ledger of calibrated re-tests of animal-communication claims:
https://github.com/munimtechnologies/calibrated-animal-claims

By MV2 of Munim, Inc. (mv2@munimtech.com). Made with AI agents working in MV2's name; no human
expert has checked it yet. Code Apache-2.0; text CC BY 4.0.
