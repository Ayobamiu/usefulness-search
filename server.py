"""Xtract hosted API. Run: uvicorn server:app

Needs OPENAI_API_KEY, KEENABLE_API_KEY, SUPABASE_URL and SUPABASE_SERVICE_KEY in the environment
(locally, clients.py also reads .env). Keys are never logged, returned or put in errors.
"""
import asyncio
import datetime
import hashlib
import html
import json
import logging
import pathlib
import re
import secrets
import time

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse

import clients
import store
import usefulness

ROOT = pathlib.Path(__file__).parent
REQUEST_TIMEOUT_S = 30
MAX_QUERY_CHARS = 300
MAX_TASK_CHARS = 500
# Snippets are trimmed in the response: the full page is what the price is for, and a 50 KB response
# breaks agent tool-output limits. Scoring still reads the longer text internally.
SNIPPET_CHARS = 400
MAX_SNIPPET_CHARS = 2000
MAX_FEEDBACK_URLS = 50
KEYS_PER_IP_PER_DAY = 3
EMAIL = re.compile(r"^[^@\s]{1,64}@[^@\s]{1,190}\.[^@\s]{2,}$")
# Consumer webmail and disposable inboxes. A company address is any other domain.
# Checked before a key is issued, so a rejected address does not use the daily key allowance.
FREE_EMAIL_DOMAINS = frozenset({
    "gmail.com", "googlemail.com",
    "yahoo.com", "yahoo.co.uk", "yahoo.fr", "yahoo.de", "yahoo.ca", "yahoo.com.au", "yahoo.co.in", "yahoo.co.jp",
    "ymail.com", "rocketmail.com",
    "hotmail.com", "hotmail.co.uk", "hotmail.fr", "outlook.com", "outlook.co.uk", "outlook.fr",
    "live.com", "live.co.uk", "msn.com",
    "icloud.com", "me.com", "mac.com",
    "aol.com", "aim.com",
    "proton.me", "protonmail.com", "protonmail.ch", "pm.me",
    "gmx.com", "gmx.net", "gmx.de", "mail.com", "email.com",
    "yandex.com", "yandex.ru", "inbox.ru",
    "tutanota.com", "tuta.com", "hey.com", "fastmail.com", "duck.com",
    "qq.com", "163.com", "126.com", "naver.com", "daum.net", "hanmail.net",
    "web.de", "freenet.de", "orange.fr", "libero.it", "seznam.cz", "rediffmail.com",
    "example.com", "example.org", "example.net",
    "mailinator.com", "mailinator.net",
    "guerrillamail.com", "guerrillamail.info", "guerrillamail.biz", "guerrillamail.de",
    "guerrillamail.net", "guerrillamail.org", "guerrillamailblock.com",
    "grr.la", "sharklasers.com", "pokemail.net", "spam4.me",
    "yopmail.com", "yopmail.fr", "yopmail.net",
    "10minutemail.com", "10minutemail.net",
    "tempmail.com", "temp-mail.org", "tempmailo.com", "tempinbox.com", "throwawaymail.com", "tmpmail.org",
    "trashmail.com", "trashmail.de", "trash-mail.com",
    "getnada.com", "maildrop.cc", "dispostable.com", "mailnesia.com", "mohmal.com",
    "emailondeck.com", "fakemail.net", "mailsac.com", "discard.email", "moakt.com",
    "emailfake.com", "generator.email", "fakemailgenerator.com", "dropmail.me",
    "burnermail.io", "spamgourmet.com", "mailnull.com", "inboxkitten.com",
    "getairmail.com", "mytemp.email", "mintemail.com",
})

log = logging.getLogger("xtract")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI(title="Xtract", docs_url=None, redoc_url=None, openapi_url=None)
clients.USE_SUPABASE_CACHE = store.enabled()


# ---- plumbing ----------------------------------------------------------------

def _error(status, message):
    return JSONResponse({"error": message}, status_code=status)


@app.exception_handler(HTTPException)
async def _http_error(request, exc):
    return _error(exc.status_code, exc.detail)


@app.middleware("http")
async def _any_error(request, call_next):
    # A middleware, not an exception handler: Starlette re-raises after handlers, and uvicorn then logs the
    # full traceback. Logged: the exception type and, for upstream calls, the service and HTTP status only.
    # Never the message body (upstream errors can echo request details) and never a stack trace.
    try:
        return await call_next(request)
    except Exception as exc:
        upstream = re.match(r"(\w+ https://[^/\s]+)\S* failed: (HTTP \d+)", str(exc))
        log.error("%s %s failed: %s%s", request.method, request.url.path, type(exc).__name__,
                  f" ({upstream.group(1)} {upstream.group(2)})" if upstream else "")
        return _error(500, "internal error, please try again")


async def _run(fn, *args):
    """Runs blocking work off the event loop, and gives up after REQUEST_TIMEOUT_S."""
    try:
        return await asyncio.wait_for(asyncio.to_thread(fn, *args), REQUEST_TIMEOUT_S)
    except asyncio.TimeoutError:
        raise HTTPException(504, f"the request took longer than {REQUEST_TIMEOUT_S} s and was stopped; "
                                 "please try again") from None


