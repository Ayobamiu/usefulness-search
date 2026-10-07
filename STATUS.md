# Status (resume from here)

Updated 2026-10-06. Spec: build order in Part 8. Each step ends with a local commit, so a
new session starts from the last commit and this file, not from scratch.

## Done
- Step 1: `.env` copied and git-ignored, `clients.py` (Keenable search/fetch, OpenAI
  embed/chat, disk cache in `cache/`, `OFFLINE=1` switch), `config.json`, `tasks.json`
  (24 drafts, all UNVERIFIED, fixed 18/6 split).
- Step 2: `run_evals.py` (E1 to E9 + end-to-end, report), `grading.py`,
  `eval_thresholds.json` (placeholders), `eval_fixtures.json` (planted pairs and
  duplicates). All 10 evals FAIL against the stubs in `usefulness.py` and `agents.py`.

## Next, in order
- Step 3: `agents.run_naive` + shared answer prompt, usage log. Target: E3.
- Step 4: `usefulness.score / price_cents / search`, then `update_history`. Target: E1, E2, E6, E8, E4.
- Step 5: `agents.run_buyer`, `usefulness.reprice_after_purchase`. Target: E7, E9, E5, end-to-end.
- Step 6: demo screen (Beats 1, 3, 4, then 2). Step 7: video run with `--pace`.

## Waiting on Usman
- Verify the 24 tasks in `tasks.json` (set `status` to `VERIFIED`).
- Confirm `eval_thresholds.json` (set `confirmed_by_usman` to true).
- Decide whether `cache/` is committed to the public repo (it holds third-party page text).

## Facts worth not rediscovering
- No pip dependencies: stdlib only (Python 3.14).
- Keenable REST: `POST api.keenable.ai/v1/search`, `GET /v1/fetch`, header `X-API-Key`.
  Search results carry `title, url, description, snippet, acquired_at`. No headings, no score.
- Chat model `gpt-4o-mini` accepts temperature 0.
