# Copyright 2026 MV2, Munim, Inc. Licensed under the Apache License, Version 2.0 (Apache-2.0).
# Made with AI agents working in MV2's name.
"""Exact female-level test of the reproductive-state x coercion interaction in
Bouchard et al. 2026, PNAS 123(24): e2531602123 ("Female dolphins use individual vocal labels to
track coercive males"). Registered in DOLPHIN-PREREG.md. Standard library only.

Reproductive state (fem_repro) is a property of the female in Dataset S1A, so the claim that
available females avoid frequently consorting males more is a comparison of a few females with a
few others. The test enumerates every way of choosing which females are 'available' (the
observed number of them), keeping each female's playbacks together, and recomputes the
interaction slope difference each time.

Usage: python dolphin_test.py --data PATH_TO_DATASET_S1A.csv --out-dir OUT
"""
import argparse
import csv
import hashlib
import itertools
import json
import math
import os
import random
import sys

CODE_VERSION = "dolphin-test-1"
SEED_MALE = 20261122
B_MALE = 19999
EXPECT = {"rows": 34, "females": 17, "males": 11, "available_females": 7}
PRIORS = {
    "P1_naive_reproduced": 0.80,
    "P2_exact_female_p_le_05": 0.40,
    "P3_verdict_survives": 0.20,
    "P4_naive_false_alarm_gt_10pct": 0.60,
    "P5_male_relabel_p_le_05": 0.35,
    "P6_rank_exact_p_le_05": 0.30,
    "P7_without_HRS_p_gt_10": 0.55,
}


# ------------------------------------------------------------------ Student t tail (stdlib)
def _betacf(a, b, x):
    fpmin = 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < fpmin:
        d = fpmin
    d = 1.0 / d
    h = d
    for m in range(1, 400):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < 1e-15:
            break
    return h


def betai(a, b, x):
    """Regularised incomplete beta I_x(a, b)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                  + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def tsf(t, df):
    """P(T > t) for Student's t with df degrees of freedom."""
    if t != t:  # NaN
        return 1.0
    if t < 0:
        return 1.0 - tsf(-t, df)
    if math.isinf(t):
        return 0.0
    return 0.5 * betai(df / 2.0, 0.5, df / (df + t * t))


# ------------------------------------------------------------------ data
def read_rows(path):
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            if not (r.get("Pb_ID") or "").strip():
                continue
            rows.append({
                "id": int(float(r["Pb_ID"])),
                "female": r["Pb_target"].strip(),
                "male": r["Pb_signal_ID"].strip(),
                "avail": int(float(r["fem_repro"])),
                "consort_male": float(r["consort_male"]),
                "SRI": float(r["SRI"]),
                "avoid": float(r["Dist_avoid"]),
                "dur": float(r["Resp_dur"]),
            })
    return rows


def female_state(rows):
    """{female: 0/1} if fem_repro is constant within every female, else None."""
    st = {}
    for r in rows:
        if st.setdefault(r["female"], r["avail"]) != r["avail"]:
            return None
    return st


def male_values(rows, key="consort_male"):
    """{male: value} if the value is constant within every male, else None."""
    v = {}
    for r in rows:
        if abs(v.setdefault(r["male"], r[key]) - r[key]) > 1e-9:
            return None
    return v


def midranks(vals):
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    ranks = [0.0] * len(vals)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        r = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = r
        i = j + 1
    return ranks


# ------------------------------------------------------------------ statistic from sums
def sums_of(pairs):
    n = sx = sy = sxx = sxy = syy = 0.0
    for x, y in pairs:
        n += 1
        sx += x
        sy += y
        sxx += x * x
        sxy += x * y
        syy += y * y
    return [n, sx, sy, sxx, sxy, syy]


def add(a, b):
    return [p + q for p, q in zip(a, b)]


def sub(a, b):
    return [p - q for p, q in zip(a, b)]


def group_fit(s):
    """(slope, cxx, ssr) of y on x from sums, or None if undefined."""
    n, sx, sy, sxx, sxy, syy = s
    if n < 2:
        return None
    cxx = sxx - sx * sx / n
    if cxx <= 1e-12:
        return None
    cxy = sxy - sx * sy / n
    cyy = syy - sy * sy / n
    b = cxy / cxx
    return b, cxx, max(cyy - cxy * cxy / cxx, 0.0)


