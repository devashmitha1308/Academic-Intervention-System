"""SC03 Product V1 inference module.

Student Performance and Academic Intervention System.
Provides input validation, model loading, and risk prediction with supportive interventions.
"""

from pathlib import Path
import json
import math
import pickle
import pandas as pd

FEATURES = [
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
    "assessment_average",
    "assessment_count",
    "assessment_max",
    "assessment_min",
    "assessment_weighted_average",
    "total_clicks",
    "average_clicks",
    "maximum_clicks",
    "active_days",
    "unique_resources",
]

CATEGORICAL_FEATURES = {
    "code_module",
    "code_presentation",
    "gender",
    "region",
    "highest_education",
    "imd_band",
    "age_band",
    "disability",
}

PERCENTAGE_FEATURES = {
    "assessment_average",
    "assessment_max",
    "assessment_min",
    "assessment_weighted_average",
}

NON_NEGATIVE_NUMERICAL_FEATURES = {
    "num_of_prev_attempts",
    "studied_credits",
    "assessment_count",
    "total_clicks",
    "average_clicks",
    "maximum_clicks",
    "active_days",
    "unique_resources",
}

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "ann_model.pkl"
META_PATH = ROOT / "models" / "ann_model_metadata.json"


def validate_inputs(values):
    """Validate student academic indicators and reject invalid inputs."""
    clean = {}
    for name in FEATURES:
        if name not in values:
            raise ValueError(f"{name}: missing required feature.")
        raw = values.get(name)
        if raw is None or str(raw).strip() == "":
            raise ValueError(f"{name}: enter a value.")

        if name in CATEGORICAL_FEATURES:
            clean[name] = str(raw).strip()
        else:
            try:
                number = float(raw)
            except (ValueError, TypeError) as error:
                raise ValueError(f"{name}: enter a number.") from error

            if not math.isfinite(number):
                raise ValueError(f"{name}: use a finite number.")

            if name in PERCENTAGE_FEATURES and not (0.0 <= number <= 100.0):
                raise ValueError(f"{name}: score must be between 0 and 100.")

            if (name in NON_NEGATIVE_NUMERICAL_FEATURES or name in PERCENTAGE_FEATURES) and number < 0:
                raise ValueError(f"{name}: negative values are invalid.")

            clean[name] = number

    return clean


def load_model():
    """Load only the saved Step 3 model pipeline created in this repository."""
    if not MODEL_PATH.is_file() or not META_PATH.is_file():
        raise FileNotFoundError(
            "Saved model or metadata is missing. Restore your Step 3 files."
        )

    metadata = json.loads(META_PATH.read_text(encoding="utf-8"))
    saved_features = metadata.get("input_features", [])
    if saved_features != FEATURES:
        raise ValueError("Model metadata feature order does not match the app.")

    with MODEL_PATH.open("rb") as source:
        model = pickle.load(source)

    return model


def predict_one(model, values):
    """Run inference for a single student profile and return decision support output."""
    clean = validate_inputs(values)
    frame = pd.DataFrame([[clean[name] for name in FEATURES]], columns=FEATURES)

    prediction = int(model.predict(frame)[0])
    if prediction not in (0, 1):
        raise ValueError("Unexpected model class. Check the saved model.")

    proba = float(model.predict_proba(frame)[0][1])

    if prediction == 1:
        label = "Higher Risk (Academic Intervention Recommended)"
        recommendation = (
            "Supportive Action: Schedule a faculty mentoring consultation, "
            "develop a personalized study plan, and check in on upcoming assessment deadlines."
        )
    else:
        label = "Lower Risk (Standard Academic Progress)"
        recommendation = (
            "Standard Monitoring: Student engagement and scores indicate steady progress. "
            "Continue regular coursework and feedback routines."
        )

    return {
        "predicted_class": prediction,
        "label": label,
        "risk_probability": round(proba, 4),
        "recommendation": recommendation,
        "notice": (
            "Educational decision-support prediction only. "
            "This model assists mentors in proactive outreach and must not be used "
            "to punish, penalize, or take automated adverse actions against students."
        ),
        **clean,
    }
