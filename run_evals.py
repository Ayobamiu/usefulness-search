"""Runs every eval, prints one table and saves it to eval_report.md.

    python run_evals.py

Thresholds live in eval_thresholds.json. Do not edit that file or the logic
here without asking Usman. A failing eval is reported as failed.
"""
import functools
import json
import re
import pathlib
import statistics
import subprocess
import sys

import agents
import usefulness
from clients import CONFIG
from grading import grade

ROOT = pathlib.Path(__file__).parent
T = json.loads((ROOT / "eval_thresholds.json").read_text())
FIX = json.loads((ROOT / "eval_fixtures.json").read_text())
TASKS = json.loads((ROOT / "tasks.json").read_text())["tasks"]
TRAIN = [t for t in TASKS if t["split"] == "train"]
HELDOUT = [t for t in TASKS if t["split"] == "heldout"]
RUNS = CONFIG["heldout_runs"]
N = f"n={len(HELDOUT)} held-out tasks x {RUNS} runs (small sample)"
EVAL_FILES = ["run_evals.py", "grading.py", "eval_thresholds.json", "eval_fixtures.json", "tasks.json", "alert_cases.json"]


# ---- shared runs (each computed once; held-out tasks never touch the history) ----

@functools.cache
def train_logs():
    """Naive agent on the training tasks, with no history. These are the usage logs."""
    return [agents.run_naive(t, usefulness.empty_history()) for t in TRAIN]


@functools.cache
def trained_history():
    history = usefulness.empty_history()
    for log in train_logs():
        history = usefulness.update_history(history, log)
    return history


@functools.cache
def heldout_logs(agent):
    logs = []
    for task in HELDOUT:
        for run in range(RUNS):
            if agent == "naive":
                logs.append(agents.run_naive(task, trained_history(), run=run))
            else:
                buy = agents.run_buyer if agent == "buyer" else agents.run_topk
                logs.append(buy(task, trained_history(), CONFIG["budget_cents"], run=run))
    return logs


def task_by_id(task_id):
    return next(t for t in TASKS if t["id"] == task_id)


def pairs_correct(history):
    """E2 core: the planted page must score higher under the query it answers."""
    rows = []
    for pair in FIX["e2_pairs"]:
        a = usefulness.score(pair["query_a"], pair["page"], history)
        b = usefulness.score(pair["query_b"], pair["page"], history)
        rows.append((round(a, 3), round(b, 3)))
    return sum(a > b for a, b in rows), rows


# ---- unit evals: each returns (passed, raw numbers, notes) ----

def e1_score_and_price():
    total = valid = 0
    for task in TASKS:
        for r in usefulness.search(task["question"], trained_history()):
            total += 1
            u, p = r.get("usefulness"), r.get("price_cents")
            valid += (isinstance(u, (int, float)) and 0 <= u <= 1
                      and isinstance(p, (int, float)) and p >= 0
                      and all(r.get(k) for k in ("url", "title", "keenable_rank")))
    frac = valid / total if total else 0
    return (total > 0 and frac >= T["e1_min_fraction_valid"],
            f"{valid}/{total} results valid", f"all {len(TASKS)} tasks")


def e2_task_dependent():
    correct, rows = pairs_correct(trained_history())
    return (correct >= T["e2_min_pairs_correct"], f"{correct}/{len(rows)} pairs; (A, B) scores {rows}",
            "trained history")


def e3_honest_log():
    logs = train_logs() + heldout_logs("naive") + heldout_logs("buyer") + heldout_logs("topk")
    honest = sum(set(log["citations"]) <= set(log["fetched"]) for log in logs)
    return (honest / len(logs) >= T["e3_min_fraction_honest_runs"],
            f"{honest}/{len(logs)} runs cite only fetched pages", "train + held-out, all agents")


def e4_loop_direction():
    right = total = 0
    for log in train_logs():
        before = usefulness.empty_history()
        after = usefulness.update_history(before, log)
        pages = {r["url"]: r for r in log["results"]}
        for url in log["fetched"]:
            old = usefulness.score(log["query"], pages[url], before)
            new = usefulness.score(log["query"], pages[url], after)
            total += 1
            right += new > old if url in log["citations"] else new < old
    frac = right / total if total else 0
    return (total > 0 and frac >= T["e4_min_fraction_right_direction"],
            f"{right}/{total} pages moved the right way ({frac:.0%})", "training tasks only")


