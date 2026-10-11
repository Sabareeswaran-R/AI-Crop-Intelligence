import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# 1. Load cleaned dataset
data_path = r"C:\AI_Crop_Optimization\data\processed\crop_yield_clean.csv"

df = pd.read_csv(data_path)


# 2. Separate features and target
X = df.drop("yield_ton_per_hectare", axis=1)
y = df["yield_ton_per_hectare"]


# 3. Identify categorical and numerical columns
categorical_columns = [
    "state",
    "district",
    "season",
    "crop",
    "soil_type",
    "irrigation_type"
]

numerical_columns = [
    "year",
    "crop_area_hectare",
    "rainfall_mm",
    "temperature_c",
    "humidity_percent",
    "soil_ph",
    "nitrogen_kg_ha",
    "phosphorus_kg_ha",
    "potassium_kg_ha"
]


# 4. Preprocessing
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


# 5. Random Forest model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)


# 6. Create ML pipeline
pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# 7. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# 8. Train model
pipeline.fit(X_train, y_train)


# 9. Make predictions
y_pred = pipeline.predict(X_test)


# 10. Evaluate model
mae = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred) ** 0.5
r2 = r2_score(y_test, y_pred)


print("\n===== Crop Yield Prediction Model =====")
print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

print("\nModel Performance:")
print("MAE :", round(mae, 3))
print("RMSE:", round(rmse, 3))
print("R2  :", round(r2, 3))


# 11. Show actual vs predicted
results = pd.DataFrame({
    "Actual Yield": y_test.values,
    "Predicted Yield": y_pred
})

print("\nActual vs Predicted:")
print(results)