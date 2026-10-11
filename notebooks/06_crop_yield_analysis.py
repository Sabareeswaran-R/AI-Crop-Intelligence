import pandas as pd

data_path = r"C:\AI_Crop_Optimization\data\processed\crop_yield_india_clean.csv"

df = pd.read_csv(data_path)

# Clean text columns
for col in ["Crop", "Season", "State"]:
    df[col] = df[col].astype(str).str.strip()

print("\n=== CROP-WISE YIELD STATISTICS ===")

crop_stats = (
    df.groupby("Crop")["Yield"]
    .agg(["count", "min", "median", "mean", "max"])
    .sort_values("median", ascending=False)
)

print(crop_stats.to_string())

print("\n=== CROPS WITH EXTREME YIELD VALUES ===")

extreme = (
    df.groupby("Crop")["Yield"]
    .max()
    .sort_values(ascending=False)
    .head(15)
)

print(extreme)