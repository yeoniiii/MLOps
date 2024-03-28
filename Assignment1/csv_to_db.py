# train.csv, test.csv파일을 data.db 파일 내 train, test 테이블로 변환하는 코드

import sqlite3
import pandas as pd
import database

db_name = "data.db"
conn = sqlite3.connect(db_name)
c = conn.cursor()

train_df = pd.read_csv('./data/train.csv')
test_df = pd.read_csv('./data/test.csv')
pred_df = pd.DataFrame()

# 테이블 생성
database.create_table(train_df, 'train')
database.create_table(test_df, 'test')
database.create_table(pred_df, 'predict', pred=True)

# 테이블에 csv 파일 적재
train_df.to_sql('train', conn, if_exists='replace')
test_df.to_sql('test', conn, if_exists='replace')

conn.commit()
conn.close()