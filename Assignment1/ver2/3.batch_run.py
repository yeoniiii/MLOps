import sqlite3
import pandas as pd
import numpy as np
import database
import inference as inf


## load test dataset
dat = database.load_table("test")

## make prediction for test set
print("\n\n make prediction...")
pred = inf.inference(dat) # 583개

## insert prediction into predict table 
print("\n\n insert predict table...")

db_name = "./data/steel.db"
conn = sqlite3.connect(db_name)
c = conn.cursor()

#c.executemany("INSERT INTO predict VALUES (?)", dat)
pred.to_sql("predict", conn, index=False, if_exists='replace')

conn.commit()
conn.close()

## print predict table
database.show_table("predict", 10)

