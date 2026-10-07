"""Tuning alert cases only (never the held-out ones): what gets flagged, what the buyer buys, who goes stale."""
import json, re, sys
sys.path.insert(0, ".")
import agents, usefulness as u
A = json.load(open("alert_cases.json")); E = u.empty_history()
show = sys.argv[1:]
for c in A["cases"]:
    if c["split"] != "tune": continue
    task = {"id": c["id"], "kind": "alert", "query": c["query"], "question": A["task"].format(alert=c["alert"], name=c["name"])}
    n = agents.run_naive(task, E); b = agents.run_buyer(task, E, 10)
    res = b["results"]; rk = {r["url"]: r["keenable_rank"] for r in res}
    m = lambda pat, r: bool(re.search(pat, f"{r['title']} {r['snippet']}".lower()))
    stale = lambda a: bool(re.search(c["old"], a.lower())) and not re.search(c["new"], a.lower())
    tb, tn = agents.totals(b), agents.totals(n)
    print(c["id"], c["name"][:12], "| old-kw", [r["keenable_rank"] for r in res if m(c["old"], r) and not m(c["new"], r)],
          "flagged", [f"{r['keenable_rank']}<-{rk[r['superseded_by']['url']]}" for r in res if r["superseded_by"]],
          "| stale naive", stale(n["answer"]), "ours", stale(b["answer"]), "bought", [rk[x] for x in b["fetched"]],
          "| tok naive", tn["total_tokens"], "ours", tb["reading_tokens"], "+", tb["scoring_tokens"])
    if c["id"] in show: print("   ", b["answer"][:500])
