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

- Plan, predictions and priors: [DOLPHIN-PREREG.md](DOLPHIN-PREREG.md) (fixed before any statistic)
- Code: [dolphin_test.py](dolphin_test.py) (standard library only), tests:
  [test_dolphin_test.py](test_dolphin_test.py)
- Data: Dataset S1A of the paper's supplement at
  [pnas.org](https://www.pnas.org/doi/10.1073/pnas.2531602123). Not redistributed here;
  save sheet "Dataset S1A" as CSV and pass its path.

```
python -m unittest -v test_dolphin_test
python dolphin_test.py --data Dataset_S1A.csv --out-dir out
```

Results will appear in `results/` with a reading against the pre-registered predictions.

By MV2 of Munim, Inc. (mv2@munimtech.com). Made with AI agents working in MV2's name; no human
expert has checked it yet. Code Apache-2.0; text CC BY 4.0.
