"""Analyze synthetic supply-chain data with SQLite (standard library only)."""
import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA, OUT = ROOT / "data", ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def load(conn, name):
    with (DATA / f"{name}.csv").open(newline="") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames
        rows = list(reader)
    conn.execute(f"CREATE TABLE {name} (" + ", ".join(f"{c} TEXT" for c in columns) + ")")
    placeholders = ",".join("?" for _ in columns)
    conn.executemany(f"INSERT INTO {name} VALUES ({placeholders})",
                     [tuple(row[c] for c in columns) for row in rows])

def export(conn, query, filename):
    cursor = conn.execute(query)
    records = cursor.fetchall()
    with (OUT / filename).open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([col[0] for col in cursor.description])
        writer.writerows(records)
    return records

inventory_sql = """
WITH sold AS (
  SELECT sku, SUM(CAST(units_sold AS INTEGER)) units_sold,
         ROUND(SUM(CAST(units_sold AS REAL))/180,2) avg_daily_demand
  FROM sales GROUP BY sku
), received AS (
  SELECT sku, SUM(CAST(units_received AS INTEGER)) units_received
  FROM purchase_orders WHERE actual_delivery <= '2025-06-29' GROUP BY sku
), inventory AS (
  SELECT p.*, s.supplier_name,
         COALESCE(sold.units_sold,0) units_sold,
         COALESCE(sold.avg_daily_demand,0) avg_daily_demand,
         800 + COALESCE(received.units_received,0) - COALESCE(sold.units_sold,0) estimated_ending_stock
  FROM products p JOIN suppliers s ON p.supplier_id=s.supplier_id
  LEFT JOIN sold ON p.sku=sold.sku
  LEFT JOIN received ON p.sku=received.sku
)
SELECT sku, product_name, category, supplier_name, units_sold, avg_daily_demand,
       estimated_ending_stock, reorder_point,
       ROUND(estimated_ending_stock * CAST(unit_cost AS REAL),2) estimated_inventory_value,
       CASE WHEN estimated_ending_stock <= CAST(reorder_point AS INTEGER)
            THEN 'REORDER' ELSE 'OK' END reorder_flag
FROM inventory ORDER BY estimated_ending_stock ASC
"""
supplier_sql = """
SELECT s.supplier_name, COUNT(*) total_orders,
       SUM(CASE WHEN po.actual_delivery > po.expected_delivery THEN 1 ELSE 0 END) late_orders,
       ROUND(100.0*AVG(CASE WHEN po.actual_delivery <= po.expected_delivery THEN 1.0 ELSE 0.0 END),1) on_time_pct,
       ROUND(AVG(julianday(po.actual_delivery)-julianday(po.expected_delivery)),2) avg_days_vs_plan
FROM purchase_orders po JOIN suppliers s ON po.supplier_id=s.supplier_id
GROUP BY s.supplier_name ORDER BY on_time_pct ASC
"""
with sqlite3.connect(":memory:") as conn:
    for table in ("products", "suppliers", "sales", "purchase_orders"):
        load(conn, table)
    rows = export(conn, inventory_sql, "inventory_kpis.csv")
    export(conn, supplier_sql, "supplier_performance.csv")
    print("SKUs analyzed:", len(rows))
    print("SKUs flagged for reorder:", sum(row[-1] == "REORDER" for row in rows))
    print("Estimated ending inventory value: ${:,.2f}".format(sum(float(row[-2]) for row in rows)))
    print("Outputs saved to outputs/")
