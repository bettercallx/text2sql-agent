import json
v1 = json.load(open("./output/baseline_sonnet_500.json", "r"))
v2 = json.load(open("./output/ph2_addrow_sonnet_500.json", "r"))

fixed =[]
broken=[]
# 用索引对齐两个列表 而不是嵌套
for i in range(len(v1)):
    
    if not v1[i]["correct"] and v2[i]["correct"]:
        fixed.append(v1[i])
    elif v1[i]["correct"] and not v2[i]["correct"]:
        broken.append(v1[i])

print(f"Fixed: {len(fixed)}, Broken: {len(broken)}")
print("Fixed:")
for item in fixed:
    print(f"{item['question_id']} ({item['db_id']}, {item['difficulty']})")
print("Broken:")
for item in broken:
    print(f"{item['question_id']} ({item['db_id']}, {item['difficulty']})")


# print("About fix sql in financial db:")
# for i in range(len(v1)):
#     if v1[i]["db_id"] == "financial" and not v1[i]["correct"] and v2[i]["correct"]:
#         print(f"FIXED: {v1[i]['question_id']}")
#         print(f"base: {v1[i]['predicted_sql']}\n")
#         print(f"v2: {v2[i]['predicted_sql']}\n")
#         print(f"gold: {v1[i]['gold_sql']}\n")

# print("About broken sql in debit_card_specializing db:")
# for i in range(len(v1)):
#     if v1[i]["db_id"] == "debit_card_specializing" and v1[i]["correct"] and not v2[i]["correct"]:
#         print(f"Broken: {v1[i]['question_id']}")
#         print(f"base: {v1[i]['predicted_sql']}\n")
#         print(f"v2: {v2[i]['predicted_sql']}\n")
#         print(f"gold: {v1[i]['gold_sql']}\n")

print("About broken sql in california_schools db:")
for i in range(len(v1)):
    if v1[i]["db_id"] == "california_schools" and v1[i]["correct"] and not v2[i]["correct"]:
        print(f"Broken: {v1[i]['question_id']}")
        print(f"base: {v1[i]['predicted_sql']}\n")
        print(f"v2: {v2[i]['predicted_sql']}\n")
        print(f"gold: {v1[i]['gold_sql']}\n")


