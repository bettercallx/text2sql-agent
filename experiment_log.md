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
| 1.baseline(schema+question) | x | | x |
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

**experiment1 raw stats:**

``` python
correct simple is 111, ( 75.0 %)
failed simple is 37
failed id:[1498, 1500, 1505, 1514, 1525, 1410, 1166, 1251, 1092, 1144, 1145, 847, 854, 898, 902, 915, 950, 951, 959, 967, 978, 738, 533, 671, 710, 340, 341, 358, 383, 424, 440, 239, 17, 41, 46, 92, 159]
correct moderate is 144, ( 57.6 %)
failed moderate is 106
failed id:[1490, 1501, 1529, 1531, 1533, 1322, 1323, 1338, 1350, 1376, 1381, 1399, 1404, 1427, 1435, 1149, 1175, 1179, 1205, 1225, 1235, 1252, 1254, 1256, 1265, 1267, 1275, 1029, 1032, 1040, 1080, 1107, 1135, 1136, 1146, 846, 865, 866, 877, 892, 894, 897, 904, 906, 928, 931, 963, 972, 989, 1002, 726, 728, 758, 766, 557, 565, 584, 595, 604, 637, 640, 672, 682, 683, 685, 694, 344, 347, 349, 352, 405, 407, 408, 412, 462, 465, 469, 473, 480, 483, 484, 522, 529, 530, 197, 234, 244, 245, 255, 23, 24, 25, 26, 27, 37, 48, 85, 93, 95, 128, 136, 129, 145, 152, 168, 186]
correct challenging is 56, ( 54.9 %)
failed challenging is 46
failed id:[1481, 1482, 1526, 1460, 1464, 1168, 1169, 1241, 1242, 1243, 1247, 1302, 1031, 1058, 1094, 896, 944, 955, 988, 990, 1011, 1014, 772, 829, 586, 639, 371, 415, 416, 477, 198, 207, 215, 218, 219, 231, 247, 281, 28, 87, 94, 115, 116, 125, 149, 173]
debit_card_specializing :17-13, ( 56.7 %)
student_club :35-13, ( 72.9 %)
thrombosis_prediction :29-21, ( 58.0 %)
european_football_2 :37-14, ( 72.5 %)
formula_1 :34-32, ( 51.5 %)
superhero :45-7, ( 86.5 %)
codebase_community :32-17, ( 65.3 %)
card_games :24-28, ( 46.2 %)
toxicology :26-14, ( 65.0 %)
california_schools :17-13, ( 56.7 %)
financial :15-17, ( 46.9 %)
```

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

**experiment1 raw stats:**

``` python
correct simple is 108, ( 73.0 %)
failed simple is 40
failed id:[1498, 1500, 1505, 1514, 1524, 1525, 1389, 1410, 1166, 1251, 1078, 1092, 1144, 1145, 847, 854, 898, 902, 915, 930, 937, 950, 951, 959, 967, 978, 738, 533, 671, 710, 340, 341, 358, 366, 383, 440, 17, 41, 46, 159]
correct moderate is 142, ( 56.8 %)
failed moderate is 108
failed id:[1473, 1480, 1490, 1501, 1529, 1531, 1533, 1322, 1323, 1338, 1376, 1381, 1399, 1404, 1427, 1435, 1149, 1175, 1179, 1187, 1205, 1225, 1235, 1252, 1254, 1255, 1256, 1265, 1267, 1275, 1029, 1032, 1040, 1080, 1107, 1135, 1136, 1146, 1148, 865, 866, 877, 892, 894, 897, 904, 906, 928, 931, 963, 972, 989, 1002, 726, 728, 736, 758, 557, 565, 584, 595, 604, 637, 640, 672, 682, 683, 685, 694, 344, 347, 349, 352, 397, 405, 407, 408, 412, 459, 462, 465, 469, 473, 483, 484, 522, 529, 530, 197, 201, 213, 234, 255, 23, 24, 25, 26, 27, 37, 48, 85, 95, 136, 129, 145, 152, 168, 186]
correct challenging is 58, ( 56.9 %)
failed challenging is 44
failed id:[1481, 1482, 1526, 1460, 1168, 1169, 1241, 1242, 1243, 1247, 1302, 1031, 1058, 1094, 896, 944, 955, 988, 1011, 1014, 743, 772, 586, 639, 371, 416, 477, 528, 198, 207, 215, 218, 219, 231, 247, 263, 281, 28, 83, 87, 94, 116, 125, 149]
debit_card_specializing :14-16, ( 46.7 %)
student_club :36-12, ( 75.0 %)
thrombosis_prediction :27-23, ( 54.0 %)
european_football_2 :35-16, ( 68.6 %)
formula_1 :34-32, ( 51.5 %)
superhero :45-7, ( 86.5 %)
codebase_community :32-17, ( 65.3 %)
card_games :23-29, ( 44.2 %)
toxicology :26-14, ( 65.0 %)
california_schools :16-14, ( 53.3 %)
financial :20-12, ( 62.5 %)
```



