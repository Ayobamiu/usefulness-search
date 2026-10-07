# Status (resume from here)

Updated 2026-10-06. Spec: build order in Part 8. Each step ends with a local commit, so a
new session starts from the last commit and this file, not from scratch.

## Done
- Step 1: `.env` git-ignored, `clients.py` (cached Keenable + OpenAI, retries, `OFFLINE=1`),
  `config.json`, `tasks.json` (24 version-specific drafts, all UNVERIFIED, fixed 18/6 split).
- Step 2: `run_evals.py`, `grading.py`, `eval_thresholds.json`, `eval_fixtures.json`.
- Steps 3 to 5: `agents.py` (naive + buyer, one shared prompt), `usefulness.py` (score,
  price, search, usage loop, duplicate discount). Evals: 8 of 10 pass, reruns offline.

## Failing, and why (found on TRAINING tasks only)
- E5 (ours 0.556 vs Keenable 0.833 p@3) and E6 (1 of 18 result sets has score range 0.023 < 0.05).
- Keenable snippets nearly always contain the answer (155 of 180 rated "yes"), so the
  cheap check cannot separate pages.
- The naive agent cites by reading position: reading the same pages in reversed order moved
  citations from rank 1-3 (40 -> 26) to rank 7-10 (17 -> 35). So the E5 labels favour
  Keenable's order by construction.
- A Keenable-rank prior lifts our train p@3 from 0.54 to 0.74 (a tie with Keenable, not a win).
  Not added: waiting on Usman's choice below.

## Next, in order
- Usman decides how to handle E5 label bias (shuffle reading order / rank prior / leave as is).
- Step 6: demo screen (Beats 1, 3, 4, then 2). Step 7: video run with `--pace`.

## Waiting on Usman
- E5 decision above.
- Verify the 24 tasks. t04 draft fact looks stale: pages say the current GitHub API
  version is 2026-03-10, the draft expects 2022-11-28.
- Confirm `eval_thresholds.json` (set `confirmed_by_usman` to true).

## Facts worth not rediscovering
- No pip dependencies: stdlib only (Python 3.14).
- Keenable REST: `POST api.keenable.ai/v1/search`, `GET /v1/fetch`, header `X-API-Key`.
  Search results carry `title, url, description, snippet, acquired_at`. No headings, no score.
- Chat model `gpt-4o-mini` accepts temperature 0.

## Option 4 experiment (2026-10-06, training topics only): no win
- `experiments/option4.py`: 18 contextual tasks, model-written query, label = page answers the task alone.
- 88% of ALL pages Keenable returns answer the task alone. Keenable p@3 0.93, ours (sees task) 0.94 to 0.98:
  a difference of 1 to 3 pages out of 54, i.e. noise. Control: with an unrelated page the model is right 1 of 18.
- Conclusion: on single-fact docs questions there is no ranking headroom. The win must be claimed elsewhere
  (fewer pages for the same answer, stop rule, duplicates) or on harder tasks.
