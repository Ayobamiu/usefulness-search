# Status (resume from here)

Updated 2026-10-06. Spec: build order in Part 8. Each step ends with a local commit, so a
new session starts from the last commit and this file, not from scratch.

## Done
- Step 1: `.env` git-ignored, `clients.py` (cached Keenable + OpenAI, retries, `OFFLINE=1`),
  `config.json`, `tasks.json` (24 version-specific drafts, all UNVERIFIED, fixed 18/6 split).
- Step 2: `run_evals.py`, `grading.py`, `eval_thresholds.json`, `eval_fixtures.json`.
- Steps 3 to 5: `agents.py` (naive + buyer, one shared prompt), `usefulness.py` (score,
  price, search, usage loop, duplicate discount). Evals: 8 of 10 pass, reruns offline.

## Current evals: 10 of 10 pass (2026-10-06), placeholders thresholds, tasks unverified
- Score includes Keenable rank (W_KEENABLE_RANK); every agent reads pages in a fixed shuffled order;
  E5 means "no worse than Keenable"; end-to-end also reports a same-budget Keenable baseline
  (`agents.run_topk`, not part of pass/fail).
- E5: exact tie, 0.500 vs 0.500. Passes only because tolerance is 0 and the scores are equal.
- End-to-end: ours 100% vs naive 100%; spend 9.03c vs 27.63c (67% less); tokens 7345 vs 18829.
  Same-budget Keenable baseline: 100%, 9.17c, 6255 tokens. Ours TIES it (and uses more tokens).
- Grading now treats a hyphen between words as a space; t03 and t11 accept singular forms
  ("five minute", "30 second"). Both approved in spirit by Usman on 2026-10-06.

## Step 6 done: demo screen
- `python3 demo.py [--pace N]` builds `demo.html` (git-ignored) from cache only and opens it; Space or the
  button starts it. All four beats, row markers and the end card work. About 26s unpaced.
- Demo query t16 (Next.js 15 force-static), the only training task that met the rule; see `demo_candidates.md`.
  History for the demo excludes t16 itself, so all 10 pages show "new".
- In this example all 3 bought pages were cited, so Beat 4 shows only upward score changes.

## Next, in order
- Step 7: Usman records the video (`python3 demo.py --pace 8` or similar).
- README with the one-paragraph thesis, then push to a public repo (only when Usman says so).

## Waiting on Usman
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
