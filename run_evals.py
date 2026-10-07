"""Runs every eval, prints one table and saves it to eval_report.md.

    python run_evals.py

Thresholds live in eval_thresholds.json. Do not edit that file or the logic
here without asking Usman. A failing eval is reported as failed.
"""
import functools
import json
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
EVAL_FILES = ["run_evals.py", "grading.py", "eval_thresholds.json", "eval_fixtures.json", "tasks.json"]


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
                logs.append(agents.run_buyer(task, trained_history(), CONFIG["budget_cents"], run=run))
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
    logs = train_logs() + heldout_logs("naive") + heldout_logs("buyer")
    honest = sum(set(log["citations"]) <= set(log["fetched"]) for log in logs)
    return (honest / len(logs) >= T["e3_min_fraction_honest_runs"],
            f"{honest}/{len(logs)} runs cite only fetched pages", "train + held-out, both agents")


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
    return (ours > keen, f"precision@{k}: ours {ours:.3f} vs Keenable raw {keen:.3f}; per task (ours vs raw): {detail}",
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
    for agent in ("naive", "buyer"):
        logs = heldout_logs(agent)
        stats[agent] = {
            "correct": statistics.mean(grade(task_by_id(l["task_id"]), l["answer"]) for l in logs),
            "spent": statistics.mean(l["spent_cents"] for l in logs),
            "tokens": statistics.mean(l["tokens"]["total"] for l in logs),
        }
    n, o = stats["naive"], stats["buyer"]
    gap_pp = (n["correct"] - o["correct"]) * 100
    saving = 1 - o["spent"] / n["spent"] if n["spent"] else 0
    passed = (gap_pp <= T["e2e_max_correctness_gap_pp"] and saving >= T["e2e_min_spend_reduction"]
              and o["tokens"] < n["tokens"])
    return (passed,
            f"correct: ours {o['correct']:.0%} vs naive {n['correct']:.0%} (gap {gap_pp:.0f}pp); "
            f"spend per task: ours {o['spent']:.2f}c vs naive {n['spent']:.2f}c ({saving:.0%} less, SIMULATED); "
            f"tokens per task: ours {o['tokens']:.0f} vs naive {n['tokens']:.0f}", N)


EVALS = [
    ("E1 score and price on every result", e1_score_and_price),
    ("E2 usefulness depends on the task", e2_task_dependent),
    ("E3 usage log is honest", e3_honest_log),
    ("E4 loop learns in the right direction", e4_loop_direction),
    ("E5 prediction beats plain relevance (KEY)", e5_beats_relevance),
    ("E6 cold start is not a blank score", e6_cold_start),
    ("E7 duplicates lose value", e7_duplicates),
    ("E8 price follows usefulness", e8_price_follows_usefulness),
    ("E9 budget is respected", e9_budget),
    ("END-TO-END ours vs naive", e2e_demo_claim),
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
    env_ignored = git("check-ignore", ".env") == ".env"
    out = ["# Eval report", "",
           "**Prices are simulated.** No real money moves anywhere in this demo.", "",
           f"Held-out numbers come from {N}. Treat them as a small sample.", "",
           "| eval | pass/fail | the raw numbers behind it | notes |", "|---|---|---|---|"]
    out += [f"| {r['eval']} | {'PASS' if r['passed'] else 'FAIL'} | {r['numbers']} | {r['notes']} |" for r in rows]
    out += ["", f"Passed {sum(r['passed'] for r in rows)} of {len(rows)}.", "",
            f"Thresholds confirmed by Usman: {'yes' if T['confirmed_by_usman'] else 'NO (placeholders)'}", "",
            f"UNVERIFIED tasks ({len(unverified)} of {len(TASKS)}): {', '.join(unverified) or 'none'}", "",
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
