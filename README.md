# text2sql

benchmark mini_dev

| **model** | **SQLite** |
| :---: | ---: |
| claude-sonnet-4-6 | 50% (10 queries) |

**Baseline:**

| | Sonnet-4-6 (500queries) | Haiku (50queries) | Haiku (10queries) |
| :--- | :---: | :---: | :---: |
| 1.baseline(schema+question) | 311/500 (62.2%) | | 40% |
| 2.baseline+ 3 rows real data | | | |
| 3.schema linking? | | | |
| 4.error recovering? | | | |

**Phase1 baseline:**

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

**Phase2 add example row:**


