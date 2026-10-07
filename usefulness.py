"""Usefulness scorer and pricing. Prices are SIMULATED.

Shapes:
  page    {"url", "title", "snippet"}
  result  page + {"keenable_rank": int (1 = Keenable's top), "usefulness": float in [0, 1],
                  "price_cents": float >= 0 (SIMULATED), "is_new": bool}
  history {"pages": {url: {"fetched": n, "cited": n}}, "domains": {domain: {"fetched": n, "cited": n}}}
"""
import copy
import json
import math
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

import clients

# ---- the whole formula, on one slide -----------------------------------------
#
#   usefulness = BASELINE
#              + W_SIMILARITY   * similarity(query, title + snippet)     0..1
#              + W_ANSWER_CHECK * "does this snippet answer the query?"  0, 0.5 or 1
#              + W_PAGE_USAGE   * page usage                             -1..+1
#              + W_DOMAIN_USAGE * domain usage                           -1..+1
#
#   usage = +1 if always cited when read, -1 if read and never cited, 0 if never read.
#   The weights sum to 1 with BASELINE, so the result always stays inside [0, 1].
#
BASELINE = 0.20
W_SIMILARITY = 0.30
W_ANSWER_CHECK = 0.30
W_PAGE_USAGE = 0.15
W_DOMAIN_USAGE = 0.05

# Embedding cosines for text-embedding-3-small rarely leave this band; stretch it to 0..1.
SIMILARITY_LOW, SIMILARITY_HIGH = 0.15, 0.75

# price = PRICE_FLOOR + PRICE_PER_USEFULNESS * usefulness  (cents, simulated)
PRICE_FLOOR_CENTS = 0.5
PRICE_PER_USEFULNESS_CENTS = 3.5

# A page whose snippet is this similar to one already bought repeats it and loses value.
DUPLICATE_FROM = 0.70       # snippet-to-snippet cosine where the discount starts
DUPLICATE_MAX_DISCOUNT = 0.6

CHECK_PROMPT = (
    "You judge search results for a coding question. Given the question and one result's "
    "title and snippet, decide whether the snippet itself contains the answer.\n"
    'Reply with JSON: {"verdict": "yes"} if it states the answer, {"verdict": "partial"} if it '
    'is on the exact topic but does not state the answer, {"verdict": "no"} otherwise.')
VERDICTS = {"yes": 1.0, "partial": 0.5, "no": 0.0}


def empty_history():
    return {"pages": {}, "domains": {}}


def _text(page):
    return f"{page['title']}\n{page['snippet']}"[:2000]


def _cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


def _similarity(query, page):
    q, p = clients.embed([query, _text(page)])
    scaled = (_cosine(q, p) - SIMILARITY_LOW) / (SIMILARITY_HIGH - SIMILARITY_LOW)
    return min(1.0, max(0.0, scaled))


def _answer_check(query, page):
    reply = clients.chat([{"role": "system", "content": CHECK_PROMPT},
                          {"role": "user", "content": f"Question: {query}\n\nResult:\n{_text(page)}"}],
                         json_mode=True)
    return VERDICTS.get(json.loads(reply["content"]).get("verdict"), 0.0)


def _usage(counts):
    """-1..+1. Zero with no history; smoothed so one read does not swing a whole domain."""
    if not counts:
        return 0.0
    return 2 * (counts["cited"] + 1) / (counts["fetched"] + 2) - 1


def _page_usage(counts):
    """-1..+1 from this exact page's record: the share of reads that ended in a citation."""
    if not counts:
        return 0.0
    return 2 * counts["cited"] / counts["fetched"] - 1


def _domain(url):
    return urlparse(url).netloc.removeprefix("www.")


def score(query, page, history):
    """Usefulness in [0, 1] of this page for THIS query."""
    return (BASELINE
            + W_SIMILARITY * _similarity(query, page)
            + W_ANSWER_CHECK * _answer_check(query, page)
            + W_PAGE_USAGE * _page_usage(history["pages"].get(page["url"]))
            + W_DOMAIN_USAGE * _usage(history["domains"].get(_domain(page["url"]))))


def price_cents(usefulness):
    """Simulated price. Never decreases as usefulness increases."""
    return round(PRICE_FLOOR_CENTS + PRICE_PER_USEFULNESS_CENTS * usefulness, 4)


def search(query, history):
    """Keenable's top pages for the query, each as a `result`."""
    pages = [{"url": r["url"], "title": r.get("title") or r["url"],
              "snippet": r.get("snippet") or r.get("description") or "", "keenable_rank": rank}
             for rank, r in enumerate(clients.keenable_search(query), 1)]
    with ThreadPoolExecutor(len(pages) or 1) as pool:
        scores = list(pool.map(lambda p: score(query, p, history), pages))
    return [{**p, "usefulness": u, "price_cents": price_cents(u), "is_new": p["url"] not in history["pages"]}
            for p, u in zip(pages, scores)]


def update_history(history, run_log):
    """New history after one run: cited pages move up, fetched-but-uncited move down."""
    history = copy.deepcopy(history)
    for url in run_log["fetched"]:
        for table, key in ((history["pages"], url), (history["domains"], _domain(url))):
            counts = table.setdefault(key, {"fetched": 0, "cited": 0})
            counts["fetched"] += 1
            counts["cited"] += url in run_log["citations"]
    return history


def reprice_after_purchase(query, offers, bought_pages):
    """Offers re-scored and re-priced given what was already bought: duplicates lose value.

    Always pass the ORIGINAL offers, so the discount is not applied twice.
    """
    if not bought_pages or not offers:
        return [dict(o) for o in offers]
    bought = clients.embed([_text(p) for p in bought_pages])
    repriced = []
    for offer, vector in zip(offers, clients.embed([_text(o) for o in offers])):
        overlap = max(_cosine(vector, b) for b in bought)
        repeat = max(0.0, (overlap - DUPLICATE_FROM) / (1 - DUPLICATE_FROM))
        u = offer["usefulness"] * (1 - DUPLICATE_MAX_DISCOUNT * repeat)
        repriced.append({**offer, "usefulness": u, "price_cents": price_cents(u), "duplicate": repeat > 0})
    return repriced
