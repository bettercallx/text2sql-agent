# parse sqlite json(question&evidence) -> combine schema&Q&evidence as prompt -> API -> compare result with "SQL" -> statistical matrix
# client已经配好了API key和 API endpoint,不需要指定URL client.messages.create()发送了一个HTTP POST请求, 把model messages max_tokens打包成json发过去

import os
import sqlite3
import json
from anthropic import Anthropic
client = Anthropic()
with open("mini_dev/llm/mini_dev_data/data_minidev/MINIDEV/mini_dev_sqlite.json","r") as file:
    data_list = json.load(file)

correct = 0
wrong = 0
def get_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'")
    schemas = cursor.fetchall()

    conn.close()
    return "\n".join(s[0] for s in schemas if s[0])

def is_correct(db_path, predicted_sql, gold_sql):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(predicted_sql)
        predicted = cursor.fetchall()
        #print("predicted is :", predicted)
        cursor.execute(gold_sql)
        gold = cursor.fetchall()
        #print("real one is :", gold)
        return predicted == gold
    except Exception as e:
        return False
    finally:
        conn.close()

# responce is .md(```sql````), sometimes return long thought process. both need to be cleaned 
#---RAW OUTPUT---
#"```sql\nSELECT SUM(ym.Consumption) / 12 AS AvgMonthlyConsumption\nFROM yearmonth ym\nJOIN customers c ON ym.CustomerID = c.CustomerID\nWHERE c.Segment = 'SME'\nAND ym.Date BETWEEN '201301' AND '201312'\n```"
#---END---
def clean_sql(response_text):
    text = response_text.strip()
    if "```sql" in text:
        text = text.split("```sql")[-1] #最后一个sql代码块
        text = text.split("```")[0]
    elif text.startswith("```"):
        text = text.split("\n", 1)[1]  #去掉第一行 ```sql
        text = text.rsplit("```", 1)[0]  #去掉最后的 ```
    return text.strip().rstrip(";")

for item in data_list[:10]:
    db_path = "mini_dev/llm/mini_dev_data/data_minidev/MINIDEV/dev_databases/" + item.get("db_id") +"/"+item.get("db_id")+".sqlite"
    question = item.get("question")
    evidence = item.get("evidence")
    schema = get_schema(db_path)
    #print(schema)
    prompt = f"""Given this database schema:{schema}
    Question: {question}
    Evidence: {evidence}
    Write a SQLite SQL query to answer the question. Return only the SQL, nothing else."""

    message = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],

        model="claude-sonnet-4-6",
    )

    raw = message.content[0].text
    print("---RAW OUTPUT---")
    print(repr(raw))  # repr会显示\n和```等隐藏字符
    print("---END---")

    predict_sql = clean_sql(message.content[0].text)
    if(is_correct(db_path, predict_sql, item.get("SQL"))):
        correct+=1
    else:
        print("this one failed:", item.get("question_id"),"level:" ,item.get("difficulty"))
        wrong+=1

print("nums of correct:",correct,"nums of wrong:",wrong)