def e5_beats_relevance():
    k = T["e5_precision_at_k"]
    per_task = {}
    for log in heldout_logs("naive"):
        used = set(log["citations"])
        raw = sorted(log["results"], key=lambda r: r["keenable_rank"])
        ours = sorted(log["results"], key=lambda r: -r["usefulness"])
        p = [sum(r["url"] in used for r in ranking[:k]) / k for ranking in (raw, ours)]
        per_task.setdefault(log["task_id"], []).append(p)
    means = {tid: [statistics.mean(x[i] for x in ps) for i in (0, 1)] for tid, ps in per_task.items()}
    keen = statistics.mean(m[0] for m in means.values())
    ours = statistics.mean(m[1] for m in means.values())
    detail = ", ".join(f"{tid} {m[1]:.2f} vs {m[0]:.2f}" for tid, m in means.items())
    # Reframed 2026-10-06 with Usman: the claim is "no worse than Keenable", not "beats it".
    return (ours >= keen - T["e5_max_shortfall_vs_keenable"], f"precision@{k}: ours {ours:.3f} vs Keenable raw {keen:.3f}; per task (ours vs raw): {detail}",
            f"{N}; labels = naive agent citations")


def e6_cold_start():
    empty = usefulness.empty_history()
    ranges = []
    for task in TRAIN:
        scores = [r["usefulness"] for r in usefulness.search(task["question"], empty)]
        ranges.append(max(scores) - min(scores))
    spread_ok = sum(r >= T["e6_min_score_range_per_result_set"] for r in ranges)
    correct, rows = pairs_correct(empty)
    return (spread_ok == len(ranges) and correct >= T["e6_min_pairs_correct_unseen"],
            f"{spread_ok}/{len(ranges)} result sets have score range >= {T['e6_min_score_range_per_result_set']} "
            f"(min range {min(ranges):.3f}); E2 unseen {correct}/{len(rows)}", "empty history, training queries")


def e7_duplicates():
    empty = usefulness.empty_history()
    dropped, rows = 0, []
    for case in FIX["e7_duplicates"]:
        offers = []
        for page in (case["page_a"], case["page_b"]):
            u = usefulness.score(case["query"], page, empty)
            offers.append({**page, "usefulness": u, "price_cents": usefulness.price_cents(u)})
        before = offers[1]
        after = next(o for o in usefulness.reprice_after_purchase(case["query"], offers[1:], [case["page_a"]])
                     if o["url"] == before["url"])
        ok = after["usefulness"] < before["usefulness"] and after["price_cents"] < before["price_cents"]
        dropped += ok
        rows.append(f"score {before['usefulness']:.2f}->{after['usefulness']:.2f}, "
                    f"price {before['price_cents']:.2f}->{after['price_cents']:.2f}")
    frac = dropped / len(rows)
    return (frac >= T["e7_min_fraction_cases_dropped"], f"{dropped}/{len(rows)} planted cases dropped; {rows}", "")


def e8_price_follows_usefulness():
    ok = total = 0
    for task in TASKS:
        results = sorted(usefulness.search(task["question"], trained_history()), key=lambda r: r["usefulness"])
        total += 1
        ok += all(a["price_cents"] <= b["price_cents"] for a, b in zip(results, results[1:]))
    return (total > 0 and ok / total >= T["e8_min_fraction_monotonic_sets"],
            f"{ok}/{total} result sets monotonic", f"all {len(TASKS)} tasks")


def per_cent(offer):
    return offer["usefulness"] / max(offer["price_cents"], 1e-9)


