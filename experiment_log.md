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
| 2.baseline+ 3 rows real data | x | | x |
| 3.schema linking? | | | |
| 4.error recovering? | | | |

**fixed:** add run.sh, get_request.py(combine path, retry times, save results)

**2026/7/28:**

**problem:** waiting prompt/api response and stucked for a long time, generating prompt & accessing API need to be split

## Phase2 

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

**failure analysis:**

- debit_card_specializing 5, thrombosis_prediction 3, european_football_2 6, card_games 6, california_schools 8 . generate sql quality decrease

``` sql
Fixed: 17, Broken: 20
Fixed:
1350 (student_club, moderate)
1464 (student_club, challenging)
846 (formula_1, moderate)
990 (formula_1, challenging)
766 (superhero, moderate)
829 (superhero, challenging)
415 (card_games, challenging)
424 (card_games, simple)
480 (card_games, moderate)
239 (toxicology, simple)
244 (toxicology, moderate)
245 (toxicology, moderate)
92 (financial, simple)
93 (financial, moderate)
115 (financial, challenging)
128 (financial, moderate)
173 (financial, challenging)
Broken:
1473 (debit_card_specializing, moderate)
1480 (debit_card_specializing, moderate)
1524 (debit_card_specializing, simple)
1389 (student_club, simple)
1187 (thrombosis_prediction, moderate)
1255 (thrombosis_prediction, moderate)
1078 (european_football_2, simple)
1148 (european_football_2, moderate)
930 (formula_1, simple)
937 (formula_1, simple)
736 (superhero, moderate)
743 (superhero, challenging)
366 (card_games, simple)
397 (card_games, moderate)
459 (card_games, moderate)
528 (card_games, challenging)
201 (toxicology, moderate)
213 (toxicology, moderate)
263 (toxicology, challenging)
83 (california_schools, challenging)
```

**Analysis financial db:**

