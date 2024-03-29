# 모델을 로드하고 추론결과를 적재하는 코드
## (data.db내 predict 테이블을 화면에 출력했을 때 test데이터의 3, 5, 12번째 row의 추론결과가 출력되어야 함)

import pandas as pd
import pickle as pkl
import database
import sqlite3

## load preprocessing and model
trans = pkl.load(open("trans.pkl", "rb"))
model = pkl.load(open("model.pkl", "rb"))

## load new dataset
for i in [3, 5, 12]:
    pred = database.row_lookup('test', i)
    x_cols = ['V'+str(i) for i in range(1, 28)]

    ## prediction for new dataset
    x = trans.transform(pred[x_cols])
    pred = model.predict(x)

    ## predict 테이블의 pred 컬럼에 적재
    db_name = "data.db"
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("INSERT INTO predict VALUES (?)", pred)

    conn.commit()
    conn.close()