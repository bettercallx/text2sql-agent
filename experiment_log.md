# Experiment Log

## Baseline (10 queries)

**2026/7/23:**
**Setup:** naive prompt (schema + question + evidence) → Claude Sonnet → execute & compare

**Result:** 5/10 correct (50%). Simple all correct, moderate/challenging all failed.

**Failure analysis:**

- Q1481 (challenging): Claude return long thought process + SQL, 说明还要clean再写入prompt
- Q1479 (moderate):

**Fixed:** 加 clean_sql 处理 .md


**Next:** 修改 clean_sql, loop through sqlite.json看正确率



