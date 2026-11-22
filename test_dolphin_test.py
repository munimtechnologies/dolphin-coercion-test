# Copyright 2026 MV2, Munim, Inc. Licensed under the Apache License, Version 2.0 (Apache-2.0).
# Made with AI agents working in MV2's name.
"""Unit tests of dolphin_test.py on hand-checked toy data (standard library only)."""
import csv
import json
import os
import tempfile
import unittest

import dolphin_test as dt


def row(i, female, male, avail, x, y, sri=0.0, dur=0.0):
    return {"id": i, "female": female, "male": male, "avail": avail, "consort_male": x,
            "SRI": sri, "avoid": y, "dur": dur}


def toy():
    # F1, F2 available: avoidance 0 at x = 0 and 10 at x = 1 (slope 10).
    # F3, F4 unavailable: avoidance 0 at both (slope 0). Observed slope difference = 10.
    rows, i = [], 1
    for f, a, y1 in (("F1", 1, 10.0), ("F2", 1, 10.0), ("F3", 0, 0.0), ("F4", 0, 0.0)):
        rows.append(row(i, f, "M0", a, 0.0, 0.0))
        rows.append(row(i + 1, f, "M1", a, 1.0, y1))
        i += 2
    return rows


class TestT(unittest.TestCase):
    def test_cauchy(self):
        self.assertAlmostEqual(dt.tsf(1.0, 1), 0.25, places=9)
        self.assertAlmostEqual(dt.tsf(-1.0, 1), 0.75, places=9)

    def test_df2(self):
        self.assertAlmostEqual(dt.tsf(1.0, 2), 0.5 - 1.0 / (2.0 * 3.0 ** 0.5), places=9)

    def test_df30_critical(self):
        self.assertAlmostEqual(dt.tsf(2.0422724563, 30), 0.025, places=5)

    def test_zero_and_inf(self):
        self.assertAlmostEqual(dt.tsf(0.0, 5), 0.5, places=12)
        self.assertEqual(dt.tsf(float("inf"), 4), 0.0)
        self.assertEqual(dt.tsf(float("-inf"), 4), 1.0)


class TestHelpers(unittest.TestCase):
    def test_midranks(self):
        self.assertEqual(dt.midranks([3, 1, 3, 2]), [3.5, 1.0, 3.5, 2.0])

    def test_group_fit(self):
        b, cxx, ssr = dt.group_fit(dt.sums_of([(0, 1), (1, 3), (2, 5)]))
        self.assertAlmostEqual(b, 2.0)
        self.assertAlmostEqual(cxx, 2.0)
        self.assertAlmostEqual(ssr, 0.0)
        self.assertIsNone(dt.group_fit(dt.sums_of([(1, 1), (1, 3)])))

    def test_states(self):
        rows = toy()
        self.assertEqual(dt.female_state(rows), {"F1": 1, "F2": 1, "F3": 0, "F4": 0})
        self.assertEqual(dt.male_values(rows), {"M0": 0.0, "M1": 1.0})
        bad = toy()
        bad[0]["avail"] = 0
        self.assertIsNone(dt.female_state(bad))
        bad2 = toy()
        bad2[2]["consort_male"] = 0.5
        self.assertIsNone(dt.male_values(bad2))

    def test_holm(self):
        h = dt.holm({"a": 0.01, "b": 0.04})
        self.assertAlmostEqual(h["a"], 0.02)
        self.assertAlmostEqual(h["b"], 0.04)


class TestExact(unittest.TestCase):
    def test_toy_enumeration(self):
        r = dt.exact_female_test(toy(), "avoid", fa=True)
        self.assertTrue(r["testable"])
        self.assertEqual(r["k"], 2)
        self.assertEqual(r["n_relabelings"], 6)
        self.assertAlmostEqual(r["slope_diff"], 10.0)
        self.assertAlmostEqual(r["p_greater"], 1 / 6)
        self.assertAlmostEqual(r["p_two"], 2 / 6)
        self.assertAlmostEqual(r["p_less"], 1.0)
        self.assertAlmostEqual(r["naive_false_alarm_two_sided"], 2 / 6)
        self.assertEqual(r["naive_p_greater"], 0.0)
        self.assertIsNone(r["naive_t"])
        self.assertEqual(r["naive_df"], 4)

    def test_untestable(self):
        rows = [x for x in toy() if x["avail"] == 0]
        self.assertFalse(dt.exact_female_test(rows, "avoid")["testable"])

    def test_leave_one_female_out(self):
        lo = dt.leave_one_out(toy(), "female")
        for f in ("F1", "F2", "F3", "F4"):
            self.assertAlmostEqual(lo["per_unit"][f]["p_greater"], 1 / 3)
            self.assertEqual(lo["per_unit"][f]["n_relabelings"], 3)
        self.assertAlmostEqual(lo["max_p"], 1 / 3)

    def test_male_relabel(self):
        m = dt.male_relabel_test(toy(), b=199, seed=1)
        self.assertTrue(m["testable"])
        self.assertAlmostEqual(m["slope_diff"], 10.0)
        # Two males: every shuffle is either the identity (S = 10) or the swap (S = -10).
        self.assertGreater(m["p_greater"], 0.2)
        self.assertLess(m["p_greater"], 0.8)


