"""Server state in Supabase, over plain HTTP to PostgREST. Used only when SUPABASE_URL is set.

The service-role key is read from SUPABASE_SERVICE_KEY and never written to logs or errors.
"""
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request


def enabled():
    return bool(os.environ.get("SUPABASE_URL"))


def _request(method, table, params=None, body=None, prefer=None):
    key = os.environ["SUPABASE_SERVICE_KEY"]
    url = os.environ["SUPABASE_URL"].rstrip("/") + "/rest/v1/" + table
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {"apikey": key, "Authorization": "Bearer " + key, "Content-Type": "application/json"}
    if prefer:
        headers["Prefer"] = prefer
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                raw = resp.read()
                return resp.headers, (json.loads(raw) if raw else None)
        except urllib.error.HTTPError as e:
            if e.code in (500, 502, 503, 504) and attempt < 2:
                time.sleep(2 ** attempt)
                continue
            # Status and table only: never the URL query, headers or key.
            raise RuntimeError(f"supabase {method} {table} failed: HTTP {e.code}") from None
        except OSError:
            if attempt == 2:
                raise RuntimeError(f"supabase {method} {table} failed: connection error") from None
            time.sleep(2 ** attempt)


def select(table, params):
    return _request("GET", table, params)[1]


def insert(table, rows):
    _request("POST", table, body=rows, prefer="return=minimal")


def upsert(table, rows, on_conflict):
    _request("POST", table, {"on_conflict": on_conflict}, rows,
             prefer="resolution=merge-duplicates,return=minimal")


def count(table, params):
    headers, _ = _request("GET", table, {**params, "select": "*", "limit": "0"}, prefer="count=exact")
    return int(headers["Content-Range"].split("/")[-1])


def in_list(values):
    """PostgREST `in.(...)` filter value, with every item quoted."""
    return "in.(" + ",".join('"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"' for v in values) + ")"
