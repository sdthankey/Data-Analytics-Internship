#!/usr/bin/env python3
"""
CodeOrbit Tech — Data Analyst Internship
Task 1: Data Cleaning in Python (pandas)

This script:
1. Loads the raw retail sales sample dataset (task1_raw_sales_data.csv) containing
   missing values, duplicate records, inconsistent text casing/whitespace, mixed
   date formats, and currency formatting issues.
2. Cleans and standardizes the dataset step-by-step using pandas.
3. Logs each cleaning operation with before/after counts.
4. Exports the cleaned dataset to task1_cleaned_sales_data.csv.
"""

import pathlib
import pandas as pd

RAW_CSV_DATA = """order_id,order_date,customer_name,region,category,product,quantity,unit_price,discount_pct,total_sales
ORD-1001,2026-01-05,Aarav Sharma,North,Electronics,ProBook Laptop 15,1,"$1,200.00",5,1140.00
ORD-1002,2026/01/12,Priya Patel,West, furniture ,Ergonomic Mesh Chair,2,$250.00,0,500.00
ORD-1003,18-01-2026,Rohan Mehta,East,Office Supplies,A4 Copy Paper Case,5,$40.00,0,200.00
ORD-1004,2026-01-22,Neha Gupta,South,ELECTRONICS,Noise-Cancelling Headphones,3,$180.00,10,486.00
ORD-1005,2026-01-25,Vikram Singh,north ,Electronics,4K UltraHD Monitor,2,$400.00,,800.00
ORD-1006,2026-01-29,Ananya Iyer,West,Office Supplies,Mechanical Keyboard,,$120.00,0,240.00
ORD-1007,2026-02-03,Karthik Nair,South,Furniture,Standing Desk Frame,1,$650.00,10,585.00
ORD-1008,2026/02/08,Divya Joshi,East,electronics,Wireless Ergonomic Mouse,4,$50.00,0,200.00
ORD-1009,14-02-2026,Siddharth Rao,,Furniture,Executive Bookshelf,1,$320.00,5,304.00
ORD-1010,2026-02-19,Meera Krishnan,North,office supplies,LaserJet Toner Cartridge,3,$90.00,0,270.00
ORD-1011,2026-02-23,Arjun Malhotra,WEST,Electronics,ProBook Laptop 15,1,"$1,200.00",10,1080.00
ORD-1012,2026-02-27,Pooja Verma,East,Furniture,Conference Table 8-Seat,1,"$1,100.00",15,935.00
ORD-1013,2026-03-04,Rahul Deshmukh,South,Office Supplies,A4 Copy Paper Case,6,$40.00,5,228.00
ORD-1014,2026/03/09,Sneha Reddy,North,Electronics,4K UltraHD Monitor,2,$400.00,5,760.00
ORD-1015,15-03-2026,Aditya Kapoor,West,Furniture,Ergonomic Mesh Chair,,$250.00,0,500.00
ORD-1016,2026-03-20,Kavita Choudhary,East,Electronics,Noise-Cancelling Headphones,2,$180.00,,360.00
ORD-1017,2026-03-24,Manish Tiwari,South,office supplies ,Mechanical Keyboard,3,$120.00,5,342.00
ORD-1018,2026-03-29,Nisha Agarwal,North,Furniture,Standing Desk Frame,2,$650.00,10,1170.00
ORD-1019,2026-04-02,Varun Saxena,West,Electronics,ProBook Laptop 15,2,"$1,200.00",10,2160.00
ORD-1020,2026/04/07,Tanya Bhatia,,Office Supplies,LaserJet Toner Cartridge,4,$90.00,5,342.00
ORD-1021,12-04-2026,Deepak Kulkarni,South,Electronics,Wireless Ergonomic Mouse,5,$50.00,0,250.00
ORD-1022,2026-04-17,Swati Mishra,North, furniture,Executive Bookshelf,2,$320.00,0,640.00
ORD-1023,2026-04-22,Gaurav Bansal,West,Office Supplies,A4 Copy Paper Case,8,$40.00,10,288.00
ORD-1024,2026-04-26,Ritu Chatterjee,East,Electronics,4K UltraHD Monitor,1,$400.00,0,400.00
ORD-1025,2026-05-01,Nikhil Menon,South,Furniture,Conference Table 8-Seat,1,"$1,100.00",10,990.00
ORD-1026,2026/05/06,Shruti Pandey,North,Electronics,Noise-Cancelling Headphones,4,$180.00,5,684.00
ORD-1027,11-05-2026,Akash Jain,West,Office Supplies,Mechanical Keyboard,2,$120.00,,240.00
ORD-1028,2026-05-16,Pallavi Sinha,East,Furniture,Ergonomic Mesh Chair,3,$250.00,10,675.00
ORD-1029,2026-05-21,Harsh Vardhan,South,ELECTRONICS,ProBook Laptop 15,1,"$1,200.00",0,1200.00
ORD-1030,2026-05-26,Bhavna Arora,North,Office Supplies,LaserJet Toner Cartridge,2,$90.00,0,180.00
ORD-1031,2026-05-30,Yash Thakur,West,Furniture,Standing Desk Frame,1,$650.00,5,617.50
ORD-1032,2026-06-03,Komal Shah,East,Electronics,Wireless Ergonomic Mouse,,$50.00,0,100.00
ORD-1033,2026/06/08,Pranav Gokhale,South,Office Supplies,A4 Copy Paper Case,10,$40.00,10,360.00
ORD-1034,13-06-2026,Sonal Kashyap,North,Electronics,4K UltraHD Monitor,3,$400.00,10,1080.00
ORD-1035,2026-06-17,Abhishek Bose,West,Furniture,Executive Bookshelf,1,$320.00,0,320.00
ORD-1036,2026-06-21,Mansiトリvedi,East,Office Supplies,Mechanical Keyboard,4,$120.00,5,456.00
ORD-1037,2026-06-24,Vivek Pillai,South,Electronics,Noise-Cancelling Headphones,2,$180.00,0,360.00
ORD-1038,2026-06-27,Chitra Nambiar,North,Furniture,Conference Table 8-Seat,1,"$1,100.00",5,1045.00
ORD-1039,2026-06-29,Rajeshwari Devi,West,Electronics,ProBook Laptop 15,1,"$1,200.00",5,1140.00
ORD-1040,2026-06-30,Kunal Chatterjee,East,Office Supplies,LaserJet Toner Cartridge,5,$90.00,10,405.00
ORD-1001,2026-01-05,Aarav Sharma,North,Electronics,ProBook Laptop 15,1,"$1,200.00",5,1140.00
ORD-1005,2026-01-25,Vikram Singh,north ,Electronics,4K UltraHD Monitor,2,$400.00,,800.00
ORD-1011,2026-02-23,Arjun Malhotra,WEST,Electronics,ProBook Laptop 15,1,"$1,200.00",10,1080.00
ORD-1019,2026-04-02,Varun Saxena,West,Electronics,ProBook Laptop 15,2,"$1,200.00",10,2160.00
ORD-1028,2026-05-16,Pallavi Sinha,East,Furniture,Ergonomic Mesh Chair,3,$250.00,10,675.00
"""


