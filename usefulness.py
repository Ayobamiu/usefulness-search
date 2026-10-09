"""Usefulness scorer and pricing. Prices are SIMULATED.

Shapes:
  page    {"url", "title", "snippet", "published": "YYYY-MM-DD" or "" (a hint only),
           "superseded_by": None or {"url", "title", "published", "event"}}
  result  page + {"keenable_rank": int (1 = Keenable's top), "usefulness": float in [0, 1],
                  "price_cents": float >= 0 (SIMULATED), "is_new": bool}
  history {"pages": {url: {"fetched": n, "cited": n}}, "domains": {domain: {"fetched": n, "cited": n}}}
"""
import copy
import json
import math
import re
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
#   If a later page in the same result set replaces or reverses this page's event,
#   the whole score is multiplied by (1 - W_SUPERSEDED). Price follows through the price rule.
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
W_SUPERSEDED = 0.50         # share of usefulness a superseded page loses (tuned on the tuning alert cases only)

# Embedding cosines for text-embedding-3-small rarely leave this band; stretch it to 0..1.
SIMILARITY_LOW, SIMILARITY_HIGH = 0.15, 0.75

# price = PRICE_FLOOR + PRICE_PER_USEFULNESS * usefulness  (cents, simulated)
PRICE_FLOOR_CENTS = 0.5
PRICE_PER_USEFULNESS_CENTS = 3.5

# A page that states the same answer as one already bought loses this share of its usefulness.
DUPLICATE_DISCOUNT = 0.35

DUPLICATE_PROMPT = (
    "A question is shown with the search results an agent ALREADY HAS and numbered CANDIDATE results. "
    "Which candidates state the same answer to the question as a result the agent already has, so that "
    "reading them would add nothing new?\n"
    'Reply with JSON: {"duplicates": [<candidate numbers>]} (an empty list if none).')
DUPLICATE_SNIPPET_CHARS = 400   # keeps the check cheap: it is charged against our savings

FRESHNESS_PROMPT = (
    "Below are numbered search results for one query about a company. Find every page whose main news about "
    "that company is no longer the current state of affairs, because ANOTHER page in this set reports a later "
    "event that replaces or reverses it. Examples: a product launch, then the product is shut down; a deal, "
    "then the deal collapses; an executive is appointed, then leaves; an expansion or funding round, then a "
    "bankruptcy or closure; a partnership, then its end.\n"
    "Rules:\n"
    "- Flag a page only when another page IN THIS SET reports the later event. Name that page in \"by\".\n"
    "- A page that itself reports the later event is never flagged, even if it also retells the earlier one.\n"
    "- A later page that continues, confirms or completes the earlier event does not replace it.\n"
    "- Do not judge whether anything is true in general, and do not use outside knowledge.\n"
    "- Publish dates are a hint only: old stories get republished with new dates. Decide from what the pages "
    "say happened and when.\n"
    'Reply with JSON: {"superseded": [{"page": <number>, "by": <number of the later page>, '
    '"later_event": "<the later event and when it happened, at most 15 words>"}]} (an empty list if none).')

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


def published(result):
    """Publish date as YYYY-MM-DD from Keenable's field or the URL, else "". Never the crawl time."""
    for key in ("published_at", "published", "publish_date"):
        if result.get(key):
            return str(result[key])[:10]
    m = re.search(r"/(20\d\d)/(\d\d)/(\d\d)/", result["url"])
    return "-".join(m.groups()) if m else ""


def freshness(query, pages):
    """One call per result set, on the stronger freshness model. {url: the later page and event that replace it}."""
    listing = "\n\n".join(f"[{i}] {p['title']}\npublished: {p.get('published') or 'unknown'}\n{p['snippet'][:600]}"
                           for i, p in enumerate(pages, 1))
    reply = clients.chat([{"role": "system", "content": FRESHNESS_PROMPT},
                          {"role": "user", "content": f"Query: {query}\n\n{listing}"}], json_mode=True,
                         model=clients.CONFIG["freshness_model"])
    superseded = {}
    for item in json.loads(reply["content"]).get("superseded", []):
        try:
            old, new = pages[int(item["page"]) - 1], pages[int(item["by"]) - 1]
        except (KeyError, ValueError, TypeError, IndexError):
            continue
        if old is not new:
            superseded[old["url"]] = {**{k: new.get(k, "") for k in ("url", "title", "published")},
                                      "event": str(item.get("later_event", ""))[:200]}
    # A page cannot be replaced by a page that is itself replaced by it.
    return {url: by for url, by in superseded.items() if superseded.get(by["url"], {}).get("url") != url}


def score(query, page, history):
    """Usefulness in [0, 1] of this page for THIS query."""
    return (1 - W_SUPERSEDED * bool(page.get("superseded_by"))) * (BASELINE
            + W_SIMILARITY * _similarity(query, page)
            + W_ANSWER_CHECK * _answer_check(query, page)
            + W_KEENABLE_RANK * _rank_prior(page)
            + W_PAGE_USAGE * _page_usage(history["pages"].get(page["url"]))
            + W_DOMAIN_USAGE * _usage(history["domains"].get(_domain(page["url"]))))


def price_cents(usefulness):
    """Simulated price. Never decreases as usefulness increases."""
    return round(PRICE_FLOOR_CENTS + PRICE_PER_USEFULNESS_CENTS * usefulness, 4)


def search(query, history, check_freshness=True):
    """Keenable's top pages for the query, each as a `result`."""
    pages = [{"url": r["url"], "title": r.get("title") or r["url"],
              "snippet": r.get("snippet") or r.get("description") or "", "keenable_rank": rank,
              "published": published(r)}
             for rank, r in enumerate(clients.keenable_search(query), 1)]
    replaced = freshness(query, pages) if pages and check_freshness else {}
    for p in pages:
        p["superseded_by"] = replaced.get(p["url"])
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


def _brief(page):
    return f"{page['title']}\n{page['snippet'][:DUPLICATE_SNIPPET_CHARS]}"


def reprice_after_purchase(query, offers, bought_pages):
    """Offers re-scored and re-priced given what was already bought: duplicates lose value.

    One model call per purchase, covering every remaining offer.
    Always pass the ORIGINAL offers, so the discount is not applied twice.
    """
    duplicates = set()
    if bought_pages and offers:
        have = "\n\n".join(f"- {_brief(p)}" for p in bought_pages)
        candidates = "\n\n".join(f"[{i}] {_brief(o)}" for i, o in enumerate(offers, 1))
        reply = clients.chat([{"role": "system", "content": DUPLICATE_PROMPT},
                              {"role": "user", "content": f"Question: {query}\n\nALREADY HAS:\n{have}"
                                                          f"\n\nCANDIDATES:\n{candidates}"}], json_mode=True)
        duplicates = {n for n in json.loads(reply["content"]).get("duplicates", []) if isinstance(n, int)}
    repriced = []
    for i, offer in enumerate(offers, 1):
        u = offer["usefulness"] * (1 - DUPLICATE_DISCOUNT * (i in duplicates))
        repriced.append({**offer, "usefulness": u, "price_cents": price_cents(u), "duplicate": i in duplicates})
    return repriced
