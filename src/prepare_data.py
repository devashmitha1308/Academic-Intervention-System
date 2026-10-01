from pathlib import Path
import json
import pandas as pd
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "raw" / "oulad_check"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
RESULTS_DIR = PROJECT_ROOT / "results"

CUTOFF_DAY = 90

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    student_info = pd.read_csv(
        RAW_DIR / "studentInfo.csv"
    )

    student_assessment = pd.read_csv(
        RAW_DIR / "studentAssessment.csv",
        dtype={"score": str}
    )

    assessments = pd.read_csv(
        RAW_DIR / "assessments.csv",
        dtype={"date": str}
    )

    student_vle = pd.read_csv(
        RAW_DIR / "studentVle.csv"
    )

    return (
        student_info,
        student_assessment,
        assessments,
        student_vle
    )


def clean_assessment_data(student_assessment, assessments):
    assessment_data = student_assessment.merge(
        assessments,
        on="id_assessment",
        how="left",
        validate="many_to_one"
    )

    assessment_data["score"] = pd.to_numeric(
        assessment_data["score"],
        errors="coerce"
    )

    assessment_data["date"] = pd.to_numeric(
        assessment_data["date"],
        errors="coerce"
    )

    assessment_data = assessment_data[
        assessment_data["score"].notna()
    ].copy()

    assessment_data = assessment_data[
        assessment_data["date"].notna()
    ].copy()

    assessment_data = assessment_data[
        assessment_data["assessment_type"].isin(
            ["TMA", "CMA"]
        )
    ].copy()

    assessment_data = assessment_data[
        (assessment_data["date"] >= 0)
        & (assessment_data["date"] <= CUTOFF_DAY)
    ].copy()

    assessment_data["weighted_score"] = (
        assessment_data["score"]
        * assessment_data["weight"]
        / 100
    )

    return assessment_data


def create_assessment_features(assessment_data):
    grouped = assessment_data.groupby(
        [
            "id_student",
            "code_module",
            "code_presentation"
        ]
    )

    features = grouped.agg(
        assessment_average=("score", "mean"),
        assessment_count=("score", "count"),
        assessment_max=("score", "max"),
        assessment_min=("score", "min"),
        total_assessment_weight=("weight", "sum"),
        total_weighted_score=("weighted_score", "sum")
    ).reset_index()

    features["assessment_weighted_average"] = (
        features["total_weighted_score"]
        / features["total_assessment_weight"]
        * 100
    )

    features = features.drop(
        columns=[
            "total_assessment_weight",
            "total_weighted_score"
        ]
    )

    return features


def create_vle_features(student_vle):
    student_vle = student_vle.copy()

    student_vle["sum_click"] = pd.to_numeric(
        student_vle["sum_click"],
        errors="coerce"
    )

    student_vle["date"] = pd.to_numeric(
        student_vle["date"],
        errors="coerce"
    )

    student_vle = student_vle[
        student_vle["sum_click"].notna()
    ].copy()

    student_vle = student_vle[
        student_vle["date"].notna()
    ].copy()

    student_vle = student_vle[
        (student_vle["date"] >= 0)
        & (student_vle["date"] <= CUTOFF_DAY)
    ].copy()

    features = student_vle.groupby(
        [
            "id_student",
            "code_module",
            "code_presentation"
        ]
    ).agg(
        total_clicks=("sum_click", "sum"),
        average_clicks=("sum_click", "mean"),
        maximum_clicks=("sum_click", "max"),
        active_days=("date", "nunique"),
        unique_resources=("id_site", "nunique")
    ).reset_index()

    return features


def create_target(student_info):
    target = student_info.copy()

    target["risk"] = target["final_result"].map(
        {
            "Fail": 1,
            "Withdrawn": 1,
            "Pass": 0,
            "Distinction": 0
        }
    )

    target = target[
        target["risk"].notna()
    ].copy()

    return target[
        [
            "id_student",
            "code_module",
            "code_presentation",
            "gender",
            "region",
            "highest_education",
            "imd_band",
            "age_band",
            "num_of_prev_attempts",
            "studied_credits",
            "disability",
            "final_result",
            "risk"
        ]
    ]


