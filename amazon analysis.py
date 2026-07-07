#Amazon Sales Analysis Project
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
#Load dataset
df = pd.read_csv("amazon_sales_dataset.csv", encoding="latin1")
plt.rcParams["font.family"] = ["Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False
os.makedirs("output", exist_ok=True)
def save_plot(filename):
    plt.tight_layout(rect=[0,0,1,0.95])
    plt.savefig(f"output/{filename}", dpi=300)
    plt.show()
df["order_date"] = pd.to_datetime(df["order_date"])
df["month"] = df["order_date"].dt.strftime("%Y-%m")
#1.Overview
print(df.shape)
print(df.head())
print(df.columns)
print(df.isna().sum())
print(df.info())
print(df.describe())
#2.KPI Summary
total_revenue=df["total_revenue"].sum()
avg_order_value=df["total_revenue"].mean()
total_quantity=df["quantity_sold"].sum()
avg_rating=df["rating"].mean()
total_orders=len(df)
print("Total Revenue:", total_revenue)
print("Average Order Value:", avg_order_value)
print("Total Quantity Sold:", total_quantity)
print("Average Rating:", avg_rating)
print("Total Orders:", total_orders)
print(df["order_date"].describe())
# KPI Dashboard
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 8))
axes = axes.flatten()
colors = ["#1f77b4", "#2ca02c", "#ff7f0e", "#9467bd", "#d62728"]
kpi_card = [("Total Revenue", f"{total_revenue:,.0f}"),("Average Order Value", f"{avg_order_value:,.2f}"),("Total Quantity Sold", f"{total_quantity:,.0f}"),("Average Rating", f"{avg_rating:.2f}"),("Total Orders", f"{total_orders:,}")]
for i, (title, value) in enumerate(kpi_card):
    axes[i].text(0.5, 0.6, value,ha="center", va="center",fontsize=28,fontweight="bold",color=colors[i])
    axes[i].text(0.5, 0.35, title,ha="center", va="center",fontsize=12,fontweight="bold")
    axes[i].set_xticks([])
    axes[i].set_yticks([])
    axes[i].set_frame_on(True)
    for spine in axes[i].spines.values():
        spine.set_linewidth(1.5)
