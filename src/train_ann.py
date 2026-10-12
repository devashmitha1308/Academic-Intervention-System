
from pathlib import Path
import json
import pickle

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay
)

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "processed"
MODEL_DIR = PROJECT_DIR / "models"
RESULTS_DIR = PROJECT_DIR / "results"
REPORTS_DIR = PROJECT_DIR / "data" / "reports"

for folder in [MODEL_DIR, RESULTS_DIR, REPORTS_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

TARGET = "risk"
EXCLUDED = ["risk", "final_result", "id_student"]

def load_data(filename):
    return pd.read_csv(DATA_DIR / filename)

def main():
    train_df = load_data("train.csv")
    val_df = load_data("validation.csv")
    test_df = load_data("test.csv")

    X_train = train_df.drop(columns=EXCLUDED, errors="ignore")
    y_train = train_df[TARGET].astype(int)

    X_val = val_df.drop(columns=EXCLUDED, errors="ignore")
    y_val = val_df[TARGET].astype(int)

    X_test = test_df.drop(columns=EXCLUDED, errors="ignore")
    y_test = test_df[TARGET].astype(int)

    categorical = X_train.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    numerical = X_train.select_dtypes(
        include=np.number
    ).columns.tolist()

    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer([
        ("numeric", numeric_pipeline, numerical),
        ("categorical", categorical_pipeline, categorical)
    ])

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("ann", MLPClassifier(
            hidden_layer_sizes=(64, 32),
            activation="relu",
            solver="adam",
            max_iter=150,
            early_stopping=True,
            random_state=42
        ))
    ])

    print("Training ANN...")
    model.fit(X_train, y_train)
    print("Training complete.")

    ann = model.named_steps["ann"]

    plt.figure(figsize=(8, 5))
    plt.plot(ann.loss_curve_)
    plt.xlabel("Training iteration")
    plt.ylabel("Loss")
    plt.title("ANN Training Loss Curve")
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "step3_ann_loss_curve.png", dpi=150)
    plt.close()

    metrics = []

    for split_name, X, y in [
        ("validation", X_val, y_val),
        ("test", X_test, y_test)
    ]:
        predictions = model.predict(X)
        probabilities = model.predict_proba(X)[:, 1]

        metrics.append({
            "Split": split_name,
            "Accuracy": accuracy_score(y, predictions),
            "Precision": precision_score(y, predictions, zero_division=0),
            "Recall": recall_score(y, predictions, zero_division=0),
            "F1 Score": f1_score(y, predictions, zero_division=0)
        })

        pd.DataFrame({
            "actual_risk": y.to_numpy(),
            "predicted_risk": predictions,
            "risk_probability": probabilities
        }).to_csv(
            REPORTS_DIR / f"step3_ann_{split_name}_predictions.csv",
            index=False
        )

        cm = confusion_matrix(y, predictions, labels=[0, 1])
        display = ConfusionMatrixDisplay(
            confusion_matrix=cm,
            display_labels=["Lower risk", "Higher risk"]
        )
        display.plot(cmap="Blues", values_format="d")
        plt.title(f"ANN {split_name.title()} Confusion Matrix")
        plt.tight_layout()
        plt.savefig(
            RESULTS_DIR / f"step3_ann_{split_name}_confusion_matrix.png",
            dpi=150
        )
        plt.close()

    metrics_df = pd.DataFrame(metrics)
    metrics_df.to_csv(
        REPORTS_DIR / "step3_ann_metrics.csv",
        index=False
    )

    with open(MODEL_DIR / "ann_model.pkl", "wb") as file:
        pickle.dump(model, file)

    metadata = {
        "model": "MLPClassifier",
        "hidden_layer_sizes": [64, 32],
        "target": TARGET,
        "excluded_features": EXCLUDED,
        "input_features": X_train.columns.tolist(),
        "training_rows": len(X_train),
        "validation_rows": len(X_val),
        "test_rows": len(X_test),
        "random_state": 42
    }

    with open(
        MODEL_DIR / "ann_model_metadata.json", "w", encoding="utf-8"
    ) as file:
        json.dump(metadata, file, indent=2)

    print("\nEvaluation metrics:")
    print(metrics_df.to_string(index=False))
    print("\nStep 3 output files saved successfully.")

if __name__ == "__main__":
    main()
