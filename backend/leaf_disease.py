
from pathlib import Path
import json

import numpy as np
import tensorflow as tf
from PIL import Image, UnidentifiedImageError
from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter(prefix="/api/leaf-disease", tags=["Leaf Disease"])

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = PROJECT_ROOT / "models" / "leaf_disease"
MODEL_PATH = MODEL_DIR / "best_leaf_disease.keras"
CLASS_NAMES_PATH = MODEL_DIR / "class_names.json"

IMAGE_SIZE = (160, 160)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# Load the model once when this module is imported.
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Leaf disease model not found: {MODEL_PATH}")

model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
    CLASS_NAMES = json.load(f)


@router.get("/health")
def leaf_disease_health():
    return {
        "status": "ready",
        "classes": len(CLASS_NAMES),
        "model": MODEL_PATH.name,
    }


@router.post("/predict")
async def predict_leaf_disease(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an image file.",
        )

    contents = await file.read(MAX_FILE_SIZE + 1)

    if not contents:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Image must be 10 MB or smaller.",
        )

    try:
        import io

        image = Image.open(io.BytesIO(contents)).convert("RGB")
        image = image.resize(IMAGE_SIZE)
    except (UnidentifiedImageError, OSError, ValueError):
        raise HTTPException(
            status_code=400,
            detail="Invalid or unsupported image. Upload a JPG or PNG.",
        )

    image_array = np.asarray(image, dtype=np.float32)
    image_array = np.expand_dims(image_array, axis=0)

    probabilities = model.predict(image_array, verbose=0)[0]
    predicted_index = int(np.argmax(probabilities))
    predicted_class = CLASS_NAMES[predicted_index]
    confidence = float(probabilities[predicted_index])

    crop, _, condition = predicted_class.partition("___")
    is_healthy = condition.lower() == "healthy"

    return {
        "crop": crop.replace("_", " "),
        "predicted_class": predicted_class,
        "condition": condition.replace("_", " "),
        "is_healthy": is_healthy,
        "confidence": round(confidence * 100, 2),
        "note": (
            "AI screening result only. Confirm with a local agricultural expert "
            "before making treatment decisions."
        ),
    }