def e9_budget():
    logs = heldout_logs("buyer")
    ok = 0
    for log in logs:
        budget = CONFIG["budget_cents"]
        good = abs(sum(p["price_cents"] for p in log["purchases"]) - log["spent_cents"]) < 1e-6
        good &= log["spent_cents"] <= budget + 1e-9
        good &= set(log["fetched"]) <= {p["url"] for p in log["purchases"]}
        left = budget
        for p in log["purchases"]:
            affordable = [o for o in p["offers_before"] if o["price_cents"] <= left + 1e-9]
            good &= bool(affordable) and per_cent(p) >= max(map(per_cent, affordable)) - 1e-9
            left -= p["price_cents"]
        ok += good
    return (ok / len(logs) >= T["e9_min_fraction_runs_within_budget"],
            f"{ok}/{len(logs)} runs within {CONFIG['budget_cents']}c budget and bought best usefulness-per-cent first", N)


def e2e_demo_claim():
    stats = {}
    for agent in ("naive", "buyer", "topk"):
        logs = heldout_logs(agent)
        stats[agent] = {
            "correct": statistics.mean(grade(task_by_id(l["task_id"]), l["answer"]) for l in logs),
            "spent": statistics.mean(l["spent_cents"] for l in logs),
            "tokens": statistics.mean(l["tokens"]["total"] for l in logs),
        }
    n, o, k = stats["naive"], stats["buyer"], stats["topk"]
    gap_pp = (n["correct"] - o["correct"]) * 100
    saving = 1 - o["spent"] / n["spent"] if n["spent"] else 0
    tb = lambda key: statistics.mean(agents.totals(l)[key] for l in heldout_logs("buyer"))
    tn = lambda key: statistics.mean(agents.totals(l)[key] for l in heldout_logs("naive"))
    # Approved by Usman 2026-10-08: "fewer tokens" counts our scoring tokens, not reading tokens alone.
    passed = (gap_pp <= T["e2e_max_correctness_gap_pp"] and saving >= T["e2e_min_spend_reduction"]
              and tb("total_tokens") < tn("total_tokens"))
    return (passed,
            f"correct: ours {o['correct']:.0%} vs naive {n['correct']:.0%} (gap {gap_pp:.0f}pp); "
            f"spend per task: ours {o['spent']:.2f}c vs naive {n['spent']:.2f}c ({saving:.0%} less, SIMULATED); "
            f"READING tokens per task: ours {o['tokens']:.0f} vs naive {n['tokens']:.0f}. "
            f"SAME-BUDGET BASELINE (Keenable order, {CONFIG['budget_cents']}c, not part of pass/fail): "
            f"correct {k['correct']:.0%}, spend {k['spent']:.2f}c, tokens {k['tokens']:.0f}. "
            f"WITH OUR SCORING COUNTED (this is the pass rule for tokens): ours {tb('total_tokens'):.0f} tokens "
            f"(reading {tb('reading_tokens'):.0f} + scoring {tb('scoring_tokens'):.0f}) vs naive {tn('total_tokens'):.0f}, "
            f"NET tokens saved {tn('total_tokens') - tb('total_tokens'):.0f}; cost incl. model tokens: ours {tb('total_cents'):.2f}c "
            f"vs naive {tn('total_cents'):.2f}c, NET cost saved {tn('total_cents') - tb('total_cents'):.2f}c. "
            f"IF A SECOND AGENT REUSES CACHED SCORES: net tokens saved {tn('total_tokens') - tb('reading_tokens'):.0f}", N)


# ---- freshness evals (alert-driven sales cases, alert_cases.json) ----

ALERTS = json.loads((ROOT / "alert_cases.json").read_text())
A_HELDOUT = [c for c in ALERTS["cases"] if c["split"] == "heldout"]
A_CONTROL = [c for c in ALERTS["cases"] if c["split"] == "control"]
NA = f"n={len(A_HELDOUT)} held-out alert cases"


def alert_task(case):
    return {"id": case["id"], "kind": "alert", "query": case["query"],
            "question": ALERTS["task"].format(alert=case["alert"], name=case["name"])}


@functools.cache
def alert_results(case_id):
    if not hasattr(usefulness, "W_SUPERSEDED"):
        raise NotImplementedError("freshness check")
    case = next(c for c in ALERTS["cases"] if c["id"] == case_id)
    return usefulness.search(case["query"], usefulness.empty_history())


