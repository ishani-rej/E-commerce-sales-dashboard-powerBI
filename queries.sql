-- Total Revenue
SELECT SUM(payment_value) AS Total_Revenue
FROM merged_ecommerce_data;

-- Top 10 Customers
SELECT customer_unique_id,
SUM(payment_value) AS Revenue
FROM merged_ecommerce_data
GROUP BY customer_unique_id
ORDER BY Revenue DESC
LIMIT 10;

-- Top Product Categories
SELECT product_category_name,
COUNT(*) AS Orders
FROM merged_ecommerce_data
GROUP BY product_category_name
ORDER BY Orders DESC
LIMIT 10;

-- Payment Type Analysis
SELECT payment_type,
COUNT(*) AS Total
FROM merged_ecommerce_data
GROUP BY payment_type;

-- Monthly Sales
SELECT strftime('%Y-%m', order_purchase_timestamp) AS Month,
SUM(payment_value) AS Revenue
FROM merged_ecommerce_data
GROUP BY Month
ORDER BY Month;

SELECT COUNT(*)
FROM merged_ecommerce_data