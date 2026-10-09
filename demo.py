"""Builds the demo screen (demo.html) from the same code and logs as the evals.

    python3 demo.py                     the sales research demo, offline from cache
    python3 demo.py --company "Acme"    run any company LIVE (90 second limit, then nearest cached run)
    python3 demo.py --docs              the coding-docs demo (backup), offline from cache
    python3 demo.py --pace 8            add 8 second pauses between beats, for narration
    python3 demo.py --pick              re-check the demo candidates, write demo_candidates.md

Prices are simulated. Nothing on the screen is computed anywhere but here and in the modules it imports.
"""
import argparse
import difflib
import json
import os
import pathlib
import subprocess
import sys
import webbrowser

ROOT = pathlib.Path(__file__).parent
CONFIG = json.loads((ROOT / "config.json").read_text())
LIVE_LIMIT_SECONDS = 90
TONE = {"current": "good", "stale": "bad", "other": "plain"}


def score_changes(question, log, history):
    """What the usage loop does to each bought page after this run."""
    import usefulness
    after = usefulness.update_history(history, log)
    pages = {r["url"]: r for r in log["results"]}
    return {url: {"before": pages[url]["usefulness"], "after": usefulness.score(question, pages[url], after)}
            for url in log["fetched"]}


# ---- sales research mode ----

def sales_data(company):
    import sales
    import usefulness
    r = sales.run(company)
    if r["verdicts"]:
        verdicts = {a: {"text": v, "tone": TONE[v], "how": "keyword check on the latest event"} for a, v in r["verdicts"].items()}
    else:
        verdicts = {a: {"text": "live run, not graded", "tone": "plain", "how": ""} for a in ("naive", "buyer")}
    return {"mode": "sales", "company": company, "task": r["task"], "budget_cents": CONFIG["budget_cents"],
            "naive": r["naive"], "buyer": r["buyer"], "totals": r["totals"], "verdicts": verdicts,
            "score_changes": score_changes(r["buyer"]["query"], r["buyer"], usefulness.empty_history())}


def cached_companies():
    import sales
    return [c["name"] for c in sales.cases()] + CONFIG["precached_companies"]


def live_sales_data(company):
    """Run in a child process so the 90 second limit is hard. On any failure, the nearest cached run."""
    out = ROOT / "demo_run.json"
    out.unlink(missing_ok=True)
    try:
        ok = subprocess.run([sys.executable, __file__, "--company", company, "--worker"], cwd=ROOT,
                            timeout=LIVE_LIMIT_SECONDS - 5, capture_output=True).returncode == 0
    except subprocess.TimeoutExpired:
        ok = False
    if ok and out.exists():
        return {**json.loads(out.read_text()), "notice": "", "fallback": False}
    os.environ["OFFLINE"] = "1"
    nearest = max(cached_companies(), key=lambda name: difflib.SequenceMatcher(None, company.lower(), name.lower()).ratio())
    return {**sales_data(nearest), "fallback": True,
            "notice": f'The live run for "{company}" failed or timed out. Showing the nearest cached run: {nearest}.'}


def pick_sales():
    """Rule: both agents' answers are "current". Among those: largest cost saved, scoring included."""
    import sales
    rows = []
    for r in sales.measured():
        saved = r["totals"]["naive"]["total_cents"] - r["totals"]["buyer"]["total_cents"]
        ok = r["verdicts"]["naive"] == r["verdicts"]["buyer"] == "current"
        rows.append((r["company"], r["verdicts"]["naive"], r["verdicts"]["buyer"], saved, ok))
    qualifying = [r for r in rows if r[4]]
    chosen = max(qualifying, key=lambda r: (r[3], r[0]))[0] if qualifying else None
    out = ["## Sales demo case", "",
           f"All {len(rows)} companies in the case list were checked (see experiments/sales_results.md).",
           'Rule: both agents\' answers are "current" by the keyword check. Among those: largest cost saved, scoring included.', "",
           f"**Chosen: {chosen or 'none qualifies'}**", "",
           "| company | naive | ours | cost saved (simulated) | qualifies |", "|---|---|---|---|---|"]
    out += [f"| {c} | {n} | {b} | {s:.2f}c | {'yes' if ok else 'no'} |" for c, n, b, s, ok in rows]
    out += ["", "This is one example, not the average. The demo's end card shows the means over all companies."]
    return chosen, out


# ---- coding-docs mode (backup) ----

