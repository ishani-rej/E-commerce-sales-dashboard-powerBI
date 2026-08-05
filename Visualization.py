import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect database
conn = sqlite3.connect("ecommerce.db")

# =========================================
# 1. Monthly Revenue
# =========================================
query1 = """
SELECT
strftime('%Y-%m', order_purchase_timestamp) AS Month,
SUM(payment_value) AS Revenue
FROM merged_ecommerce_data
GROUP BY Month
ORDER BY Month;
"""

df1 = pd.read_sql_query(query1, conn)

df1["Revenue"] = pd.to_numeric(df1["Revenue"])

plt.figure(figsize=(10,5))
plt.plot(df1["Month"], df1["Revenue"], marker="o")
plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# =========================================
# 2. Payment Type Distribution
# =========================================
query2 = """
SELECT
payment_type,
COUNT(*) AS Total
FROM merged_ecommerce_data
GROUP BY payment_type;
"""

df2 = pd.read_sql_query(query2, conn)

# Remove NULL values
df2["payment_type"] = df2["payment_type"].fillna("Unknown").astype(str)
df2["Total"] = pd.to_numeric(df2["Total"])

plt.figure(figsize=(8,5))
plt.bar(df2["payment_type"], df2["Total"])
plt.title("Payment Type Distribution")
plt.xlabel("Payment Type")
plt.ylabel("Orders")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()


# =========================================
# 3. Top Product Categories
# =========================================
query3 = """
SELECT
product_category_name,
COUNT(*) AS Orders
FROM merged_ecommerce_data
GROUP BY product_category_name
ORDER BY Orders DESC
LIMIT 10;
"""

df3 = pd.read_sql_query(query3, conn)

df3["product_category_name"] = df3["product_category_name"].fillna("Unknown").astype(str)
df3["Orders"] = pd.to_numeric(df3["Orders"])

plt.figure(figsize=(12,6))
plt.bar(df3["product_category_name"], df3["Orders"])
plt.title("Top 10 Product Categories")
plt.xlabel("Product Category")
plt.ylabel("Orders")
plt.xticks(rotation=60, ha="right")
plt.tight_layout()
plt.show()

conn.close()