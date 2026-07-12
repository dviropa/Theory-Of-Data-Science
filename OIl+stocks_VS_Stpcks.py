
"""
compare_oil_results.py

Compare two experiment CSVs:
1. all_results_per_stock.csv
2. all_results_per_stock_with_oil.csv

Outputs:
- comparison_all_rows.csv
- best_vs_best.csv
- stock_summary.csv
- report_tables.xlsx
- comparison_plots/*
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    from scipy.stats import ttest_rel, wilcoxon
    SCIPY = True
except Exception:
    SCIPY = False

WITHOUT_OIL = "all_results_per_stock.csv"
WITH_OIL = "all_results_per_stock_with_oil.csv"

PLOT_DIR = "comparison_plots"
os.makedirs(PLOT_DIR, exist_ok=True)

print("="*70)
print("Loading files...")
print("="*70)

df_no = pd.read_csv(WITHOUT_OIL)
df_oil = pd.read_csv(WITH_OIL)

keys = ["Stock","Feature Set","Model"]

merged = df_no.merge(
    df_oil,
    on=keys,
    suffixes=("_NoOil","_Oil")
)

metrics = ["Accuracy","Precision","Recall","Macro F1"]

for m in metrics:
    merged[f"Delta_{m}"] = merged[f"{m}_Oil"] - merged[f"{m}_NoOil"]

merged.to_csv("comparison_all_rows.csv", index=False)

# -------- Best vs Best --------
best_no = df_no.sort_values("Accuracy", ascending=False).groupby("Stock").head(1)
best_oil = df_oil.sort_values("Accuracy", ascending=False).groupby("Stock").head(1)

best = best_no.merge(
    best_oil,
    on="Stock",
    suffixes=("_NoOil","_Oil")
)

best["Delta_Accuracy"] = best["Accuracy_Oil"]-best["Accuracy_NoOil"]
best.to_csv("best_vs_best.csv", index=False)

stock_summary = best[[
    "Stock",
    "Model_NoOil",
    "Feature Set_NoOil",
    "Accuracy_NoOil",
    "Model_Oil",
    "Feature Set_Oil",
    "Accuracy_Oil",
    "Delta_Accuracy"
]].copy()

stock_summary["Improved"] = np.where(
    stock_summary["Delta_Accuracy"]>0,
    "Yes",
    np.where(stock_summary["Delta_Accuracy"]<0,"No","Same")
)

stock_summary.to_csv("stock_summary.csv", index=False)

# -------- summaries --------
model_summary = (
    merged.groupby("Model")[["Delta_Accuracy","Delta_Precision","Delta_Recall","Delta_Macro F1"]]
    .mean()
    .sort_values("Delta_Accuracy", ascending=False)
)

feature_summary = (
    merged.groupby("Feature Set")[["Delta_Accuracy","Delta_Precision","Delta_Recall","Delta_Macro F1"]]
    .mean()
    .sort_values("Delta_Accuracy", ascending=False)
)

# Excel
with pd.ExcelWriter("report_tables.xlsx") as writer:
    merged.to_excel(writer, sheet_name="All Comparisons", index=False)
    best.to_excel(writer, sheet_name="Best vs Best", index=False)
    stock_summary.to_excel(writer, sheet_name="Stock Summary", index=False)
    model_summary.to_excel(writer, sheet_name="Model Summary")
    feature_summary.to_excel(writer, sheet_name="Feature Summary")

# -------- plots --------
plt.figure(figsize=(6,6))
plt.scatter(best["Accuracy_NoOil"], best["Accuracy_Oil"], alpha=.7)
mn=min(best["Accuracy_NoOil"].min(),best["Accuracy_Oil"].min())
mx=max(best["Accuracy_NoOil"].max(),best["Accuracy_Oil"].max())
plt.plot([mn,mx],[mn,mx],"r--")
plt.xlabel("Without Oil")
plt.ylabel("With Oil")
plt.title("Best Accuracy Per Stock")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR,"scatter_best_vs_best.png"))
plt.close()

plt.figure(figsize=(7,4))
plt.hist(best["Delta_Accuracy"], bins=30)
plt.xlabel("Accuracy Improvement")
plt.ylabel("Count")
plt.title("Delta Accuracy")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR,"histogram_delta_accuracy.png"))
plt.close()

model_summary["Delta_Accuracy"].plot(kind="bar", figsize=(7,4))
plt.ylabel("Average Delta Accuracy")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR,"model_improvement.png"))
plt.close()

feature_summary["Delta_Accuracy"].plot(kind="bar", figsize=(12,4))
plt.ylabel("Average Delta Accuracy")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR,"feature_set_improvement.png"))
plt.close()

top = stock_summary.sort_values("Delta_Accuracy",ascending=False).head(20)
plt.figure(figsize=(10,5))
plt.bar(top["Stock"],top["Delta_Accuracy"])
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR,"top20_improvements.png"))
plt.close()

worst = stock_summary.sort_values("Delta_Accuracy").head(20)
plt.figure(figsize=(10,5))
plt.bar(worst["Stock"],worst["Delta_Accuracy"])
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR,"top20_losses.png"))
plt.close()

heat = merged.pivot_table(index="Model",columns="Feature Set",
                          values="Delta_Accuracy",aggfunc="mean")
plt.figure(figsize=(12,5))
plt.imshow(heat, aspect="auto")
plt.colorbar(label="Delta Accuracy")
plt.xticks(range(len(heat.columns)), heat.columns, rotation=90)
plt.yticks(range(len(heat.index)), heat.index)
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR,"heatmap_models_features.png"))
plt.close()

print("="*70)
print("SUMMARY")
print("="*70)
print("Stocks:", len(stock_summary))
print("Improved:", (stock_summary["Delta_Accuracy"]>0).sum())
print("Worsened:", (stock_summary["Delta_Accuracy"]<0).sum())
print("Same:", (stock_summary["Delta_Accuracy"]==0).sum())
print("Average Delta:", stock_summary["Delta_Accuracy"].mean())
print("Median Delta :", stock_summary["Delta_Accuracy"].median())

if SCIPY:
    t = ttest_rel(best["Accuracy_Oil"], best["Accuracy_NoOil"])
    print("\nPaired t-test")
    print(t)

    try:
        w = wilcoxon(best["Accuracy_Oil"], best["Accuracy_NoOil"])
        print("\nWilcoxon")
        print(w)
    except Exception:
        pass

print("\nFinished successfully.")
