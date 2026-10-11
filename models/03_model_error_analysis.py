import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


data_path = r"C:\AI_Crop_Optimization\data\processed\crop_yield_ml_ready.csv"

df = pd.read_csv(data_path)

X = df.drop("Yield", axis=1)
y = df["Yield"]

categorical_columns = [
    "Crop",
    "Season",
    "State"
]

numerical_columns = [
    "Crop_Year",
    "Area",
    "Annual_Rainfall",
    "Fertilizer",
    "Pesticide"
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_columns
        ),
        (
            "numerical",
            "passthrough",
            numerical_columns
        )
    ]
)

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)

results = X_test.copy()

results["Actual_Yield"] = y_test.values
results["Predicted_Yield"] = y_pred

results["Absolute_Error"] = (
    results["Actual_Yield"] - results["Predicted_Yield"]
).abs()

print("\n===== TOP 20 PREDICTION ERRORS =====")

print(
    results[
        [
            "Crop",
            "State",
            "Crop_Year",
            "Actual_Yield",
            "Predicted_Yield",
            "Absolute_Error"
        ]
    ]
    .sort_values("Absolute_Error", ascending=False)
    .head(20)
    .to_string(index=False)
)

print("\n===== MAE BY CROP =====")

crop_mae = (
    results
    .groupby("Crop")
    .apply(
        lambda group: mean_absolute_error(
            group["Actual_Yield"],
            group["Predicted_Yield"]
        )
    )
    .sort_values(ascending=False)
)

print(crop_mae.to_string())