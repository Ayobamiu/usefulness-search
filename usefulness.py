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
#              + W_KEENABLE_RANK * Keenable's own rank (1st = 1, 10th = 0)  0..1
#              + W_PAGE_USAGE   * page usage                             -1..+1
#              + W_DOMAIN_USAGE * domain usage                           -1..+1
#
#   usage = +1 if always cited when read, -1 if read and never cited, 0 if never read.
#   The weights sum to 1 with BASELINE, so the result always stays inside [0, 1].
#
BASELINE = 0.15
W_SIMILARITY = 0.25
W_ANSWER_CHECK = 0.25
W_KEENABLE_RANK = 0.15      # we build on Keenable's ranking, we do not replace it
W_PAGE_USAGE = 0.15
W_DOMAIN_USAGE = 0.05

# Embedding cosines for text-embedding-3-small rarely leave this band; stretch it to 0..1.
SIMILARITY_LOW, SIMILARITY_HIGH = 0.15, 0.75

# price = PRICE_FLOOR + PRICE_PER_USEFULNESS * usefulness  (cents, simulated)
PRICE_FLOOR_CENTS = 0.5
PRICE_PER_USEFULNESS_CENTS = 3.5

# A page that states the same answer as one already bought loses this share of its usefulness.
DUPLICATE_DISCOUNT = 0.35

DUPLICATE_PROMPT = (
    "Two search results for the same coding question are shown. Decide whether result B states the same "
    "answer to the question as result A, so that reading B after A would add nothing new.\n"
    'Reply with JSON: {"same_answer": true} or {"same_answer": false}')

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


def _rank_prior(page):
    """1 for Keenable's top result, 0 for its 10th. Neutral 0.5 for a page Keenable did not rank."""
    rank = page.get("keenable_rank")
    return 0.5 if rank is None else max(0.0, 1 - (rank - 1) / 9)


def _domain(url):
    return urlparse(url).netloc.removeprefix("www.")


def score(query, page, history):
    """Usefulness in [0, 1] of this page for THIS query."""
    return (BASELINE
            + W_SIMILARITY * _similarity(query, page)
            + W_ANSWER_CHECK * _answer_check(query, page)
            + W_KEENABLE_RANK * _rank_prior(page)
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


def _same_answer(query, bought, offer):
    reply = clients.chat([{"role": "system", "content": DUPLICATE_PROMPT},
                          {"role": "user", "content": f"Question: {query}\n\nResult A:\n{_text(bought)}"
                                                      f"\n\nResult B:\n{_text(offer)}"}], json_mode=True)
    return json.loads(reply["content"]).get("same_answer") is True


def reprice_after_purchase(query, offers, bought_pages):
    """Offers re-scored and re-priced given what was already bought: duplicates lose value.

    Always pass the ORIGINAL offers, so the discount is not applied twice.
    """
    def reprice(offer):
        duplicate = any(_same_answer(query, bought, offer) for bought in bought_pages)
        u = offer["usefulness"] * (1 - DUPLICATE_DISCOUNT * duplicate)
        return {**offer, "usefulness": u, "price_cents": price_cents(u), "duplicate": duplicate}
    with ThreadPoolExecutor(len(offers) or 1) as pool:
        return list(pool.map(reprice, offers))