def docs_data(task, train):
    import agents
    import usefulness
    from grading import grade
    history = usefulness.empty_history()   # usage history from every OTHER training task
    for other in train:
        if other["id"] != task["id"]:
            history = usefulness.update_history(history, agents.run_naive(other, usefulness.empty_history()))
    naive = agents.run_naive(task, history)
    buyer = agents.run_buyer(task, history, CONFIG["budget_cents"])
    verdict = lambda log: (lambda ok: {"text": "pass" if ok else "fail", "tone": "good" if ok else "bad",
                                       "how": "correctness check"})(grade(task, log["answer"]))
    return {"mode": "docs", "task": task, "budget_cents": CONFIG["budget_cents"], "naive": naive, "buyer": buyer,
            "totals": {"naive": agents.totals(naive), "buyer": agents.totals(buyer)},
            "verdicts": {"naive": verdict(naive), "buyer": verdict(buyer)},
            "score_changes": score_changes(task["question"], buyer, history)}


def pick_docs(train):
    """Rule: both agents correct, our top 3 shares at most 1 page with Keenable's top 3.
    Among those: fewest shared pages, then lowest task id."""
    rows = []
    for task in train:
        d = docs_data(task, train)
        ours = {r["url"] for r in sorted(d["naive"]["results"], key=lambda r: -r["usefulness"])[:3]}
        shared = len(ours & {r["url"] for r in d["naive"]["results"] if r["keenable_rank"] <= 3})
        good = [d["verdicts"][a]["text"] == "pass" for a in ("naive", "buyer")]
        rows.append((task["id"], shared, good[0], good[1], shared <= 1 and all(good), task["question"]))
    ok = [r for r in rows if r[4]]
    chosen = min(ok, key=lambda r: (r[1], r[0]))[0] if ok else None
    out = ["## Docs demo query (backup)", "",
           "All 18 training tasks were checked. Held-out tasks are never used for the demo.",
           "Rule: both agents answer correctly, and our top 3 shares at most 1 page with Keenable's top 3.",
           "Among those: fewest shared pages, then lowest task id. The usage history excludes the task itself.", "",
           f"**Chosen: {chosen or 'none qualifies'}**", "",
           "| task | top-3 pages shared with Keenable | naive correct | ours correct | qualifies | question |",
           "|---|---|---|---|---|---|"]
    out += [f"| {i} | {s} | {'yes' if n else 'no'} | {'yes' if b else 'no'} | {'yes' if q else 'no'} | {text} |"
            for i, s, n, b, q, text in rows]
    return chosen, out


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--company", help="run the sales task live for any company")
    parser.add_argument("--docs", action="store_true", help="the coding-docs demo (backup)")
    parser.add_argument("--pace", type=float, default=0, help="extra seconds between beats, for narration")
    parser.add_argument("--pick", action="store_true", help="re-check the demo candidates and write demo_candidates.md")
    parser.add_argument("--live", action="store_true", help="allow network calls in the cached modes")
    parser.add_argument("--no-open", action="store_true", help="build demo.html without opening a browser")
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.worker:                       # child of live_sales_data: compute, write, exit
        (ROOT / "demo_run.json").write_text(json.dumps(sales_data(args.company)))
        return
    if not args.company and not args.live:
        os.environ["OFFLINE"] = "1"
    train = [t for t in json.loads((ROOT / "tasks.json").read_text())["tasks"] if t["split"] == "train"]

    if args.pick:
        sales_choice, sales_lines = pick_sales()
        docs_choice, docs_lines = pick_docs(train)
        (ROOT / "demo_candidates.md").write_text("\n".join(["# Demo candidates", "", *sales_lines, "", *docs_lines]) + "\n")
        print(f"Sales: {sales_choice}. Docs: {docs_choice}. Wrote demo_candidates.md; set them in config.json.")
        return

    if args.docs:
        data = {**docs_data(next(t for t in train if t["id"] == CONFIG["demo_task_id"]), train), "notice": "", "fallback": False}
    elif args.company:
        data = live_sales_data(args.company)
    else:
        data = {**sales_data(CONFIG["demo_sales_company"]), "notice": "", "fallback": False}

    report = json.loads((ROOT / "eval_report.json").read_text())
    wanted, data["end_title"] = ((("E5", "END-TO-END"), "Across the held-out docs tasks, not just this example") if args.docs
                                 else (("S1", "S2"), "Across every company in our case list, not just this one"))
    data["end_card"] = [r for r in report if r["eval"].startswith(wanted)]
    data["pace"] = args.pace
    (ROOT / "demo_run.json").write_text(json.dumps(data))
    html = (ROOT / "demo_template.html").read_text().replace("/*DATA*/null", json.dumps(data).replace("</", "<\\/"))
    (ROOT / "demo.html").write_text(html)
    if not args.no_open:
        webbrowser.open((ROOT / "demo.html").as_uri())


if __name__ == "__main__":
    main()
