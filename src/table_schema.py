import sqlite3

db_table_map = {
    "debit_card_specializing": [
        "customers",
        "gasstations",
        "products",
        "transactions_1k",
        "yearmonth",
    ],
    "student_club": [
        "major",
        "member",
        "attendance",
        "budget",
        "event",
        "expense",
        "income",
        "zip_code",
    ],
    "thrombosis_prediction": ["Patient", "Examination", "Laboratory"],
    "european_football_2": [
        "League",
        "Match",
        "Player",
        "Player_Attributes",
        "Team",
        "Team_Attributes",
    ],
    "formula_1": [
        "circuits",
        "seasons",
        "races",
        "constructors",
        "constructorResults",
        "constructorStandings",
        "drivers",
        "driverStandings",
        "lapTimes",
        "pitStops",
        "qualifying",
        "status",
        "results",
    ],
    "superhero": [
        "alignment",
        "attribute",
        "colour",
        "gender",
        "publisher",
        "race",
        "superpower",
        "superhero",
        "hero_attribute",
        "hero_power",
    ],
    "codebase_community": [
        "posts",
        "users",
        "badges",
        "comments",
        "postHistory",
        "postLinks",
        "tags",
        "votes",
    ],
    "card_games": [
        "cards",
        "foreign_data",
        "legalities",
        "rulings",
        "set_translations",
        "sets",
    ],
    "toxicology": ["molecule", "atom", "bond", "connected"],
    "california_schools": ["satscores", "frpm", "schools"],
    "financial": [
        "district",
        "account",
        "client",
        "disp",
        "card",
        "loan",
        "order",
        "trans",
    ],
}

def generate_schema_prompt_sqlite_nodata(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'")
    schemas = cursor.fetchall()
    conn.close()
    # return schema:
    # CREATE TABLE customers
    # (
    #    CustomerID INTEGER UNIQUE     not null
    #        primary key,
    #    Segment    TEXT null,
    #    Currency   TEXT null
    # )
    return "\n".join(s[0] for s in schemas if s[0])


# data 对齐成整齐的文本表格
# CustomerID, SME, CZK.  变为 CustomerID Segment Currency
# 1, LAM, EUR                         1     SME      CZK
def nice_look_table(column_names: list, values: list):
    rows = []
    # Determine the maximum width of each column
    widths = [
        max(len(str(value[i])) for value in values + [column_names])
        for i in range(len(column_names))
        # list comprehension 列表推导式 把循环和append压缩成一行写在[]
    ]

    # Print the column names
    header = "".join(
        f"{column.rjust(width)} " for column, width in zip(column_names, widths)
    )
    # print(header)
    # Print the values
    for value in values:
        row = "".join(f"{str(v).rjust(width)} " for v, width in zip(value, widths))
        rows.append(row)
    rows = "\n".join(rows)
    final_output = header + "\n" + rows
    return final_output

# 为了数据 和 table名 和 table schema一一对应, 先获取tables名, 遍历tables名获得对应CREATE, 用tables名获得data, 拼接存进dict
def generate_schema_prompt_sqlite(db_path, num_rows=None):
    # extract create ddls
    """
    :param root_place:
    :param db_name:
    :return:
    """
    full_schema_prompt_list = []
    conn = sqlite3.connect(db_path)
    # Create a cursor object
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    schemas = {}

    #遍历每个table获得schema
    for table in tables:
        if table[0] == "sqlite_sequence":
            # 跳过内部表, sqlite_sequence 是自动创建的表, 不是业务数据, 不跳过会出现CREATE TABLE sqlite_sequence(name,seq)
            continue
        cursor.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name='{}';".format(
                table[0]
            )
        )
        create_prompt = cursor.fetchone()[0]
        schemas[table[0]] = create_prompt

        #增加 样例data
        if num_rows:
            cur_table = table[0]
            if cur_table in ["order", "by", "group"]:
                cur_table = "`{}`".format(cur_table)

            cursor.execute("SELECT * FROM {} LIMIT {}".format(cur_table, num_rows))
            column_names = [description[0] for description in cursor.description]
            values = cursor.fetchall()

            rows_prompt = nice_look_table(column_names=column_names, values=values)
            verbose_prompt = "/* \n {} example rows: \n SELECT * FROM {} LIMIT {}; \n {} \n */".format(
                num_rows, cur_table, num_rows, rows_prompt
            )
            schemas[table[0]] = "{} \n {}".format(create_prompt, verbose_prompt)

    for k, v in schemas.items():
        full_schema_prompt_list.append(v)

    schema_prompt = "\n\n".join(full_schema_prompt_list)

    return schema_prompt