def matches(pattern, page):
    return bool(re.search(pattern, f"{page['title']} {page['snippet']}".lower()))


def is_stale(case, answer):
    """Keyword check: the answer pitches the old event and does not reflect the newer one."""
    answer = answer.lower()
    return bool(re.search(case["old"], answer)) and not re.search(case["new"], answer)


def f1_catches_superseded():
    caught, eligible, flagged_pages = 0, 0, 0
    for case in A_HELDOUT:
        results = alert_results(case["id"])
        by_url = {r["url"]: r for r in results}
        old = [r for r in results if matches(case["old"], r) and not matches(case["new"], r)]
        if not old or not any(matches(case["new"], r) for r in results):
            continue                      # Keenable did not return both stories: nothing to catch
        eligible += 1
        flagged = [r for r in old if r["superseded_by"]]
        flagged_pages += len(flagged)
        caught += any(matches(case["new"], by_url[r["superseded_by"]["url"]]) for r in flagged)
    frac = caught / eligible if eligible else 0
    return (eligible > 0 and frac >= T["f1_min_fraction_eligible_cases_caught"],
            f"caught {caught} of {eligible} eligible cases ({flagged_pages} old-story pages flagged)",
            f"{NA}; eligible = Keenable returned both an old-story and a new-story page (keyword match)")


def f2_no_false_alarms():
    alarms, pages, total = 0, 0, 0
    for case in A_CONTROL:
        flagged = [r for r in alert_results(case["id"]) if r["superseded_by"]]
        total += len(alert_results(case["id"]))
        pages += len(flagged)
        alarms += bool(flagged)
    return (alarms <= T["f2_max_control_cases_with_false_alarm"],
            f"{alarms} of {len(A_CONTROL)} control cases have a false alarm ({pages} of {total} pages flagged)",
            f"n={len(A_CONTROL)} control cases, drafts UNVERIFIED")


def f3_flag_lowers_price():
    cheaper = total = 0
    for case in ALERTS["cases"]:
        if case["split"] == "control":
            continue
        for r in alert_results(case["id"]):
            if r["superseded_by"]:
                unflagged = usefulness.score(case["query"], {**r, "superseded_by": None}, usefulness.empty_history())
                total += 1
                cheaper += r["price_cents"] < usefulness.price_cents(unflagged)
    frac = cheaper / total if total else 0
    return (total > 0 and frac >= T["f3_min_fraction_flagged_pages_cheaper"],
            f"{cheaper}/{total} flagged pages are cheaper than the same page without the flag", "tuning + held-out alert cases")


def f4_alert_end_to_end():
    if not hasattr(agents, "totals"):
        raise NotImplementedError("scoring cost accounting")
    sums = {"naive": [], "buyer": []}
    stale = {"naive": 0, "buyer": 0}
    for case in A_HELDOUT:
        for run in range(RUNS):
            for agent in sums:
                fn = agents.run_naive if agent == "naive" else agents.run_buyer
                args = (alert_task(case), usefulness.empty_history()) + ((CONFIG["budget_cents"],) if agent == "buyer" else ())
                log = fn(*args, run=run)
                stale[agent] += is_stale(case, log["answer"])
                sums[agent].append({**agents.totals(log), "pages": len(log["fetched"])})
    mean = lambda agent, key: statistics.mean(x[key] for x in sums[agent])
    runs = len(sums["naive"])
    net_tokens = mean("naive", "total_tokens") - mean("buyer", "total_tokens")
    net_cents = mean("naive", "total_cents") - mean("buyer", "total_cents")
    reuse_tokens = mean("naive", "total_tokens") - mean("buyer", "reading_tokens")
    return (stale["buyer"] < stale["naive"],
            f"answers pitching the old event as current (keyword check): ours {stale['buyer']}/{runs} vs naive {stale['naive']}/{runs}; "
            f"pages read: ours {mean('buyer', 'pages'):.1f} vs naive {mean('naive', 'pages'):.1f}; "
            f"tokens per query: naive {mean('naive', 'total_tokens'):.0f}, ours {mean('buyer', 'total_tokens'):.0f} "
            f"(reading {mean('buyer', 'reading_tokens'):.0f} + scoring {mean('buyer', 'scoring_tokens'):.0f}); "
            f"NET tokens saved INCLUDING scoring {net_tokens:.0f}; NET cost saved INCLUDING scoring {net_cents:.2f}c "
            f"(pages SIMULATED + model tokens at configured prices: naive {mean('naive', 'total_cents'):.2f}c, ours {mean('buyer', 'total_cents'):.2f}c). "
            f"IF A SECOND AGENT REUSES CACHED SCORES (scoring paid once): net tokens saved {reuse_tokens:.0f}",
            f"{NA} x {RUNS} runs (small sample); keyword verdicts need Usman's hand read")