def interaction(sa, total):
    """Slope difference (available minus unavailable), the naive OLS t of that interaction
    (trials independent, separate lines, df = n - 4) and a flag for a defined statistic."""
    fa, fu = group_fit(sa), group_fit(sub(total, sa))
    if fa is None or fu is None:
        return 0.0, 0.0, 1, False
    s = fa[0] - fu[0]
    df = int(round(total[0])) - 4
    if df < 1:
        return s, 0.0, 1, True
    s2 = (fa[2] + fu[2]) / df
    se = math.sqrt(s2 * (1.0 / fa[1] + 1.0 / fu[1]))
    if se <= 0.0:
        t = 0.0 if s == 0 else math.copysign(math.inf, s)
    else:
        t = s / se
    return s, t, df, True


# ------------------------------------------------------------------ tests
def exact_female_test(rows, ykey, xkey="consort_male", fa=False):
    """Enumerate every choice of k 'available' females (k observed). Returns a dict."""
    st = female_state(rows)
    fems = sorted(st)
    avail = [f for f in fems if st[f] == 1]
    k = len(avail)
    per = {f: sums_of([(r[xkey], r[ykey]) for r in rows if r["female"] == f]) for f in fems}
    total = [0.0] * 6
    for f in fems:
        total = add(total, per[f])
    if k == 0 or k == len(fems):
        return {"testable": False, "k": k, "n_females": len(fems)}
    sa = [0.0] * 6
    for f in avail:
        sa = add(sa, per[f])
    s_obs, t_obs, df, ok = interaction(sa, total)
    n = ge = le = ab = fa2 = undefined = 0
    eps = 1e-12
    for comb in itertools.combinations(fems, k):
        s = [0.0] * 6
        for f in comb:
            s = add(s, per[f])
        sv, tv, dfv, okv = interaction(s, total)
        n += 1
        if not okv:
            undefined += 1
        if sv >= s_obs - eps:
            ge += 1
        if sv <= s_obs + eps:
            le += 1
        if abs(sv) >= abs(s_obs) - eps:
            ab += 1
        if fa and okv and 2.0 * tsf(abs(tv), dfv) <= 0.05:
            fa2 += 1
    out = {"testable": True, "k": k, "n_females": len(fems), "n_trials": int(total[0]),
           "available": avail, "slope_diff": s_obs, "defined": ok,
           "naive_t": t_obs if not math.isinf(t_obs) else None, "naive_df": df,
           "naive_p_greater": tsf(t_obs, df), "n_relabelings": n,
           "p_greater": ge / n, "p_less": le / n, "p_two": ab / n, "min_p": 1.0 / n,
           "undefined_relabelings": undefined}
    if fa:
        out["naive_false_alarm_two_sided"] = fa2 / n
    return out


def male_relabel_test(rows, ykey="avoid", xkey="consort_male", b=B_MALE, seed=SEED_MALE):
    vals = male_values(rows, xkey)
    if vals is None:
        return {"testable": False, "reason": "value varies within male"}
    males = sorted(vals)
    st = female_state(rows)

    def stat(mapping):
        sa = sums_of([(mapping[r["male"]], r[ykey]) for r in rows if st[r["female"]] == 1])
        su = sums_of([(mapping[r["male"]], r[ykey]) for r in rows if st[r["female"]] == 0])
        return interaction(sa, add(sa, su))[0]

    s_obs = stat(vals)
    rng = random.Random(seed)
    v = [vals[m] for m in males]
    ge = 0
    for _ in range(b):
        rng.shuffle(v)
        if stat(dict(zip(males, v))) >= s_obs - 1e-12:
            ge += 1
    return {"testable": True, "n_males": len(males), "B": b, "seed": seed,
            "slope_diff": s_obs, "p_greater": (1 + ge) / (b + 1)}


def leave_one_out(rows, key, ykey="avoid"):
    out = {}
    for unit in sorted({r[key] for r in rows}):
        sub_rows = [r for r in rows if r[key] != unit]
        res = exact_female_test(sub_rows, ykey)
        out[unit] = ({"slope_diff": res["slope_diff"], "p_greater": res["p_greater"],
                      "n_relabelings": res["n_relabelings"]}
                     if res["testable"] else {"testable": False})
    ps = [v["p_greater"] for v in out.values() if "p_greater" in v]
    worst = max(out, key=lambda u: out[u].get("p_greater", -1.0)) if ps else None
    return {"per_unit": out, "max_p": max(ps) if ps else None, "worst_unit": worst}


