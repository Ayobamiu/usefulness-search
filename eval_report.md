# Eval report

**Prices are simulated.** No real money moves anywhere in this demo.

Held-out numbers come from n=6 held-out tasks x 3 runs (small sample). Treat them as a small sample.

| eval | pass/fail | the raw numbers behind it | notes |
|---|---|---|---|
| E1 score and price on every result | PASS | 240/240 results valid | all 24 tasks |
| E2 usefulness depends on the task | PASS | 6/6 pairs; (A, B) scores [(0.62, 0.225), (0.604, 0.241), (0.606, 0.261), (0.676, 0.225), (0.491, 0.294), (0.66, 0.317)] | trained history |
| E3 usage log is honest | PASS | 72/72 runs cite only fetched pages | train + held-out, all agents |
| E4 loop learns in the right direction | PASS | 180/180 pages moved the right way (100%) | training tasks only |
| E5 prediction no worse than plain relevance (KEY) | PASS | precision@3: ours 0.500 vs Keenable raw 0.500; per task (ours vs raw): t03 0.33 vs 0.33, t07 1.00 vs 1.00, t11 0.33 vs 0.33, t15 0.33 vs 0.33, t19 0.67 vs 0.67, t23 0.33 vs 0.33 | n=6 held-out tasks x 3 runs (small sample); labels = naive agent citations |
| E6 cold start is not a blank score | PASS | 18/18 result sets have score range >= 0.05 (min range 0.145); E2 unseen 6/6 | empty history, training queries |
| E7 duplicates lose value | PASS | 3/3 planted cases dropped; ['score 0.71->0.46, price 2.99->2.12', 'score 0.71->0.46, price 2.98->2.12', 'score 0.65->0.42, price 2.79->1.99'] |  |
| E8 price follows usefulness | PASS | 24/24 result sets monotonic | all 24 tasks |
| E9 budget is respected | PASS | 18/18 runs within 10c budget and bought best usefulness-per-cent first | n=6 held-out tasks x 3 runs (small sample) |
| END-TO-END ours vs naive | PASS | correct: ours 100% vs naive 100% (gap 0pp); spend per task: ours 9.03c vs naive 27.26c (67% less, SIMULATED); tokens per task: ours 7364 vs naive 18829. SAME-BUDGET BASELINE (Keenable order, 10c, not part of pass/fail): correct 100%, spend 9.17c, tokens 6255 | n=6 held-out tasks x 3 runs (small sample) |
| F1 catches superseded pages | FAIL | caught 2 of 4 eligible cases (8 old-story pages flagged) | n=8 held-out alert cases; eligible = Keenable returned both an old-story and a new-story page (keyword match) |
| F2 no false alarms on controls | PASS | 0 of 5 control cases have a false alarm (0 of 50 pages flagged) | n=5 control cases, drafts UNVERIFIED |
| F3 a flagged page costs less | PASS | 41/41 flagged pages are cheaper than the same page without the flag | tuning + held-out alert cases |
| F4 END-TO-END alert cases, ours vs naive | FAIL | answers pitching the old event as current (keyword check): ours 24/24 vs naive 21/24; pages read: ours 2.9 vs naive 10.0; tokens per query: naive 13804, ours 35498 (reading 4010 + scoring 31488); NET tokens saved INCLUDING scoring -21694; NET cost saved INCLUDING scoring 15.73c (pages SIMULATED + model tokens at configured prices: naive 23.99c, ours 8.26c). IF A SECOND AGENT REUSES CACHED SCORES (scoring paid once): net tokens saved 9794 | n=8 held-out alert cases x 3 runs (small sample); keyword verdicts need Usman's hand read |

Passed 12 of 14.

Thresholds confirmed by Usman: NO (placeholders)

UNVERIFIED tasks (24 of 24): t01, t02, t03, t04, t05, t06, t07, t08, t09, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, t20, t21, t22, t23, t24

UNVERIFIED control cases (5 of 5): c01, c02, c03, c04, c05

Changes to eval code, thresholds, fixtures or tasks since the last run:
- fd00ced Freshness evals F1-F4 (failing), alert cases with draft controls, placeholder thresholds

.env ignored by git: yes