# ---- sales research mode (the main demo): "{company} news", all 15 companies ----

def sales_module():
    try:
        import sales
    except ImportError:
        raise NotImplementedError("sales mode") from None
    return sales


def s1_sales_quality():
    summary = sales_module().summary()
    o, n = summary["buyer"], summary["naive"]
    passed = (o["stale"] - n["stale"] <= T["s1_max_extra_stale_answers"]
              and n["current"] - o["current"] <= T["s1_max_fewer_current_answers"])
    return (passed, f"current: ours {o['current']} vs naive {n['current']}; stale: ours {o['stale']} vs naive {n['stale']}; "
                    f"other: ours {o['other']} vs naive {n['other']} (of {summary['n']} each)",
            f"n={summary['n']} companies, 1 run each; keyword verdicts, Usman reads experiments/sales_results.md")


def s2_sales_cost():
    summary = sales_module().summary()
    o, n = summary["buyer"], summary["naive"]
    return (o["total_cents"] < n["total_cents"],
            f"cost per query, scoring included (pages SIMULATED + model tokens): ours {o['total_cents']:.2f}c vs naive {n['total_cents']:.2f}c; "
            f"pages read: ours {o['pages']:.1f} vs naive {n['pages']:.1f}; tokens: ours {o['total_tokens']:.0f} "
            f"(reading {o['reading_tokens']:.0f} + scoring {o['scoring_tokens']:.0f}) vs naive {n['total_tokens']:.0f}; "
            f"if a second agent reuses the cached scores, ours uses {o['reading_tokens']:.0f} tokens",
            f"n={summary['n']} companies, 1 run each")


def s3_live_query():
    import os
    import time
    if "--company" not in (ROOT / "demo.py").read_text():
        raise NotImplementedError("demo.py --company")
    runs = [(name, {"OFFLINE": "1"}) for name in CONFIG["precached_companies"][:3]] + [(CONFIG["s3_online_company"], {})]
    rows, ok = [], 0
    for name, extra in runs:
        start = time.time()
        proc = subprocess.run([sys.executable, "demo.py", "--company", name, "--no-open"], cwd=ROOT,
                              capture_output=True, text=True, env={**os.environ, **extra})
        seconds = time.time() - start
        run = json.loads((ROOT / "demo_run.json").read_text()) if proc.returncode == 0 else {}
        good = proc.returncode == 0 and not run.get("fallback") and seconds < T["s3_max_seconds"]
        ok += good
        rows.append(f"{name} ({'offline' if extra else 'online allowed'}): {seconds:.0f}s {'ok' if good else 'FAILED or fell back'}")
    return (ok == len(runs), f"{ok}/{len(runs)} ran end to end under {T['s3_max_seconds']}s; " + "; ".join(rows),
            "3 pre-cached companies with OFFLINE=1, plus 1 other company with the network allowed (cached after its first run)")


def s4_no_hardcoding():
    names = {c["name"].split(" (")[0].lower() for c in ALERTS["cases"]} | {n.lower() for n in CONFIG.get("precached_companies", [])}
    names |= {CONFIG.get("s3_online_company", "").lower()} - {""}
    files = [f for f in ("usefulness.py", "agents.py", "demo.py", "sales.py") if (ROOT / f).exists()]
    hits = [f"{f}: {name}" for f in files for name in sorted(names)
            if re.search(rf"\b{re.escape(name)}\b", (ROOT / f).read_text().lower())]
    return (not hits, f"{len(hits)} company names found in {', '.join(files)} ({len(names)} names checked)" + (f": {hits}" if hits else ""),
            "grep for every case, control and pre-cached company name")