``` python
FIXED: 92
base: SELECT COUNT(DISTINCT d.district_id)
FROM district d
JOIN client c ON d.district_id = c.district_id
WHERE c.gender = 'F'
GROUP BY d.district_id
HAVING AVG(d.A11) > 6000 AND AVG(d.A11) < 10000

v2: SELECT COUNT(DISTINCT c.district_id)
FROM client c
JOIN district d ON c.district_id = d.district_id
WHERE c.gender = 'F'
AND d.A11 > 6000
AND d.A11 < 10000

gold: SELECT COUNT(DISTINCT T2.district_id)  FROM client AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T1.gender = 'F' AND T2.A11 BETWEEN 6000 AND 10000

# base 用HAVING AVG(d.A11) 做分组后过滤，v2 直接用 WHERE d.A11 做行级过滤

FIXED: 93
base: SELECT COUNT(DISTINCT c.client_id)
FROM client c
JOIN district d ON c.district_id = d.district_id
WHERE c.gender = 'M'
AND d.A3 = 'North Bohemia'
AND d.A11 > 8000

v2: SELECT COUNT(DISTINCT c.client_id)
FROM client c
JOIN district d ON c.district_id = d.district_id
WHERE c.gender = 'M'
AND d.A3 = 'north Bohemia'
AND d.A11 > 8000

gold: SELECT COUNT(T1.client_id) FROM client AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T1.gender = 'M' AND T2.A3 = 'north Bohemia' AND T2.A11 > 8000

# base大写North Bohemia v2 改成了小写

FIXED: 115
base: SELECT CAST(SUM(CASE WHEN c.gender = 'M' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(c.client_id)
FROM client c
JOIN district d ON c.district_id = d.district_id
WHERE d.district_id = (
    SELECT district_id
    FROM district
    WHERE A3 = 'south Bohemia'
    ORDER BY CAST(A4 AS INTEGER) DESC
    LIMIT 1
)

v2: SELECT CAST(SUM(CASE WHEN c.gender = 'M' THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(c.client_id)
FROM client c
JOIN district d ON c.district_id = d.district_id
WHERE d.district_id = (
    SELECT district_id
    FROM district
    WHERE A3 = 'south Bohemia'
    ORDER BY A4 DESC
    LIMIT 1
)

gold: SELECT CAST(SUM(T1.gender = 'M') AS REAL) * 100 / COUNT(T1.client_id) FROM client AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T2.A3 = 'south Bohemia' GROUP BY T2.A4 ORDER BY T2.A4 DESC LIMIT 1

# base 转换类型CAST(A4 AS INTEGER) v1知道是数值不用转换

FIXED: 128
base: SELECT d.A2, COUNT(c.client_id) AS num_female_holders
FROM client c
JOIN disp dp ON c.client_id = dp.client_id
JOIN account a ON dp.account_id = a.account_id
JOIN district d ON a.district_id = d.district_id
WHERE c.gender = 'F'
GROUP BY d.A2
ORDER BY num_female_holders DESC
LIMIT 9

v2: SELECT d.A2, COUNT(c.client_id) AS num_female_holders
FROM district d
JOIN client c ON d.district_id = c.district_id
JOIN disp dp ON c.client_id = dp.client_id
JOIN account a ON dp.account_id = a.account_id
WHERE c.gender = 'F'
GROUP BY d.district_id, d.A2
ORDER BY num_female_holders DESC
LIMIT 9

gold: SELECT T2.A2, COUNT(T1.client_id) FROM client AS T1 INNER JOIN district AS T2 ON T1.district_id = T2.district_id WHERE T1.gender = 'F' GROUP BY T2.district_id, T2.A2 ORDER BY COUNT(T1.client_id) DESC LIMIT 9

# base join 很多次

FIXED: 173
base: SELECT a.frequency, t.k_symbol
FROM account a
JOIN trans t ON a.account_id = t.account_id
WHERE a.account_id = 3
AND t.amount = 3539
AND t.type = 'VYDAJ'

v2: SELECT a.frequency, t.k_symbol
FROM account a
JOIN trans t ON a.account_id = t.account_id
WHERE a.account_id = 3 AND t.amount = 3539
LIMIT 1

gold: SELECT T1.frequency, T2.k_symbol FROM account AS T1 INNER JOIN (SELECT account_id, k_symbol, SUM(amount) AS total_amount FROM `order` GROUP BY account_id, k_symbol) AS T2 ON T1.account_id = T2.account_id WHERE T1.account_id = 3 AND T2.total_amount = 3539
```


