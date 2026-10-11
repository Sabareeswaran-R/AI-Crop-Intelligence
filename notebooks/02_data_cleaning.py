import pandas as pd

# Load raw dataset
input_path = r"C:\AI_Crop_Optimization\data\raw\crop_yield_raw.csv"

df = pd.read_csv(input_path, sep="\t")

# Remove duplicate rows
df = df.drop_duplicates()

# Remove rows with missing values
df = df.dropna()

# Save cleaned dataset
output_path = r"C:\AI_Crop_Optimization\data\processed\crop_yield_clean.csv"

df.to_csv(output_path, index=False)

print("Cleaning completed successfully!")
print("Final dataset shape:", df.shape)
print("Saved to:", output_path)