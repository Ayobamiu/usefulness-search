"""Naive agent, buyer agent and the same-budget Keenable baseline.

Both agents use the same model and the same prompt on the same cached pages.
The only difference is which pages get read.

Both return a run log:
  {"task_id", "agent": "naive" | "buyer" | "topk", "run": int, "query",
   "results":   [result, ...]         what the search layer returned
   "fetched":   [url, ...]            pages actually read
   "purchases": [{"url", "usefulness", "price_cents",
                  "offers_before": [{"url", "usefulness", "price_cents"}, ...]}, ...]
                                      in buying order; offers_before = everything still
                                      unbought at that moment, at its price at that moment
   "spent_cents": float               SIMULATED
   "answer": str, "citations": [url, ...]
   "invalid_citations": [str, ...]    cited by the model but never read; not counted as used
   "tokens": {"prompt", "completion", "total"}   from the API usage fields}
"""
import hashlib
import json

import clients
import usefulness

ANSWER_PROMPT = (
    "You answer a coding documentation question using ONLY the pages provided. "
    "Be short and state the specific fact asked for. If the pages do not contain the answer, "
    "say that you could not find it.\n"
    "Cite the URL of every page you actually took the answer from, and no other page.\n"
    'Reply with JSON: {"answer": "...", "citations": ["<url>", ...]}')

# The buyer stops when the best remaining page is worth less than this.
STOP_BELOW_USEFULNESS = 0.45


def _slim(offer):
    return {k: offer[k] for k in ("url", "usefulness", "price_cents")}


def _answer(question, pages, run):
    """The one prompt both agents share. Reads the pages and returns answer, citations, tokens."""
    # Pages are shown in a fixed shuffled order (by URL hash), the same rule for every agent,
    # so the model cannot favour a page just because a ranking put it first.
    read = []
    for page in sorted(pages, key=lambda p: hashlib.sha256(p["url"].encode()).hexdigest()):
        try:
            content = clients.keenable_fetch(page["url"]).get("content") or page["snippet"]
        except RuntimeError:
            content = page["snippet"]
        read.append(f"URL: {page['url']}\nTITLE: {page['title']}\n{content}")
    reply = clients.chat([{"role": "system", "content": ANSWER_PROMPT},
                          {"role": "user", "content": f"Question: {question}\n\n" + "\n\n-----\n\n".join(read)}],
                         run=run, json_mode=True)
    out = json.loads(reply["content"])
    urls = {p["url"] for p in pages}
    cited = [c for c in out.get("citations", []) if isinstance(c, str)]
    usage = reply["usage"]
    return {"answer": str(out.get("answer", "")),
            "citations": [c for c in cited if c in urls],
            "invalid_citations": [c for c in cited if c not in urls],
            "tokens": {"prompt": usage["prompt_tokens"], "completion": usage["completion_tokens"],
                       "total": usage["total_tokens"]}}


def _log(task, agent, run, results, purchases):
    bought = {p["url"] for p in purchases}
    pages = [r for r in results if r["url"] in bought]
    pages.sort(key=lambda r: [p["url"] for p in purchases].index(r["url"]))
    return {"task_id": task["id"], "agent": agent, "run": run, "query": task["question"],
            "results": results, "fetched": [p["url"] for p in pages], "purchases": purchases,
            "spent_cents": sum(p["price_cents"] for p in purchases),
            **_answer(task["question"], pages, run)}


def run_naive(task, history, run=0):
    """Reads the top 10 pages in Keenable's order and pays the listed price for each."""
    results = usefulness.search(task["question"], history)
    left = sorted(results, key=lambda r: r["keenable_rank"])
    purchases = [{**_slim(r), "offers_before": [_slim(o) for o in left[i:]]} for i, r in enumerate(left)]
    return _log(task, "naive", run, results, purchases)


def run_topk(task, history, budget_cents, run=0):
    """Same-budget baseline: buys in Keenable's order until the next page is unaffordable."""
    results = usefulness.search(task["question"], history)
    queue = sorted(results, key=lambda r: r["keenable_rank"])
    purchases, left = [], budget_cents
    for i, r in enumerate(queue):
        if r["price_cents"] > left:
            break
        purchases.append({**_slim(r), "offers_before": [_slim(o) for o in queue[i:]]})
        left -= r["price_cents"]
    return _log(task, "topk", run, results, purchases)


def run_buyer(task, history, budget_cents, run=0):
    """Buys in order of usefulness per cent, within the budget."""
    results = usefulness.search(task["question"], history)
    remaining, bought, purchases, left = list(results), [], [], budget_cents
    while remaining:
        offers = usefulness.reprice_after_purchase(task["question"], remaining, bought)
        affordable = [o for o in offers if o["price_cents"] <= left]
        if not affordable:
            break
        best = max(affordable, key=lambda o: o["usefulness"] / max(o["price_cents"], 1e-9))
        if best["usefulness"] < STOP_BELOW_USEFULNESS:
            break
        purchases.append({**_slim(best), "offers_before": [_slim(o) for o in offers]})
        left -= best["price_cents"]
        bought.append(next(r for r in remaining if r["url"] == best["url"]))
        remaining = [r for r in remaining if r["url"] != best["url"]]
    return _log(task, "buyer", run, results, purchases)
