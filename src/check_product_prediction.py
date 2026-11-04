"""Compare this printed result with the same example in the interface."""

from pathlib import Path
import pandas as pd

try:
    from src.product_predict import ROOT, FEATURES, load_model, predict_one
except ImportError:
    from product_predict import ROOT, FEATURES, load_model, predict_one


def main():
    sample = pd.read_csv(ROOT / "data" / "processed" / "validation.csv", nrows=1)
    values = {name: sample.iloc[0][name] for name in FEATURES}
    result = predict_one(load_model(), values)
    output = ROOT / "data" / "reports" / "step5_ui_reference_prediction.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([result]).to_csv(output, index=False)
    print("Reference Prediction (CLI):")
    print(pd.DataFrame([result]).to_string(index=False))
    print(f"\nSaved reference prediction to: {output}")
    print("Compare with 'Load one existing example' in the Streamlit app.")


if __name__ == "__main__":
    main()
