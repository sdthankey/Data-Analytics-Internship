#!/usr/bin/env python3
"""
CodeOrbit Tech — Data Analyst Internship
Task 2: Sales Data Analysis with Pandas

This script:
1. Loads the cleaned retail sales dataset (task1_cleaned_sales_data.csv).
2. Calculates core business KPIs: Total Sales, Total Orders, Total Units Sold,
   Average Order Value (AOV), and Top-Selling Products.
3. Groups and summarizes sales performance by:
   - Product Category
   - Geographical Region
   - Time Period (Monthly Trend)
4. Prints a clear analytical summary report to the console.
"""

import pathlib
import pandas as pd


def analyze_sales_data(csv_path: str = "task1_cleaned_sales_data.csv") -> dict:
    """Performs comprehensive pandas analysis on the cleaned sales dataset."""
    path = pathlib.Path(csv_path)
    if not path.exists():
        alt_path = pathlib.Path(__file__).parent / "task1_cleaned_sales_data.csv"
        if alt_path.exists():
            path = alt_path
    df = pd.read_csv(path)

    # 1. Core KPIs
    total_sales = df["total_sales"].sum()
    gross_sales = df["gross_sales"].sum()
    total_discount = df["discount_amount"].sum()
    total_orders = df["order_id"].nunique()
    total_units = int(df["quantity"].sum())
    avg_order_value = total_sales / total_orders

    # 2. Top Products Summary
    by_product = (
        df.groupby(["product", "category"], as_index=False)
        .agg(
            orders=("order_id", "count"),
            units_sold=("quantity", "sum"),
            total_sales=("total_sales", "sum"),
            avg_order_value=("total_sales", "mean"),
        )
        .sort_values("total_sales", ascending=False)
        .reset_index(drop=True)
    )
    by_product["revenue_share_pct"] = (by_product["total_sales"] / total_sales * 100).round(2)

    # 3. Category Summary
    by_category = (
        df.groupby("category", as_index=False)
        .agg(
            orders=("order_id", "count"),
            units_sold=("quantity", "sum"),
            total_sales=("total_sales", "sum"),
            avg_order_value=("total_sales", "mean"),
        )
        .sort_values("total_sales", ascending=False)
        .reset_index(drop=True)
    )
    by_category["revenue_share_pct"] = (by_category["total_sales"] / total_sales * 100).round(2)

    # 4. Region Summary
    by_region = (
        df.groupby("region", as_index=False)
        .agg(
            orders=("order_id", "count"),
            units_sold=("quantity", "sum"),
            total_sales=("total_sales", "sum"),
            avg_order_value=("total_sales", "mean"),
        )
        .sort_values("total_sales", ascending=False)
        .reset_index(drop=True)
    )
    by_region["revenue_share_pct"] = (by_region["total_sales"] / total_sales * 100).round(2)

    # 5. Monthly Time Period Summary
    by_month = (
        df.groupby("order_month", as_index=False)
        .agg(
            orders=("order_id", "count"),
            units_sold=("quantity", "sum"),
            total_sales=("total_sales", "sum"),
            avg_order_value=("total_sales", "mean"),
        )
        .sort_values("order_month", ascending=True)
        .reset_index(drop=True)
    )
    by_month["mom_growth_pct"] = (by_month["total_sales"].pct_change() * 100).round(2).fillna(0.0)

    print("=" * 76)
    print("TASK 2: SALES DATA ANALYSIS WITH PANDAS — EXECUTIVE SUMMARY")
    print("=" * 76)
    print(f"Total Net Sales Revenue : ${total_sales:,.2f} (Gross: ${gross_sales:,.2f}, Discounts: ${total_discount:,.2f})")
    print(f"Total Completed Orders  : {total_orders}")
    print(f"Total Units Sold        : {total_units}")
    print(f"Average Order Value     : ${avg_order_value:,.2f}")
    print(f"Top Revenue Product     : {by_product.loc[0, 'product']} (${by_product.loc[0, 'total_sales']:,.2f})")
    print(f"Top Volume Product      : {by_product.sort_values('units_sold', ascending=False).iloc[0]['product']} ({int(by_product['units_sold'].max())} units)")

    print("\n--- 1. SALES BY CATEGORY ---")
    print(by_category.to_string(index=False))

    print("\n--- 2. SALES BY REGION ---")
    print(by_region.to_string(index=False))

    print("\n--- 3. SALES BY TIME PERIOD (MONTHLY TREND) ---")
    print(by_month.to_string(index=False))

    print("\n--- 4. TOP PRODUCTS PERFORMANCE ---")
    print(by_product.to_string(index=False))
    print("=" * 76)

    return {
        "total_sales": total_sales,
        "gross_sales": gross_sales,
        "total_discount": total_discount,
        "total_orders": total_orders,
        "total_units": total_units,
        "avg_order_value": avg_order_value,
        "by_product": by_product,
        "by_category": by_category,
        "by_region": by_region,
        "by_month": by_month,
    }


if __name__ == "__main__":
    analyze_sales_data()
