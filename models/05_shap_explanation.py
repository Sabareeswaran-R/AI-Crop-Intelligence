import pandas as pd
import joblib
from sklearn.inspection import permutation_importance

MODEL_PATH = r"C:\AI_Crop_Optimization\models\yield_random_forest.joblib"
DATA_PATH = r"C:\AI_Crop_Optimization\data\processed\crop_yield_ml_ready.csv"

print("=" * 60)
print("     FAST EXPLAINABLE AI - CROP YIELD")
print("=" * 60)

# Load pipeline
pipeline = joblib.load(MODEL_PATH)

# Load dataset
df = pd.read_csv(DATA_PATH)

X = df.drop(columns=["Yield"])
y = df["Yield"]

print("\nDataset:", X.shape)

# Use only 500 samples for fast explanation
X_sample = X.sample(
    n=min(500, len(X)),
    random_state=42
)

y_sample = y.loc[X_sample.index]

print("Explanation samples:", X_sample.shape)
print("\nCalculating feature importance...")
print("Please wait...")

# Fast permutation importance
result = permutation_importance(
    pipeline,
    X_sample,
    y_sample,
    n_repeats=3,
    random_state=42,
    scoring="neg_mean_absolute_error",
    n_jobs=-1
)

importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": result.importances_mean
})

importance = importance.sort_values(
    "Importance",
    ascending=False
)

print("\nEXPLAINABLE AI ANALYSIS COMPLETED!")
print("\nTOP 10 IMPORTANT FEATURES")
print("-" * 50)
print(importance.head(10).to_string(index=False))

# Save results
output_path = r"C:\AI_Crop_Optimization\data\processed\explainable_ai_importance.csv"

importance.to_csv(output_path, index=False)

print("\nResults saved to:")
print(output_path)

print("\n" + "=" * 60)
print("       EXPLAINABLE AI TEST COMPLETED")
print("=" * 60)