axes[5].axis("off")
plt.suptitle("Amazon Sales KPI Dashboard", fontsize=18, fontweight="bold")
save_plot("amazon_kpi_dashboard.png")
#3.Monthly Revenue Analysis
month_revenue = df.groupby("month")["total_revenue"].sum().reset_index()
print(month_revenue)
month_revenue_rank = month_revenue.sort_values(by="total_revenue",ascending=False).reset_index(drop=True)
print(month_revenue_rank)
#Findings:
#January 2023 generated the highest monthly revenue
#August 2022 ranked second
#February 2023 recorded the lowest monthly revenue
month_revenue.plot(x="month",y="total_revenue",kind="line",marker="o",color="#1f77b4",figsize=(10, 5),legend=False)
plt.ticklabel_format(style="plain", axis="y")
plt.xlabel("Month")
plt.ylabel("Revenue",labelpad=15)
plt.title("Monthly Revenue Trend")
plt.xticks(rotation=45)
save_plot("monthly_revenue_trend.png")
#4.Monthly Revenue by Region
region_month_revenue = (df.groupby(["customer_region", "month"])["total_revenue"].sum().reset_index())
print(region_month_revenue)
pivot = region_month_revenue.pivot(index="month",columns="customer_region",values="total_revenue")
pivot.plot(kind="line", figsize=(10, 6),color=["#1f77b4", "#2ca02c", "#ff7f0e", "#9467bd"])
plt.ticklabel_format(style="plain", axis="y")
plt.xlabel("Month")
plt.ylabel("Revenue",labelpad=15)
plt.title("Monthly Revenue by Region")
plt.xticks(rotation=45)
plt.legend(title="Customer Region")
save_plot("monthly_revenue_by_region.png")
#5.Regional Revenue Analysis
region_revenue = (df.groupby("customer_region")["total_revenue"].sum().reset_index())
print(region_revenue)
region_revenue_rank = region_revenue.sort_values(by="total_revenue",ascending=False)
print(region_revenue_rank)
# Findings:
# Middle East generated the highest revenue
# North America ranked second
# Europe recorded the lowest revenue among the customer_region
region_revenue_rank.plot(kind="bar",x="customer_region", y="total_revenue",color="#1f77b4",legend=False,figsize=(8, 5))
plt.ticklabel_format(style="plain", axis="y")
plt.xlabel("Customer Region")
plt.ylabel("Revenue",labelpad=15)
plt.title("Revenue by Customer Region")
plt.xticks(rotation=45)
save_plot("revenue_by_region.png")
#6.Revenue by Product Category
category_revenue = (df.groupby("product_category")["total_revenue"].sum().reset_index().sort_values(by="total_revenue", ascending=False))
print(category_revenue)
#Findings:
# Beauty generated the highest revenue,followed by Books and Fashion
category_revenue.plot(kind="bar",x="product_category",y="total_revenue",color="#1f77b4",legend=False,figsize=(10, 5))
plt.ticklabel_format(style="plain", axis="y")
plt.xlabel("Product Category")
plt.ylabel("Revenue",labelpad=15)
plt.title("Revenue by Product Category")
plt.xticks(rotation=45)
save_plot("revenue_by_product_category.png")
#7.Sales Volume by Product Category
category_sales = (df.groupby("product_category")["quantity_sold"].sum().reset_index().sort_values(by="quantity_sold", ascending=False))
print(category_sales)
#Findings:
# Beauty recorded the highest sales volume,
# followed by Fashion and Books.
category_sales.plot(kind="bar", x="product_category",y="quantity_sold",color="#1f77b4",legend=False,figsize=(10, 5))
plt.ticklabel_format(style="plain", axis="y")
plt.xlabel("Product Category")
plt.ylabel("Quantity Sold",labelpad=15)
plt.title("Sales Volume by Product Category")
plt.xticks(rotation=45)
save_plot("sales_volume_by_product_category.png")
#8.Average Rating by Product Category
category_avg_rating = (df.groupby("product_category")["rating"].mean().reset_index().sort_values(by="rating", ascending=False))
print(category_avg_rating)
#Findings:
# Books received the highest average rating.
# Beauty recorded the lowest average rating.
category_avg_rating.plot(kind="bar",x="product_category",y="rating",color="#1f77b4",legend=False,figsize=(10, 5))
plt.xlabel("Product Category")
plt.ylabel("Average Rating",labelpad=15)
plt.title("Average Rating by Product Category")
plt.xticks(rotation=45)
save_plot("average_rating_by_product_category.png")
#9.Review Count vs. Average Revenue
df["review_group"] = pd.cut(df["review_count"],bins=[0, 50, 100, 200, 300, 400, 500],labels=["0-50", "50-100", "100-200", "200-300", "300-400", "400-500"])
review_summary = (df.groupby("review_group", observed=True).agg(average_revenue=("total_revenue", "mean"),orders=("order_id", "count")).reset_index())
print(review_summary)
#Findings:
# Products with 300–400 reviews achieved the highest average revenue among all review groups.
# Overall, average revenue remained relatively stable across different review count groups, suggesting that review volume alone was not a strong predictor of revenue.
review_summary.plot(kind="bar",x="review_group",y="average_revenue",color="#1f77b4",legend=False,figsize=(8, 5))
plt.xlabel("Review Count Group")
plt.ylabel("Average Revenue",labelpad=15)
plt.title("Average Revenue by Review Count")
save_plot("average_revenue_by_review_count.png")
#10.Payment Method Analysis
print(df["payment_method"].value_counts())
print(df["customer_region"].value_counts())
# Payment methods include Wallet, UPI, Cash on Delivery,Debit Card, and Credit Card
# Customer regions include Asia, North America, Middle East, and Europe
region_payment = (df.groupby(["customer_region", "payment_method"]).size().reset_index(name="orders"))
print(region_payment)
# Wallet usage in Asia
asia = df[df["customer_region"] == "Asia"]
asia_wallet_usage = asia.groupby("payment_method").size()
print(asia_wallet_usage)
#Findings:
# UPI was the most frequently used payment method among customers in Asia.
# Revenue by Payment Method
payment_method_revenue = (df.groupby("payment_method")["total_revenue"].sum().reset_index().sort_values(by="total_revenue", ascending=False))
print(payment_method_revenue)
#Findings:
# Wallet generated the highest revenue.
# UPI ranked second.
payment_method_revenue.plot(kind="bar",x="payment_method",y="total_revenue",color="#1f77b4",legend=False,figsize=(8, 5))
plt.ticklabel_format(style="plain", axis="y")
plt.xlabel("Payment Method")
plt.ylabel("Total Revenue",labelpad=15)
plt.title("Revenue by Payment Method")
plt.xticks(rotation=45)
save_plot("revenue_by_payment_method.png")
#Average Order Value by Payment Method
payment_avg = (df.groupby("payment_method")["total_revenue"].mean().reset_index())
print(payment_avg)
payment_avg.plot(kind="bar",x="payment_method",y="total_revenue",color="#1f77b4",legend=False,figsize=(8, 5))
plt.ticklabel_format(style="plain", axis="y")
plt.xlabel("Payment Method")
plt.ylabel("Average Order Value",labelpad=15)
plt.title("Average Order Value by Payment Method")
plt.xticks(rotation=45)
save_plot("average_order_value_by_payment_method.png")
#11.Revenue Heatmap by Region and Product Category
region_category_pivot = pd.pivot_table(df,index="customer_region",columns="product_category",values="total_revenue",aggfunc="sum",fill_value=0)
print(region_category_pivot)
heatmap_data = region_category_pivot / 1_000_000
plt.figure(figsize=(11, 6))
sns.heatmap(heatmap_data,annot=True,fmt=".2f",cmap="YlGnBu",linewidths=0.5,annot_kws={"size":11},cbar_kws={"shrink":0.9,"pad":0.02})
plt.xlabel("")
plt.ylabel("")
plt.title("Revenue by Region and Product Category (Million)")
save_plot("revenue_heatmap_region_category.png")
#12.Top 10 Product IDs by Revenue
top_10_product = (df.groupby("product_id")["total_revenue"].sum().sort_values(ascending=False).head(10).reset_index())
print(top_10_product)
#Findings:
# Product ID 1931 generated the highest total revenue in the dataset.
# However, the same product ID appears in multiple product categories,
# suggesting that product IDs may not uniquely identify individual products.
top_10_product.plot(kind="bar",x="product_id",y="total_revenue",color="#1f77b4",legend=False,figsize=(10, 5))
plt.ticklabel_format(style="plain", axis="y")
plt.xlabel("Product ID")
plt.ylabel("Total Revenue",labelpad=15)
plt.title("Top 10 Products by Revenue")
plt.xticks(rotation=45)
save_plot("top_10_products_by_revenue.png")
#13.Discount Analysis
discount_summary = (df.groupby("discount_percent").agg(revenue=("total_revenue", "sum"),orders=("order_id", "count"),average_order_value=("total_revenue", "mean")).reset_index())
print(discount_summary)
discount_summary.plot(kind="bar",x="discount_percent",y="average_order_value",color="#1f77b4",legend=False,figsize=(8, 5))
plt.xlabel("Discount Percent")
plt.ylabel("Average Order Value",labelpad=15)
plt.title("Average Order Value by Discount")
save_plot("average_order_value_by_discount.png")
#14.Price Range Analysis
df["price_group"] = pd.cut(df["price"],bins=[0, 50, 100, 200, 500, 1000],labels=["0-50", "50-100", "100-200", "200-500", "500-1000"])
price_summary = (df.groupby("price_group", observed=True).agg(revenue=("total_revenue", "sum"),orders=("order_id", "count"),average_rating=("rating", "mean")).reset_index())
print(price_summary)
price_summary.plot(kind="bar",x="price_group",y="revenue",color="#1f77b4",legend=False,figsize=(8, 5))
plt.ticklabel_format(style="plain", axis="y")
plt.xlabel("Price Group")
plt.ylabel("Revenue",labelpad=15)
plt.title("Revenue by Price Group")
save_plot("revenue_by_price_group.png")