def _sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()


def _today_utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT00:00:00Z")


def _key_hash(request):
    """The caller's key hash, or 401. Only the hash ever leaves this function."""
    auth = request.headers.get("authorization", "")
    if not auth.lower().startswith("bearer ") or not auth[7:].strip():
        raise HTTPException(401, "missing API key: send 'Authorization: Bearer <your key>' (get one at /)")
    key_hash = _sha256(auth[7:].strip())
    rows = store.select("api_keys", {"key_hash": f"eq.{key_hash}", "select": "daily_limit,active"})
    if not rows or not rows[0]["active"]:
        raise HTTPException(401, "unknown or inactive API key")
    return key_hash, rows[0]["daily_limit"]


def _load_history(urls):
    """The usage history rows for these pages and their domains, in usefulness.py's shape."""
    urls = sorted(set(urls))
    domains = sorted({usefulness._domain(u) for u in urls})
    history = usefulness.empty_history()
    if urls and store.enabled():   # without Supabase (the saved example) the history is empty
        for row in store.select("page_usage", {"url": store.in_list(urls), "select": "url,fetched,cited"}):
            history["pages"][row["url"]] = {"fetched": row["fetched"], "cited": row["cited"]}
        for row in store.select("domain_usage", {"domain": store.in_list(domains), "select": "domain,fetched,cited"}):
            history["domains"][row["domain"]] = {"fetched": row["fetched"], "cited": row["cited"]}
    return history


def _scoring_cost_usd(meter):
    price = clients.CONFIG["token_prices_usd_per_million"]
    return round(sum(meter[kind] * price[rate] for kind, rate in (
        ("chat_prompt", "chat_input"), ("chat_completion", "chat_output"),
        ("strong_prompt", "strong_input"), ("strong_completion", "strong_output"),
        ("embedding", "embedding"))) / 1e6, 6)


# ---- search ------------------------------------------------------------------

def short_snippet(text, limit):
    """At most `limit` characters, cut at a sentence end when one is near, else at a word, marked with "…"."""
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    cut = text[:limit - 1]
    sentence = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
    if sentence >= limit // 2:
        return cut[:sentence + 1] + " …"
    space = cut.rfind(" ")
    return (cut[:space] if space > 0 else cut) + "…"


def search(query, task=None, snippet_chars=SNIPPET_CHARS):
    """Shared by GET /v1/search and the saved example on the page."""
    with clients.metering() as meter:
        raw = clients.keenable_search(query)
        history = _load_history([r["url"] for r in raw])
        results = usefulness.search(query, history, task=task)
    return {"query": query, "task": task,
            "results": [{"url": r["url"], "title": r["title"], "snippet": short_snippet(r["snippet"], snippet_chars),
                         "keenable_rank": r["keenable_rank"], "usefulness": round(r["usefulness"], 4),
                         "price_cents": r["price_cents"], "is_new": r["is_new"],
                         "superseded_by": r["superseded_by"]} for r in results],
            "scoring_cost_usd": _scoring_cost_usd(meter),
            "prices": "simulated"}


def _search_logged(key_hash, daily_limit, query, task, snippet_chars):
    used = store.count("queries", {"key_hash": f"eq.{key_hash}", "created_at": f"gte.{_today_utc()}"})
    if used >= daily_limit:
        raise HTTPException(429, f"daily limit reached ({daily_limit} searches per key per day, resets 00:00 UTC)")
    start = time.monotonic()
    body = search(query, task, snippet_chars)
    store.insert("queries", [{"key_hash": key_hash, "query": query,
                              "latency_ms": int((time.monotonic() - start) * 1000),
                              "scoring_cost_usd": body["scoring_cost_usd"], "result_count": len(body["results"])}])
    return body


@app.get("/v1/search")
async def v1_search(request: Request, q: str = "", task: str = "", snippet_chars: str = ""):
    key_hash, daily_limit = await _run(_key_hash, request)
    query, task = q.strip(), task.strip() or None
    if not query:
        raise HTTPException(400, "missing query: use /v1/search?q=...")
    if len(query) > MAX_QUERY_CHARS:
        raise HTTPException(400, f"query too long: at most {MAX_QUERY_CHARS} characters")
    if task and len(task) > MAX_TASK_CHARS:
        raise HTTPException(400, f"task too long: at most {MAX_TASK_CHARS} characters")
    chars = SNIPPET_CHARS
    if snippet_chars:
        if not snippet_chars.isdigit() or not 100 <= int(snippet_chars) <= MAX_SNIPPET_CHARS:
            raise HTTPException(400, f"snippet_chars must be a whole number from 100 to {MAX_SNIPPET_CHARS}")
        chars = int(snippet_chars)
    return await _run(_search_logged, key_hash, daily_limit, query, task, chars)


# ---- feedback ----------------------------------------------------------------