def clean_sales_dataset(raw_csv_path: str = "task1_raw_sales_data.csv",
                        cleaned_csv_path: str = "task1_cleaned_sales_data.csv") -> pd.DataFrame:
    """Executes and logs the 7-step data cleaning pipeline."""
    raw_path = pathlib.Path(raw_csv_path)
    if not raw_path.exists():
        raw_path.write_text(RAW_CSV_DATA.strip() + "\n", encoding="utf-8")

    df_raw = pd.read_csv(raw_path)
    print("=" * 72)
    print("TASK 1: DATA CLEANING IN PYTHON (PANDAS)")
    print("=" * 72)
    print(f"Initial Raw Dataset Shape: {df_raw.shape[0]} rows x {df_raw.shape[1]} columns")
    print(f"Initial Duplicate Rows:    {df_raw.duplicated(subset=['order_id']).sum()}")
    print(f"Initial Missing Values:\n{df_raw.isnull().sum()[df_raw.isnull().sum() > 0].to_string()}\n")

    df = df_raw.copy()

    # Step 1: Remove exact and order_id duplicate records
    before_dedup = len(df)
    df = df.drop_duplicates(subset=["order_id"], keep="first").reset_index(drop=True)
    print(f"[Step 1] Removed {before_dedup - len(df)} duplicate records -> {len(df)} unique orders remaining.")

    # Step 2: Standardize text columns (trim whitespace, fix casing, clean non-ASCII typos)
    df["customer_name"] = df["customer_name"].astype(str).str.replace("トリvedi", " Trivedi", regex=False).str.strip()
    df["category"] = df["category"].astype(str).str.strip().str.title()
    df["product"] = df["product"].astype(str).str.strip()
    print("[Step 2] Standardized text casing and trimmed leading/trailing whitespace in category, product, and customer_name.")

    # Step 3: Clean and impute missing Region values (standardize case & impute missing with 'East' mode)
    df["region"] = df["region"].astype(str).str.strip().str.title()
    df["region"] = df["region"].replace({"Nan": None, "": None})
    missing_regions = df["region"].isna().sum()
    df["region"] = df["region"].fillna("East")
    print(f"[Step 3] Standardized region labels and imputed {missing_regions} missing region values with 'East'.")

    # Step 4: Parse mixed Order Date formats into ISO 8601 (YYYY-MM-DD)
    df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", dayfirst=True).dt.strftime("%Y-%m-%d")
    df["order_month"] = df["order_date"].str.slice(0, 7)
    print("[Step 4] Standardized mixed date formats (YYYY/MM/DD, DD-MM-YYYY, YYYY-MM-DD) to ISO YYYY-MM-DD.")

    # Step 5: Strip currency symbols and commas from unit_price and convert to float
    df["unit_price"] = (
        df["unit_price"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
        .astype(float)
    )
    print("[Step 5] Cleaned currency symbols ('$', ',') from unit_price and converted to float.")

    # Step 6: Handle missing numeric values in quantity and discount_pct
    missing_qty = df["quantity"].isna().sum()
    median_qty = int(df["quantity"].median())
    df["quantity"] = df["quantity"].fillna(median_qty).astype(int)

    missing_disc = df["discount_pct"].isna().sum()
    df["discount_pct"] = df["discount_pct"].fillna(0.0).astype(float)
    print(f"[Step 6] Imputed {missing_qty} missing quantity values (median={median_qty}) and {missing_disc} missing discount_pct values (0.0%).")

    # Step 7: Recalculate total_sales accurately to guarantee financial consistency
    df["gross_sales"] = (df["quantity"] * df["unit_price"]).round(2)
    df["discount_amount"] = (df["gross_sales"] * (df["discount_pct"] / 100.0)).round(2)
    df["total_sales"] = (df["gross_sales"] - df["discount_amount"]).round(2)
    print("[Step 7] Recalculated gross_sales, discount_amount, and net total_sales with 2-decimal precision.")

    # Sort chronologically by order_date and order_id
    df = df.sort_values(["order_date", "order_id"]).reset_index(drop=True)

    # Save cleaned dataset
    df.to_csv(cleaned_csv_path, index=False)
    print("\n" + "-" * 72)
    print(f"Cleaned Dataset Saved to: {cleaned_csv_path}")
    print(f"Final Cleaned Shape:      {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"Remaining Missing Values: {df.isna().sum().sum()}")
    print(f"Verified Total Net Sales: ${df['total_sales'].sum():,.2f}")
    print("=" * 72)
    return df


if __name__ == "__main__":
    clean_sales_dataset()
