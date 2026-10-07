"""Usefulness scorer and pricing. NOT IMPLEMENTED YET (build step 4).

The signatures below are the contract run_evals.py tests against.

Shapes:
  page    {"url", "title", "snippet"}
  result  page + {"keenable_rank": int (1 = Keenable's top), "usefulness": float in [0, 1],
                  "price_cents": float >= 0 (SIMULATED), "is_new": bool}
  history {"pages": {url: {"fetched": n, "cited": n}}, "domains": {domain: {"fetched": n, "cited": n}}}
"""


def empty_history():
    return {"pages": {}, "domains": {}}


def score(query, page, history):
    """Usefulness in [0, 1] of this page for THIS query."""
    raise NotImplementedError("scorer (step 4)")


def price_cents(usefulness):
    """Simulated price. Must never decrease as usefulness increases."""
    raise NotImplementedError("pricing (step 4)")


def search(query, history):
    """Keenable's top pages for the query, each as a `result`."""
    raise NotImplementedError("search layer (step 4)")


def update_history(history, run_log):
    """New history after one run: cited pages move up, fetched-but-uncited move down."""
    raise NotImplementedError("usage loop (step 4)")


def reprice_after_purchase(query, offers, bought_pages):
    """Offers re-scored and re-priced given what was already bought: duplicates lose value."""
    raise NotImplementedError("duplicate discount (step 5)")
