import pandas as pd

input_path = r"C:\AI_Crop_Optimization\data\processed\crop_yield_india_clean.csv"
output_path = r"C:\AI_Crop_Optimization\data\processed\crop_yield_ml_ready.csv"

df = pd.read_csv(input_path)

# Clean categorical values
for col in ["Crop", "Season", "State"]:
    df[col] = df[col].astype(str).str.strip()

# Remove Production to avoid possible target leakage
df = df.drop(columns=["Production"])

# Keep only required ML columns
features = [
    "Crop",
    "Crop_Year",
    "Season",
    "State",
    "Area",
    "Annual_Rainfall",
    "Fertilizer",
    "Pesticide",
    "Yield"
]

df = df[features]

df.to_csv(output_path, index=False)

print("ML dataset created successfully!")
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print("Saved to:", output_path)