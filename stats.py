import json
data = json.load(open("./output/baseline_sonnet_500.json", "r"))

# 用 数据结构 替代 重复复制粘贴变量名，用一个dict或list收起来

stats ={}
for item in data:
    diff = item["difficulty"]
    if diff not in stats:
        stats[diff] ={"correct":0, "wrong":0, "fail_ids":[]} #初始化
    if item["correct"]:
        stats[diff]["correct"] +=1
    else:
        stats[diff]["wrong"] +=1
        stats[diff]["fail_ids"].append(item.get("question_id"))

for diff in ['simple', 'moderate', 'challenging']:
    s=stats[diff]
    all = s['correct']+s['wrong']
    print(f"correct {diff} is {s['correct']}, ( {s['correct']/all*100:.1f} %)")
    print(f"failed {diff} is {s['wrong']}")
    print(f"failed id:{s['fail_ids']}")

stats_db={}
for item in data:
    db_type = item["db_id"]
    if db_type not in stats_db:
        stats_db[db_type]={"correct":0, "wrong":0}
    if item["correct"]:
        stats_db[db_type]["correct"] +=1
    else:
        stats_db[db_type]["wrong"] +=1

for k,v in stats_db.items():
    each_db = v['correct']+v['wrong']
    print(f"{k} :{v['correct']}-{v['wrong']}, ( {v['correct']/each_db*100:.1f} %)")



    

 



