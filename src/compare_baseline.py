
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

ROOT = Path(__file__).resolve().parents[1]

TRAIN_PATH = ROOT / "data" / "processed" / "train.csv"
VALIDATION_PATH = ROOT / "data" / "processed" / "validation.csv"
TEST_PATH = ROOT / "data" / "processed" / "test.csv"

ANN_VALIDATION_PATH = (
    ROOT / "data" / "reports" / "step3_ann_validation_predictions.csv"
)
ANN_TEST_PATH = ROOT / "data" / "reports" / "step3_ann_test_predictions.csv"

REPORT_DIR = ROOT / "data" / "reports"
RESULTS_DIR = ROOT / "results"

BASELINE_THRESHOLD = 50.0


def calculate_metrics(actual, predicted, split, model_name):
    return {
        "Split": split,
        "Model": model_name,
        "Accuracy": accuracy_score(actual, predicted),
        "Precision": precision_score(
            actual, predicted, zero_division=0
        ),
        "Recall": recall_score(
            actual, predicted, zero_division=0
        ),
        "F1 Score": f1_score(
            actual, predicted, zero_division=0
        ),
        "False Positives": int(
            ((actual == 0) & (predicted == 1)).sum()
        ),
        "False Negatives": int(
            ((actual == 1) & (predicted == 0)).sum()
        ),
    }


def load_and_validate(split_path, prediction_path, split_name):
    split = pd.read_csv(split_path)
    ann = pd.read_csv(prediction_path)

    required_split_columns = {"risk", "assessment_average"}
    required_prediction_columns = {
        "actual_risk",
        "predicted_risk",
        "risk_probability",
    }

    if not required_split_columns.issubset(split.columns):
        raise ValueError(
            f"{split_name}: required columns are missing from split data."
        )

    if not required_prediction_columns.issubset(ann.columns):
        raise ValueError(
            f"{split_name}: required ANN prediction columns are missing."
        )

    if len(split) != len(ann):
        raise ValueError(
            f"{split_name}: split and ANN prediction row counts differ."
        )

    actual = split["risk"].reset_index(drop=True).astype(int)
    ann_actual = ann["actual_risk"].reset_index(drop=True).astype(int)

    if not actual.equals(ann_actual):
        raise ValueError(
            f"{split_name}: actual labels do not match row by row. "
            "Comparison stopped to prevent misleading results."
        )

    if split["assessment_average"].isna().any():
        raise ValueError(
            f"{split_name}: assessment_average contains missing values."
        )

    return split.reset_index(drop=True), ann.reset_index(drop=True)


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    train = pd.read_csv(TRAIN_PATH)

    if "assessment_average" not in train.columns or "risk" not in train.columns:
        raise ValueError("Training data is missing required columns.")

    if train["assessment_average"].isna().any():
        raise ValueError("Training assessment averages contain missing values.")

    if set(train["risk"].dropna().unique()) != {0, 1}:
        raise ValueError("Expected risk labels 0 and 1 in training data.")

    print(f"Baseline rule: assessment_average <= {BASELINE_THRESHOLD}")
    print("Threshold was fixed before validation/test evaluation.")

    all_metrics = []
    comparison_rows = []
    paired_outputs = {}

    for split_name, split_path, ann_path in [
        ("validation", VALIDATION_PATH, ANN_VALIDATION_PATH),
        ("test", TEST_PATH, ANN_TEST_PATH),
    ]:
        split, ann = load_and_validate(
            split_path, ann_path, split_name
        )

        actual = split["risk"].astype(int)
        baseline_pred = (
            split["assessment_average"] <= BASELINE_THRESHOLD
        ).astype(int)

        ann_pred = ann["predicted_risk"].astype(int)

        baseline_metrics = calculate_metrics(
            actual, baseline_pred, split_name, "Threshold Baseline"
        )
        ann_metrics = calculate_metrics(
            actual, ann_pred, split_name, "ANN"
        )

        all_metrics.extend([baseline_metrics, ann_metrics])

        comparison_rows.append({
            "Split": split_name,
            "Baseline Threshold": BASELINE_THRESHOLD,
            "Baseline Accuracy": baseline_metrics["Accuracy"],
            "ANN Accuracy": ann_metrics["Accuracy"],
            "Baseline Precision": baseline_metrics["Precision"],
            "ANN Precision": ann_metrics["Precision"],
            "Baseline Recall": baseline_metrics["Recall"],
            "ANN Recall": ann_metrics["Recall"],
            "Baseline F1 Score": baseline_metrics["F1 Score"],
            "ANN F1 Score": ann_metrics["F1 Score"],
            "Baseline False Positives": baseline_metrics["False Positives"],
            "ANN False Positives": ann_metrics["False Positives"],
            "Baseline False Negatives": baseline_metrics["False Negatives"],
            "ANN False Negatives": ann_metrics["False Negatives"],
        })

        paired = pd.DataFrame({
            "row_index": range(len(split)),
            "id_student": split["id_student"],
            "actual_risk": actual,
            "assessment_average": split["assessment_average"],
            "baseline_predicted_risk": baseline_pred,
            "ann_predicted_risk": ann_pred,
            "ann_risk_probability": ann["risk_probability"],
        })

        paired_outputs[split_name] = paired

        print(f"\n===== {split_name.upper()} =====")
        print(pd.DataFrame([baseline_metrics, ann_metrics]).round(4).to_string(index=False))
        print("\nBaseline confusion matrix:")
        print(confusion_matrix(actual, baseline_pred, labels=[0, 1]))

    metrics_df = pd.DataFrame(all_metrics)
    comparison_df = pd.DataFrame(comparison_rows)

    metrics_df.to_csv(
        REPORT_DIR / "step4_baseline_metrics.csv", index=False
    )
    comparison_df.to_csv(
        REPORT_DIR / "step4_comparison.csv", index=False
    )

    paired_outputs["validation"].to_csv(
        REPORT_DIR / "step4_validation_paired_predictions.csv",
        index=False,
    )
    paired_outputs["test"].to_csv(
        REPORT_DIR / "step4_test_paired_predictions.csv",
        index=False,
    )

    plot_data = comparison_df.set_index("Split")
    ax = plot_data[
        ["Baseline F1 Score", "ANN F1 Score"]
    ].plot(kind="bar", figsize=(8, 5), ylim=(0, 1))

    ax.set_title("Threshold Baseline vs ANN")
    ax.set_ylabel("F1 Score")
    ax.set_xlabel("Data split")
    ax.legend(["Threshold Baseline", "ANN"])
    ax.grid(axis="y", alpha=0.3)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(
        RESULTS_DIR / "step4_baseline_vs_ann.png",
        dpi=150,
    )
    plt.close()

    print("\nStep 4 comparison completed.")
    print("Reports saved in:", REPORT_DIR)
    print("Graph saved in:", RESULTS_DIR / "step4_baseline_vs_ann.png")


if __name__ == "__main__":
    main()
