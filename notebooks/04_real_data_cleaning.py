import pandas as pd

input_path = r"C:\AI_Crop_Optimization\data\raw\crop_yield_india.csv"

df = pd.read_csv(input_path)

print("Original Shape:", df.shape)

# Remove duplicate rows
df = df.drop_duplicates()

# Remove rows with missing values
df = df.dropna()

output_path = r"C:\AI_Crop_Optimization\data\processed\crop_yield_india_clean.csv"

df.to_csv(output_path, index=False)

print("Cleaning completed successfully!")
print("Cleaned Shape:", df.shape)
print("Saved to:", output_path)