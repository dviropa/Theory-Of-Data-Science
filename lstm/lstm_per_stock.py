import numpy as np
import pandas as pd
import os
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, recall_score, accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input

# --- הגדרות ---
CSV_PATH = "Featured_Engineering_Stocks_With_Oil.csv"
WINDOW_SIZE = 60
RESULTS_FILE = "Oil_lstm_results_per_stock.csv"
PREDS_FILE = "Oil_lstm_predictions.csv"

# --- טעינה וסידור ---
df = pd.read_csv(CSV_PATH)
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(["Name", "date"]).reset_index(drop=True)

df["next_close"] = df.groupby("Name")["close"].shift(-1)
df = df.dropna()
df["Target"] = (df["next_close"] > df["close"]).astype(int)

feature_cols = [c for c in df.columns if c not in ["date", "Name", "Target", "next_close"]]

def make_windows(X, y, w):
    xs, ys = [], []
    for i in range(w, len(X)):
        xs.append(X[i-w:i])
        ys.append(y.iloc[i])
    return np.array(xs), np.array(ys)

# --- לולאת הרצה ---
for stock, stock_df in df.groupby("Name"):
    stock_df = stock_df.sort_values("date")
    
    # חיתוך: שנה אחרונה לטסט
    cutoff_date = stock_df["date"].max() - pd.Timedelta(days=365)
    train = stock_df[stock_df["date"] <= cutoff_date]
    test = stock_df[stock_df["date"] > cutoff_date]

    if len(train) < WINDOW_SIZE or len(test) < WINDOW_SIZE:
        continue
    
    scaler = StandardScaler()
    X_train = scaler.fit_transform(train[feature_cols])
    X_test = scaler.transform(test[feature_cols])

    X_train_w, y_train_w = make_windows(X_train, train["Target"], WINDOW_SIZE)
    X_test_w, y_test_w = make_windows(X_test, test["Target"], WINDOW_SIZE)

    # --- מודל ---
    model = Sequential([
        Input(shape=(WINDOW_SIZE, len(feature_cols))),
        LSTM(64, return_sequences=True),
        Dropout(0.2),
        LSTM(32),
        Dense(1, activation="sigmoid")
    ])
    
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    model.fit(X_train_w, y_train_w, epochs=20, batch_size=32, verbose=0)

    # חיזוי
    probs = model.predict(X_test_w, verbose=0).flatten()
    preds = (probs > 0.5).astype(int)

    # חישוב מדדים
    acc = accuracy_score(y_test_w, preds)
    prec = precision_score(y_test_w, preds, zero_division=0)
    rec = recall_score(y_test_w, preds, zero_division=0)

    # --- שמירה ---
    # סיכום למניה
    res_df = pd.DataFrame([{"Stock": stock, "Accuracy": acc, "Precision": prec, "Recall": rec}])
    res_df.to_csv(RESULTS_FILE, mode='a', header=not os.path.exists(RESULTS_FILE), index=False)
    
    # תחזיות יומיות
    dates = test.iloc[WINDOW_SIZE:]["date"].values
    pred_df = pd.DataFrame({"Stock": stock, "Date": dates, "True": y_test_w, "Pred": preds, "Prob": probs})
    pred_df.to_csv(PREDS_FILE, mode='a', header=not os.path.exists(PREDS_FILE), index=False)

    print(f"Stock: {stock} | Acc: {acc:.2f} | Prec: {prec:.2f} | Rec: {rec:.2f} | Done")

print("Finished processing all stocks.")