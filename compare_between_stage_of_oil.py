import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# =====================================================
# Load files
# =====================================================

before = pd.read_csv("LSTM_STOCKS_STAGES_OIL.csv")
after = pd.read_csv("OIL_LSTM_STOCKS_STAGES_OIL.csv")
# =====================================================
# Merge
# =====================================================

comparison = before.merge(
    after,
    on=["Stock", "Oil_Group"],
    suffixes=("_WithoutOil", "_WithOil")
)

# =====================================================
# Summary
# =====================================================

summary = comparison.groupby("Oil_Group").agg(
    Stocks=("Stock", "count"),
    Accuracy_WithoutOil=("Accuracy_WithoutOil", "mean"),
    Accuracy_WithOil=("Accuracy_WithOil", "mean")
)

print("\n========== SUMMARY ==========\n")
print(summary)

# =====================================================
# Graph
# =====================================================

plt.figure(figsize=(9,6))

groups = summary.index

x = np.arange(len(groups))
width = 0.35

bars1 = plt.bar(
    x - width/2,
    summary["Accuracy_WithoutOil"],
    width=width,
    label="Without Oil"
)

bars2 = plt.bar(
    x + width/2,
    summary["Accuracy_WithOil"],
    width=width,
    label="With Oil"
)

# =====================================================
# Write percentages above bars
# =====================================================

for bar in bars1:
    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width()/2,
        height + 0.002,
        f"{height*100:.2f}%",
        ha="center",
        va="bottom",
        fontsize=11,
        fontweight="bold"
    )

for bar in bars2:
    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width()/2,
        height + 0.002,
        f"{height*100:.2f}%",
        ha="center",
        va="bottom",
        fontsize=11,
        fontweight="bold"
    )

# =====================================================
# Formatting
# =====================================================

plt.xticks(x, groups, fontsize=12)

plt.ylabel("Average Accuracy", fontsize=13)

plt.xlabel("Oil Dependency", fontsize=13)

plt.title(
    "Average Accuracy by Oil Dependency",
    fontsize=15,
    fontweight="bold"
)

plt.legend(fontsize=11)

plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()

plt.show()