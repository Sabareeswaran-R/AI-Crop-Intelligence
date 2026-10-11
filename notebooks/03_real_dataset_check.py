import pandas as pd

data_path = r"C:\Users\sabar\Downloads\crop_yield_dataset\crop_yield.csv"

df = pd.read_csv(data_path)

print("Dataset Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())

print("\nMissing Values:")
print(df.isnull().sum())