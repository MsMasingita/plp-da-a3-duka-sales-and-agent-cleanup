# Duka Electronics Sales Exploration & Mobile Money Agent Network Cleanup

End-to-end data exploration, quality auditing, modular cleaning pipeline development, and automated Excel reporting using **Python (`pandas`, `numpy`, `openpyxl`)**.

---

## Repository Structure

- `duka_sales_exploration.ipynb` — Engagement 1: Duka Electronics H1 2026 sales exploration, Coast & Capital filtering, and 5-sentence bullet executive summary
- `agent_cleanup_and_reporting.ipynb` — Engagement 2: Mobile money data quality audit, `cleaning_pipeline` integration, cleaning log, reporting, and data privacy review
- `cleaning_pipeline.py` — Reusable cleaning module exposing `clean_agent_data(txns, agents) -> (df_clean, cleaning_log)`
- `generate_data.py` — Reproducible dataset generator (seeds `2026` and `44`)
- `requirements.txt` — Python dependencies (`numpy`, `pandas`, `openpyxl`)
- `premium_online_coast_capital.csv` — Filtered Premium Online orders for Nairobi and Mombasa (83 rows)
- `agent_transactions_clean.csv` — Final cleaned mobile money agent transactions (580 rows)
- `duka_branch_summary.xlsx` — Dynamic Excel branch report featuring `SUMIFS`, `COUNTIFS`, `XLOOKUP`, and a Branch x Product Pivot summary
- `outputs/premium_online_coast_capital.csv` — Filtered Premium Online orders for Nairobi and Mombasa
- `outputs/agent_transactions_clean.csv` — Final cleaned mobile money agent transactions
- `outputs/agent_cleaned.csv` — Cleaned transactions dataset with audit flags
- `outputs/agent_summary.csv` — County and transaction-type summary table
- `excel/duka_branch_summary.xlsx` — Duka Electronics Excel report (`SUMIFS`, `COUNTIFS`, `XLOOKUP`, and Pivot summary)
- `excel/agent_network_report.xlsx` — Formatted Mobile Money executive summary and cleaned transaction ledger

---

## Engagement 1: Duka Electronics — Half-Year Sales Exploration

Analyzed **1,000 sales orders** (`2026-01-01` to `2026-06-29`, seed `2026`) across five Kenyan branches and three sales channels.

### Key Findings
- **Overall Revenue & Volume:** **1,000 orders** totaling **KES 71,792,500** with zero missing values.
- **Branch Performance:** **Nairobi** ranks #1 in both revenue (**KES 26,106,100**, 36.36% share) and order count (376 orders), followed in identical rank order by Mombasa, Nakuru, Kisumu, and Eldoret.
- **Product Mix:** **Laptops** lead total revenue (**KES 41,535,000** across 639 units @ KES 65,000), while **Tablets** lead unit volume (691 units @ KES 28,000 = KES 19,348,000).
- **Seasonality & Day-of-Week:** Revenue peaked in **April 2026 (KES 13,518,300)** and dipped in **June 2026 (KES 10,903,400)**—a **23.98%** difference—while average order value remained virtually identical on weekdays (**KES 71,724**) and weekends (**KES 71,972**).
- **Channel & Segment Deliverables:** **In-store** drives 57.07% of revenue (**KES 40,969,200**), while filtering for **Premium** (`unit_price >= 28,000`) **Online** orders in **Nairobi** and **Mombasa** yielded **83** high-value orders exported to `premium_online_coast_capital.csv` alongside `duka_branch_summary.xlsx`.

---

## Engagement 2: Mobile Money Agent Network — Data Audit, Cleaning & Reporting

Audited and cleaned **612 raw transactions** (`seed 44`) joined against a 20-agent master registry (`AG001`–`AG020`) via the modular `clean_agent_data(txns, agents)` function in `cleaning_pipeline.py`.

### Pre-Clean Audit vs. Post-Clean Results
| Data Quality Issue | Pre-Clean / Pipeline Count | Cleaning Action Applied |
| :--- | :---: | :--- |
| Duplicate transactions | 12 duplicate `txn_id`s | Deduplicated on `txn_id`, prioritizing valid registered `agent_id` records |
| Missing / non-numeric `amount` | 20 rows (after deduplication) | Coerced to numeric and dropped rows lacking valid amounts |
| Extreme outlier amounts | 5 rows (`KES 250,000`) | Preserved and flagged via `is_outlier_amount = True` |
| Mixed date formats | 5 slash-formatted dates (`YYYY/MM/DD`) | Standardized all dates to `datetime64[ns]` (`YYYY-MM-DD`) |
| Unregistered agent IDs | 7 rows assigned to `AG099` (post-dedup) | Flagged via `is_valid_agent = False` and mapped to `county = "Unknown"` |
| Inconsistent `txn_type` casing | 5 variants (`deposit`, `DEPOSIT `, `withdrawal`, etc.) | Stripped whitespace and standardized to `Deposit` / `Withdrawal` |

### Summary Metrics (580 Valid-Amount Transactions)
- **Gross Network Volume:** **KES 2,654,897** across **580 transactions** (360 Deposits = **KES 1,650,808**; 220 Withdrawals = **KES 1,004,089**).
- **Clean Non-Outlier Volume:** **KES 1,404,897** across **575 normal transactions** (excluding the five `KES 250,000` anomalies totaling KES 1,250,000).
- **Top County:** **Nairobi** leads with **172 transactions** totaling **KES 691,414** gross (**KES 441,414** excluding 1 outlier).

---

## How to Reproduce

1. Install dependencies: `pip install -r requirements.txt`
2. Generate raw datasets: `python generate_data.py`
3. Open either `.ipynb` notebook in Jupyter or Google Colab and run all cells from top to bottom.
