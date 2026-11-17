# Supply Chain & Inventory Analytics

A reproducible portfolio project using **Python, SQLite SQL, and synthetic retail distribution data** to analyze inventory replenishment risk and supplier delivery reliability.

## Business questions
- Which SKUs may require replenishment?
- Which suppliers have the lowest on-time delivery rates?
- How much estimated inventory value is held across product categories?
- What limitations should decision-makers consider before acting on the results?

## Data
All data is **synthetic**; no employer or customer records are used. The deterministic generator creates 60 SKUs across five categories, 6 suppliers, 180 days of SKU-level sales (10,800 records), and 360 purchase orders. The observation window is January 1–June 29, 2025. Currency: USD.

## Run locally
Requires Python 3.9+ and **no third-party packages**.

```bash
python src/generate_data.py
python src/analyze.py
```

The generator creates `data/products.csv`, `data/suppliers.csv`, `data/sales.csv`, and `data/purchase_orders.csv`. The analysis writes `outputs/inventory_kpis.csv` and `outputs/supplier_performance.csv`. Generated CSVs are intentionally excluded from Git to keep the project reproducible and lightweight.

## KPI definitions
- **On-time delivery rate:** percentage of orders received on or before the planned delivery date.
- **Average daily demand:** total units sold / 180 days.
- **Estimated ending stock:** assumed initial stock (800 units per SKU) + received units through June 29 − units sold.
- **Reorder flag:** estimated stock at or below the synthetic reorder point.
- **Estimated inventory value:** estimated ending stock × unit cost.

## Important limitations
This is a teaching model, **not a production inventory system**. Initial stock and reorder points are assumed, and generated sales do not enforce physical stock constraints. Negative estimated stock can occur and represents a **reconciliation issue**, not physically negative inventory. Reorder flags are preliminary indicators rather than purchase recommendations. The model does not yet include returns, cancellations, stock counts, safety-stock optimization, or lead-time uncertainty.

## Next steps
Add stock reconciliation, inventory turns, supplier scorecards, lead-time-based reorder points, automated tests, and a Power BI dashboard.

## Skills demonstrated
Python ETL · SQL joins and aggregations · inventory KPIs · supplier performance analysis · reproducible data generation · business communication
