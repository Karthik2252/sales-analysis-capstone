# Sales Performance Analysis: Data Analysis Capstone

**Author:** Karthik CG | 3rd BCA, Sri JCBM College, Sringeri

## Project Overview
End-to-end analysis of retail sales data: cleaning, exploratory analysis, visualisation, an interactive Power BI dashboard, and business recommendations. Version control with Git and GitHub.

## Problem Statement
A retail company has strong sales but uneven profit. Which categories, regions, products and discount levels drive or hurt profit, and what should the business change to improve profitability?

## Dataset Description
- **Source:** Superstore dataset (Kaggle), 9,994 order lines and 21 columns, orders from 2014 to 2017.
- **Key columns:** Order ID, Order Date, Ship Date, Ship Mode, Customer Name, Segment, Region, State, Category, Sub-Category, Product Name, Sales, Quantity, Discount, Profit.
- **File:** `data/superstore.csv` (raw). `analysis.py` creates `data/superstore_cleaned.csv` (cleaned) when run.

## Tools Used
Python (Pandas, NumPy, Matplotlib, Seaborn), Power BI Desktop, Git, GitHub, VS Code / Jupyter.

## Data Cleaning Process
1. Inspected shape, data types and head of the data.
2. Checked missing values (0 found) and duplicate rows (0 found); the code still handles both (mode for text, median for numbers, drop duplicates).
3. Verified that no column had incorrect values.
4. Converted Order Date / Ship Date to datetime; Postal Code to text.
5. Removed incorrect records (Sales <= 0, Quantity <= 0, Ship Date before Order Date).
6. Created Year, Month and Profit Margin % columns.

## Exploratory Data Analysis
Descriptive statistics, correlation matrix, IQR outlier detection on Profit, and group-wise analysis by category, region, month and discount band. See `analysis.py`.
Summary of findings:
- Total Sales 2,297,201, Total Profit 286,397, Profit Margin 12.47%.
- Sales and Profit correlation is 0.48; Discount and Profit is -0.22.
- 1,881 profit outliers (18.8%) found with the IQR method.
- Orders with 30%+ discount are loss-making 96.8% of the time.

## Visualizations
| Chart | File |
|---|---|
| Monthly sales trend | `images/chart1_monthly_sales.svg` |
| Sales by category | `images/chart2_sales_category.svg` |
| Profit by region | `images/chart3_profit_region.svg` |
| Discount vs profit | `images/chart4_discount_profit.svg` |
| Correlation heatmap | `images/chart5_correlation.svg` |
| Top 10 products | `images/chart6_top_products.svg` |
| Profit outliers (bonus) | `images/chart7_profit_boxplot.svg` |

![Monthly Sales](images/chart1_monthly_sales.svg)

## Power BI Dashboard
Interactive dashboard file: [`dashboard.html`](dashboard.html). It reads `data/superstore.csv` automatically when hosted with GitHub Pages (Settings > Pages > main branch), or you can load the CSV with the file picker.
- **KPI cards:** Total Sales, Total Profit, Profit Margin %, Total Orders
- **Visuals:** monthly sales line chart, sales and profit by category, profit by region, sales share by segment (donut), profit by sub-category
- **Slicers:** Year, Region, Category

![Dashboard](images/dashboard.svg)

A Power BI build guide with DAX measures is in [`docs/powerbi_dashboard_guide.md`](docs/powerbi_dashboard_guide.md).

## Key Insights
1. Sales peak in Nov (352K) and Dec (325K) and are lowest in Feb (60K).
2. Technology is the most profitable category (145K); Furniture earns only 18K profit on 742K sales.
3. Tables (-17.7K), Bookcases (-3.5K) and Supplies (-1.2K) lose money.
4. Orders with 30%+ discount lose money 96.8% of the time (total -135K profit).
5. Central is the weakest region (39.7K profit); West is the best (108.4K).
6. The top 20% of customers generate 48% of sales.
7. Sales grew 51% from 2014 to 2017 (484K to 733K).

## Business Recommendations
1. Cap discounts at about 20% and require approval above 30%.
2. Reprice or drop loss-making sub-categories (Tables, Bookcases, Supplies).
3. Launch festive campaigns early and stock up before November.
4. Improve the Central region and run a loyalty programme for top customers.

## Conclusion
Profit depends more on pricing and discount discipline than on sales volume. Acting on discount policy, product mix and seasonality can raise margin without needing extra sales.

## How to Run
```bash
pip install pandas numpy matplotlib seaborn
# put superstore.csv inside data/, then from the repo root:
python analysis.py
```
Then open `dashboard.html` in a browser and load the CSV.

## Repository Structure
```
├── README.md
├── analysis.py          (cleaning, EDA, charts)
├── dashboard.html       (interactive dashboard)
├── data/                (superstore.csv, computed_insights.txt)
├── images/              (6 charts, outlier chart, dashboard overview)
└── docs/                (summary PDF, insights and recommendations)
```

## Author
Karthik CG
3rd BCA, Sri JCBM College, Sringeri
Email: karthikankush59@gmail.com
GitHub: https://github.com/karthik2252
