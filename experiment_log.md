# Experiment Log

Todo: design of pipeline? schema linking(table augmentation?), error recovery, memory?

## Baseline (10 queries -> 500 queries)

**2026/7/23:**

**Setup:** naive prompt (schema + question + evidence) -> claude-sonnet-4-6 -> execute & compare

**Result:** 5/10 correct (50%). Simple all correct, moderate/challenging all failed.

**Failure analysis:**

- Q1481 (challenging): Claude return long thought process + SQL, 说明还要clean再写入prompt

**Fixed:** 加 clean_sql 处理 .md

**Next:** 修改 clean_sql, loop through sqlite.json看正确率

**2026/7/24:**

**Data:**  参考prompt.py refine prompt, 约束responce格式, 重构代码, add retry times in case it crashes halfway through. Save 500 queries results as JSON

Smart model: Claude Sonnet 5: claude-sonnet-5, using claude-sonnet-4-6 so far

For fast, cost-effective tasks: Claude Haiku 4.5: claude-haiku-4-5-20251001

**Next:** schema only 500 queries baseline; schema+sample rows 500 queries. multi threads(get_request.py)? chain of thoughts?

**2026/7/25:**

**Experiments design:**

| | Sonnet-4-6 (500queries) | Haiku (50queries) | Haiku (10queries) |
| :--- | :---: | :---: | :---: |
| 1.baseline(schema+question) | | | |
| 2.baseline+ 3 rows real data | | | |
| 3.schema linking? | | | |
| 4.error recovering? | | | |

**fixed:** add run.sh, get_request.py(combine path, retry times, save results)

**2026/7/28:**

**problem:** waiting prompt/api response and stucked for a long time, generating prompt & accessing API need to be split

**2026/7/29:**

**Failure analysis:**

- need add more log and decouple prompt generation & call api

**Result:** finished baseline of sonnet-4-6, achieved 62.2%, saved results in *baseline_sonnet_500.json*

| | simple (true-false) | moderate | challenging |
| :---: | :---: | :---: | :---: |
| **sonnet-4-6** | 111-37 75% | 144-106 57.6% | 56-46 54.9% |

| db_id | true | false | percentage |
| :---: | :---: | :---: | :---: |
| superhero | 45 | 7 | 86.5% |
| student_club | 35 | 13 | 72.9% |
| european_football_2 | 37 | 14 | 72.5% |
| toxicology | 26 | 14 | 65.0% |
| codebase_community | 32 | 17 | 65.3% |
| thrombosis_prediction | 29 | 21 | 58.0% |
| debit_card_specializing | 17 | 13 | 56.7% |
| california_schools | 17 | 13 | 56.7% |
| formula_1 | 34 | 32 | 51.5% |
| financial | 15 | 17 | 46.9% |
| card_games | 24 | 28 | 46.2% |

considering adding a few example row

