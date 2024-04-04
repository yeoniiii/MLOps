import sqlite3
import pandas as pd
import database

db_name = "./data/steel.db"
conn = sqlite3.connect(db_name)
c = conn.cursor()

# 데이터 로드
train_df = pd.read_csv("./data/train.csv")
test_df = pd.read_csv("./data/test.csv")
col_nm = ', '.join(train_df.columns)

# 테이블 생성
database.create_table('train', col_nm)
database.create_table('test', col_nm)
database.create_table('predict', col_nm+', pred')

# 테이블에 csv 파일 적재
train_df.to_sql("train", conn, index=False, if_exists='replace')
test_df.to_sql("test", conn, index=False, if_exists='replace')

conn.commit()

# 테이블 확인
database.show_table('train', 3)
database.show_table('test', 3)
database.show_table('predict', 3)
    
## close our connection
conn.close()
