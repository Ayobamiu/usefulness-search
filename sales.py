"""Sales research mode (the main demo): one task, any company.

    python3 sales.py        runs every company in the case list, writes experiments/sales_results.md

Both agents get the same task, model, prompt and cached pages. The freshness check is OFF in this mode.
The case list (alert_cases.json) only supplies company names and the keyword lists used to grade answers.
"""
import functools
import json
import pathlib
import re
import statistics

import agents
import usefulness
from clients import CONFIG

ROOT = pathlib.Path(__file__).parent
TASK = "Write a one-paragraph sales outreach angle for {company} based on their latest news."
QUERY = "{company} news"


def task_for(company):
    return {"id": "sales:" + company.lower(), "kind": "sales",
            "question": TASK.format(company=company), "query": QUERY.format(company=company)}


@functools.cache
def cases():
    """Companies we can grade: each has keywords for its old event and its newer event."""
    data = json.loads((ROOT / "alert_cases.json").read_text())
    return [c for c in data["cases"] if c["split"] != "control"]


def find_case(company):
    wanted = company.strip().lower()
    return next((c for c in cases() if wanted in (c["name"].lower(), c["name"].split(" (")[0].lower())), None)


def verdict(case, answer):
    """Keyword check. current = reflects the newer event; stale = pitches the old one; else other."""
    answer = answer.lower()
    return "current" if re.search(case["new"], answer) else "stale" if re.search(case["old"], answer) else "other"


def run(company):
    """Naive vs ours on one company. Graded only if the company is in the case list."""
    task, history, case = task_for(company), usefulness.empty_history(), find_case(company)
    naive = agents.run_naive(task, history)
    buyer = agents.run_buyer(task, history, CONFIG["budget_cents"])
    return {"company": company, "task": task, "naive": naive, "buyer": buyer,
            "totals": {"naive": agents.totals(naive), "buyer": agents.totals(buyer)},
            "verdicts": {"naive": verdict(case, naive["answer"]), "buyer": verdict(case, buyer["answer"])} if case else None}


@functools.cache
def measured():
    return [run(c["name"]) for c in cases()]


def summary():
    """Counts and per-query means over every company in the case list, for both agents."""
    rows, out = measured(), {"n": len(measured())}
    for agent in ("naive", "buyer"):
        out[agent] = {v: sum(r["verdicts"][agent] == v for r in rows) for v in ("current", "stale", "other")}
        out[agent]["pages"] = statistics.mean(len(r[agent]["fetched"]) for r in rows)
        for key in ("reading_tokens", "scoring_tokens", "total_tokens", "page_cents", "total_cents"):
            out[agent][key] = statistics.mean(r["totals"][agent][key] for r in rows)
    return out


def write_results(path=ROOT / "experiments" / "sales_results.md"):
    s, rows = summary(), measured()
    o, n = s["buyer"], s["naive"]
    out = ["# Sales research: naive vs ours on every company in the case list", "",
           f"Task: \"{TASK}\"  Query: \"{QUERY}\"  n={s['n']} companies, 1 run each. Prices are simulated.",
           "Verdicts are keyword checks (current / stale / other). **Usman: please read the answers below and confirm.**", "",
           "| | naive (reads 10) | ours |", "|---|---|---|",
           f"| current | {n['current']} | {o['current']} |", f"| stale | {n['stale']} | {o['stale']} |",
           f"| other | {n['other']} | {o['other']} |",
           f"| pages read | {n['pages']:.1f} | {o['pages']:.1f} |",
           f"| tokens per query | {n['total_tokens']:.0f} | {o['total_tokens']:.0f} (reading {o['reading_tokens']:.0f} + scoring {o['scoring_tokens']:.0f}) |",
           f"| cost per query (pages simulated + tokens) | {n['total_cents']:.2f}c | {o['total_cents']:.2f}c |", "",
           "| company | naive | ours | pages | tokens naive | tokens ours (reading + scoring) | cost naive | cost ours |",
           "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        tn, tb = r["totals"]["naive"], r["totals"]["buyer"]
        out.append(f"| {r['company']} | {r['verdicts']['naive']} | {r['verdicts']['buyer']} | {len(r['buyer']['fetched'])} | "
                   f"{tn['total_tokens']} | {tb['total_tokens']} ({tb['reading_tokens']} + {tb['scoring_tokens']}) | "
                   f"{tn['total_cents']:.2f}c | {tb['total_cents']:.2f}c |")
    out += ["", "## Answers", ""]
    for r in rows:
        out += [f"### {r['company']}", "", f"**Naive ({r['verdicts']['naive']}):** {r['naive']['answer']}", "",
                f"**Ours ({r['verdicts']['buyer']}):** {r['buyer']['answer']}", ""]
    path.write_text("\n".join(out) + "\n")
    return s


if __name__ == "__main__":
    write_results()
    print((ROOT / "experiments" / "sales_results.md").read_text().split("## Answers")[0])
