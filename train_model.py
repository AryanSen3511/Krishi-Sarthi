import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

from sklearn.metrics import accuracy_score

# ================= LOAD DATASET =================

df = pd.read_csv("Krishi_ai_dataset/cleaned_crop_dataset.csv")

# ================= FEATURES & TARGET =================

X = df.drop("label", axis=1)

y = df["label"]

# ================= LABEL ENCODING =================

le = LabelEncoder()

y = le.fit_transform(y)

# ================= FEATURE SCALING =================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# ================= TRAIN TEST SPLIT =================

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y,
    test_size=0.2,
    random_state=42
)

# ================= MODELS =================

models = {

    "Random Forest": RandomForestClassifier(),

    "SVM": SVC(probability=True),

    "KNN": KNeighborsClassifier(),

    "Naive Bayes": GaussianNB()
}

# ================= TRAINING & ACCURACY =================

best_model = None
best_accuracy = 0
best_model_name = ""

print("\n========== MODEL ACCURACY ==========\n")

for name, model in models.items():

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    print(f"{name}: {accuracy:.4f}")

    if accuracy > best_accuracy:

        best_accuracy = accuracy
        best_model = model
        best_model_name = name

# ================= BEST MODEL =================

print("\n====================================")
print(f"Best Model: {best_model_name}")
print(f"Best Accuracy: {best_accuracy:.4f}")
print("====================================")

# ================= SAVE FILES =================

joblib.dump(best_model, "crop_model.pkl")

joblib.dump(scaler, "scaler.pkl")

joblib.dump(le, "label_encoder.pkl")

print("\nModel, scaler and encoder saved successfully!")