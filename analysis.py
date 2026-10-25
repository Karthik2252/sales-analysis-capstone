"""
Capstone: Sales Performance Analysis (Superstore dataset)
Covers Task 3 (data preparation), Task 4 (EDA), Task 5 (6 charts).
Run:  python 02_analysis.py
Needs: pip install pandas numpy matplotlib seaborn
Place superstore.csv (Kaggle "Sample - Superstore") in data/
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams["svg.fonttype"] = "none"
os.makedirs("images", exist_ok=True)
os.makedirs("data", exist_ok=True)

# ---------------- TASK 3: DATA PREPARATION ----------------
df = pd.read_csv("data/superstore.csv", encoding="latin1")

print("=== SHAPE ===", df.shape)
print("\n=== COLUMNS & DATA TYPES ===")
print(df.dtypes)
print("\n=== FIRST 5 ROWS ===")
print(df.head())
print("\n=== MISSING VALUES (before) ===")
print(df.isnull().sum())
print("\nDuplicate rows:", df.duplicated().sum())

# Handle duplicates
df = df.drop_duplicates()

# Handle missing values
for col in df.columns:
    if df[col].isnull().any():
        if df[col].dtype == "object":
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            df[col] = df[col].fillna(df[col].median())

# Fix data types
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])
if "Postal Code" in df.columns:
    df["Postal Code"] = df["Postal Code"].astype(str)

# Remove incorrect records
df = df[(df["Sales"] > 0) & (df["Quantity"] > 0)]
df = df[df["Ship Date"] >= df["Order Date"]]

# Feature engineering
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month
df["Month Name"] = df["Order Date"].dt.strftime("%b")
df["Profit Margin %"] = (df["Profit"] / df["Sales"]) * 100

print("\n=== MISSING VALUES (after) ===")
print(df.isnull().sum().sum(), "missing values remain")
print("Final shape:", df.shape)

df.to_csv("data/superstore_cleaned.csv", index=False)

# ---------------- TASK 4: EDA ----------------
print("\n=== DESCRIPTIVE STATISTICS ===")
print(df[["Sales", "Quantity", "Discount", "Profit"]].describe().round(2))

print("\n=== CORRELATION ===")
corr = df[["Sales", "Quantity", "Discount", "Profit"]].corr()
print(corr.round(3))

# Outliers with IQR on Profit
q1, q3 = df["Profit"].quantile([0.25, 0.75])
iqr = q3 - q1
low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
outliers = df[(df["Profit"] < low) | (df["Profit"] > high)]
print(f"\nProfit outliers (IQR): {len(outliers)} rows "
      f"({len(outliers) / len(df) * 100:.1f}%)")

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
print(f"\nTotal Sales: {total_sales:,.0f} | Total Profit: {total_profit:,.0f} "
      f"| Margin: {total_profit / total_sales * 100:.2f}%")

# Insights computed from YOUR data
cat_profit = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)
sub_profit = df.groupby("Sub-Category")["Profit"].sum().sort_values()
reg_profit = df.groupby("Region")["Profit"].sum().sort_values(ascending=False)
month_sales = df.groupby("Month Name")["Sales"].sum()
df["Discount Band"] = pd.cut(df["Discount"], [-0.01, 0, 0.2, 0.4, 1],
                             labels=["0%", "1-20%", "21-40%", ">40%"])
disc_profit = df.groupby("Discount Band", observed=True)["Profit"].mean()
top_cust_share = (df.groupby("Customer Name")["Sales"].sum()
                  .sort_values(ascending=False).head(int(0.2 * df["Customer Name"].nunique())).sum()
                  / total_sales * 100)

insights = [
    f"1. Best category by profit: {cat_profit.index[0]} ({cat_profit.iloc[0]:,.0f}); weakest: {cat_profit.index[-1]} ({cat_profit.iloc[-1]:,.0f}).",
    f"2. Loss-making sub-categories: {', '.join(sub_profit[sub_profit < 0].index) or 'none'}.",
    f"3. Best region: {reg_profit.index[0]} ({reg_profit.iloc[0]:,.0f}); weakest: {reg_profit.index[-1]} ({reg_profit.iloc[-1]:,.0f}).",
    f"4. Peak sales month: {month_sales.idxmax()} ({month_sales.max():,.0f}); lowest: {month_sales.idxmin()} ({month_sales.min():,.0f}).",
    f"5. Avg profit per order line by discount band: " + ", ".join(f"{k}: {v:,.1f}" for k, v in disc_profit.items()) + ".",
    f"6. Top 20% of customers generate {top_cust_share:.1f}% of sales.",
    f"7. Correlation Discount vs Profit = {corr.loc['Discount', 'Profit']:.2f}; Sales vs Profit = {corr.loc['Sales', 'Profit']:.2f}.",
]
with open("data/computed_insights.txt", "w") as f:
    f.write("\n".join(insights))
print("\n=== COMPUTED INSIGHTS (copy into README) ===")
print("\n".join(insights))

# ---------------- TASK 5: 6 VISUALIZATIONS ----------------
# 1 Monthly sales trend
m = df.groupby(df["Order Date"].dt.to_period("M"))["Sales"].sum()
plt.figure(figsize=(11, 5))
m.index = m.index.to_timestamp()
plt.plot(m.index, m.values, marker="o", color="#1f77b4")
plt.title("Monthly Sales Trend"); plt.xlabel("Month"); plt.ylabel("Sales")
plt.tight_layout(); plt.savefig("images/chart1_monthly_sales.svg"); plt.close()

# 2 Sales by category
plt.figure(figsize=(7, 5))
s = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
sns.barplot(x=s.index, y=s.values, hue=s.index, palette="Blues_r", legend=False)
plt.title("Total Sales by Category"); plt.xlabel("Category"); plt.ylabel("Sales")
plt.tight_layout(); plt.savefig("images/chart2_sales_category.svg"); plt.close()

# 3 Profit by region
plt.figure(figsize=(7, 5))
sns.barplot(x=reg_profit.index, y=reg_profit.values, hue=reg_profit.index, palette="Greens_r", legend=False)
plt.title("Total Profit by Region"); plt.xlabel("Region"); plt.ylabel("Profit")
plt.tight_layout(); plt.savefig("images/chart3_profit_region.svg"); plt.close()

# 4 Discount vs Profit
plt.figure(figsize=(8, 5))
smp = df.sample(600, random_state=1)
plt.plot(smp["Discount"], smp["Profit"], "o", ms=4, alpha=0.4, color="#d62728")
plt.axhline(0, color="black", lw=1)
plt.title("Discount vs Profit"); plt.xlabel("Discount"); plt.ylabel("Profit")
plt.tight_layout(); plt.savefig("images/chart4_discount_profit.svg"); plt.close()

# 5 Correlation heatmap
plt.figure(figsize=(6, 5))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", vmin=-1, vmax=1)
plt.title("Correlation Heatmap")
plt.tight_layout(); plt.savefig("images/chart5_correlation.svg"); plt.close()

# 6 Top 10 products by sales
top = df.groupby("Product Name")["Sales"].sum().nlargest(10).sort_values()
plt.figure(figsize=(10, 6))
plt.barh([n[:40] for n in top.index], top.values, color="#9467bd")
plt.title("Top 10 Products by Sales"); plt.xlabel("Sales"); plt.ylabel("Product")
plt.tight_layout(); plt.savefig("images/chart6_top_products.svg"); plt.close()

# Bonus: outlier boxplot
plt.figure(figsize=(8, 3))
sns.boxplot(x=df["Profit"], color="#ff7f0e")
plt.title("Profit Distribution and Outliers"); plt.xlabel("Profit")
plt.tight_layout(); plt.savefig("images/chart7_profit_boxplot.svg"); plt.close()

print("\nDone. Charts saved in images/, cleaned data in data/.")
