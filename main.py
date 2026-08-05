import pandas as pd

# ----------------------------
# Load datasets
# ----------------------------

customers = pd.read_csv("olist_customers_dataset.csv")
orders = pd.read_csv("olist_orders_dataset.csv")
items = pd.read_csv("olist_order_items_dataset.csv")
products = pd.read_csv("olist_products_dataset.csv")
payments = pd.read_csv("olist_order_payments_dataset.csv")

# ----------------------------
# Show column names
# ----------------------------

print("Products Columns:")
print(products.columns.tolist())

# ----------------------------
# Display first 5 rows
# ----------------------------

print("\nCustomers")
print(customers.head())

print("\nOrders")
print(orders.head())

print("\nOrder Items")
print(items.head())

print("\nProducts")
print(products.head())

print("\nPayments")
print(payments.head())

# ----------------------------
# Missing Values
# ----------------------------

print("\nMissing Values")

print("\nCustomers")
print(customers.isnull().sum())

print("\nOrders")
print(orders.isnull().sum())

print("\nOrder Items")
print(items.isnull().sum())

print("\nProducts")
print(products.isnull().sum())

print("\nPayments")
print(payments.isnull().sum())

# ----------------------------
# Fill Missing Values
# ----------------------------

products["product_category_name"] = products["product_category_name"].fillna("Unknown")

# Handle both 'length' and 'lenght'
if "product_name_length" in products.columns:
    products["product_name_length"] = products["product_name_length"].fillna(
        products["product_name_length"].median()
    )

if "product_name_lenght" in products.columns:
    products["product_name_lenght"] = products["product_name_lenght"].fillna(
        products["product_name_lenght"].median()
    )

if "product_description_length" in products.columns:
    products["product_description_length"] = products["product_description_length"].fillna(
        products["product_description_length"].median()
    )

if "product_description_lenght" in products.columns:
    products["product_description_lenght"] = products["product_description_lenght"].fillna(
        products["product_description_lenght"].median()
    )

if "product_photos_qty" in products.columns:
    products["product_photos_qty"] = products["product_photos_qty"].fillna(
        products["product_photos_qty"].median()
    )

if "product_weight_g" in products.columns:
    products["product_weight_g"] = products["product_weight_g"].fillna(
        products["product_weight_g"].median()
    )

if "product_length_cm" in products.columns:
    products["product_length_cm"] = products["product_length_cm"].fillna(
        products["product_length_cm"].median()
    )

print("\nProduct dataset cleaned successfully!")

# ----------------------------
# Duplicate Rows
# ----------------------------

print("\nDuplicate Rows")

print("Customers :", customers.duplicated().sum())
print("Orders :", orders.duplicated().sum())
print("Order Items :", items.duplicated().sum())
print("Products :", products.duplicated().sum())
print("Payments :", payments.duplicated().sum())

# ----------------------------
# Convert Date
# ----------------------------

orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)

print("\nOrders Data Types")
print(orders.dtypes)

print("\nData Cleaning Completed Successfully!")

# ----------------------------
# Merge Datasets
# ----------------------------

# Merge customers with orders
merged_df = orders.merge(customers, on="customer_id", how="left")

# Merge with order items
merged_df = merged_df.merge(items, on="order_id", how="left")

# Merge with products
merged_df = merged_df.merge(products, on="product_id", how="left")

# Merge with payments
merged_df = merged_df.merge(payments, on="order_id", how="left")

print("\nMerged Dataset Shape:")
print(merged_df.shape)

print("\nFirst 5 Rows of Merged Dataset:")
print(merged_df.head())

merged_df.to_csv("merged_ecommerce_data.csv", index=False)

print("\nMerged dataset saved successfully!")

# ----------------------------
# Exploratory Data Analysis (EDA)
# ----------------------------

print("\n========== EDA ==========")

# Total Orders
print("\nTotal Orders:")
print(merged_df["order_id"].nunique())

# Total Customers
print("\nTotal Customers:")
print(merged_df["customer_id"].nunique())

# Total Products
print("\nTotal Products:")
print(merged_df["product_id"].nunique())

# Total Revenue
print("\nTotal Revenue:")
print(round(merged_df["payment_value"].sum(), 2))

# Order Status Count
print("\nOrder Status:")
print(merged_df["order_status"].value_counts())

# Top 10 Product Categories
print("\nTop 10 Product Categories:")
print(merged_df["product_category_name"].value_counts().head(10))

# Top 10 States
print("\nTop 10 Customer States:")
print(merged_df["customer_state"].value_counts().head(10))

# Payment Types
print("\nPayment Types:")
print(merged_df["payment_type"].value_counts())

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

# ----------------------------
# Revenue by Payment Type
# ----------------------------
plt.figure(figsize=(8,5))

merged_df.groupby("payment_type")["payment_value"].sum().sort_values().plot(kind="bar")

plt.title("Revenue by Payment Type")
plt.xlabel("Payment Type")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()

# ----------------------------
# Top 10 Product Categories
# ----------------------------
plt.figure(figsize=(10,6))

merged_df["product_category_name"].value_counts().head(10).plot(kind="bar")

plt.title("Top 10 Product Categories")
plt.xlabel("Category")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.show()

# ----------------------------
# Order Status
# ----------------------------
plt.figure(figsize=(8,5))

sns.countplot(data=merged_df, x="order_status")

plt.title("Order Status Distribution")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ----------------------------
# Monthly Sales Trend
# ----------------------------
merged_df["Month"] = merged_df["order_purchase_timestamp"].dt.to_period("M")

monthly_sales = merged_df.groupby("Month")["payment_value"].sum()

plt.figure(figsize=(12,6))

monthly_sales.plot()

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.tight_layout()
plt.show()

# ----------------------------
# Customer Segmentation (RFM)
# ----------------------------

import pandas as pd

snapshot_date = merged_df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)

rfm = merged_df.groupby("customer_unique_id").agg({
    "order_purchase_timestamp": lambda x: (snapshot_date - x.max()).days,
    "order_id": "nunique",
    "payment_value": "sum"
})

rfm.columns = ["Recency", "Frequency", "Monetary"]

print("\n========== RFM Analysis ==========")
print(rfm.head())

rfm["R_Score"] = pd.qcut(rfm["Recency"], 4, labels=[4,3,2,1])
rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 4, labels=[1,2,3,4])
rfm["M_Score"] = pd.qcut(rfm["Monetary"], 4, labels=[1,2,3,4])

rfm["RFM_Score"] = (
    rfm["R_Score"].astype(str) +
    rfm["F_Score"].astype(str) +
    rfm["M_Score"].astype(str)
)

print("\nTop Customers")
print(rfm.sort_values("Monetary", ascending=False).head(10))

from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Monthly Sales
sales = merged_df.groupby(
    merged_df["order_purchase_timestamp"].dt.to_period("M")
)["payment_value"].sum().reset_index()

sales["Month"] = range(len(sales))

X = sales[["Month"]]
y = sales["payment_value"]

model = LinearRegression()
model.fit(X, y)

sales["Predicted"] = model.predict(X)

plt.figure(figsize=(10,5))
plt.plot(sales["Month"], sales["payment_value"], label="Actual Sales")
plt.plot(sales["Month"], sales["Predicted"], label="Predicted Sales")
plt.title("Sales Forecast")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.legend()
plt.grid(True)
plt.show()

print("\nSales Forecasting Completed Successfully!")