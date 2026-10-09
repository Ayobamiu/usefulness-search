"""Naive agent, buyer agent and the same-budget Keenable baseline.

All agents use the same model and the same prompt on the same cached pages.
The only differences are which pages get read, and that the buyer is shown our notes on them.

A task is {"id", "question"} plus optionally "query" (what to search for, default: the question)
and "kind": "docs" (default), "alert" (research a sales alert) or "sales" (outreach from the latest news).

Every agent returns a run log:
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
   "tokens":  {"prompt", "completion", "total"}              the agent's reading call, from the API usage fields
   "scoring": {"embedding", "chat_prompt", "chat_completion"} tokens OUR scoring used for this query
                                      (zeros for agents that do not use our scores)}
"""
import hashlib
import json

import clients
import usefulness

PROMPTS = {
    "docs": (
        "You answer a coding documentation question using ONLY the pages provided. "
        "Be short and state the specific fact asked for. If the pages do not contain the answer, "
        "say that you could not find it.\n"
        "Cite the URL of every page you actually took the answer from, and no other page.\n"
        'Reply with JSON: {"answer": "...", "citations": ["<url>", ...]}'),
    "alert": (
        "You complete the task using ONLY the pages provided. Keep it to one short paragraph.\n"
        "If the search layer marks a page as superseded, trust the newer event.\n"
        "Cite the URL of every page you actually took facts from, and no other page.\n"
        'Reply with JSON: {"answer": "...", "citations": ["<url>", ...]}'),
}
PROMPTS["sales"] = PROMPTS["alert"]

# The buyer stops when the best remaining page is worth less than this.
STOP_BELOW_USEFULNESS = 0.45
NO_SCORING = {"embedding": 0, "chat_prompt": 0, "chat_completion": 0, "strong_prompt": 0, "strong_completion": 0}


def answer_model(task):
    """The answering model for this kind of task. The same for every agent."""
    return clients.CONFIG.get("answer_models", {}).get(task.get("kind", "docs"), clients.CONFIG["chat_model"])


def _slim(offer):
    return {k: offer[k] for k in ("url", "usefulness", "price_cents")}


def superseded_note(page):
    by = page.get("superseded_by")
    if not by:
        return ""
    if by.get("event"):
        return f'Superseded: {by["event"]} (source: "{by["title"]}")'
    return f'superseded by "{by["title"]}"' + (f' ({by["published"]})' if by["published"] else "")


def _answer(task, pages, run, notes=False, results=()):
    """The one prompt all agents share. Reads the pages and returns answer, citations, tokens.

    Pages are shown in a fixed shuffled order (by URL hash), the same rule for every agent,
    so the model cannot favour a page just because a ranking put it first.
    With notes=True (the buyer), the agent also sees what the search layer said before it bought:
    which results are superseded, as a short list, and the same note on top of any such page it read.
    """
    read = []
    for page in sorted(pages, key=lambda p: hashlib.sha256(p["url"].encode()).hexdigest()):
        try:
            content = clients.keenable_fetch(page["url"]).get("content") or page["snippet"]
        except RuntimeError:
            content = page["snippet"]
        note = f"NOTE: {superseded_note(page)}.\n" if notes and page.get("superseded_by") else ""
        read.append(f"URL: {page['url']}\nTITLE: {page['title']}\n{note}{content}")
    # One line per distinct later event, with the results it replaces.
    events = {}
    for r in results:
        if notes and r.get("superseded_by"):
            events.setdefault(superseded_note(r), []).append(r["title"])
    flagged = [f'- {note}. This replaces what these results report: ' + "; ".join(f'"{t}"' for t in titles)
               for note, titles in events.items()]
    layer = "Search layer notes for this query (some results are marked as superseded):\n" + "\n".join(flagged) + "\n\n" if flagged else ""
    reply = clients.chat([{"role": "system", "content": PROMPTS[task.get("kind", "docs")]},
                          {"role": "user", "content": f"Question: {task['question']}\n\n{layer}" + "\n\n-----\n\n".join(read)}],
                         run=run, json_mode=True, model=answer_model(task))
    out = json.loads(reply["content"])
    urls = {p["url"] for p in pages}
    cited = [c for c in out.get("citations", []) if isinstance(c, str)]
    usage = reply["usage"]
    return {"answer": str(out.get("answer", "")),
            "citations": [c for c in cited if c in urls],
            "invalid_citations": [c for c in cited if c not in urls],
            "tokens": {"prompt": usage["prompt_tokens"], "completion": usage["completion_tokens"],
                       "total": usage["total_tokens"], "model": answer_model(task)}}


