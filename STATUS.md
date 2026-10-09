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

## Superseded-news experiment, Step A (2026-10-07): no headroom
- `experiments/superseded.py`, results in `experiments/superseded_results.md`. Cases 1, 2, 3, 4, 5, 9, 11 from
  `superseded-news-cases.md`. Query "<company> news", task "sales outreach angle based on their latest news".
- Keenable returned the NEW story (or later news) in the top results for every case. The OLD story appeared
  once in 70 results (Natron, rank 10). The exact URLs from the cases file were never returned.
- Naive agent by keyword: 5 CORRECT, 1 WRONG (Humane), 1 OTHER (Figure). Read by hand, neither is a real miss:
  the Humane answer describes the Ai Pin's failure without naming HP; the Figure answer uses 2026 news and
  does not mention OpenAI. So 0 of 7 pitch the old event as current. Decision rule: no headroom, nothing built.
- Publish dates: Keenable's API returned `published_at` for 44 of 70 results; with page text, 57 of 70 had a date.
- Untested: event-specific queries (the agent searches for the old event by name), or reversals only days old.

## Superseded-news experiment, Step B (2026-10-07): HEADROOM FOUND, 4 of 7 wrong
- `python3 experiments/superseded.py alert`, results in `experiments/superseded_alert_results.md`.
  Task: "We got an alert: <old event>. Write a one-paragraph outreach angle for <company>." Query built from the alert.
- Naive agent pitched the old event as current on 4 of 7: Humane, Builder.ai, Rad Power Bikes, Forward.
  All four read by hand and confirmed. Correct on Windsurf, Figure AI, Natron.
- In every wrong case the NEW story was among the 10 pages the agent read (5 to 7 of the 10 results).
  So this is not a retrieval miss: the agent follows the alert's framing. Re-ordering alone will not fix it;
  the fix has to reach the agent as a flag on the page.
- Publish date found for 53 of 70 results (API 47, page text 6).
- Proposed, NOT built: publish date per result + one model call per result set asking which pages are
  contradicted by a newer page on the same company; superseded pages lose usefulness and carry a
  "superseded by <newer page, date>" note that is shown to the agent.
- Open risk: a one-line prompt change ("check for newer news") might fix the naive agent for free. Test that first.

## Step B follow-ups (2026-10-07): neither a prompt sentence nor a stronger model fixes it
- `python3 experiments/superseded.py alert prompt` -> `superseded_alert_prompt_results.md`:
  default model + "Before writing, check whether newer news contradicts the alert." WRONG on 4 of 7,
  the same four (Humane, Builder.ai, Rad Power Bikes, Forward). All read by hand and confirmed.
- `python3 experiments/superseded.py alert strong` -> `superseded_alert_strong_results.md`:
  gpt-4o, default prompt. Keyword verdict WRONG on 5 of 7. By hand: the same four are real misses;
  Natron is borderline (says the factory was cancelled, does not say the company closed).
- Both models saw the newer story in the pages they read and still wrote from the old one.
- Freshness check still NOT built. Waiting on Usman.

## Freshness build (2026-10-07): built, NOT working well enough. Alert demo NOT started. Waiting on Usman.
Built and committed:
- `usefulness.freshness` (one gpt-4o-mini call per result set), `W_SUPERSEDED = 0.5` (multiplies the score, so
  price drops through the normal price rule), publish date from Keenable's `published_at` or the URL.
- Buyer sees the search layer's superseded notes (a short list before the pages, and on any flagged page it reads).
  Naive sees none. Alert tasks use a neutral prompt (`PROMPTS["alert"]`); docs prompt unchanged.
- Scoring cost: `clients.metering()` counts every scoring token; `agents.totals(log)` gives reading, scoring,
  total tokens and simulated cost. Token prices are in `config.json`.
- `alert_cases.json` (7 tune, 8 held-out, 5 draft controls UNVERIFIED), evals F1 to F4, `experiments/tune_alerts.py`.

