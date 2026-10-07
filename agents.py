"""Naive agent and buyer agent. NOT IMPLEMENTED YET (build steps 3 and 5).

Both agents use the same model and the same prompt on the same cached pages.
The only difference is which pages get read.

Both return a run log:
  {"task_id", "agent": "naive" | "buyer", "run": int, "query",
   "results":   [result, ...]         what the search layer returned
   "fetched":   [url, ...]            pages actually read
   "purchases": [{"url", "usefulness", "price_cents",
                  "offers_before": [{"url", "usefulness", "price_cents"}, ...]}, ...]
                                      in buying order; offers_before = everything still
                                      unbought at that moment, at its price at that moment
   "spent_cents": float               SIMULATED
   "answer": str, "citations": [url, ...]
   "tokens": {"prompt", "completion", "total"}   from the API usage fields}
"""


def run_naive(task, history, run=0):
    """Reads the top 10 pages in Keenable's order and pays the listed price for each."""
    raise NotImplementedError("naive agent (step 3)")


def run_buyer(task, history, budget_cents, run=0):
    """Buys in order of usefulness per cent, within the budget."""
    raise NotImplementedError("buyer agent (step 5)")
