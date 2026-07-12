import pandas as pd

df = pd.read_csv("Feature_Engineering_Data.csv")
df=df.drop(columns=[col for col in df.columns if "Unnamed" in col])

# לקחת רק numeric columns
df_numeric = df.select_dtypes(include=['number'])

# להחזיר את Name
df_numeric['Name'] = df['Name']

# aggregation
df_agg = df_numeric.groupby('Name').agg(['mean', 'std', 'min', 'max', 'median'])

# flatten columns
df_agg.columns = ['{}_{}'.format(col, stat) for col, stat in df_agg.columns]

df_agg = df_agg.reset_index()

df_agg = df_agg.drop(columns=[col for col in df_agg.columns if "Unnamed" in col])

# שמירה לקובץ חדש
df_agg.to_csv("stocks_aggregated.csv", index=False)

print(df_agg.head())