EVALS = [
    ("E1 score and price on every result", e1_score_and_price),
    ("E2 usefulness depends on the task", e2_task_dependent),
    ("E3 usage log is honest", e3_honest_log),
    ("E4 loop learns in the right direction", e4_loop_direction),
    ("E5 prediction no worse than plain relevance (KEY)", e5_beats_relevance),
    ("E6 cold start is not a blank score", e6_cold_start),
    ("E7 duplicates lose value", e7_duplicates),
    ("E8 price follows usefulness", e8_price_follows_usefulness),
    ("E9 budget is respected", e9_budget),
    ("END-TO-END ours vs naive", e2e_demo_claim),
    ("S1 sales quality: ours no worse than naive", s1_sales_quality),
    ("S2 sales cost: ours cheaper, scoring included", s2_sales_cost),
    ("S3 live company query runs", s3_live_query),
    ("S4 no company names in the logic", s4_no_hardcoding),
    ("F1 catches superseded pages", f1_catches_superseded),
    ("F2 no false alarms on controls", f2_no_false_alarms),
    ("F3 a flagged page costs less", f3_flag_lowers_price),
    ("F4 END-TO-END alert cases, ours vs naive", f4_alert_end_to_end),
]


# ---- report ----

def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()


def eval_changes():
    """Changes to eval code, thresholds, fixtures or tasks since the last eval run."""
    marker = ROOT / ".eval_last_run"
    last = marker.read_text().strip() if marker.exists() else ""
    head = git("rev-parse", "HEAD")
    lines = []
    if last and last != head:
        lines += git("log", "--oneline", f"{last}..HEAD", "--", *EVAL_FILES).splitlines()
    lines += ["uncommitted: " + l for l in git("status", "--porcelain", "--", *EVAL_FILES).splitlines()]
    if head:
        marker.write_text(head)
    return lines or ["none" if last else "none recorded (first run)"]


def main():
    rows = []
    for name, fn in EVALS:
        try:
            passed, numbers, notes = fn()
        except NotImplementedError as e:
            passed, numbers, notes = False, "no numbers", f"not implemented: {e}"
        rows.append({"eval": name, "passed": bool(passed), "numbers": numbers, "notes": notes})

    unverified = [t["id"] for t in TASKS if t["status"] != "VERIFIED"]
    unverified_controls = [c["id"] for c in A_CONTROL if c["status"] != "VERIFIED"]
    env_ignored = git("check-ignore", ".env") == ".env"
    out = ["# Eval report", "",
           "**Prices are simulated.** No real money moves anywhere in this demo.", "",
           f"Held-out numbers come from {N}. Treat them as a small sample.", "",
           "| eval | pass/fail | the raw numbers behind it | notes |", "|---|---|---|---|"]
    out += [f"| {r['eval']} | {'PASS' if r['passed'] else 'FAIL'} | {r['numbers']} | {r['notes']} |" for r in rows]
    out += ["", f"Passed {sum(r['passed'] for r in rows)} of {len(rows)}.", "",
            f"Thresholds confirmed by Usman: {'yes' if T['confirmed_by_usman'] else 'NO (placeholders)'}", "",
            f"UNVERIFIED tasks ({len(unverified)} of {len(TASKS)}): {', '.join(unverified) or 'none'}", "",
            f"UNVERIFIED control cases ({len(unverified_controls)} of {len(A_CONTROL)}): {', '.join(unverified_controls) or 'none'}", "",
            "Changes to eval code, thresholds, fixtures or tasks since the last run:"]
    out += [f"- {line}" for line in eval_changes()]
    out += ["", f".env ignored by git: {'yes' if env_ignored else 'NO - FIX BEFORE COMMITTING'}", ""]
    report = "\n".join(out)
    print(report)
    (ROOT / "eval_report.md").write_text(report)
    (ROOT / "eval_report.json").write_text(json.dumps(rows, indent=1))
    sys.exit(0 if all(r["passed"] for r in rows) else 1)


if __name__ == "__main__":
    main()
