# Eval report

**Prices are simulated.** No real money moves anywhere in this demo.

Held-out numbers come from n=6 held-out tasks x 3 runs (small sample). Treat them as a small sample.

| eval | pass/fail | the raw numbers behind it | notes |
|---|---|---|---|
| E1 score and price on every result | FAIL | no numbers | not implemented: naive agent (step 3) |
| E2 usefulness depends on the task | FAIL | no numbers | not implemented: naive agent (step 3) |
| E3 usage log is honest | FAIL | no numbers | not implemented: naive agent (step 3) |
| E4 loop learns in the right direction | FAIL | no numbers | not implemented: naive agent (step 3) |
| E5 prediction beats plain relevance (KEY) | FAIL | no numbers | not implemented: naive agent (step 3) |
| E6 cold start is not a blank score | FAIL | no numbers | not implemented: search layer (step 4) |
| E7 duplicates lose value | FAIL | no numbers | not implemented: scorer (step 4) |
| E8 price follows usefulness | FAIL | no numbers | not implemented: naive agent (step 3) |
| E9 budget is respected | FAIL | no numbers | not implemented: naive agent (step 3) |
| END-TO-END ours vs naive | FAIL | no numbers | not implemented: naive agent (step 3) |

Passed 0 of 10.

Thresholds confirmed by Usman: NO (placeholders)

UNVERIFIED tasks (24 of 24): t01, t02, t03, t04, t05, t06, t07, t08, t09, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, t20, t21, t22, t23, t24

Changes to eval code, thresholds, fixtures or tasks since the last run:
- uncommitted: ?? eval_fixtures.json
- uncommitted: ?? eval_thresholds.json
- uncommitted: ?? grading.py
- uncommitted: ?? run_evals.py
- uncommitted: ?? tasks.json

.env ignored by git: yes