def _log(task, agent, run, results, purchases, scoring=NO_SCORING):
    order = [p["url"] for p in purchases]
    pages = sorted((r for r in results if r["url"] in order), key=lambda r: order.index(r["url"]))
    return {"task_id": task["id"], "agent": agent, "run": run, "query": _query(task),
            "results": results, "fetched": [p["url"] for p in pages], "purchases": purchases,
            "spent_cents": sum(p["price_cents"] for p in purchases), "scoring": dict(scoring),
            **_answer(task, pages, run, notes=agent == "buyer", results=results)}


def _query(task):
    return task.get("query", task["question"])


def _search(task, history):
    return usefulness.search(_query(task), history)


def totals(log):
    """Tokens and simulated cost for one query, WITH our scoring work counted.

    total_cents = pages bought (simulated prices) + every model token at the configured prices.
    """
    price = clients.CONFIG["token_prices_usd_per_million"]
    s, t = log["scoring"], log["tokens"]
    cents = lambda n, kind: n * price[kind] / 1e6 * 100
    tier = "chat" if t.get("model", clients.CONFIG["chat_model"]) == clients.CONFIG["chat_model"] else "strong"
    reading_cents = cents(t["prompt"], tier + "_input") + cents(t["completion"], tier + "_output")
    scoring_cents = (cents(s["chat_prompt"], "chat_input") + cents(s["chat_completion"], "chat_output")
                     + cents(s.get("strong_prompt", 0), "strong_input") + cents(s.get("strong_completion", 0), "strong_output")
                     + cents(s["embedding"], "embedding"))
    scoring_tokens = sum(s.values())
    return {"reading_tokens": t["total"], "scoring_tokens": scoring_tokens, "total_tokens": t["total"] + scoring_tokens,
            "page_cents": log["spent_cents"], "reading_cents": reading_cents, "scoring_cents": scoring_cents,
            "total_cents": log["spent_cents"] + reading_cents + scoring_cents}


def run_naive(task, history, run=0):
    """Reads the top 10 pages in Keenable's order and pays the listed price for each.
    It does not use our scores, so it is not charged for scoring."""
    results = _search(task, history)
    left = sorted(results, key=lambda r: r["keenable_rank"])
    purchases = [{**_slim(r), "offers_before": [_slim(o) for o in left[i:]]} for i, r in enumerate(left)]
    return _log(task, "naive", run, results, purchases)


def run_topk(task, history, budget_cents, run=0):
    """Same-budget baseline: buys in Keenable's order until the next page is unaffordable."""
    results = _search(task, history)
    queue = sorted(results, key=lambda r: r["keenable_rank"])
    purchases, left = [], budget_cents
    for i, r in enumerate(queue):
        if r["price_cents"] > left:
            break
        purchases.append({**_slim(r), "offers_before": [_slim(o) for o in queue[i:]]})
        left -= r["price_cents"]
    return _log(task, "topk", run, results, purchases)


def run_buyer(task, history, budget_cents, run=0):
    """Buys in order of usefulness per cent, within the budget. Charged for all scoring it relies on."""
    with clients.metering() as scoring:
        results = _search(task, history)
        remaining, bought, purchases, left = list(results), [], [], budget_cents
        while remaining:
            offers = usefulness.reprice_after_purchase(_query(task), remaining, bought)
            affordable = [o for o in offers if o["price_cents"] <= left]
            if not affordable:
                break
            best = max(affordable, key=lambda o: o["usefulness"] / max(o["price_cents"], 1e-9))
            if best["usefulness"] < STOP_BELOW_USEFULNESS and purchases:
                break                     # the stop rule never leaves the agent with nothing to read
            purchases.append({**_slim(best), "offers_before": [_slim(o) for o in offers]})
            left -= best["price_cents"]
            bought.append(next(r for r in remaining if r["url"] == best["url"]))
            remaining = [r for r in remaining if r["url"] != best["url"]]
    return _log(task, "buyer", run, results, purchases, scoring)
