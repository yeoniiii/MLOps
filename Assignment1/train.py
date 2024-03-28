# 모델을 생성하는 코드
## (해당 코드 실행시 trans.pkl, model.pkl 생성)

import pandas as pd
import numpy as np
import pickle as pkl
import sqlite3

db_name = "data.db"
conn = sqlite3.connect(db_name)
c = conn.cursor()

train = pd.read_sql("SELECT * FROM train", conn, index_col=None)

# x variables preprocessing
x_cols = ['V'+str(i) for i in range(1, 28)]
from sklearn.preprocessing import StandardScaler
trans = StandardScaler()
trans.fit(train[x_cols])
train_x = trans.transform(train[x_cols])

## y variables preprocessing
train['V34'] = train['Class'] - 1
train_y = [str(np.where(r==1)[0][0]) for r in train[['V'+str(i) for i in range(28, 35)]].to_numpy()]

## classification modeling
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(train_x, train_y)

# save models
pkl.dump(model, open("model.pkl", "wb"))
pkl.dump(trans, open("trans.pkl", "wb"))