# ------------------------------------------------------------------ grading
def grade(res):
    """Verdict and predictions from the results dict (rules of DOLPHIN-PREREG.md section 7)."""
    c = res["checks"]
    if not (c["rows"] == EXPECT["rows"] and c["females"] == EXPECT["females"]
            and c["males"] == EXPECT["males"]
            and c["available_females"] == EXPECT["available_females"]
            and c["repro_constant_within_female"]):
        return {"verdict": "DATA_MISMATCH", "predictions": {}, "brier": None}
    p = res["primary"]
    lofo, lomo = res["lofo"]["max_p"], res["lomo"]["max_p"]
    if p["p_greater"] <= 0.05:
        robust = (lofo is not None and lofo <= 0.10) and (lomo is not None and lomo <= 0.10)
        verdict = "SURVIVES_AT_FEMALE_LEVEL" if robust else "FRAGILE_AT_FEMALE_LEVEL"
    else:
        verdict = "NOT_SUPPORTED_AT_FEMALE_LEVEL"
    hrs = res["lofo"]["per_unit"].get("HRS", {})
    pred = {
        "P1_naive_reproduced": p["slope_diff"] > 0 and p["naive_p_greater"] <= 0.05,
        "P2_exact_female_p_le_05": p["p_greater"] <= 0.05,
        "P3_verdict_survives": verdict == "SURVIVES_AT_FEMALE_LEVEL",
        "P4_naive_false_alarm_gt_10pct": p["naive_false_alarm_two_sided"] > 0.10,
        "P5_male_relabel_p_le_05": bool(res["male_relabel"].get("testable"))
        and res["male_relabel"]["p_greater"] <= 0.05,
        "P6_rank_exact_p_le_05": res["rank"]["p_greater"] <= 0.05,
        "P7_without_HRS_p_gt_10": hrs.get("p_greater", 0.0) > 0.10,
    }
    brier = sum((PRIORS[k] - (1.0 if v else 0.0)) ** 2 for k, v in pred.items()) / len(pred)
    return {"verdict": verdict, "predictions": pred, "brier": brier}


def holm(pvals):
    """Holm-adjusted p values for a dict name -> p."""
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    out, run = {}, 0.0
    for i, (k, p) in enumerate(items):
        run = max(run, min(1.0, (m - i) * p))
        out[k] = run
    return out


# ------------------------------------------------------------------ main
def run(rows, data_sha256):
    st = female_state(rows)
    checks = {"rows": len(rows), "females": len({r["female"] for r in rows}),
              "males": len({r["male"] for r in rows}),
              "repro_constant_within_female": st is not None,
              "available_females": sum(st.values()) if st else None,
              "consort_male_constant_within_male": male_values(rows) is not None,
              "data_sha256": data_sha256}
    res = {"code_version": CODE_VERSION, "checks": checks}
    if st is None:
        res["verdict"] = "DATA_MISMATCH"
        return res
    res["primary"] = exact_female_test(rows, "avoid", fa=True)
    ranked = [dict(r) for r in rows]
    for r, y in zip(ranked, midranks([r["avoid"] for r in rows])):
        r["avoid_rank"] = y
    res["rank"] = exact_female_test(ranked, "avoid_rank")
    res["male_relabel"] = male_relabel_test(rows)
    res["lofo"] = leave_one_out(rows, "female")
    res["lomo"] = leave_one_out(rows, "male")
    res["loto"] = leave_one_out(rows, "id")
    sec = {"SRI_avoid": exact_female_test(rows, "avoid", xkey="SRI", fa=True),
           "consort_duration": exact_female_test(rows, "dur", fa=True)}
    res["secondary"] = sec
    res["secondary_holm"] = holm({k: v["p_two"] for k, v in sec.items() if v["testable"]})
    # descriptive
    fem = {}
    for f in sorted(st):
        rs = [r for r in rows if r["female"] == f]
        fem[f] = {"available": st[f], "playbacks": len(rs),
                  "mean_avoid_m": sum(r["avoid"] for r in rs) / len(rs),
                  "avoided": sum(1 for r in rs if r["avoid"] > 0)}
    res["per_female"] = fem
    mal = {}
    for m in sorted({r["male"] for r in rows}):
        rs = [r for r in rows if r["male"] == m]
        ra = [r["avoid"] for r in rs if st[r["female"]] == 1]
        ru = [r["avoid"] for r in rs if st[r["female"]] == 0]
        mal[m] = {"consort_male": rs[0]["consort_male"], "playbacks": len(rs),
                  "mean_avoid_available": sum(ra) / len(ra) if ra else None,
                  "mean_avoid_unavailable": sum(ru) / len(ru) if ru else None}
    res["per_male"] = mal
    res.update(grade(res))
    return res


