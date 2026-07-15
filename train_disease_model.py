# import os
# import numpy as np
# import tensorflow as tf

# from tensorflow.keras.preprocessing.image import load_img, img_to_array
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import (
#     Conv2D,
#     MaxPooling2D,
#     Flatten,
#     Dense,
#     Dropout
# )

# from tensorflow.keras.utils import to_categorical

# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder


# # =========================================================
# # ================= DATASET PATH ==========================
# # =========================================================

# dataset_path = "Disease_Dataset"

# # =========================================================
# # ================= EMPTY LISTS ===========================
# # =========================================================

# images = []
# labels = []

# # =========================================================
# # ================= IMAGE SIZE ============================
# # =========================================================

# IMG_SIZE = 128

# # =========================================================
# # ================= LOAD DATASET ==========================
# # =========================================================

# classes = os.listdir(dataset_path)

# for label in classes:

#     folder_path = os.path.join(dataset_path, label)

#     for image_name in os.listdir(folder_path):

#         image_path = os.path.join(folder_path, image_name)

#         try:

#             # Load Image
#             image = load_img(
#                 image_path,
#                 target_size=(IMG_SIZE, IMG_SIZE)
#             )

#             # Convert to Array
#             image = img_to_array(image)

#             # Normalize
#             image = image / 255.0

#             # Store
#             images.append(image)

#             labels.append(label)

#         except:
#             print(f"Error loading image: {image_path}")

# # =========================================================
# # ================= CONVERT TO NUMPY ======================
# # =========================================================

# images = np.array(images)

# labels = np.array(labels)

# # =========================================================
# # ================= LABEL ENCODING ========================
# # =========================================================

# encoder = LabelEncoder()

# labels = encoder.fit_transform(labels)

# labels = to_categorical(labels)

# # =========================================================
# # ================= TRAIN TEST SPLIT ======================
# # =========================================================

# X_train, X_test, y_train, y_test = train_test_split(
#     images,
#     labels,
#     test_size=0.2,
#     random_state=42
# )

# # =========================================================
# # ================= CNN MODEL =============================
# # =========================================================

# model = Sequential()

# # ---------------------------------------------------------
# # First Convolution Layer
# # ---------------------------------------------------------

# model.add(
#     Conv2D(
#         32,
#         (3, 3),
#         activation='relu',
#         input_shape=(IMG_SIZE, IMG_SIZE, 3)
#     )
# )

# model.add(MaxPooling2D(pool_size=(2, 2)))

# # ---------------------------------------------------------
# # Second Convolution Layer
# # ---------------------------------------------------------

# model.add(
#     Conv2D(
#         64,
#         (3, 3),
#         activation='relu'
#     )
# )

# model.add(MaxPooling2D(pool_size=(2, 2)))

# # ---------------------------------------------------------
# # Third Convolution Layer
# # ---------------------------------------------------------

# model.add(
#     Conv2D(
#         128,
#         (3, 3),
#         activation='relu'
#     )
# )

# model.add(MaxPooling2D(pool_size=(2, 2)))

# # =========================================================
# # ================= FLATTEN ===============================
# # =========================================================

# model.add(Flatten())

# # =========================================================
# # ================= DENSE LAYERS ==========================
# # =========================================================

# model.add(Dense(128, activation='relu'))

# model.add(Dropout(0.5))

# # Output Layer
# model.add(
#     Dense(
#         len(classes),
#         activation='softmax'
#     )
# )

# # =========================================================
# # ================= COMPILE MODEL =========================
# # =========================================================

# model.compile(
#     optimizer='adam',
#     loss='categorical_crossentropy',
#     metrics=['accuracy']
# )

# # =========================================================
# # ================= MODEL SUMMARY =========================
# # =========================================================

# model.summary()

# # =========================================================
# # ================= TRAIN MODEL ===========================
# # =========================================================

# history = model.fit(
#     X_train,
#     y_train,
#     epochs=10,
#     validation_data=(X_test, y_test),
#     batch_size=32
# )

# # =========================================================
# # ================= EVALUATE MODEL ========================
# # =========================================================

# loss, accuracy = model.evaluate(X_test, y_test)

# print("\n==============================")
# print(f"Test Accuracy: {accuracy * 100:.2f}%")
# print("==============================")

# # =========================================================
# # ================= SAVE MODEL ============================
# # =========================================================

# model.save("plant_disease_model.h5")

# print("\n✅ Model Saved Successfully!")

# # =========================================================
# # ================= SAVE LABELS ===========================
# # =========================================================

# import joblib

# joblib.dump(encoder, "disease_label_encoder.pkl")

# print("✅ Label Encoder Saved Successfully!")





import os
import numpy as np
import tensorflow as tf
import joblib
import matplotlib.pyplot as plt
 
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Conv2D, MaxPooling2D, Flatten, Dense,
    Dropout, BatchNormalization, GlobalAveragePooling2D
)
from tensorflow.keras.callbacks import (
    EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
)
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
 
