import sqlite3
db_path = "mini_dev/llm/mini_dev_data/data_minidev/MINIDEV/dev_databases/debit_card_specializing/debit_card_specializing.sqlite"
predicted_sql = "SELECT CAST(SUM(CASE WHEN Currency = 'EUR' THEN 1 ELSE 0 END) AS REAL) / SUM(CASE WHEN Currency = 'CZK' THEN 1 ELSE 0 END) FROM customers"
gold_sql = "SELECT CAST(SUM(IIF(Currency = 'EUR', 1, 0)) AS FLOAT) / SUM(IIF(Currency = 'CZK', 1, 0)) AS ratio FROM customers"

def is_correct(db_path, predicted_sql, gold_sql):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(predicted_sql)
        predicted = cursor.fetchall()
        print("predicted is :", predicted)
        cursor.execute(gold_sql)
        gold = cursor.fetchall()
        print("real one is :", gold)
        return predicted == gold
    except Exception as e:
        return False
    finally:
        conn.close()

is_correct(db_path, predicted_sql, gold_sql)