def render(res):
    L = ["# RESULTS-DOLPHIN: is the reproductive-state x coercion interaction a female-level effect?",
         "",
         "Registered in DOLPHIN-PREREG.md. Data: Dataset S1A of Bouchard et al. 2026, PNAS "
         "e2531602123 (read inside the job, not redistributed). Made with AI agents working in "
         "MV2's name; not yet checked by a human expert.", ""]
    c = res["checks"]
    L += ["Checks: " + json.dumps(c, sort_keys=True), ""]
    if res.get("verdict") == "DATA_MISMATCH":
        L += ["**Verdict: DATA_MISMATCH**", ""]
        return "\n".join(L) + "\n"
    p = res["primary"]
    L += ["**Verdict: %s**" % res["verdict"], "",
          "| quantity | value |", "|---|---|",
          "| slope difference, avoidance on consort_male (available - unavailable), m per unit | %.2f |" % p["slope_diff"],
          "| naive OLS interaction t (trials independent), df | %s, %d |" % (
              "%.3f" % p["naive_t"] if p["naive_t"] is not None else "inf", p["naive_df"]),
          "| naive one-sided p | %.5f |" % p["naive_p_greater"],
          "| exact female-level p (one-sided), relabelings | %.4f, %d |" % (p["p_greater"], p["n_relabelings"]),
          "| exact female-level p (two-sided) | %.4f |" % p["p_two"],
          "| naive two-sided p <= 0.05 among relabelings | %.4f |" % p["naive_false_alarm_two_sided"],
          "| rank version, exact one-sided p | %.4f |" % res["rank"]["p_greater"],
          "| male relabeling of consort_male, p (B = %d) | %.4f |" % (
              res["male_relabel"].get("B", 0), res["male_relabel"].get("p_greater", float("nan"))),
          "| leave one female out, max p (female) | %.4f (%s) |" % (res["lofo"]["max_p"], res["lofo"]["worst_unit"]),
          "| leave one male out, max p (male) | %.4f (%s) |" % (res["lomo"]["max_p"], res["lomo"]["worst_unit"]),
          "| leave one playback out, max p (Pb_ID) | %.4f (%s) |" % (res["loto"]["max_p"], res["loto"]["worst_unit"]),
          ""]
    L += ["## Leave one female out", "", "| female | available | slope diff | exact p |", "|---|---|---|---|"]
    for f, v in res["lofo"]["per_unit"].items():
        if "p_greater" in v:
            L.append("| %s | %d | %.2f | %.4f |" % (f, res["per_female"][f]["available"], v["slope_diff"], v["p_greater"]))
    L += ["", "## Secondary claims (two-sided exact female-level p, Holm over 2)", "",
          "| claim | slope diff | naive one-sided p | exact p two-sided | Holm | naive false alarm |",
          "|---|---|---|---|---|---|"]
    for k, v in res["secondary"].items():
        if v["testable"]:
            L.append("| %s | %.2f | %.5f | %.4f | %.4f | %.4f |" % (
                k, v["slope_diff"], v["naive_p_greater"], v["p_two"], res["secondary_holm"][k],
                v["naive_false_alarm_two_sided"]))
    L += ["", "## Per female (descriptive)", "", "| female | available | playbacks | avoided | mean avoidance (m) |",
          "|---|---|---|---|---|"]
    for f, v in res["per_female"].items():
        L.append("| %s | %d | %d | %d | %.1f |" % (f, v["available"], v["playbacks"], v["avoided"], v["mean_avoid_m"]))
    L += ["", "## Per male (descriptive)", "", "| male | consort_male | playbacks | mean avoidance, available (m) | mean avoidance, unavailable (m) |",
          "|---|---|---|---|---|"]
    fmt = lambda x: "n/a" if x is None else "%.1f" % x  # noqa: E731
    for m, v in sorted(res["per_male"].items(), key=lambda kv: kv[1]["consort_male"]):
        L.append("| %s | %.4f | %d | %s | %s |" % (m, v["consort_male"], v["playbacks"],
                                                  fmt(v["mean_avoid_available"]), fmt(v["mean_avoid_unavailable"])))
    L += ["", "## Predictions (priors fixed in DOLPHIN-PREREG.md)", "", "| prediction | prior | came true |", "|---|---|---|"]
    for k, v in res["predictions"].items():
        L.append("| %s | %.2f | %s |" % (k, PRIORS[k], "**true**" if v else "false"))
    L += ["", "Brier score: %.3f" % res["brier"], ""]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out-dir", required=True)
    a = ap.parse_args(argv)
    with open(a.data, "rb") as fh:
        sha = hashlib.sha256(fh.read().replace(b"\r\n", b"\n")).hexdigest()
    rows = read_rows(a.data)
    res = run(rows, sha)
    os.makedirs(a.out_dir, exist_ok=True)
    with open(os.path.join(a.out_dir, "dolphin_results.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
    with open(os.path.join(a.out_dir, "RESULTS-DOLPHIN.md"), "w", encoding="utf-8") as fh:
        fh.write(render(res))
    print(json.dumps({"verdict": res.get("verdict"), "brier": res.get("brier")}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
