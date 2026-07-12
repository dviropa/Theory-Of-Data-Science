import pandas as pd

# ==========================
# Load
# ==========================

stocks = pd.read_csv("Featured_Engineering_Data_To_CSV.csv")
oil = pd.read_csv("Oil_Data.csv")   # תשנה לשם הקובץ שלך

# ==========================
# Convert dates
# ==========================

stocks["date"] = pd.to_datetime(stocks["date"])
oil["date"] = pd.to_datetime(oil["date"])

# ==========================
# Keep only basic Oil features
# ==========================

oil = oil[
    [
        "date",
        "Oil_open",
        "Oil_high",
        "Oil_low",
        "Oil_close",
        "Oil_volume"
    ]
]

# ==========================
# Merge
# ==========================

merged = stocks.merge(
    oil,
    on="date",
    how="left"
)

# ==========================
# Check
# ==========================

print(merged.shape)
print(merged.isna().sum())

# ==========================
# Save
# ==========================

merged.to_csv(
    "Featured_Engineering_Stocks_With_Oil.csv",
    index=False
)
merged.head(10)

print("Done!")