Evals: 12 of 14 pass. The original 10 all pass.
- F1 FAIL: caught 2 of 4 eligible held-out cases (only 4 of 8 had both stories in Keenable's results).
- F2 PASS: 0 of 5 control cases flagged (0 of 50 pages). F3 PASS: 41 of 41 flagged pages are cheaper.
- F4 FAIL: stale answers (keyword check) ours 24/24 vs naive 21/24 (8 held-out cases x 3 runs).
  Tokens per query: naive 13,804; ours 4,010 reading + 31,488 scoring. NET tokens saved including scoring: -21,694.
  NET cost saved including scoring: 15.73c (driven by simulated page prices). Second agent reusing scores: +9,794 tokens.
- Docs held-out with scoring counted: naive 18,829 tokens; ours 7,364 reading + 37,782 scoring = 45,146. Net -26,317.
  Cost with scoring: naive 27.54c, ours 9.67c.

Why it fails (tuning cases only):
- Detection is noisy: gpt-4o-mini in one call misses the old pages on Humane, Builder.ai, Forward and sometimes
  flags new-story pages. A two-step prompt was noisier and was reverted.
- The agent ignores the evidence: with the real detector the buyer is stale on 5 of 7 tuning cases (naive 4 of 7).
- Ceiling tests with PERFECT flags (from the keyword lists): stale 3 of 7 with the "superseded by <title>" note,
  2 of 7 when the note states the later event instead of a page title. So the specified note format caps the gain.
- Scoring tokens are dominated by the duplicate check (one call per offer per purchase).

Options put to Usman: (1) note states the later event + shared prompt tells agents to follow search-layer notes +
better detector; (2) batch the duplicate check to cut scoring tokens; (3) fall back to the docs demo (cost + loop).

## Decision 2026-10-07 (Usman): docs demo is the main demo; duplicate check batched. Alert work is "what's next".
- Duplicate check is now ONE model call per purchase (snippets cut to 400 chars). Scoring tokens per docs
  query fell from 37,782 to 14,564. Docs held-out with scoring counted: ours 20,698 (6,134 reading + 14,564
  scoring) vs naive 18,829, NET -1,870 tokens; cost 9.42c vs 27.54c, NET +18.13c (simulated page prices).
  Second agent reusing scores: +12,695 tokens. Alert held-out: NET -3,468 tokens, +16.10c.
- Evals: 12 of 14. Original 10 pass. F2, F3 pass. F1 and F4 fail (freshness left in place, not fixed).
- Docs end-to-end line now also reports the scoring-included numbers (not part of pass/fail).
  OPEN: its pass rule "ours uses fewer tokens" still compares READING tokens only. With scoring counted
  ours uses MORE. Changing the rule needs Usman's OK.
- Demo (`python3 demo.py`, still t16): counters show pages + model-token cost and tokens with scoring
  included (this example: naive 18,349 tokens / 27.45c; ours 20,080 tokens = 5,302 reading + 14,778 scoring / 9.27c),
  plus "a second agent reusing these scores would use 5,302 tokens". End card closes with x, click outside, Esc.
- Remaining scoring cost: answer checks (10 calls) and embeddings on snippets up to 2,000 chars. Trimming
  those would likely make net tokens positive but changes docs scores; not done.

## Next
- Usman: record the video; verify tasks (t04 first) and the 5 control cases; confirm thresholds; decide the
  token pass rule above.
- README with the one-paragraph thesis; push only when Usman says so.

## Sales pivot (2026-10-08): built. 14 of 18 evals pass. Demo freezes Fri night. Nothing pushed.
Built:
- `sales.py`: task "Write a one-paragraph sales outreach angle for {company} based on their latest news.",
  query "{company} news", freshness check OFF in this mode, no weights changed. `python3 sales.py` writes
  `experiments/sales_results.md` (all 30 answers).
- `demo.py`: no args = sales demo from cache (Windsurf, see `demo_candidates.md`); `--company "X"` = live run in a
  child process with a hard 90 s limit, falls back to the nearest cached run and says so; `--docs` = t16 backup.
  Live runs took 11 to 14 s. Pre-cached: Nvidia, Stripe, Figma, Databricks, Shopify (+ Airbnb for S3).
- Demo screen: task line is the largest text; beats are answers + verdict, cost counters, reuse line, loop;
  end card shows S1 and S2. Companies outside the case list show "live run, not graded".
- One fix: the buyer now always reads at least one page (it had bought zero pages for Figure AI).

Numbers, sales, n=15 companies, 1 run each, scoring included:
- Quality by keyword: current ours 8 vs naive 9; stale ours 0 vs naive 2; other ours 7 vs naive 4.
- BY HAND (4 of our "other" answers read): Natron and Forward are real misses. Both companies shut down; ours
  pitched them as growing (naive caught the shutdown). So "same results" is NOT supported; it is "close".
- Pages 2.9 vs 10.0. Cost 8.38c vs 25.07c. Tokens 17,132 (4,574 reading + 12,559 scoring) vs 14,054.

Evals:
- PASS: E1 to E9, S2, S3 (4 of 4 runs under 90 s), S4 (0 company names in the logic), F2, F3.
- FAIL: S1 (one fewer "current" answer than naive). Docs END-TO-END (token rule now counts scoring:
  20,698 vs 18,829). F1, F4 (freshness, unchanged).
- Step 5 (trim scoring snippets) NOT done: the brief allows it only if Steps 1 to 4 pass, and S1 fails.
- Secret scan of the whole history, all branches: no keys found. `.env`, `cache/`, `demo.html`, `demo_run.json` untracked.
- README.md drafted on local `main`. GitHub PR #1 (branch `add-readme`) holds the OLD README and is now out of date.

Waiting on Usman:
- Read `experiments/sales_results.md` and confirm or correct the verdicts.
- Decide the pitch wording given S1 (see chat), and whether to do Step 5 anyway.
- Approve README.md, add the video link, say when to push and what to do with PR #1.
