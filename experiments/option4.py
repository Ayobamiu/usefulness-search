"""Experiment (training topics only): does scoring for the full TASK beat Keenable's
ranking for the agent's own search QUERY?  Not part of the evals. Tasks here are drafts.

Label: a page is useful if the agent answers correctly from that page ALONE (no position bias).
"""
import json, statistics as st, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, ".")
import agents, clients, usefulness as u
from grading import grade

TASKS = [
 ("I am paginating the Stripe Search API (for example /v1/customers/search), not a list endpoint. Which field of the response holds the cursor I pass to get the following page?", ["next_page"]),
 ("My job retried a failed Stripe POST three days later with the same Idempotency-Key and Stripe executed it as a new request. After how long does Stripe remove idempotency keys?", ["24 hours"]),
 ("My service calls the GitHub REST API with a GitHub App installation access token, on a normal (non Enterprise Cloud) organization. What is the minimum primary rate limit per hour?", ["5,000", "5000"]),
 ("My CI script calls the GitHub REST API without any token and gets rate limited. How many requests per hour are allowed for unauthenticated requests?", ["60"]),
 ("My library must run on Python 3.10, where import tomllib fails. Which third-party package is the backport that tomllib was based on?", ["tomli"]),
 ("On Python 3.11 my code fails with AttributeError: module 'itertools' has no attribute 'batched'. Which Python version added itertools.batched?", ["3.12"]),
 ("Our database is PostgreSQL 14 and the MERGE statement gives a syntax error. Which PostgreSQL major version first supports MERGE?", ["15"]),
 ("The SQLite bundled with my Python is 3.31 and INSERT ... RETURNING raises a syntax error. What is the minimum SQLite version that supports RETURNING?", ["3.35"]),
 ("With BuildKit, pip install in my Dockerfile re-downloads every wheel on each build. Which RUN flag keeps pip's download directory between builds without adding it to the image?", ["--mount=type=cache"]),
 ("Our build server has Git 2.20 and 'git switch' is not a git command. Which Git version introduced git switch?", ["2.23"]),
 ("My Kubernetes pod is killed with SIGKILL before it finishes shutting down and I have not configured anything. Which pod spec field controls how long Kubernetes waits after SIGTERM?", ["terminationGracePeriodSeconds"]),
 ("After upgrading from Next.js 14 to 15, the GET Route Handler in my app directory is no longer cached. Which value of the dynamic route config option makes it static again?", ["force-static"]),
 ("I run Node.js 20.6 or later and want to drop the dotenv dependency. Which command-line flag loads variables from a .env file?", ["--env-file"]),
 ("FastAPI prints a deprecation warning for @app.on_event('startup'). Which FastAPI() parameter is the recommended replacement?", ["lifespan"]),
 ("With response_format type json_object, the OpenAI Chat Completions API sometimes omits fields my code requires. Which response_format type guarantees the output matches my JSON Schema?", ["json_schema"]),
 ("On Redis 6.2 or later I run GET then DEL inside MULTI to pop a string key. Which single command does both atomically?", ["GETDEL"]),
 ("On TypeScript 4.9 or later, annotating my config object with a Record type loses its literal key types. Which operator checks it against the type without widening the inferred type?", ["satisfies"]),
 ("aws s3 sync leaves objects in the bucket after I delete the files locally. Which flag removes destination files that no longer exist in the source?", ["--delete"]),
]
QUERY_PROMPTS = {
 "natural query": "You are a coding agent. Write the single web search query you would run to find documentation for the task. Reply with JSON: {\"query\": \"...\"}",
 "keyword query": "You are a coding agent. Write the single web search query you would run to find documentation for the task: keywords only, at most 6 words. Reply with JSON: {\"query\": \"...\"}",
}

def run(prompt):
    rows, base, top1 = [], [], []
    for question, facts in TASKS:
        task = {"question": question, "ground_truth": {"type": "expected_fact", "any_of": facts}}
        query = json.loads(clients.chat([{"role": "system", "content": prompt}, {"role": "user", "content": question}], json_mode=True)["content"])["query"]
        pages = [{"url": r["url"], "title": r.get("title") or r["url"], "snippet": r.get("snippet") or r.get("description") or "", "rank": i}
                 for i, r in enumerate(clients.keenable_search(query))]
        def feats(p):
            p["useful"] = grade(task, agents._answer(question, [p], 0)["answer"])
            p["q"] = .3 * u._similarity(query, p) + .3 * u._answer_check(query, p)
            p["t"] = .3 * u._similarity(question, p) + .3 * u._answer_check(question, p)
            p["prior"] = 1 - p["rank"] / 9
        with ThreadPoolExecutor(10) as ex: list(ex.map(feats, pages))
        rankers = {"Keenable raw": lambda p: p["rank"], "ours, sees query only": lambda p: -p["q"],
                   "ours, sees task": lambda p: -p["t"], "ours, sees task + Keenable rank": lambda p: -(p["t"] + .2 * p["prior"])}
        rows.append([sum(p["useful"] for p in sorted(pages, key=k)[:3]) / 3 for k in rankers.values()])
        top1.append([sorted(pages, key=k)[0]["useful"] for k in rankers.values()])
        base.append(sum(p["useful"] for p in pages) / len(pages))
    print(f"  share of all returned pages that answer the task alone: {st.mean(base):.2f}")
    for name, p3, t1 in zip(rankers, zip(*rows), zip(*top1)):
        print(f"  {name:34s} precision@3 {st.mean(p3):.3f}   top page answers it {st.mean(t1):.2f}")

for name, prompt in QUERY_PROMPTS.items():
    print(name); run(prompt)
