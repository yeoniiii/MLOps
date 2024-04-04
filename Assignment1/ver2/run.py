import sqlite3
import pandas as pd
import numpy as np
import call_func as cf
import inference as infer
import database

db_name = "./data/steel.db"
conn = sqlite3.connect(db_name)
c = conn.cursor()

c.execute(""" SELECT count(*) FROM train """) # 1358
print(c.fetchall())
c.execute(""" SELECT count(*) FROM test """) # 583
print(c.fetchall())

for i in range(100):
    ind = str(np.random.randint(0,582, size=1)[0])
    dat = cf.call_x_value(ind)

    pred = infer.inference(dat)

    pred.to_sql("predict", conn, index=False, if_exists='append')

c.execute(""" SELECT count(*) FROM predict """) # 683
print(c.fetchall())
conn.close()

database.show_table("predict", 3)