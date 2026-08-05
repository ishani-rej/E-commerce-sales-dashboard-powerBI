import sqlite3
import pandas as pd

df = pd.read_csv("merged_ecommerce_data.csv")

conn = sqlite3.connect("ecommerce.db")
df.to_sql("merged_ecommerce_data", conn, if_exists="replace", index=False)
conn.close()

print("Database created successfully!")