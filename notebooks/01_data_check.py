import pandas as pd

df = pd.read_csv(
    r"C:\AI_Crop_Optimization\data\raw\crop_yield_raw.csv",
    sep="\t"
)

print("Dataset Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())

print("\nMissing Values:")
print(df.isnull().sum())