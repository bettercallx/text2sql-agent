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

| **sonnet-4-6** | simple (true-false) | moderate | challenging |
| :---: | :---: | :---: | :---: |
| **baseline** | 111-37 75% | 144-106 57.6% | 56-46 54.9% |
| **baseline+3rows** | 108-40 73% | 142-108 56.8% | 58-44 56.9% |



ph1 : baseline

ph2 : baseline + 3 rows data for all db

ph3 : baseline + 3 rows data for some db

| db_id | tables | ph1 (true-false) | ph2 (true-false) | ph1 percentage | ph2 percentage |
| :--- | :---: | :---: | :---: | :---: | :---: |
| debit_card_specializing | 5 | 17-13 | 14-16 | 56.7% | 46.7% **-** |
| student_club | 8 | 35-13 | 36-12 | 72.9% | 75.0% **+** |
| thrombosis_prediction | 3 | 29-21 | 27-23 | 58.0% | 54.0% **-** |
| european_football_2 | 6 | 37-14 | 35-16 | 72.5% | 68.6% **-** |
| formula_1 | 13 | 34-32 | 34-32 | 51.5% | 51.5% **=** |
| superhero | 10 | 45-7 | 45-7 | 86.5% | 86.5% **=** |
| codebase_community | 8 | 32-17 | 32-17 | 65.3% | 65.3% **=** |
| card_games | 6 | 24-28 | 23-29 | 46.2% | 44.2% **-** |
| toxicology | 4 | 26-14 | 26-14 | 65.0% | 65.0% **=** |
| california_schools | 3 | 17-13 | 16-14 | 56.7% | 53.3% **-** |
| financial | 8 | 15-17 | 20-12 | 46.9% | 62.5% **+** |

**Phase2 add example row:**


