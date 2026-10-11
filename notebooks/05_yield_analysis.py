import pandas as pd

data_path = r"C:\AI_Crop_Optimization\data\processed\crop_yield_india_clean.csv"

df = pd.read_csv(data_path)

# Remove unwanted spaces from text columns
text_columns = ["Crop", "Season", "State"]

for col in text_columns:
    df[col] = df[col].astype(str).str.strip()

print("\n=== CLEANED CATEGORICAL VALUES ===")
print("Crops:", df["Crop"].nunique())
print("States:", df["State"].nunique())
print("Seasons:", df["Season"].unique())

print("\n=== YIELD STATISTICS ===")
print(df["Yield"].describe())

print("\n=== TOP 10 HIGHEST YIELD VALUES ===")
print(df[["Crop", "State", "Crop_Year", "Yield"]]
      .sort_values("Yield", ascending=False)
      .head(10))

print("\n=== YIELD ABOVE 100 ===")
print((df["Yield"] > 100).sum())

print("\n=== YIELD ABOVE 1000 ===")
print((df["Yield"] > 1000).sum())