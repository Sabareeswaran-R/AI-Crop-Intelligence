import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Dataset path
DATA_PATH = r"C:\AI_Crop_Optimization\data\raw\Crop_recommendation.csv"

# Load dataset
df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully!")
print("Shape:", df.shape)
print("Columns:", list(df.columns))

# Features and target
X = df[
    [
        "N",
        "P",
        "K",
        "temperature",
        "humidity",
        "ph",
        "rainfall"
    ]
]

y = df["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Random Forest model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

# Train
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("------------------------------------")
print("Crop Recommendation Model")
print("------------------------------------")
print("Accuracy:", round(accuracy, 4))

# Save model
MODEL_PATH = r"C:\AI_Crop_Optimization\models\crop_recommendation_model.joblib"

joblib.dump(model, MODEL_PATH)

print("------------------------------------")
print("Model saved successfully!")
print(MODEL_PATH)
print("------------------------------------")