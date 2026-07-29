import json
base_data = json.load(open("./output/baseline_sonnet_500.json", "r"))
addrow_data = json.load(open("./output/ph2_addrow_sonnet_500.json", "r"))

fixed =[]
broken=[]
# 用索引对齐两个列表 而不是嵌套
cmptwo = {}
for i in range(len(base_data)):
    base_item=base_data[i]
    add_item=addrow_data[i]
    
    if base_item.get("correct")==True and add_item.get("correct")==False:
        cmptwo[diff]["wrong"]+=1
        print(f"fail for {base_item.get('question_id')} , {diff}")
        print(f"ph1 predicted sql {base_item.get('predicted_sql')}")
        print(f"ph2 predicted sql {add_item.get('predicted_sql')}")

    elif base_item.get("correct")==False and add_item.get("correct")==True:
        cmptwo[diff]["correct"]+=1
        print(f"fail for {base_item.get('question_id')} , {diff}")
        print(f"ph1 predicted sql {base_item.get('predicted_sql')}")
        print(f"ph2 predicted sql {add_item.get('predicted_sql')}")
    else:
        continue


for diff in ['simple', 'moderate', 'challenging']:
    s=cmptwo[diff]
    all = s['correct']+s['wrong']
    print(f"correct {diff} is {s['correct']}")
    print(f"failed {diff} is {s['wrong']}")
