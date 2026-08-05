import sqlite3
import pandas as pd

conn = sqlite3.connect("ecommerce.db")

query = """
SELECT
    strftime('%Y-%m', order_purchase_timestamp) AS Month,
    SUM(payment_value) AS Revenue
FROM merged_ecommerce_data
GROUP BY Month
ORDER BY Month;
"""

df = pd.read_sql_query(query, conn)

print(df)

conn.close()