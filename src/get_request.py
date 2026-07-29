import argparse
import time
import json
import sqlite3
from prompt import generate_combined_prompts_one
from anthropic import Anthropic
client = Anthropic()


# combine path
def decouple_question_schema(datasets, db_root_path):
    question_list = []
    db_path_list = []
    knowledge_list = []
    for i, data in enumerate(datasets):
        question_list.append(data["question"])
        cur_db_path = db_root_path + data["db_id"] + "/" + data["db_id"] + ".sqlite"
        db_path_list.append(cur_db_path)
        knowledge_list.append(data["evidence"])
    
    return question_list, db_path_list, knowledge_list

# clean the response
def clean_sql(response_text):
    text = response_text.strip()
    if "```sql" in text:
        text = text.split("```sql")[-1]
        text = text.split("```")[0]
    elif text.startswith("```"):
        text = text.split("\n", 1)[1]
        text = text.rsplit("```", 1)[0]
    return text.strip().rstrip(";")


# temperature control text generation randomness(0.0->1.0)
def connect_claude(engine, prompt):
    """
    Function to connect to API and get response.
    """
    MAX_API_RETRY = 3
    for attempt in range(MAX_API_RETRY):
        try:
            message = client.messages.create(
                max_tokens=1024,
                temperature=0,
                model=engine,
                timeout=60,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )
            return message.content[0].text
        except Exception as e:
            print(f"Retry {attempt}: {e}")
            time.sleep(4)
    return None

# compare result of predicted_sql with gold_sql
def is_correct(db_path, predicted_sql, gold_sql):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(predicted_sql)
        predicted = cursor.fetchall()

        cursor.execute(gold_sql)
        gold = cursor.fetchall()

        return predicted == gold
    except:
        return False
    finally:
        conn.close()


# Generate peompt, compare sql result and save results
def collect_responce_evaluation(datasets, db_path_list, question_list,knowledge_list, engine, query_times,sql_dialect, addrow):
    prompts =[]
    results =[]
    correct =0

    # generate prompt
    for i in range(query_times):
        prompt = generate_combined_prompts_one(db_path=db_path_list[i],
            question=question_list[i], sql_dialect=sql_dialect,addrow=addrow,knowledge=knowledge_list[i])
        prompts.append(prompt)
        print(f"Prompt {i}: {len(prompt)} chars")
        print(prompts[i])

    print(f"All prompt generated, starting call API")

    # connect_claude: API calls,  is_correct: compare the results
    for i in range(query_times):
        print(f"Now [{i+1}/{query_times}] Processing {datasets[i].get('question_id')}")

        raw = connect_claude(engine, prompts[i])
        if raw is None:
            print(f"Failed: {datasets[i].get('question_id')} after retries")
            results.append({"question_id": datasets[i].get("question_id"),"result": False})
            continue

        predicted_sql = clean_sql(raw)
        gold_sql = datasets[i].get("SQL")
        match = is_correct(db_path_list[i], predicted_sql,gold_sql)

        if match:
            correct+=1
        else:
            print(f"Failed: {datasets[i].get('question_id')} ({datasets[i].get('difficulty')})")

        results.append({
            "question_id": datasets[i].get("question_id"),
            "db_id": datasets[i].get("db_id"),
            "difficulty": datasets[i].get("difficulty"),
            "predicted_sql": predicted_sql,
            "gold_sql": gold_sql,
            "correct": match,
            "raw_output": raw,
        })

    print(f"\nResult: {correct}/{query_times} ({correct/query_times*100:.1f}%)")
    return results


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--db_root_path", type=str, default="")
    args_parser.add_argument("--engine", type=str, required=True, default="")
    args_parser.add_argument("--q_nums", type=int, default=10)
    args_parser.add_argument("--eval_path", type=str, default="")
    args_parser.add_argument("--data_output_path", type=str, default="")
    args_parser.add_argument("--addrow", type=int, default=0)
    args_parser.add_argument("--sql_dialect", type=str, default="SQLite")
    args = args_parser.parse_args()

    eval_data = json.load(open(args.eval_path, "r"))
    question_list, db_path_list, knowledge_list = decouple_question_schema(
        datasets=eval_data, db_root_path=args.db_root_path)

    res = collect_responce_evaluation( datasets= eval_data,db_path_list=db_path_list, 
                                      question_list= question_list, knowledge_list=knowledge_list,
                                      engine= args.engine, query_times=args.q_nums,sql_dialect=args.sql_dialect,addrow=args.addrow)

    with open(args.data_output_path, "w") as f:
        json.dump(res, f, indent=2)
    print(f"Results saved to {args.data_output_path}")

