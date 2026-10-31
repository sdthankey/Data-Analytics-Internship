# CodeOrbit Tech — Data Analyst Internship: Tasks 1, 2 & 3 Complete Report & Submission Guide

Prepared for the [CodeOrbit Tech Data Analytics Internship](https://codeorbittech.in/internships/16) (1-Month Track — 3 Tasks). Methodology and schema conventions follow industry retail analytics benchmarks from the [Kaggle Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final), [Kaggle Sample Sales Data](https://www.kaggle.com/datasets/kyanyoga/sample-sales-data), and the [Python Sales Data Analysis Guide](https://medium.com/@gaurigiri777/python-data-analyst-project-for-beginners-sales-data-analysis-real-life-example-9e85c5fb0ff1).

## Executive Overview of Completed Deliverables

| Internship Task | Deliverable Files | Core Tools Used | Key Outcome | 
| ----- | ----- | ----- | ----- | 
| **Task 1: Data Cleaning in Excel/Python** | `task1_data_cleaning.py`, `task1_raw_sales_data.csv`, `task1_cleaned_sales_data.csv`, `task1_data_cleaning.xlsx` | Python (`pandas`) & Microsoft Excel (`.xlsx`) | Cleaned 45 raw records into 40 unique orders, resolved 8 missing values, standardized dates/text/currency, and verified `$24,032.50` in net sales | 
| **Task 2: Sales Data Analysis with Pandas** | `task2_sales_analysis.py`, `task2_sales_analysis_report.md` | Python (`pandas`) | Calculated core KPIs (`$600.81` AOV, `108` units sold) and grouped performance by Category, Region, Month, and Product | 
| **Task 3: Dashboard Creation Using Excel** | `task3_sales_dashboard.xlsx` | Microsoft Excel (`COUNTIF`, `SUMIF`, Native Charts) | Built a 2-sheet interactive dashboard with a 6-metric KPI scorecard, 4 summary tables, and 3 native charts | 

## Task 1: Data Cleaning in Python (pandas) & Excel

### 1. Dataset Overview & Initial Data Quality Audit

The raw dataset (`task1_raw_sales_data.csv`) contains **45 rows and 10 columns** capturing retail orders across Q1–Q2 2026 (`2026-01-05` to `2026-06-30`). Before analysis, an automated audit in `task1_data_cleaning.py` identified four categories of data quality defects modeled after standard [Retail Sales Analytics Reference Repository](https://github.com/siddeshr007/Retail-sales-analytics) pipelines:

* **Duplicate Records:** 5 exact duplicate rows (`ORD-1001`, `ORD-1005`, `ORD-1011`, `ORD-1019`, `ORD-1028`) caused by repeated batch ingestion.

* **Missing Values:** 2 missing `region` entries (`ORD-1009`, `ORD-1020`), 3 missing `quantity` entries (`ORD-1006`, `ORD-1015`, `ORD-1032`), and 3 missing `discount_pct` entries (`ORD-1005`, `ORD-1016`, `ORD-1027`) among unique orders.

* **Inconsistent Text & Character Formatting:** Leading/trailing whitespace and mixed casing in `category` (`" furniture "`, `"ELECTRONICS"`, `"office supplies "`) and `region` (`"north "`, `"WEST"`), plus a non-ASCII character typo in `customer_name` (`"Mansiトリvedi"`).

* **Mixed Date & Currency Formats:** Dates stored in three incompatible formats (`YYYY-MM-DD`, `YYYY/MM/DD`, and `DD-MM-YYYY`), and `unit_price` stored as text strings with currency symbols and thousands separators (`"$1,200.00"`).

### 2. Step-by-Step Cleaning Pipeline Log

| Step ID | Cleaning Rule Applied | Target Column(s) | Issue Identified in Raw Data | Action Taken in Python (`pandas`) & Excel | Records Fixed | 
| ----- | ----- | ----- | ----- | ----- | ----- | 
| **STEP-01** | Deduplication | `order_id` (All Columns) | 5 duplicate order rows (`ORD-1001`, `1005`, `1011`, `1019`, `1028`) | Removed duplicate `order_id` rows via `df.drop_duplicates(subset=["order_id"], keep="first")` | 5 | 
| **STEP-02** | Text Standardization | `category`, `product`, `customer_name` | Leading/trailing whitespace, mixed casing (`" furniture "`, `"ELECTRONICS"`), non-ASCII typo | Trimmed whitespace via `.str.strip()`, applied `.str.title()`, and fixed `"Mansi Trivedi"` | 11 | 
| **STEP-03** | Missing Region Imputation | `region` | 2 missing region entries (`ORD-1009`, `ORD-1020`) and mixed casing (`"north "`, `"WEST"`) | Standardized Title Case and imputed missing values with the modal region (`"East"`) | 4 | 
| **STEP-04** | Date Format Normalization | `order_date`, `order_month` | Mixed date strings (`YYYY/MM/DD`, `DD-MM-YYYY`, `YYYY-MM-DD`) | Parsed via `pd.to_datetime(..., format="mixed", dayfirst=True)` into ISO `YYYY-MM-DD` and derived `YYYY-MM` | 12 | 
| **STEP-05** | Currency String Parsing | `unit_price` | Currency symbols and commas stored as text (`"$1,200.00"`, `"$250.00"`) | Stripped `"$"` and `","` characters and cast to `float64` | 40 | 
| **STEP-06** | Numeric Imputation | `quantity`, `discount_pct` | 3 missing quantities (`ORD-1006`, `1015`, `1032`) and 3 missing discount percentages | Imputed missing `quantity` with median (`2`) and missing `discount_pct` with `0.0%` | 6 | 
| **STEP-07** | Financial Recalculation | `gross_sales`, `discount_amount`, `total_sales` | Potential manual calculation drift after numeric imputation | Recalculated `gross_sales = quantity * unit_price` and `total_sales = gross_sales * (1 - discount_pct / 100)` | 40 | 

### 3. Before vs. After Data Quality Summary

| Metric | Raw Dataset (`task1_raw_sales_data.csv`) | Cleaned Dataset (`task1_cleaned_sales_data.csv`) | 
| ----- | ----- | ----- | 
| **Total Row Count** | 45 | 40 | 
| **Unique Order IDs** | 40 | 40 | 
| **Duplicate Rows** | 5 | 0 | 
| **Total Missing Cells** | 9 (raw) / 8 (unique) | 0 | 
| **Date Format Consistency** | 3 mixed formats | 100% ISO `YYYY-MM-DD` | 
| **Verified Gross Sales** | Unverified text/float mix | `$25,600.00` | 
| **Verified Total Discounts** | Incomplete (`NaN` cells) | `$1,567.50` | 
| **Verified Net Sales Revenue** | `$27,967.50` (inflated by duplicates) | `$24,032.50` | 

## Task 2: Sales Data Analysis with Pandas

### 1. Executive KPI Scorecard

Running `task2_sales_analysis.py` on the 40 validated orders produces the following headline performance indicators:

* **Total Net Sales Revenue:** `$24,032.50` (from `$25,600.00` Gross Sales less `$1,567.50` in promotional discounts, representing an effective discount rate of `6.12%`).

* **Total Completed Orders:** `40` unique orders across 6 months (`2026-01` through `2026-06`).

* **Total Units Sold:** `108` units (`2.70` average units per order).

* **Average Order Value (AOV):** `$600.81` per order.

* **Top Revenue-Generating Product:** `ProBook Laptop 15` (`$6,720.00` net sales across 5 orders / 6 units, representing `27.96%` of company revenue).

* **Top Volume Product:** `A4 Copy Paper Case` (`29` units sold across 4 orders, generating `$1,076.00`).

### 2. Sales Performance by Product Category

| Category | Orders | Units Sold | Net Sales (\$) | Average Order Value (\$) | Revenue Share (%) | 
| ----- | ----- | ----- | ----- | ----- | ----- | 
| **Electronics** | 16 | 36 | `$12,200.00` | `$762.50` | `50.76%` | 
| **Furniture** | 12 | 18 | `$8,281.50` | `$690.13` | `34.46%` | 
| **Office Supplies** | 12 | 54 | `$3,551.00` | `$295.92` | `14.78%` | 
| **Total / Overall** | **40** | **108** | **`$24,032.50`** | **`$600.81`** | **`100.00%`** | 

**Category Insights:**

* **Electronics Drives Majority Revenue:** Electronics generates more than half of total revenue (`50.76%`, `$12,200.00`) and commands the highest AOV (`$762.50`), led by high-ticket laptops and 4K monitors.

* **Office Supplies Drives Unit Volume:** Office Supplies accounts for exactly `50.00%` of total units sold (`54` of `108` units) but only `14.78%` of revenue due to lower unit price points (`$40.00`–`$120.00`).

* **Furniture Provides High-Ticket Stability:** Furniture achieves a strong `$690.13` AOV across 12 orders (`$8,281.50`), anchored by 8-seat conference tables and standing desk frames.

### 3. Sales Performance by Geographical Region

| Region | Orders | Units Sold | Net Sales (\$) | Average Order Value (\$) | Revenue Share (%) | 
| ----- | ----- | ----- | ----- | ----- | ----- | 
| **North** | 10 | 22 | `$7,769.00` | `$776.90` | `32.33%` | 
| **West** | 10 | 22 | `$7,085.50` | `$708.55` | `29.48%` | 
| **South** | 9 | 32 | `$4,801.00` | `$533.44` | `19.98%` | 
| **East** | 11 | 32 | `$4,377.00` | `$397.91` | `18.21%` | 
| **Total / Overall** | **40** | **108** | **`$24,032.50`** | **`$600.81`** | **`100.00%`** | 

**Regional Insights:**

* **North and West Lead Revenue Efficiency:** North (`$7,769.00`, `32.33%`) and West (`$7,085.50`, `29.48%`) together generate `61.81%` of total sales despite accounting for only half of the orders (`20` of `40`), driven by enterprise hardware and furniture purchases.

* **East and South Have High Unit Volume but Lower AOV:** East (`11` orders, `32` units) and South (`9` orders, `32` units) move more physical units than North or West (`32` vs. `22` units each) but skew toward lower-priced accessories and consumables (`$397.91` and `$533.44` AOV).

### 4. Sales Performance by Time Period (Monthly Trend, Q1–Q2 2026)

| Order Month | Orders | Units Sold | Net Sales (\$) | Average Order Value (\$) | MoM Revenue Growth (%) | 
| ----- | ----- | ----- | ----- | ----- | ----- | 
| **2026-01** | 6 | 15 | `$3,366.00` | `$561.00` | `0.00%` | 
| **2026-02** | 6 | 11 | `$3,374.00` | `$562.33` | `+0.24%` | 
| **2026-03** | 6 | 17 | `$3,360.00` | `$560.00` | `-0.41%` | 
| **2026-04** | 6 | 22 | `$4,080.00` | `$680.00` | `+21.43%` | 
| **2026-05** | 7 | 14 | `$4,586.50` | `$655.21` | `+12.41%` | 
| **2026-06** | 9 | 29 | `$5,266.00` | `$585.11` | `+14.82%` | 
| **Total / Overall** | **40** | **108** | **`$24,032.50`** | **`$600.81`** | **`+56.45%` (Jan to Jun)** | 

**Time-Series Insights:**

* **Q2 Acceleration (+37.93% over Q1):** After steady Q1 revenue (`$10,100.00` across Jan–Mar, averaging `$3,366.67`/month), Q2 revenue surged to `$13,932.50` across Apr–Jun (`+37.95%` quarter-over-quarter).

* **Peak Month in June 2026:** June recorded the highest order volume (`9` orders), highest unit volume (`29` units), and highest monthly net revenue (`$5,266.00`, up `56.45%` compared to January).

### 5. Product-Level Performance Leaderboard

| Rank | Product Name | Category | Orders | Units Sold | Net Sales (\$) | Average Order Value (\$) | Revenue Share (%) | 
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | 
| **1** | **ProBook Laptop 15** | Electronics | 5 | 6 | `$6,720.00` | `$1,344.00` | `27.96%` | 
| **2** | **4K UltraHD Monitor** | Electronics | 4 | 8 | `$3,040.00` | `$760.00` | `12.65%` | 
| **3** | **Conference Table 8-Seat** | Furniture | 3 | 3 | `$2,970.00` | `$990.00` | `12.36%` | 
| **4** | **Standing Desk Frame** | Furniture | 3 | 4 | `$2,372.50` | `$790.83` | `9.87%` | 
| **5** | **Noise-Cancelling Headphones** | Electronics | 4 | 11 | `$1,890.00` | `$472.50` | `7.86%` | 
| **6** | **Ergonomic Mesh Chair** | Furniture | 3 | 7 | `$1,675.00` | `$558.33` | `6.97%` | 
| **7** | **Mechanical Keyboard** | Office Supplies | 4 | 11 | `$1,278.00` | `$319.50` | `5.32%` | 
| **8** | **Executive Bookshelf** | Furniture | 3 | 4 | `$1,264.00` | `$421.33` | `5.26%` | 
| **9** | **LaserJet Toner Cartridge** | Office Supplies | 4 | 14 | `$1,197.00` | `$299.25` | `4.98%` | 
| **10** | **A4 Copy Paper Case** | Office Supplies | 4 | 29 | `$1,076.00` | `$269.00` | `4.48%` | 
| **11** | **Wireless Ergonomic Mouse** | Electronics | 3 | 11 | `$550.00` | `$183.33` | `2.29%` | 

### 6. Strategic Business Recommendations

* **Bundle High-Volume Accessories with Flagship Hardware in East & South:** Since East and South exhibit high order frequency (`20` combined orders) but lower AOV (`$397.91`–`$533.44`), introducing workstation bundles (`ProBook Laptop 15` + `4K UltraHD Monitor` + `Mechanical Keyboard`) can lift regional AOV toward the North/West benchmark (`$708+`).

* **Protect Margin on Top 3 Products:** The top 3 products (`ProBook Laptop 15`, `4K UltraHD Monitor`, and `Conference Table 8-Seat`) generate `52.97%` (`$12,730.00`) of total revenue. Capping promotional discounts at `5%` on single-unit orders for these three SKUs will preserve gross margin without hurting demand.

* **Expand Q2 Corporate Procurement Campaigns into Q3:** The `+37.95%` Q2 revenue expansion was fueled by multi-unit monitor, headphone, and furniture orders between April and June. Maintaining targeted B2B replenishment outreach in Q3 can sustain the `$5,000+/month` run rate.

## Task 3: Dashboard Creation Using Excel (`task3_sales_dashboard.xlsx`)

The Excel dashboard workbook (`task3_sales_dashboard.xlsx`) is structured on best-practice BI layout principles modeled after the [Superstore Sales Dashboard Reference](https://github.com/praveen-kumar-maurya/Superstore-Sales-Dashboard-Power-BI):

* **Sheet 1 (`Sales_Dashboard`):**

  * **Executive KPI Scorecard (`A11:B16`):** Dynamically computes Total Net Sales (`$24,032.50`), Gross Sales (`$25,600.00`), Total Completed Orders (`40`), Total Units Sold (`108`), Average Order Value (`$600.81`), and Average Unit Price (`$388.25`) using live `SUM`, `COUNTA`, and `AVERAGE` references to `Cleaned_Data`.

  * **4 Formula-Driven Summary Tables (`Row 4`):** Side-by-side analytical tables for **Category Performance** (`A4:E8`), **Regional Performance** (`G4:K9`), **Monthly Revenue Trend** (`M4:Q11`), and **Product Leaderboard** (`S4:W16`), calculated dynamically via `COUNTIF` and `SUMIF` formulas.

  * **3 Embedded Native Excel Charts (`Row 19`):**

    1. **Net Sales Revenue by Category (`A19`):** Vertical column chart comparing Electronics (`$12,200.00`), Furniture (`$8,281.50`), and Office Supplies (`$3,551.00`).

    2. **Regional Net Sales Breakdown (`G19`):** Horizontal bar chart ranking North (`$7,769.00`), West (`$7,085.50`), South (`$4,801.00`), and East (`$4,377.00`).

    3. **Monthly Net Sales Trend (`M19`):** Time-series line chart tracking the climb from `$3,366.00` in January 2026 to `$5,266.00` in June 2026.

* **Sheet 2 (`Cleaned_Data`):** Holds all 40 cleaned order records with dynamic line-item formulas (`=H5*I5` for Gross Sales and `=J5*(1-K5)` for Net Sales), column totals, and a category validation chart.

## Submission Guide: GitHub Repositories & LinkedIn Screen Recording

### 1. How to Upload to GitHub for the Submission Form

You can create either **three separate GitHub repositories** (one per task) or **one main repository with three task folders** and paste the folder URLs into your [CodeOrbit Tech Data Analytics Internship](https://codeorbittech.in/internships/16) submission form:

* **Task 1 Link (`GitHub Repository Link – Task 1`):** Upload `task1_data_cleaning.py`, `task1_raw_sales_data.csv`, `task1_cleaned_sales_data.csv`, and `task1_data_cleaning.xlsx` (plus this report renamed to `README.md`).

* **Task 2 Link (`GitHub Repository Link – Task 2`):** Upload `task2_sales_analysis.py`, `task1_cleaned_sales_data.csv`, and `task2_sales_analysis_report.md` (renamed to `README.md`).

* **Task 3 Link (`GitHub Repository Link – Task 3`):** Upload `task3_sales_dashboard.xlsx` and `task2_sales_analysis_report.md` (renamed to `README.md`).

### 2. Ready-to-Use 3-Minute LinkedIn Screen Recording Script

For the final required field on the form (**"Share a link screen recording (2–5 minutes) showing the working of at least one completed project on LinkedIn"**), record your screen (using OBS Studio, Loom, or Windows `Win + Alt + R`) while following these steps:

* **0:00 – 0:30 (Introduction & Task 1 Raw vs. Cleaned Data):** Show `task1_data_cleaning.py` in VS Code or your terminal and run `python task1_data_cleaning.py`. Point out how the script removes 5 duplicate orders, imputes missing values in `region`, `quantity`, and `discount_pct`, normalizes mixed dates to `YYYY-MM-DD`, and cleans currency strings to produce `task1_cleaned_sales_data.csv` (`40` orders, `$24,032.50` net sales).

* **0:30 – 1:30 (Task 2 Pandas Sales Analysis):** Run `python task2_sales_analysis.py` in the terminal. Highlight the printed tables showing `$24,032.50` total net sales, `$600.81` average order value, Electronics leading categories at `50.76%` (`$12,200.00`), North leading regions at `32.33%` (`$7,769.00`), and monthly sales growing `+56.45%` from January to June 2026.

* **1:30 – 2:30 (Task 3 Excel Dashboard Walkthrough):** Open `task3_sales_dashboard.xlsx` in Excel. Click on a few cells in `Sales_Dashboard` to show the live `SUMIF` and `COUNTIF` formulas connected to the `Cleaned_Data` tab, and scroll across the 3 charts (Category Column Chart, Regional Bar Chart, and Monthly Trend Line Chart).

* **2:30 – 3:00 (Wrap-Up):** Show your GitHub repository containing all code, datasets, and reports, thank CodeOrbit Tech for the internship opportunity, upload the video to LinkedIn, and paste the LinkedIn post URL into the form.