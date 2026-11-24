# Duka Electronics Sales Exploration & Mobile Money Agent Network Cleanup

End-to-end data exploration, quality auditing, cleaning pipeline development, and automated executive reporting using **Python (`pandas`, `numpy`, `openpyxl`)**.

---

## Repository Structure

```text
plp-da-a3-duka-sales-and-agent-cleanup/
├── duka_sales_exploration.ipynb         # Engagement 1: Duka Electronics H1 2026 sales exploration
├── agent_cleanup_and_reporting.ipynb    # Engagement 2: Agent transaction audit, cleaning & reporting
├── outputs/
│   ├── agent_cleaned.csv                # 580 deduplicated, standardized transactions with quality flags
│   └── agent_summary.csv                # County & transaction-type executive summary table
├── excel/
│   └── agent_network_report.xlsx        # Formatted multi-sheet Excel report with live formulas
├── generate_data.py                     # Reproducible dataset generator (seeds 42 & 44)
├── requirements.txt                     # Python dependencies
└── README.md

cat << 'EOF' > README.md
# Duka Electronics Sales Exploration & Mobile Money Agent Network Cleanup

End-to-end data exploration, quality auditing, cleaning pipeline development, and automated executive reporting using **Python (`pandas`, `numpy`, `openpyxl`)**.

---

## Repository Structure

```text
plp-da-a3-duka-sales-and-agent-cleanup/
├── duka_sales_exploration.ipynb         # Engagement 1: Duka Electronics H1 2026 sales exploration
├── agent_cleanup_and_reporting.ipynb    # Engagement 2: Agent transaction audit, cleaning & reporting
├── outputs/
│   ├── agent_cleaned.csv                # 580 deduplicated, standardized transactions with quality flags
│   └── agent_summary.csv                # County & transaction-type executive summary table
├── excel/
│   └── agent_network_report.xlsx        # Formatted multi-sheet Excel report with live formulas
├── generate_data.py                     # Reproducible dataset generator (seeds 42 & 44)
├── requirements.txt                     # Python dependencies
└── README.md
```

---

## Engagement 1: Duka Electronics — Half-Year Sales Exploration

Analyzed **1,000 sales orders** (`2026-01-01` to `2026-06-29`, seed `42`) across five Kenyan branches and three sales channels.

### Key Findings
* **Overall Revenue & Volume:** **1,000 orders** totaling **KES 71,792,500** with zero missing values.
* **Branch Performance:** **Nairobi** ranks #1 in both revenue (**KES 26,106,100**, 36.36% share) and order count (376 orders), followed in identical rank order by Mombasa, Nakuru, Kisumu, and Eldoret.
* **Product Mix:** **Laptops** lead total revenue (**KES 41,535,000** across 639 units @ KES 65,000), while **Tablets** lead unit volume (691 units @ KES 28,000 = KES 19,348,000).
* **Seasonality & Day-of-Week:** Revenue peaked in **April 2026 (KES 13,518,300)** and dipped in **June 2026 (KES 10,903,400)**—a **23.98%** difference—while average order value remained virtually identical on weekdays (**KES 71,724**) and weekends (**KES 71,972**).
* **Channel Breakdown:** **In-store** drives 57.07% of revenue (**KES 40,969,200**), while **Phone orders** achieve the highest average order value (**KES 79,576**).

---

## Engagement 2: Mobile Money Agent Network — Data Audit, Cleaning & Reporting

Audited and cleaned **612 raw transactions** (`seed 44`) joined against a 20-agent master registry (`AG001`–`AG020`).

### Pre-Clean Audit vs. Post-Clean Results
| Data Quality Issue | Pre-Clean Count | Cleaning Action Applied |
| :--- | :---: | :--- |
| Duplicate transactions | 12 duplicate `txn_id`s (11 exact rows + 1 mutated `agent_id`) | Deduplicated on `txn_id`, prioritizing valid `agent_id` records |
| Missing `amount` values | 22 (`15` blank/`NaN` + `7` literal `"N/A"`) | Coerced to numeric and dropped rows lacking valid amounts |
| Extreme outlier amounts | 5 rows (`KES 250,000`) | Preserved and flagged via `is_outlier_amount = True` |
| Mixed date formats | 5 slash-formatted dates (`YYYY/MM/DD`) | Standardized all dates to `datetime64[ns]` (`YYYY-MM-DD`) |
| Unregistered agent IDs | 8 rows assigned to `AG099` | Flagged via `is_valid_agent = False` and mapped to `county = "Unknown"` |
| Inconsistent `txn_type` casing | 5 variants (`deposit`, `DEPOSIT `, `withdrawal`, etc.) | Stripped whitespace and standardized to `Deposit` / `Withdrawal` |

### Summary Metrics (580 Valid-Amount Transactions)
* **Gross Network Volume:** **KES 2,654,897** across **580 transactions** (360 Deposits = **KES 1,650,808**; 220 Withdrawals = **KES 1,004,089**).
* **Clean Non-Outlier Volume:** **KES 1,404,897** across **575 normal transactions** (excluding the five `KES 250,000` anomalies totaling KES 1,250,000).
* **Top County:** **Nairobi** leads with **172 transactions** totaling **KES 691,414** gross (**KES 441,414** excluding 1 outlier).

---

## How to Reproduce

```bash
pip install -r requirements.txt
python generate_data.py
```
Open either `.ipynb` notebook in Jupyter or Google Colab and run all cells from top to bottom.
