# Eval report

**Prices are simulated.** No real money moves anywhere in this demo.

Held-out numbers come from n=6 held-out tasks x 3 runs (small sample). Treat them as a small sample.

| eval | pass/fail | the raw numbers behind it | notes |
|---|---|---|---|
| E1 score and price on every result | PASS | 240/240 results valid | all 24 tasks |
| E2 usefulness depends on the task | PASS | 6/6 pairs; (A, B) scores [(0.674, 0.2), (0.658, 0.222), (0.657, 0.243), (0.741, 0.2), (0.519, 0.283), (0.722, 0.311)] | trained history |
| E3 usage log is honest | PASS | 54/54 runs cite only fetched pages | train + held-out, both agents |
| E4 loop learns in the right direction | PASS | 180/180 pages moved the right way (100%) | training tasks only |
| E5 prediction beats plain relevance (KEY) | FAIL | precision@3: ours 0.556 vs Keenable raw 0.833; per task (ours vs raw): t03 0.67 vs 1.00, t07 0.33 vs 1.00, t11 0.67 vs 0.67, t15 0.67 vs 1.00, t19 0.33 vs 0.67, t23 0.67 vs 0.67 | n=6 held-out tasks x 3 runs (small sample); labels = naive agent citations |
| E6 cold start is not a blank score | FAIL | 17/18 result sets have score range >= 0.05 (min range 0.023); E2 unseen 6/6 | empty history, training queries |
| E7 duplicates lose value | FAIL | 1/3 planted cases dropped; ['score 0.78->0.78, price 3.25->3.25', 'score 0.78->0.78, price 3.24->3.24', 'score 0.71->0.46, price 3.00->2.10'] |  |
| E8 price follows usefulness | PASS | 24/24 result sets monotonic | all 24 tasks |
| E9 budget is respected | PASS | 18/18 runs within 10c budget and bought best usefulness-per-cent first | n=6 held-out tasks x 3 runs (small sample) |
| END-TO-END ours vs naive | PASS | correct: ours 100% vs naive 100% (gap 0pp); spend per task: ours 9.05c vs naive 29.65c (69% less, SIMULATED); tokens per task: ours 5634 vs naive 18852 | n=6 held-out tasks x 3 runs (small sample) |

Passed 7 of 10.

Thresholds confirmed by Usman: NO (placeholders)

UNVERIFIED tasks (24 of 24): t01, t02, t03, t04, t05, t06, t07, t08, t09, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, t20, t21, t22, t23, t24

Changes to eval code, thresholds, fixtures or tasks since the last run:
- uncommitted: M tasks.json

.env ignored by git: yes
