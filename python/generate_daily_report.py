import pandas as pd

# Load data
orders = pd.read_csv("data/orders.csv")
customers = pd.read_csv("data/customers.csv")
products = pd.read_csv("data/products.csv")
purchase_orders = pd.read_csv("data/purchase_orders.csv")

# Join orders with customer and product information
df = orders.merge(customers, on="Customer_ID")
df = df.merge(products, on="Product_ID")

# Calculate shortage
df["Shortage"] = (df["Quantity"] - df["Inventory_Qty"]).clip(lower=0)

# Get the earliest incoming ETA for each product
next_eta = (
    purchase_orders
    .groupby("Product_ID", as_index=False)["ETA"]
    .min()
)

# Add supplier ETA
df = df.merge(
    next_eta,
    on="Product_ID",
    how="left"
)

# Convert dates
df["Requested_Date"] = pd.to_datetime(df["Requested_Date"])
df["ETA"] = pd.to_datetime(df["ETA"])

# Find orders requiring attention:
# shortage exists AND inventory arrives after requested date
attention = df[
    (df["Shortage"] > 0) &
    (df["ETA"] > df["Requested_Date"])
].copy()

# Add issue description
attention["Issue"] = "Late incoming inventory"

# Create final report
report = attention[
    ["Order_ID", "Customer_Name", "Issue", "Shortage", "ETA"]
]

# Save report
report.to_csv("reports/daily_order_status.csv", index=False)

print("Daily order status report created successfully.")