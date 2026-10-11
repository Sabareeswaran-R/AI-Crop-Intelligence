import joblib
import pandas as pd

MODEL_PATH = r"C:\AI_Crop_Optimization\models\yield_random_forest.joblib"

# Load trained model
model = joblib.load(MODEL_PATH)

print("====================================")
print("     AI CROP YIELD PREDICTION")
print("====================================")

# Get user inputs
crop = input("Enter Crop: ")
crop_year = int(input("Enter Crop Year: "))
season = input("Enter Season: ")
state = input("Enter State: ")
area = float(input("Enter Area: "))
rainfall = float(input("Enter Annual Rainfall: "))
fertilizer = float(input("Enter Fertilizer: "))
pesticide = float(input("Enter Pesticide: "))

# Create input DataFrame
sample = pd.DataFrame([{
    "Crop": crop,
    "Crop_Year": crop_year,
    "Season": season,
    "State": state,
    "Area": area,
    "Annual_Rainfall": rainfall,
    "Fertilizer": fertilizer,
    "Pesticide": pesticide
}])

# Predict
prediction = model.predict(sample)[0]

print("------------------------------------")
print("Predicted Yield:", round(prediction, 4))
print("------------------------------------")