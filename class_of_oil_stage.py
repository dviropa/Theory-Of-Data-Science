import pandas as pd

# ==========================
# Load CSV
# ==========================
#df = pd.read_csv("lstm\lstm_results_per_stock.csv")
df = pd.read_csv("lstm\Oil_lstm_results_per_stock.csv")

# ==========================
# Oil dependency groups
# ==========================

HIGH = {
    "APA","APC","ANDV","CHK","COG","COP","CVX","CXO","DVN","EOG","EQT",
    "FTI","HAL","HES","KMI","MPC","MRO","NBL","NFX","NOV","OKE","OXY",
    "PSX","PX","PXD","RRC","SLB","VLO","WMB","XEC","XOM","BHGE"
}

MEDIUM = {
    # Airlines
    "AAL","ALK","DAL","LUV","UAL",

    # Transportation
    "CSX","JBHT","KSU","NSC","UNP","UPS","FDX","CHRW","EXPD",

    # Automotive
    "BWA","F","GM","PCAR",

    # Heavy Industry
    "CAT","CMI","DE","DOV","EMR","ETN","GE","HON","IR","ITW",
    "PH","PWR","TXT","URI",

    # Chemicals / Materials
    "APD","CF","DWDP","EMN","FMC","LYB","MOS","NUE",
    "PKG","PPG","SEE","SHW","WRK",

    # Travel / Cruise / Hotels
    "CCL","NCLH","RCL","MAR","HLT","MGM","WYNN"
}

# ==========================
# Classification function
# ==========================

def classify(stock):
    if stock in HIGH:
        return "High"
    elif stock in MEDIUM:
        return "Medium"
    else:
        return "Low"

df["Oil_Group"] = df["Stock"].apply(classify)

# ==========================
# Save
# ==========================

df.to_csv("OIL_LSTM_STOCKS_STAGES_OIL.csv", index=False)

print(df["Oil_Group"].value_counts())

print("Done!")