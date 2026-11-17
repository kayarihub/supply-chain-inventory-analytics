-- Run after loading the generated CSVs into SQLite tables.
-- Supplier on-time delivery performance
SELECT s.supplier_name, COUNT(*) AS total_orders,
       SUM(CASE WHEN po.actual_delivery > po.expected_delivery THEN 1 ELSE 0 END) AS late_orders,
       ROUND(100.0 * AVG(CASE WHEN po.actual_delivery <= po.expected_delivery THEN 1.0 ELSE 0.0 END), 1) AS on_time_pct
FROM purchase_orders AS po
JOIN suppliers AS s ON po.supplier_id = s.supplier_id
GROUP BY s.supplier_name
ORDER BY on_time_pct ASC;

-- Category demand and gross sales value
SELECT p.category,
       SUM(CAST(s.units_sold AS INTEGER)) AS units_sold,
       ROUND(SUM(CAST(s.units_sold AS REAL) * CAST(p.unit_price AS REAL)), 2) AS gross_sales_value
FROM sales AS s
JOIN products AS p ON s.sku = p.sku
GROUP BY p.category
ORDER BY gross_sales_value DESC;
