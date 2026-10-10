# Usefulness search for agents

A hackathon demo of a search layer for AI agents, built on [Keenable](https://keenable.ai) search.
**All prices are simulated. No real money moves.**

Demo video: https://youtu.be/Lup7Obs6EhY

## What it is

Agents that research on the web read every page a search returns. This layer sits on top of the search
engine and, before the agent reads anything, gives every result a usefulness score for the agent's task
and a price derived from that score. A buyer agent then buys pages by usefulness per cent within a
budget and stops when the rest are not worth it. The pages it ends up citing feed back into the scores.

## Who it is for

Teams whose agents research companies for sales outreach: one task, thousands of companies, and a bill
for every page read. The demo task is "Write a one-paragraph sales outreach angle for {company} based on
their latest news."

## How it works

Score and price before reading, then learn from what was used. All of the scoring is one function in
[usefulness.py](usefulness.py):

```
usefulness = baseline
           + similarity of the query to the page's title and snippet
           + a cheap model check: does this snippet answer the query?
           + the search engine's own rank
           + how often this page, and its domain, were cited when read before
           x 0.5 if a later page in the same results replaces this page's news
price      = floor + rate x usefulness            (simulated cents)
```

A page that repeats one already bought loses 35% of its usefulness and its price drops with it. After a
run, cited pages move up and pages that were bought but not used move down.

## Run it

Python 3 (built and tested on 3.14). No packages to install.

```bash
cp .env.example .env          # then add OPENAI_API_KEY and KEENABLE_API_KEY
python3 demo.py                       # the sales demo; press Space to start
python3 demo.py --company "Airbnb"    # any company, live, 90 second limit
python3 demo.py --docs                # the coding-docs demo
python3 demo.py --pace 8              # adds pauses between beats for narration
python3 run_evals.py                  # every eval, saved to eval_report.md
```

Every Keenable and OpenAI response is cached in `cache/`, so reruns are repeatable and work offline
(`OFFLINE=1`). If a live company run fails or times out, the demo shows the nearest cached run and says
so on screen. The cache and the built demo page hold third-party page text and are not in this
repository, so a fresh clone makes live calls on its first run.

## Eval numbers

From `python3 run_evals.py` ([eval_report.md](eval_report.md)). 16 of 18 evals pass. Token and cost
figures always include our own scoring work.

**Sales research, 15 companies, 1 run each** (both agents answer with gpt-4o)

| | Reads the top 10 | Ours |
|---|---|---|
| Answers reflecting the company's latest event (keyword check) | 10 | 11 |
| Answers pitching an outdated event (keyword check) | 2 | 1 |
| Answers matching neither keyword list | 3 | 3 |
| Pages read per query | 10.0 | 3.1 |
| Cost per query (simulated page prices + model tokens) | 26.61c | 10.30c |
| Tokens per query | 14,067 | 19,539 (4,865 reading + 14,673 scoring) |
| Tokens if a second agent reuses the cached scores | 14,067 | 4,865 |

So: slightly better answers at well under half the cost, and more tokens unless scores are reused. The
quality difference is one answer in each direction on a keyword check over 15 companies, so read it as
"at least as good", not as a proven gain. The answers are in
[experiments/sales_results.md](experiments/sales_results.md).

**Coding-docs questions, 6 held-out tasks, 3 runs each (small sample)**

| | Reads the top 10 | Ours |
|---|---|---|
| Correct answers | 100% | 100% |
| Spend on pages (simulated) | 26.39c | 9.11c |
| Tokens per task | 18,829 | 20,819 (6,138 reading + 14,682 scoring) |
| Ranking vs Keenable, precision@3 | 0.500 | 0.500 (a tie) |

Against a simpler baseline, reading Keenable's top pages up to the same budget, we tie on correctness
and spend.

**What fails, plainly**

- The docs "fewer tokens" eval fails once scoring tokens are counted (20,819 vs 18,829).
- The alert end-to-end eval fails by one answer (next section).

**Not yet verified:** the tasks, control cases and eval thresholds are drafts not yet confirmed by a human,
and the keyword verdicts have not all been read by hand.

## Freshness: agents pitch outdated news

When an agent is told about an old event ("Builder.ai named a new CEO") and asked to write outreach, it
pitched that event as current on 4 of 7 cases, even though the newer story (insolvency, shutdown) was
among the pages it read. A prompt sentence did not fix it, and neither did a stronger model on its own.

The freshness check is our response. One gpt-4o call per result set finds pages whose news a later page
in the same results replaces or reverses. Those pages lose half their usefulness, so their price drops,
and our agent is told the later event in one line ("Superseded: Forward shut down November 2024").

- Detection: 4 of 4 eligible held-out cases caught, 0 false alarms on 5 control cases.
- On the 7 cases it was tuned on, our agent pitched the old event 3 times against 4 for the agent that
  reads everything.
- On 8 held-out cases (3 runs each) it does not yet help: 16 of 24 stale answers against 15 of 24.

So detection works and the agent still does not always act on it. That is the open problem.

## Files

| File | What it is |
|---|---|
| `usefulness.py` | scorer, price rule, usage loop, duplicate discount, freshness check |
| `agents.py` | naive agent, buyer agent, same-budget baseline, cost accounting |
| `sales.py` | the sales research task, grading keywords, the 15-company measurement |
| `clients.py` | Keenable and OpenAI calls with disk cache |
| `run_evals.py`, `eval_thresholds.json`, `eval_fixtures.json` | evals and their thresholds |
| `tasks.json`, `alert_cases.json` | task sets and case lists |
| `demo.py`, `demo_template.html`, `demo_candidates.md` | the demo screen and how its examples were chosen |
| `experiments/` | the experiments behind the findings above |
| `STATUS.md` | build log |
