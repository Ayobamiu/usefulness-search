"""Keenable and OpenAI calls, every response cached to disk keyed by request.

Reruns read from cache/. Set OFFLINE=1 to forbid any network call.
The API keys are read from .env and never written to cache, logs or errors.
"""
import contextlib
import hashlib
import json
import os
import pathlib
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).parent
CACHE = ROOT / "cache"
CONFIG = json.loads((ROOT / "config.json").read_text())


def load_env():
    env = ROOT / ".env"
    if not env.exists():
        return
    for line in env.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            name, value = line.split("=", 1)
            os.environ.setdefault(name.strip(), value.strip().strip("'\""))


load_env()


_meter = None
_meter_lock = threading.Lock()


@contextlib.contextmanager
def metering():
    """Counts the tokens of every model call made inside the block, cached or not.

    Used to charge our own scoring work (embeddings, checks) against our savings.
    """
    global _meter
    outer, _meter = _meter, {"embedding": 0, "chat_prompt": 0, "chat_completion": 0, "strong_prompt": 0, "strong_completion": 0}
    try:
        yield _meter
    finally:
        _meter = outer


def _count(**tokens):
    if _meter is not None:
        with _meter_lock:
            for kind, n in tokens.items():
                _meter[kind] += n


def _cached(service, request, call):
    """Return the cached response for this request, or make the call and cache it."""
    key = hashlib.sha256(json.dumps([service, request], sort_keys=True).encode()).hexdigest()
    path = CACHE / service / f"{key}.json"
    if path.exists():
        return json.loads(path.read_text())["response"]
    if os.environ.get("OFFLINE") == "1":
        raise RuntimeError(f"OFFLINE=1 and no cached {service} response for this request")
    response = call()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"request": request, "response": response}, indent=1))
    return response


def _http(method, url, headers, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Content-Type": "application/json", **headers})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < 3:
                time.sleep(2 ** attempt)
                continue
            # Never echo auth errors: their bodies can contain part of the key.
            detail = "" if e.code in (401, 403) else e.read().decode(errors="replace")[:300]
            raise RuntimeError(f"{method} {url.split('?')[0]} failed: HTTP {e.code} {detail}") from None
        except OSError:  # dropped connection, TLS hiccup, timeout
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)


# ---- Keenable ---------------------------------------------------------------

def _keenable_headers():
    return {"X-API-Key": os.environ["KEENABLE_API_KEY"]}


def keenable_search(query, max_results=None):
    """Raw Keenable results, in Keenable's ranking order."""
    request = {"query": query, "mode": CONFIG["keenable_mode"],
               "max_results": max_results or CONFIG["top_k"]}
    response = _cached("keenable_search", request, lambda: _http(
        "POST", "https://api.keenable.ai/v1/search", _keenable_headers(), request))
    return response.get("results", [])


def keenable_fetch(url):
    """Page content as markdown: {url, title, content, ...}."""
    request = {"url": url, "max_chars": CONFIG["page_max_chars"]}
    return _cached("keenable_fetch", request, lambda: _http(
        "GET", "https://api.keenable.ai/v1/fetch?" + urllib.parse.urlencode(request),
        _keenable_headers()))


# ---- OpenAI -----------------------------------------------------------------

def _openai(path, body):
    return _http("POST", "https://api.openai.com/v1/" + path,
                 {"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]}, body)


def embed(texts):
    """One embedding per text. Cached per text, so repeated snippets cost nothing."""
    model, vectors = CONFIG["embedding_model"], []
    for text in texts:
        response = _cached("openai_embed", {"model": model, "input": text}, lambda: _openai(
            "embeddings", {"model": model, "input": text}))
        _count(embedding=response["usage"]["total_tokens"])
        vectors.append(response["data"][0]["embedding"])
    return vectors


def chat(messages, run=0, json_mode=False, model=None):
    """Returns {"content": str, "usage": {...}} with usage taken from the API response.

    `run` is part of the cache key only: it lets the 3 repeated held-out runs be
    3 real samples that are each still repeatable from cache.
    """
    body = {"model": model or CONFIG["chat_model"], "messages": messages, "temperature": 0}
    if json_mode:
        body["response_format"] = {"type": "json_object"}
    response = _cached("openai_chat", {"body": body, "run": run}, lambda: _openai(
        "chat/completions", body))
    kind = "chat" if body["model"] == CONFIG["chat_model"] else "strong"   # the stronger model is priced separately
    _count(**{kind + "_prompt": response["usage"]["prompt_tokens"], kind + "_completion": response["usage"]["completion_tokens"]})
    return {"content": response["choices"][0]["message"]["content"], "usage": response["usage"]}