def validate_data(data):
    required_columns = [
        "id_student",
        "code_module",
        "code_presentation",
        "assessment_average",
        "assessment_count",
        "assessment_weighted_average",
        "assessment_max",
        "assessment_min",
        "total_clicks",
        "average_clicks",
        "maximum_clicks",
        "active_days",
        "unique_resources",
        "num_of_prev_attempts",
        "studied_credits",
        "risk"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if data.empty:
        raise ValueError(
            "Processed dataset is empty."
        )

    if data["risk"].isna().any():
        raise ValueError(
            "Target contains missing values."
        )

    if not set(data["risk"].unique()).issubset({0, 1}):
        raise ValueError(
            "Target must contain only 0 and 1."
        )

    numeric_columns = [
        "assessment_average",
        "assessment_count",
        "assessment_weighted_average",
        "assessment_max",
        "assessment_min",
        "total_clicks",
        "average_clicks",
        "maximum_clicks",
        "active_days",
        "unique_resources",
        "num_of_prev_attempts",
        "studied_credits"
    ]

    if data[numeric_columns].isna().any().any():
        raise ValueError(
            "Required numeric features contain missing values."
        )

    duplicate_count = data.duplicated(
        subset=[
            "id_student",
            "code_module",
            "code_presentation"
        ]
    ).sum()

    if duplicate_count > 0:
        raise ValueError(
            "Duplicate student-course records detected."
        )

    if (data["assessment_count"] < 0).any():
        raise ValueError(
            "Assessment count cannot be negative."
        )

    if (data["total_clicks"] < 0).any():
        raise ValueError(
            "Total clicks cannot be negative."
        )

    if (data["active_days"] < 0).any():
        raise ValueError(
            "Active days cannot be negative."
        )


def main():
    print("Loading OULAD data...")

    (
        student_info,
        student_assessment,
        assessments,
        student_vle
    ) = load_data()

    print("Data loaded successfully.")
    print(f"Intervention cutoff: day {CUTOFF_DAY}")

    print("Cleaning assessment data...")

    assessment_data = clean_assessment_data(
        student_assessment,
        assessments
    )

    print(
        "Valid pre-cutoff TMA/CMA records:",
        len(assessment_data)
    )

    print("Creating assessment features...")

    assessment_features = create_assessment_features(
        assessment_data
    )

    print(
        "Assessment feature records:",
        len(assessment_features)
    )

    print("Creating VLE engagement features...")

    vle_features = create_vle_features(
        student_vle
    )

    print(
        "VLE feature records:",
        len(vle_features)
    )

    print("Creating target data...")

    target_data = create_target(
        student_info
    )

    print(
        "Target records:",
        len(target_data)
    )

    print("Merging datasets...")

    data = target_data.merge(
        assessment_features,
        on=[
            "id_student",
            "code_module",
            "code_presentation"
        ],
        how="left"
    )

    data = data.merge(
        vle_features,
        on=[
            "id_student",
            "code_module",
            "code_presentation"
        ],
        how="left"
    )

    aggregate_columns = [
        "assessment_average",
        "assessment_count",
        "assessment_weighted_average",
        "assessment_max",
        "assessment_min",
        "total_clicks",
        "average_clicks",
        "maximum_clicks",
        "active_days",
        "unique_resources"
    ]

    for column in aggregate_columns:
        data[column] = data[column].fillna(0)

    data["risk"] = data["risk"].astype(int)

    data = data.drop_duplicates(
        subset=[
            "id_student",
            "code_module",
            "code_presentation"
        ]
    )

    validate_data(data)

    print(
        "Final processed dataset shape:",
        data.shape
    )

    print("\nRisk distribution:")
    print(data["risk"].value_counts())

    print("\nRisk percentages:")
    print(
        data["risk"]
        .value_counts(normalize=True)
        .mul(100)
        .round(2)
    )

    train, temp = train_test_split(
        data,
        test_size=0.30,
        random_state=42,
        stratify=data["risk"]
    )

    validation, test = train_test_split(
        temp,
        test_size=0.50,
        random_state=42,
        stratify=temp["risk"]
    )

    train.to_csv(
        PROCESSED_DIR / "train.csv",
        index=False
    )

    validation.to_csv(
        PROCESSED_DIR / "validation.csv",
        index=False
    )

    test.to_csv(
        PROCESSED_DIR / "test.csv",
        index=False
    )

    data.to_csv(
        PROCESSED_DIR / "academic_intervention_dataset.csv",
        index=False
    )

    quality_report = {
        "dataset": "OULAD",
        "intervention_cutoff_day": CUTOFF_DAY,
        "total_records": int(len(data)),
        "training_records": int(len(train)),
        "validation_records": int(len(validation)),
        "test_records": int(len(test)),
        "features": list(data.columns),
        "missing_values": {
            column: int(value)
            for column, value
            in data.isnull().sum().items()
        },
        "duplicate_student_course_records": int(
            data.duplicated(
                subset=[
                    "id_student",
                    "code_module",
                    "code_presentation"
                ]
            ).sum()
        ),
        "zero_assessment_records": int(
            (data["assessment_count"] == 0).sum()
        ),
        "zero_engagement_records": int(
            (data["total_clicks"] == 0).sum()
        ),
        "risk_distribution": {
            str(key): int(value)
            for key, value
            in data["risk"].value_counts().items()
        }
    }

    with open(
        RESULTS_DIR / "data_quality_report.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            quality_report,
            file,
            indent=4
        )

    print("\nData pipeline completed successfully.")
    print("Processed files saved in data/processed/")
    print("Quality report saved in results/data_quality_report.json")


if __name__ == "__main__":
    main()