import seaborn as sns
 
 
# =========================================================
# ================= CONFIGURATION =========================
# =========================================================
 
DATASET_PATH = "Disease_Dataset"
IMG_SIZE     = 128
BATCH_SIZE   = 32
EPOCHS       = 30          # EarlyStopping will cut this short
LEARNING_RATE = 0.001
RANDOM_STATE  = 42
 
MODEL_SAVE_PATH   = "plant_disease_model.h5"
ENCODER_SAVE_PATH = "disease_label_encoder.pkl"
 
# =========================================================
# ================= LOAD DATASET ==========================
# =========================================================
 
print("\n" + "="*60)
print("  KRISHI AI — Plant Disease Model Trainer")
print("="*60)
 
if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(
        f"\n❌  Dataset folder '{DATASET_PATH}' not found.\n"
        "    Please create it and add sub-folders for each disease class.\n"
        "    e.g.  Disease_Dataset/Tomato_healthy/  with .jpg images inside."
    )
 
classes = sorted(os.listdir(DATASET_PATH))
classes = [c for c in classes if os.path.isdir(os.path.join(DATASET_PATH, c))]
 
if len(classes) == 0:
    raise ValueError(
        "❌  No class sub-folders found inside the dataset path. "
        "Make sure each disease label is a folder."
    )
 
print(f"\n📁  Dataset path   : {DATASET_PATH}")
print(f"🌿  Classes found  : {len(classes)}")
for i, cls in enumerate(classes):
    count = len(os.listdir(os.path.join(DATASET_PATH, cls)))
    print(f"      [{i+1:02d}] {cls:<40s} ({count} images)")
 
images = []
labels = []
skipped = 0
 
print("\n⏳  Loading images...")
 
for label in classes:
    folder_path = os.path.join(DATASET_PATH, label)
    for image_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_name)
        try:
            from tensorflow.keras.preprocessing.image import load_img, img_to_array
            img = load_img(image_path, target_size=(IMG_SIZE, IMG_SIZE))
            img = img_to_array(img) / 255.0
            images.append(img)
            labels.append(label)
        except Exception as e:
            skipped += 1
 
print(f"✅  Images loaded  : {len(images)}")
if skipped:
    print(f"⚠️   Skipped        : {skipped} (corrupted/unreadable files)")
 
# =========================================================
# ================= PREPARE DATA ==========================
# =========================================================
 
images = np.array(images, dtype="float32")
labels = np.array(labels)
 
encoder = LabelEncoder()
encoded_labels    = encoder.fit_transform(labels)
categorical_labels = to_categorical(encoded_labels)
 
num_classes = len(encoder.classes_)
print(f"🏷️   Unique classes : {num_classes}")
 
X_train, X_test, y_train, y_test = train_test_split(
    images, categorical_labels,
    test_size=0.2,
    random_state=RANDOM_STATE,
    stratify=encoded_labels      # keeps class balance in both splits
)
 
print(f"\n📊  Training samples  : {len(X_train)}")
print(f"📊  Testing samples   : {len(X_test)}")
 
# =========================================================
# ================= DATA AUGMENTATION =====================
# =========================================================
# Augmentation is applied ONLY on training data to boost
# generalisation — validation/test data is NOT augmented.
 
train_datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.15,
    height_shift_range=0.15,
    shear_range=0.10,
    zoom_range=0.15,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],
    fill_mode="nearest"
)
 
train_generator = train_datagen.flow(
    X_train, y_train, batch_size=BATCH_SIZE, shuffle=True
)
 
# =========================================================
# ================= CNN MODEL =============================
# =========================================================
# Architecture: 4 Conv blocks with BatchNorm + MaxPool,
# then GlobalAveragePooling → Dense → Dropout → Softmax.
# GlobalAveragePooling replaces a huge Flatten+Dense combo
# and significantly reduces overfitting.
 
def build_model(input_shape, num_classes):
    model = Sequential(name="KrishiAI_DiseaseNet")
 
    # --- Block 1 ---
    model.add(Conv2D(32, (3,3), activation="relu", padding="same",
                     input_shape=input_shape))
    model.add(BatchNormalization())
    model.add(Conv2D(32, (3,3), activation="relu", padding="same"))
    model.add(MaxPooling2D((2,2)))
    model.add(Dropout(0.25))
 
    # --- Block 2 ---
    model.add(Conv2D(64, (3,3), activation="relu", padding="same"))
    model.add(BatchNormalization())
    model.add(Conv2D(64, (3,3), activation="relu", padding="same"))
    model.add(MaxPooling2D((2,2)))
    model.add(Dropout(0.25))
 
    # --- Block 3 ---
    model.add(Conv2D(128, (3,3), activation="relu", padding="same"))
    model.add(BatchNormalization())
    model.add(Conv2D(128, (3,3), activation="relu", padding="same"))
    model.add(MaxPooling2D((2,2)))
    model.add(Dropout(0.30))
 
    # --- Block 4 ---
    model.add(Conv2D(256, (3,3), activation="relu", padding="same"))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2,2)))
    model.add(Dropout(0.30))
 
    # --- Classifier Head ---
    model.add(GlobalAveragePooling2D())
    model.add(Dense(256, activation="relu"))
    model.add(BatchNormalization())
    model.add(Dropout(0.50))
    model.add(Dense(num_classes, activation="softmax"))
 
    return model
 
