import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from xgboost import XGBClassifier
import os
# ==========================================================
# DATASET WITH BASIC OIL FEATURES
# ==========================================================

CSV_PATH = "Featured_Engineering_Stocks_With_Oil.csv"
TEST_RATIO = 0.20

BASE = ["open","high","low","close"]

OIL_FEATURES = [
    "Oil_open",
    "Oil_high",
    "Oil_low",
    "Oil_close",
    "Oil_volume"
]

FEATURE_SETS = {
    "ALL":"ALL",
    "base+EMA_12":BASE+["EMA_12"],
    "base+EMA_26":BASE+["EMA_26"],
    "base+EMA_6":BASE+["EMA_6"],
    "base+EMA_6_EMA_26":BASE+["EMA_6","EMA_26"],
    "base+High_to_Close":BASE+["High_to_Close"],
    "base+Low_to_Close":BASE+["Low_to_Close"],
    "base+MA100":BASE+["MA100"],
    "base+MA20":BASE+["MA20"],
    "base+MA50":BASE+["MA50"],
    "base+RSI":BASE+["RSI"],
    "open_close_RSI_EMA_6_EMA_12":["open","close","RSI","EMA_6","EMA_12"],
    "open_close_volume_EMA_12_MA100_Pct_Change":["open","close","volume","EMA_12","MA100","Pct_Change"],
    "open_high_low_MA20_MA50_Pct_Change":["open","high","low","MA20","MA50","Pct_Change"],
    "open_MA20_MA50_MA100_High_to_Close_Low_to_Close":["open","MA20","MA50","MA100","High_to_Close","Low_to_Close"],
    "Pct_Change_volume_RSI_EMA_6_Low_to_Close":["Pct_Change","volume","RSI","EMA_6","Low_to_Close"],
}

def models():
    return {
        "Random Forest":RandomForestClassifier(
            n_estimators=300,max_depth=10,class_weight="balanced",
            random_state=42,n_jobs=-1),

        "KNN":Pipeline([
            ("imp",SimpleImputer(strategy="median")),
            ("sc",StandardScaler()),
            ("clf",KNeighborsClassifier(5))
        ]),

        "AdaBoost":Pipeline([
            ("imp",SimpleImputer(strategy="median")),
            ("clf",AdaBoostClassifier(
                n_estimators=300,
                learning_rate=0.05,
                random_state=42))
        ]),

        "LDA":Pipeline([
            ("imp",SimpleImputer(strategy="median")),
            ("sc",StandardScaler()),
            ("clf",LinearDiscriminantAnalysis())
        ]),

        "XGBoost":Pipeline([
            ("imp",SimpleImputer(strategy="median")),
            ("clf",XGBClassifier(
                n_estimators=300,
                max_depth=6,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8,
                objective="binary:logistic",
                eval_metric="logloss",
                random_state=42))
        ])
    }

df=pd.read_csv(CSV_PATH)
df["date"]=pd.to_datetime(df["date"])
df=df.sort_values(["Name","date"]).reset_index(drop=True)

df["next_close"]=df.groupby("Name")["close"].shift(-1)
df=df[df["next_close"].notna()].copy()
df["Target"]=(df["next_close"]>df["close"]).astype(int)
df.drop(columns="next_close",inplace=True)

all_results=[]
_all=pd.DataFrame()

for stock_name,stock_df in df.groupby("Name"):
    # if stock_name<="KLAC":
    #     continue

    if len(stock_df)<30:
        continue

    split=int(len(stock_df)*(1-TEST_RATIO))
    train=stock_df.iloc[:split]
    test=stock_df.iloc[split:]

    if train["Target"].nunique()<2 or test["Target"].nunique()<2:
        continue

    print("\n"+"="*80)
    print("STOCK:",stock_name)
    print("="*80)

    for fs_name,fs in FEATURE_SETS.items():

        if fs=="ALL":
            cols=[c for c in stock_df.columns
                  if c not in ["date","Name","Target"]]
        else:
            cols=[c for c in fs if c in stock_df.columns]
            cols.extend([c for c in OIL_FEATURES if c in stock_df.columns])

        X_train=train[cols]
        X_test=test[cols]
        y_train=train["Target"]
        y_test=test["Target"]

        best_acc=-1
        best_model=""

        for model_name,model in models().items():

            model.fit(X_train,y_train)
            pred=model.predict(X_test)

            acc=accuracy_score(y_test,pred)
            prec=precision_score(y_test,pred,zero_division=0)
            rec=recall_score(y_test,pred,zero_division=0)
            f1=f1_score(y_test,pred,average="macro",zero_division=0)

            all_results.append({
                "Stock":stock_name,
                "Feature Set":fs_name,
                "Model":model_name,
                "Accuracy":acc,
                "Precision":prec,
                "Recall":rec,
                "Macro F1":f1
            })

            if acc>best_acc:
                best_acc=acc
                best_model=model_name

        print(f"{fs_name:45} Best={best_model:15} Acc={best_acc:.4f}")

    results=pd.DataFrame(all_results)
    results.to_csv(
    "all_results_per_stock_with_oil.csv",
    mode="a",
    header=not os.path.exists("all_results_per_stock_with_oil.csv"),
    index=False
    )   
    all_results.clear()
    
    _all = pd.concat(
    [_all, results],
    ignore_index=True
)

best=(_all.sort_values("Accuracy",ascending=False)
      .groupby("Stock")
      .head(1))

top3=(_all.sort_values("Accuracy",ascending=False)
      .groupby("Stock")
      .head(3))

print("\nSaved:")
print("all_results_per_stock_with_oil.csv")

