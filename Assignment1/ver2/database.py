# sqlite3을 이용해서 데이터를 추출, 적재, 화면 출력하는 함수를 갖고 있는 코드

import sqlite3
import pandas as pd

def create_table(table_nm, col_nm):
    db_name = "./data/steel.db"
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    
    c.execute(f"""CREATE TABLE IF NOT EXISTS {table_nm} ({col_nm})""")

    conn.commit()
    conn.close()


def show_table(table_nm, row_limit=None):
    db_name = "./data/steel.db"
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    
    print(f"\n\n {table_nm} table...")
    if row_limit == None:
        c.execute(f"""SELECT * FROM {table_nm}""")
    else:
        c.execute(f"""SELECT * FROM {table_nm} LIMIT {row_limit}""")
    items = c.fetchall()
    for item in items:
        print(item)

    conn.commit()
    conn.close()


def load_table(table_nm):
    db_name = "./data/steel.db"
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    print(f"\n\n Load {table_nm} table...")

    c.execute(f"""SELECT * FROM {table_nm}""")
    cols = [col[0] for col in c.description]
    dat = pd.DataFrame(data=c.fetchall(),columns=cols)

    conn.close()
    conn.close()

    return dat