"""Builds the demo screen (demo.html) from the same code and logs as the evals.

    python demo.py              build and open the demo, offline from cache
    python demo.py --pace 8     add 8 second pauses between beats, for narration
    python demo.py --pick       check every training task as a demo query, write demo_candidates.md

Prices are simulated. Nothing on the screen is computed anywhere but here and in the modules below.
"""
import argparse
import json
import os
import pathlib
import webbrowser

ROOT = pathlib.Path(__file__).parent


def history_without(task, train):
    """Usage history from every OTHER training task: the system has not seen the demo task."""
    import agents
    import usefulness
    history = usefulness.empty_history()
    for other in train:
        if other["id"] != task["id"]:
            history = usefulness.update_history(history, agents.run_naive(other, usefulness.empty_history()))
    return history


def run(task, train, budget):
    import agents
    import usefulness
    from grading import grade
    history = history_without(task, train)
    naive = agents.run_naive(task, history)
    buyer = agents.run_buyer(task, history, budget)
    after = usefulness.update_history(history, buyer)
    pages = {r["url"]: r for r in buyer["results"]}
    changes = {url: {"before": pages[url]["usefulness"],
                     "after": usefulness.score(task["question"], pages[url], after)}
               for url in buyer["fetched"]}
    return {"task": task, "budget_cents": budget, "naive": naive, "buyer": buyer, "score_changes": changes,
            "totals": {"naive": agents.totals(naive), "buyer": agents.totals(buyer)},  # scoring cost included
            "naive_correct": grade(task, naive["answer"]), "buyer_correct": grade(task, buyer["answer"])}


def top3_shared(log):
    ours = {r["url"] for r in sorted(log["results"], key=lambda r: -r["usefulness"])[:3]}
    return len(ours & {r["url"] for r in log["results"] if r["keenable_rank"] <= 3})


def pick(train, budget):
    """Rule: both agents correct, our top 3 shares at most 1 page with Keenable's top 3.
    Among those: fewest shared pages, then lowest task id."""
    rows = []
    for task in train:
        d = run(task, train, budget)
        shared = top3_shared(d["naive"])
        rows.append((task["id"], shared, d["naive_correct"], d["buyer_correct"],
                     shared <= 1 and d["naive_correct"] and d["buyer_correct"], task["question"]))
    ok = sorted(r for r in rows if r[4])
    chosen = min(ok, key=lambda r: (r[1], r[0]))[0] if ok else None
    out = ["# Demo query candidates", "",
           "All 18 training tasks were checked. Held-out tasks are never used for the demo.",
           "Rule: both agents answer correctly, and our top 3 shares at most 1 page with Keenable's top 3.",
           "Among those: fewest shared pages, then lowest task id. The usage history excludes the task itself.", "",
           f"**Chosen: {chosen or 'none qualifies'}**", "",
           "| task | top-3 pages shared with Keenable | naive correct | ours correct | qualifies | question |",
           "|---|---|---|---|---|---|"]
    out += [f"| {i} | {s} | {'yes' if n else 'no'} | {'yes' if b else 'no'} | {'yes' if q else 'no'} | {text} |"
            for i, s, n, b, q, text in rows]
    out += ["", "This is the best-looking example, not the average. The demo's end card shows the held-out average."]
    (ROOT / "demo_candidates.md").write_text("\n".join(out) + "\n")
    print(f"Chosen: {chosen}. Wrote demo_candidates.md")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--pace", type=float, default=0, help="extra seconds between beats, for narration")
    parser.add_argument("--task", help="training task id (default: demo_task_id in config.json)")
    parser.add_argument("--pick", action="store_true", help="check all training tasks and write demo_candidates.md")
    parser.add_argument("--live", action="store_true", help="allow network calls (default: cache only)")
    parser.add_argument("--no-open", action="store_true", help="build demo.html without opening a browser")
    args = parser.parse_args()
    if not args.live:
        os.environ["OFFLINE"] = "1"

    config = json.loads((ROOT / "config.json").read_text())
    tasks = json.loads((ROOT / "tasks.json").read_text())["tasks"]
    train = [t for t in tasks if t["split"] == "train"]
    if args.pick:
        return pick(train, config["budget_cents"])

    task = next((t for t in train if t["id"] == (args.task or config["demo_task_id"])), None)
    if task is None:
        raise SystemExit("The demo query must be one of the training tasks.")
    data = run(task, train, config["budget_cents"])
    report = json.loads((ROOT / "eval_report.json").read_text())
    data["end_card"] = [r for r in report if r["eval"].startswith(("E5", "END-TO-END"))]
    data["pace"] = args.pace
    html = (ROOT / "demo_template.html").read_text().replace("/*DATA*/null", json.dumps(data).replace("</", "<\\/"))
    (ROOT / "demo.html").write_text(html)
    if not args.no_open:
        webbrowser.open((ROOT / "demo.html").as_uri())


if __name__ == "__main__":
    main()