model = build_model((IMG_SIZE, IMG_SIZE, 3), num_classes)
 
# =========================================================
# ================= COMPILE ===============================
# =========================================================
 
model.compile(
    optimizer=Adam(learning_rate=LEARNING_RATE),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)
 
model.summary()
 
# =========================================================
# ================= CALLBACKS =============================
# =========================================================
 
callbacks = [
 
    # Stop early if val_accuracy stops improving for 7 epochs
    EarlyStopping(
        monitor="val_accuracy",
        patience=7,
        restore_best_weights=True,
        verbose=1
    ),
 
    # Always keep a checkpoint of the best model weights
    ModelCheckpoint(
        filepath=MODEL_SAVE_PATH,
        monitor="val_accuracy",
        save_best_only=True,
        verbose=1
    ),
 
    # Reduce LR when val_loss plateaus — helps break through saddle points
    ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=4,
        min_lr=1e-6,
        verbose=1
    )
]
 
# =========================================================
# ================= TRAIN =================================
# =========================================================
 
steps_per_epoch = max(1, len(X_train) // BATCH_SIZE)
 
print("\n🚀  Starting training...")
print("="*60)
 
history = model.fit(
    train_generator,
    steps_per_epoch=steps_per_epoch,
    epochs=EPOCHS,
    validation_data=(X_test, y_test),
    callbacks=callbacks,
    verbose=1
)
 
# =========================================================
# ================= EVALUATE ==============================
# =========================================================
 
print("\n" + "="*60)
print("  EVALUATION ON HELD-OUT TEST SET")
print("="*60)
 
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"\n  Test Loss     : {loss:.4f}")
print(f"  Test Accuracy : {accuracy * 100:.2f}%")
 
# Detailed per-class report
y_pred_probs = model.predict(X_test, verbose=0)
y_pred       = np.argmax(y_pred_probs, axis=1)
y_true       = np.argmax(y_test,      axis=1)
 
print("\n📋  Classification Report:")
print(classification_report(y_true, y_pred, target_names=encoder.classes_))
 
# =========================================================
# ================= TRAINING PLOTS ========================
# =========================================================
 
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
 
epochs_ran = range(1, len(history.history["accuracy"]) + 1)
 
# Accuracy
axes[0].plot(epochs_ran, history.history["accuracy"],     label="Train Accuracy", color="green")
axes[0].plot(epochs_ran, history.history["val_accuracy"], label="Val Accuracy",   color="blue")
axes[0].set_title("Model Accuracy", fontsize=14)
axes[0].set_xlabel("Epoch")
axes[0].set_ylabel("Accuracy")
axes[0].legend()
axes[0].grid(alpha=0.3)
 
# Loss
axes[1].plot(epochs_ran, history.history["loss"],     label="Train Loss", color="red")
axes[1].plot(epochs_ran, history.history["val_loss"], label="Val Loss",   color="orange")
axes[1].set_title("Model Loss", fontsize=14)
axes[1].set_xlabel("Epoch")
axes[1].set_ylabel("Loss")
axes[1].legend()
axes[1].grid(alpha=0.3)
 
plt.tight_layout()
plt.savefig("training_history.png", dpi=150, bbox_inches="tight")
print("\n📈  Training plots saved → training_history.png")
 
# Confusion matrix (only if ≤ 20 classes — otherwise too large to read)
if num_classes <= 20:
    cm = confusion_matrix(y_true, y_pred)
    fig_cm, ax = plt.subplots(figsize=(max(8, num_classes), max(6, num_classes - 2)))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Greens",
        xticklabels=encoder.classes_,
        yticklabels=encoder.classes_,
        ax=ax
    )
    ax.set_title("Confusion Matrix", fontsize=14)
    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("True Label")
    plt.tight_layout()
    plt.savefig("confusion_matrix.png", dpi=150, bbox_inches="tight")
    print("🧩  Confusion matrix saved → confusion_matrix.png")
 
# =========================================================
# ================= SAVE ENCODER ==========================
# =========================================================
 
joblib.dump(encoder, ENCODER_SAVE_PATH)
 
print("\n" + "="*60)
print(f"✅  Model saved   → {MODEL_SAVE_PATH}")
print(f"✅  Encoder saved → {ENCODER_SAVE_PATH}")
print("="*60 + "\n")