def base_res(p=0.01, lofo=0.05, lomo=0.05, hrs=0.2):
    return {"checks": dict(dt.EXPECT, repro_constant_within_female=True),
            "primary": {"slope_diff": 100.0, "naive_p_greater": 0.001, "p_greater": p,
                        "naive_false_alarm_two_sided": 0.2},
            "lofo": {"max_p": lofo, "per_unit": {"HRS": {"p_greater": hrs}}},
            "lomo": {"max_p": lomo},
            "male_relabel": {"testable": True, "p_greater": 0.3},
            "rank": {"p_greater": 0.3}}


class TestGrade(unittest.TestCase):
    def test_paths(self):
        self.assertEqual(dt.grade(base_res())["verdict"], "SURVIVES_AT_FEMALE_LEVEL")
        self.assertEqual(dt.grade(base_res(lofo=0.2))["verdict"], "FRAGILE_AT_FEMALE_LEVEL")
        self.assertEqual(dt.grade(base_res(lomo=0.2))["verdict"], "FRAGILE_AT_FEMALE_LEVEL")
        self.assertEqual(dt.grade(base_res(p=0.2))["verdict"], "NOT_SUPPORTED_AT_FEMALE_LEVEL")
        bad = base_res()
        bad["checks"]["rows"] = 33
        self.assertEqual(dt.grade(bad)["verdict"], "DATA_MISMATCH")

    def test_predictions_and_brier(self):
        g = dt.grade(base_res())
        pr = g["predictions"]
        self.assertTrue(pr["P1_naive_reproduced"])
        self.assertTrue(pr["P2_exact_female_p_le_05"])
        self.assertTrue(pr["P3_verdict_survives"])
        self.assertTrue(pr["P4_naive_false_alarm_gt_10pct"])
        self.assertFalse(pr["P5_male_relabel_p_le_05"])
        self.assertFalse(pr["P6_rank_exact_p_le_05"])
        self.assertTrue(pr["P7_without_HRS_p_gt_10"])
        expect = sum((dt.PRIORS[k] - (1.0 if v else 0.0)) ** 2 for k, v in pr.items()) / 7
        self.assertAlmostEqual(g["brier"], expect, places=12)


class TestEndToEnd(unittest.TestCase):
    def test_main_on_toy_csv(self):
        old = dt.EXPECT
        dt.EXPECT = {"rows": 8, "females": 4, "males": 2, "available_females": 2}
        try:
            with tempfile.TemporaryDirectory() as d:
                path = os.path.join(d, "s1a.csv")
                cols = ["Pb_ID", "Pb_target", "Pb_signal_ID", "fem_repro", "consort_male",
                        "SRI", "Dist_avoid", "Resp_dur", "Grp_size"]
                with open(path, "w", newline="", encoding="utf-8") as fh:
                    w = csv.writer(fh)
                    w.writerow(cols)
                    for r in toy():
                        w.writerow([r["id"], r["female"], r["male"], r["avail"], r["consort_male"],
                                    0.01 * r["id"], r["avoid"], 5 + r["id"], 2])
                out = os.path.join(d, "out")
                self.assertEqual(dt.main(["--data", path, "--out-dir", out]), 0)
                with open(os.path.join(out, "dolphin_results.json"), encoding="utf-8") as fh:
                    res = json.load(fh)
                self.assertEqual(res["checks"]["rows"], 8)
                self.assertNotEqual(res["verdict"], "DATA_MISMATCH")
                self.assertAlmostEqual(res["primary"]["p_greater"], 1 / 6)
                with open(os.path.join(out, "RESULTS-DOLPHIN.md"), encoding="utf-8") as fh:
                    md = fh.read()
                self.assertIn("**Verdict: ", md)
                self.assertIn("Brier score", md)
        finally:
            dt.EXPECT = old

    def test_mismatch_renders(self):
        res = dt.run(toy(), "x")  # EXPECT is the real one: the toy is a mismatch
        self.assertEqual(res["verdict"], "DATA_MISMATCH")
        self.assertIn("DATA_MISMATCH", dt.render(res))


if __name__ == "__main__":
    unittest.main()
