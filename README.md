# Usefulness search for agents

A hackathon demo of a search layer for AI agents, built on [Keenable](https://keenable.ai) search.
**All prices are simulated. No real money moves.**

## Thesis

Search engines tell an agent which pages are relevant. They do not tell it how many pages to read, what
each is worth, or when to stop, so agents read everything. This layer sits on top of a search engine and
gives every result a usefulness score for the agent's task and a price derived from that score. A buyer
agent then buys pages by usefulness per cent within a budget, a page that repeats one already bought loses
value, and the pages an agent actually cites feed back into the scores. On our held-out coding-docs
questions the buyer reached the same answers as an agent that read all ten results while spending about a
third as much on pages. We did not beat Keenable's ranking, and we say so: the value shown here is in
pricing and stopping, not in a better ranker.

## What the evals show

`python3 run_evals.py` prints the table below and saves it to [eval_report.md](eval_report.md).
Held-out numbers come from 6 coding-docs tasks, 3 runs each. That is a small sample.

| Claim | Result |
|---|---|
| Same answers as reading the top 10 | both agents 100% correct |
| Spend on pages (simulated) | 9.15c vs 27.26c, 66% less |
| Tokens, with our own scoring counted | 20,698 vs 18,829: slightly **more** than the naive agent |
| Tokens, if a second agent reuses the cached scores | 12,695 fewer per query |
| Ranking vs Keenable (precision@3) | a tie, 0.500 vs 0.500 |
| Against "read Keenable's top pages at the same budget" | a tie on correctness and spend |
| Usage loop | 180 of 180 pages moved the right way after one run |

12 of 14 evals pass. The two that fail (F1, F4) belong to an unfinished feature, described below.

### What did not work

- **Out-ranking Keenable.** On single-fact docs questions about 88% of the pages Keenable returns answer
  the question on their own, so there is no room for a better ranking.
- **Token savings.** Scoring pages costs tokens. Counted honestly, we use slightly more tokens than the
  naive agent unless the scores are reused.
- **Superseded news (the freshness check).** An agent told about an old event ("Builder.ai named a new
  CEO") pitched it as current in 4 of 7 cases, even with the newer story among the pages it read. Our
  check that flags pages replaced by a later page is built but not good enough: it catches 2 of 4 eligible
  held-out cases and does not yet change the agent's answer. This is the next thing to build.

### Not yet verified

The 24 tasks, the 5 control cases and the eval thresholds are drafts that have not been confirmed by a
human. The report lists them as UNVERIFIED.

## How the score works

All of it is in one function in [usefulness.py](usefulness.py):

```
usefulness = baseline
           + similarity of the task to the page's title and snippet
           + a cheap model check: does this snippet answer the task?
           + Keenable's own rank
           + how often this page, and its domain, were cited when read before
           x (1 - W_SUPERSEDED) if a later page in the same results replaces this page's event
price      = floor + rate x usefulness            (simulated cents)
```

## Run it

Python 3.11 or later. No packages to install.

```bash
cp .env.example .env    # then add OPENAI_API_KEY and KEENABLE_API_KEY
python3 run_evals.py    # all evals, about 3 minutes the first time
python3 demo.py         # builds demo.html and opens it; press Space to start
python3 demo.py --pace 8    # adds pauses between beats for narration
```

Every Keenable and OpenAI response is cached in `cache/`, so reruns are repeatable and work offline
(`OFFLINE=1`). The cache and `demo.html` hold third-party page text and are not in this repository, so a
fresh clone makes live calls on its first run.

## Files

| File | What it is |
|---|---|
| `usefulness.py` | scorer, price rule, usage loop, duplicate discount, freshness check |
| `agents.py` | naive agent, buyer agent, same-budget baseline, cost accounting |
| `clients.py` | Keenable and OpenAI calls with disk cache |
| `run_evals.py`, `eval_thresholds.json`, `eval_fixtures.json` | evals and their thresholds |
| `tasks.json`, `alert_cases.json` | task sets with fixed train and held-out splits |
| `demo.py`, `demo_template.html`, `demo_candidates.md` | the demo screen and how its query was chosen |
| `experiments/` | the experiments behind the "what did not work" section |
| `STATUS.md` | build log |