broken:
``` sql

About broken sql in debit_card_specializing db:
Broken: 1473
base: SELECT AVG(Consumption) / 12
FROM yearmonth
WHERE CustomerID IN (
    SELECT CustomerID
    FROM customers
    WHERE Segment = 'SME'
)
AND Date BETWEEN '201301' AND '201312'

v2: SELECT SUM(ym.Consumption) / 12 / COUNT(DISTINCT ym.CustomerID)
FROM yearmonth ym
JOIN customers c ON ym.CustomerID = c.CustomerID
WHERE c.Segment = 'SME'
AND ym.Date BETWEEN '201301' AND '201312'

gold: SELECT AVG(T2.Consumption) / 12 FROM customers AS T1 INNER JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE SUBSTR(T2.Date, 1, 4) = '2013' AND T1.Segment = 'SME'

Broken: 1480
base: SELECT SUBSTR(T1.Date, 5, 2) AS Month
FROM yearmonth AS T1
INNER JOIN customers AS T2 ON T1.CustomerID = T2.CustomerID
WHERE T2.Segment = 'SME' AND T1.Date BETWEEN '201301' AND '201312'
GROUP BY SUBSTR(T1.Date, 5, 2)
ORDER BY SUM(T1.Consumption) DESC
LIMIT 1

v2: SELECT T1.Date
FROM yearmonth T1
INNER JOIN customers T2 ON T1.CustomerID = T2.CustomerID
WHERE T2.Segment = 'SME'
AND T1.Date BETWEEN '201301' AND '201312'
GROUP BY T1.Date
ORDER BY SUM(T1.Consumption) DESC
LIMIT 1

gold: SELECT SUBSTR(T2.Date, 5, 2) FROM customers AS T1 INNER JOIN yearmonth AS T2 ON T1.CustomerID = T2.CustomerID WHERE SUBSTR(T2.Date, 1, 4) = '2013' AND T1.Segment = 'SME' GROUP BY SUBSTR(T2.Date, 5, 2) ORDER BY SUM(T2.Consumption) DESC LIMIT 1

Broken: 1524
base: SELECT g.Country
FROM transactions_1k t
JOIN gasstations g ON t.GasStationID = g.GasStationID
WHERE t.Date = '2012-08-24' AND t.Price = 548.4

v2: SELECT c.Currency
FROM customers c
JOIN transactions_1k t ON c.CustomerID = t.CustomerID
WHERE t.Date = '2012-08-24' AND t.Price = 548.4

gold: SELECT T2.Country FROM transactions_1k AS T1 INNER JOIN gasstations AS T2 ON T1.GasStationID = T2.GasStationID WHERE T1.Date = '2012-08-24' AND T1.Price  = 548.4



About broken sql in thrombosis_prediction db:
Broken: 1187
base: SELECT DISTINCT ID
FROM Laboratory
WHERE Date BETWEEN '1987-07-06' AND '1996-01-31'
AND GPT > 30
AND ALB < 4

v2: SELECT COUNT(DISTINCT L.ID) AS patient_count, L.ID
FROM Laboratory L
WHERE L.Date BETWEEN '1987-07-06' AND '1996-01-31'
AND L.GPT > 30
AND L.ALB < 4
GROUP BY L.ID

gold: SELECT DISTINCT ID FROM Laboratory WHERE Date BETWEEN '1987-07-06' AND '1996-01-31' AND GPT > 30 AND ALB < 4

Broken: 1255
base: SELECT p.Diagnosis
FROM Patient p
JOIN Laboratory l ON p.ID = l.ID
WHERE l.IGM <= 40 OR l.IGM >= 400
GROUP BY p.Diagnosis
ORDER BY COUNT(p.Diagnosis) DESC
LIMIT 1

v2: SELECT Diagnosis
FROM Patient
WHERE ID IN (
    SELECT DISTINCT ID
    FROM Laboratory
    WHERE IGM <= 40 OR IGM >= 400
)
AND Diagnosis IS NOT NULL
GROUP BY Diagnosis
ORDER BY COUNT(Diagnosis) DESC
LIMIT 1

gold: SELECT T1.Diagnosis FROM Patient AS T1 INNER JOIN Laboratory AS T2 ON T1.ID = T2.ID WHERE T2.IGM NOT BETWEEN 40 AND 400 GROUP BY T1.Diagnosis ORDER BY COUNT(T1.Diagnosis) DESC LIMIT 1



About broken sql in european_football_2 db:
Broken: 1078
base: SELECT player_name FROM Player WHERE player_name IN ('Aaron Lennon', 'Abdelaziz Barrada') ORDER BY birthday ASC LIMIT 1

v2: SELECT player_name, birthday FROM Player WHERE player_name IN ('Aaron Lennon', 'Abdelaziz Barrada') ORDER BY birthday ASC LIMIT 1

gold: SELECT player_name FROM Player WHERE player_name IN ('Aaron Lennon', 'Abdelaziz Barrada') ORDER BY birthday ASC LIMIT 1

Broken: 1148
base: SELECT CAST(COUNT(CASE WHEN p.height < 180 AND pa.overall_rating > 70 THEN 1 END) AS REAL) * 100 / COUNT(p.id)
FROM Player p
JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id

v2: SELECT CAST(COUNT(CASE WHEN p.height < 180 AND pa.overall_rating > 70 THEN 1 END) AS REAL) * 100 / COUNT(DISTINCT p.id)
FROM Player p
JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id

gold: SELECT CAST(COUNT(CASE WHEN t2.overall_rating > 70  AND t1.height < 180 THEN t1.id ELSE NULL END) AS REAL) * 100 / COUNT(t1.id) percent FROM Player AS t1 INNER JOIN Player_Attributes AS t2 ON t1.player_api_id = t2.player_api_id 




About broken sql in card_games db:
Broken: 366
base: SELECT l.format
FROM legalities l
JOIN cards c ON l.uuid = c.uuid
WHERE c.name = 'Benalish Knight'

v2: SELECT l.format, l.status
FROM legalities l
JOIN cards c ON l.uuid = c.uuid
WHERE c.name = 'Benalish Knight'

gold: SELECT T2.format FROM cards AS T1 INNER JOIN legalities AS T2 ON T1.uuid = T2.uuid WHERE T1.name = 'Benalish Knight'

Broken: 397
base: SELECT manaCost FROM cards WHERE layout = 'normal' AND frameVersion = '2003' AND borderColor = 'black' AND availability = 'mtgo,paper'

v2: SELECT DISTINCT manaCost
FROM cards
WHERE layout = 'normal'
AND frameVersion = '2003'
AND borderColor = 'black'
AND availability = 'mtgo,paper'

gold: SELECT manaCost FROM cards WHERE availability = 'mtgo,paper' AND borderColor = 'black' AND frameVersion = 2003 AND layout = 'normal'

Broken: 459
base: SELECT name FROM cards WHERE name IN ('Serra Angel', 'Shrine Keeper') ORDER BY convertedManaCost DESC LIMIT 1

v2: SELECT name, convertedManaCost
FROM cards
WHERE name IN ('Serra Angel', 'Shrine Keeper')
ORDER BY convertedManaCost DESC
LIMIT 1

gold: SELECT name FROM cards WHERE name IN ('Serra Angel', 'Shrine Keeper') ORDER BY convertedManaCost DESC LIMIT 1

Broken: 528
base: SELECT DISTINCT c.name, l.format
FROM cards c
JOIN sets s ON c.setCode = s.code
JOIN legalities l ON c.uuid = l.uuid
WHERE s.name = 'Hour of Devastation'
AND l.status = 'Legal'

v2: SELECT c.name, l.format
FROM cards c
JOIN sets s ON c.setCode = s.code
JOIN legalities l ON c.uuid = l.uuid
WHERE s.name = 'Hour of Devastation'
AND l.status = 'Legal'

gold: SELECT DISTINCT T2.name , CASE WHEN T1.status = 'Legal' THEN T1.format ELSE NULL END FROM legalities AS T1 INNER JOIN cards AS T2 ON T2.uuid = T1.uuid WHERE T2.setCode IN ( SELECT code FROM sets WHERE name = 'Hour of Devastation' )





About broken sql in california_schools db:
Broken: 83
base: SELECT s.City, COUNT(s.CDSCode) AS NumberOfSchools
FROM schools s
JOIN frpm f ON s.CDSCode = f.CDSCode
WHERE s.Magnet = 1
AND s.GSserved = 'K-8'
AND f.`NSLP Provision Status` = 'Multiple Provision Types'
GROUP BY s.City

v2: SELECT COUNT(DISTINCT s.City) AS num_cities, s.City, COUNT(s.CDSCode) AS num_schools
FROM schools s
JOIN frpm f ON s.CDSCode = f.CDSCode
WHERE s.Magnet = 1
AND s.GSserved = 'K-8'
AND f.`NSLP Provision Status` = 'Multiple Provision Types'
GROUP BY s.City

gold: SELECT T2.City, COUNT(T2.CDSCode) FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T2.Magnet = 1 AND T2.GSoffered = 'K-8' AND T1.`NSLP Provision Status` = 'Multiple Provision Types' GROUP BY T2.City

```



