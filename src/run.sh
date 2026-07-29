eval_path='./mini_dev/llm/mini_dev_data/data_minidev/MINIDEV/mini_dev_sqlite.json'
db_root_path='./mini_dev/llm/mini_dev_data/data_minidev/MINIDEV/dev_databases/'

# Choose engine to run
engine_mode=1

if [ "$engine_mode" -eq 3 ]; then
    engine='claude-sonnet-4-6'
    query_times=500
    addrow=1
elif [ "$engine_mode" -eq 2 ]; then
    engine='claude-haiku-4-5-20251001'
    query_times=50
    addrow=1
else
    engine='claude-haiku-4-5-20251001'
    query_times=2
    addrow=1
fi

sql_dialect='SQLite'
data_output_path="./output/ph2_addrow_haiku_${query_times}.json"

echo "generate $engine batch, $query_times queries"
python3 -u ./src/get_request.py --db_root_path ${db_root_path} --engine ${engine} --q_nums ${query_times} \
    --eval_path ${eval_path} --data_output_path ${data_output_path} --addrow ${addrow} --sql_dialect ${sql_dialect}

# Chain of thoughts
# cot='True'
# Choose the number of threads to run in parallel, 1 for single thread
# num_threads=3
