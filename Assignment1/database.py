# db파일 내 테이블을 생성하는 함수, db파일에서 특정 row의 데이터를 불러오는 함수가 포함된 파일.
## (다른 코드들에서 import database로 호출되어야 함)

import sqlite3
import pandas as pd

def create_table(df, table_nm, pred = False):
    db_name = "data.db"
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    if not pred:
        col_nm = ', '.join(df.columns)
    else:
        col_nm = 'pred'
    
    c.execute(f"""CREATE TABLE IF NOT EXISTS {table_nm} ({col_nm})""")

    conn.commit()
    conn.close()


def row_lookup(df, row):
    db_name = "data.db"
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute(f"""SELECT *
                FROM {df}
                WHERE rowid = {row}""")

    cols = [col[0] for col in c.description]
    df = pd.DataFrame(data=c.fetchall(), columns=cols)

    return df

    # items = c.fetchall()

    # for item in items:
    #     print(item)

    conn.commit()
    conn.close()