import os
from anthropic import Anthropic
client = Anthropic()

import sqlite3
db_path = "mini_dev/llm/mini_dev_data/data_minidev/MINIDEV/dev_databases/debit_card_specializing/debit_card_specializing.sqlite"


def get_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'")
    schemas = cursor.fetchall()

    conn.close()
    return "\n".join(s[0] for s in schemas if s[0])

schema = get_schema(db_path)
print(schema)
#每个CREATE TABLE是一张表，customers有三列，
# CustomerID 整数&主键，Segment 文本，Currency 文本
# not null 不允许为空(可存空文本""和0占位)，null允许为空值，UNIQUE表示值唯一不能出现重复值
# CREATE TABLE customers
#(
#    CustomerID INTEGER UNIQUE     not null
#        primary key,
#    Segment    TEXT null,
#    Currency   TEXT null
#)

prompt = f"""Given this database schema:
{schema}

Question: {"What is the ratio of customers who pay in EUR against customers who pay in CZK?"}
Evidence: {"ratio of customers who pay in EUR against customers who pay in CZK = count(Currency = 'EUR') / count(Currency = 'CZK')."}

Write a SQLite SQL query to answer the question. Return only the SQL, nothing else."""

message = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],

    model="claude-opus-4-6",
)

print(message.content[0].text)