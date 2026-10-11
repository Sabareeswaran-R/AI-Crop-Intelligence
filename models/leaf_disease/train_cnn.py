
from pathlib import Path
import json
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_DIR = (
    PROJECT_ROOT
    / "data"
    / "leaf_disease"
    / "extracted"
    / "Plant_leave_diseases_dataset_without_augmentation"
)
MODEL_DIR = PROJECT_ROOT / "models" / "leaf_disease"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

IMAGE_SIZE = (160, 160)
BATCH_SIZE = 32
SEED = 42
EPOCHS = 10

def main():
    if not DATASET_DIR.exists():
        raise FileNotFoundError(f"Dataset folder not found: {DATASET_DIR}")

    print(f"Dataset: {DATASET_DIR}")
    print("Loading images...")

    train_ds = keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=0.2,
        subset="training",
        seed=SEED,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="int",
    )

    val_ds = keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=0.2,
        subset="validation",
        seed=SEED,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="int",
    )

    class_names = train_ds.class_names
    print(f"Number of classes: {len(class_names)}")
    print("Classes:", class_names)

    with open(MODEL_DIR / "class_names.json", "w", encoding="utf-8") as f:
        json.dump(class_names, f, ensure_ascii=False, indent=2)

    train_ds = train_ds.prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.prefetch(tf.data.AUTOTUNE)

    data_augmentation = keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.08),
        layers.RandomZoom(0.1),
    ])

    base_model = keras.applications.MobileNetV2(
        input_shape=(*IMAGE_SIZE, 3),
        include_top=False,
        weights="imagenet",
    )
    base_model.trainable = False

    inputs = keras.Input(shape=(*IMAGE_SIZE, 3))
    x = data_augmentation(inputs)
    x = keras.applications.mobilenet_v2.preprocess_input(x)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.25)(x)
    outputs = layers.Dense(len(class_names), activation="softmax")(x)

    model = keras.Model(inputs, outputs)
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    model.summary()

    callbacks = [
        keras.callbacks.ModelCheckpoint(
            filepath=str(MODEL_DIR / "best_leaf_disease.keras"),
            monitor="val_accuracy",
            save_best_only=True,
            mode="max",
        ),
        keras.callbacks.EarlyStopping(
            monitor="val_accuracy",
            patience=3,
            restore_best_weights=True,
        ),
    ]

    print("Training started...")
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        callbacks=callbacks,
    )

    model.save(MODEL_DIR / "leaf_disease_model.keras")

    results = {
        "classes": class_names,
        "epochs_completed": len(history.history["loss"]),
        "final_train_accuracy": float(history.history["accuracy"][-1]),
        "final_validation_accuracy": float(history.history["val_accuracy"][-1]),
    }

    with open(MODEL_DIR / "training_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\nTraining complete!")
    print(json.dumps(results, indent=2))
    print(f"Saved models and results to: {MODEL_DIR}")

if __name__ == "__main__":
    main()