def _feedback(fetched, cited):
    history = _load_history(fetched)
    before = {u: usefulness.usage_score(u, history) for u in fetched}
    history = usefulness.update_history(history, {"fetched": fetched, "citations": cited})
    store.upsert("page_usage", [{"url": u, **history["pages"][u]} for u in fetched], "url")
    domains = sorted({usefulness._domain(u) for u in fetched})
    store.upsert("domain_usage", [{"domain": d, **history["domains"][d]} for d in domains], "domain")
    return {"pages": [{"url": u, "cited": u in cited,
                       "usefulness_before": round(before[u], 4),
                       "usefulness_after": round(usefulness.usage_score(u, history), 4),
                       "change": round(usefulness.usage_score(u, history) - before[u], 4)} for u in fetched],
            "note": "before and after are the usage part of usefulness only (-0.2 to +0.2 of the 0 to 1 score); "
                    "the change applies to every later search that returns the page"}


def _url_list(body, name):
    value = body.get(name, [])
    if not isinstance(value, list) or not all(isinstance(u, str) and u.startswith(("http://", "https://"))
                                              and len(u) <= 2000 for u in value):
        raise HTTPException(400, f"'{name}' must be a list of http(s) URLs")
    return list(dict.fromkeys(value))


@app.post("/v1/feedback")
async def v1_feedback(request: Request):
    await _run(_key_hash, request)
    try:
        body = await request.json()
    except ValueError:
        raise HTTPException(400, "body must be JSON: {\"query\", \"fetched\": [urls], \"cited\": [urls]}") from None
    if not isinstance(body, dict):
        raise HTTPException(400, "body must be a JSON object")
    fetched, cited = _url_list(body, "fetched"), _url_list(body, "cited")
    if not fetched:
        raise HTTPException(400, "'fetched' must list at least one URL you read")
    if len(fetched) > MAX_FEEDBACK_URLS:
        raise HTTPException(400, f"at most {MAX_FEEDBACK_URLS} URLs per report")
    if set(cited) - set(fetched):
        raise HTTPException(400, "every cited URL must also be in 'fetched'")
    return await _run(_feedback, fetched, cited)


# ---- keys --------------------------------------------------------------------

def _client_ip(request):
    forwarded = request.headers.get("x-forwarded-for", "")
    return forwarded.split(",")[0].strip() if forwarded else (request.client.host if request.client else "")


def company_email(email):
    domain = email.rsplit("@", 1)[-1].lower().rstrip(".")
    return not any(domain == blocked or domain.endswith("." + blocked) for blocked in FREE_EMAIL_DOMAINS)


def _new_key(email, ip):
    ip_hash = _sha256("xtract-ip:" + ip)
    if store.count("key_requests", {"ip_hash": f"eq.{ip_hash}", "created_at": f"gte.{_today_utc()}"}) >= KEYS_PER_IP_PER_DAY:
        raise HTTPException(429, f"at most {KEYS_PER_IP_PER_DAY} keys per day from one address")
    store.insert("key_requests", [{"ip_hash": ip_hash}])
    key = "xt_" + secrets.token_urlsafe(24)
    store.insert("api_keys", [{"key_hash": _sha256(key), "email": email}])
    return {"api_key": key, "daily_limit": 50,
            "note": "This key is shown once and only its hash is stored. Keep it somewhere safe."}


@app.post("/v1/keys")
async def v1_keys(request: Request):
    try:
        body = await request.json()
    except ValueError:
        raise HTTPException(400, "body must be JSON: {\"email\": \"you@company.com\"}") from None
    email = (body.get("email") if isinstance(body, dict) else None) or ""
    email = email.strip() if isinstance(email, str) else ""
    if not EMAIL.match(email):
        raise HTTPException(400, "a valid email is required")
    if not company_email(email):
        raise HTTPException(400, "a company email is required")
    return await _run(_new_key, email, _client_ip(request))


# ---- page and health ---------------------------------------------------------

def _page():
    example = json.loads((ROOT / "example_response.json").read_text())
    return ((ROOT / "index.html").read_text()
            .replace("{{EXAMPLE_QUERY}}", html.escape(example["response"]["query"]))
            .replace("{{EXAMPLE_DATE}}", html.escape(example["run_on"]))
            .replace("{{EXAMPLE_JSON}}", html.escape(json.dumps(example["response"], indent=2)))
            .replace("{{FREE_EMAIL_DOMAINS}}", json.dumps(sorted(FREE_EMAIL_DOMAINS))))


@app.get("/", response_class=HTMLResponse)
async def index():
    return _page()


@app.get("/healthz")
async def healthz():
    return {"ok": True}


if __name__ == "__main__":
    # python3 server.py example "<query>": runs a real search with empty history and saves it for the page.
    import sys
    if sys.argv[1:2] != ["example"] or len(sys.argv) != 3:
        sys.exit('usage: python3 server.py example "<query>"')
    response = search(sys.argv[2])
    (ROOT / "example_response.json").write_text(json.dumps(
        {"run_on": datetime.date.today().isoformat(), "response": response}, indent=1) + "\n")
    print(json.dumps([[r["keenable_rank"], r["usefulness"], r["price_cents"], bool(r["superseded_by"]), r["title"][:70]]
                      for r in response["results"]], indent=0))
