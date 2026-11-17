"""Generate deterministic synthetic retail distribution data (not employer data)."""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = random.Random(42)

def save(name, columns, rows):
    with (DATA / name).open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)

supplier_names = ["Northstar Components", "Blue Ridge Supply", "Summit Wholesale",
                  "Metro Distribution", "Evergreen Goods", "Atlas Sourcing"]
suppliers = [(f"SUP{i:03d}", name) for i, name in enumerate(supplier_names, 1)]
categories = ["Beauty", "Home", "Electronics", "Apparel", "Accessories"]
products = []
for i in range(1, 61):
    category = categories[(i - 1) // 12]
    products.append((f"SKU{i:03d}", f"{category} Item {i:03d}", category,
                     suppliers[(i - 1) % 6][0], round(rng.uniform(8, 95), 2),
                     round(rng.uniform(15, 145), 2), rng.randint(20, 120)))
save("products.csv", ["sku", "product_name", "category", "supplier_id",
                      "unit_cost", "unit_price", "reorder_point"], products)
save("suppliers.csv", ["supplier_id", "supplier_name"], suppliers)

start = date(2025, 1, 1)
sales = []
for day in range(180):
    current = start + timedelta(days=day)
    for j, product in enumerate(products):
        sales.append((current.isoformat(), product[0],
                      max(0, round(rng.gauss(4 + (j % 8), 3)))))
save("sales.csv", ["date", "sku", "units_sold"], sales)

orders = []
for i in range(1, 361):
    product = rng.choice(products)
    ordered = start + timedelta(days=rng.randint(0, 160))
    planned = ordered + timedelta(days=10)
    actual = planned + timedelta(days=rng.choice([-3, -1, 0, 0, 1, 2, 4, 7, 10]))
    quantity = rng.randint(30, 250)
    orders.append((f"PO{i:04d}", product[0], product[3], ordered.isoformat(),
                   planned.isoformat(), actual.isoformat(), quantity, quantity))
save("purchase_orders.csv", ["po_id", "sku", "supplier_id", "order_date",
                              "expected_delivery", "actual_delivery",
                              "units_ordered", "units_received"], orders)
print("Generated 60 products, 6 suppliers, 10,800 sales records and 360 purchase orders.")
