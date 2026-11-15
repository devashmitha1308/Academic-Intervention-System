# Step 6 - Testing and validation

## Project and environment

- Project: SC03 Student Performance and Academic Intervention System (Team NeuroNexus).
- Branch: `step-6-testing`.
- Commit tested: `40f5dd2`.
- Python version: `3.13.5` (dependencies: `streamlit 1.64.0`, `scikit-learn 1.9.1`, `pandas 2.2.3`, `numpy 2.2.3`).
- Launch from the repository root: `python -m streamlit run app.py`.
- Reference input: first data row in `data/processed/validation.csv` (Student STU-631293, Module DDD, Presentation 2014J).

## Planned tests and results

PASS means the app or script behaved as expected. An error message can be a PASS when the test is checking whether the app rejects invalid input.

| ID | Input or action | Expected behaviour | Actual result | Status |
| --- | --- | --- | --- | --- |
| T01 | Load existing sample and predict | Display a class, label, probability, educational notice, and supportive intervention recommendation. Allow CSV download. | Showed class 1, Higher Risk (Academic Intervention Recommended), risk probability 96.76%, supportive study plan/mentoring guidance, and the educational notice. The CSV downloaded successfully. | PASS |
| T02 | Reload sample and set assessment average to 0.0 | Accept the lower limit (0.0%) and display a valid prediction. | Accepted assessment average 0.0% and returned class 1 (probability 0.9843). | PASS |
| T03 | Reload sample and set assessment average to 100.0 | Accept the upper limit (100.0%) and display a valid prediction. | Accepted assessment average 100.0% and returned class 1 (probability 0.9547). | PASS |
| T04 | Reload sample and set assessment average to 105.0 | Show the allowed range message (0 to 100%) and withhold the prediction. | Displayed `assessment_average: score must be between 0 and 100.` No prediction was shown. | PASS |
| T05 | Reload sample and enter abc as assessment average | Ask for a number and withhold the prediction. | Displayed `assessment_average: enter a number.` No prediction was shown. | PASS |
| T06 | Reload sample and clear total clicks | Ask for a value and withhold the prediction. | Displayed `total_clicks: enter a value.` No prediction was shown. | PASS |
| T07 | Rename the saved model in a temporary copy and start copy on port 8502 | Explain that the model or metadata is missing and hide the prediction form. | The browser showed `The saved model could not be loaded: Saved model or metadata is missing. Restore your Step 3 files.` The prediction form was unavailable. | PASS |
| T08 | Restore the model filename, restart the copy and predict using the existing sample | Show the form again and return a prediction for the same sample. | The form returned and showed `Higher Risk (Academic Intervention Recommended)` and `Model class: 1`. | PASS |
| T09 | Run `python src/compare_step6_predictions.py` to compare the browser download and Python CSV | All twenty inputs, the predicted class and the displayed label should match. | The script reported `PASS: All twenty inputs, the predicted class and the label match.` Both results showed class 1 and `Higher Risk (Academic Intervention Recommended)`. | PASS |
| T10 | Run `python -m unittest -v test_product_predict` | All five input validation tests should pass. | All five tests showed `ok`. The terminal reported `Ran 5 tests in 0.001s` and ended with `OK`. | PASS |

## Evidence

| Test ID | File path or exact observed output |
| --- | --- |
| T01 | Browser download saved as `data/reports/step6_ui_prediction.csv`. Form interface and prediction cards documented in `docs/evidence/step5/01_app_form.png` and `docs/evidence/step5/02_prediction_result.png`. |
| T02–T03 | Terminal & UI evaluation: assessment average 0.0% returned class 1 (probability 0.9843); assessment average 100.0% returned class 1 (probability 0.9547). |
| T04–T06 | Validation rejection: T04 raised `assessment_average: score must be between 0 and 100.`; T05 raised `assessment_average: enter a number.`; T06 raised `total_clicks: enter a value.` Captured in `docs/evidence/step5/03_validation_error.png`. |
| T07–T08 | Missing-model simulation: terminal reported `Saved model or metadata is missing. Restore your Step 3 files.` Restored model successfully reloaded and predicted class 1. |
| T09 | `src/compare_step6_predictions.py` compared `data/reports/step6_ui_prediction.csv` with `data/reports/step5_ui_reference_prediction.csv`. Output: `PASS: All twenty inputs, the predicted class and the label match. Class 1 - Higher Risk (Academic Intervention Recommended)`. |
| T10 | `test_product_predict.py`: five named tests showed `ok`, followed by `Ran 5 tests in 0.001s` and `OK`. |

## Failures, fixes and retests

| Test ID | What failed | What changed and where | Result of repeating the case and a normal case |
| --- | --- | --- | --- |
| T09 | Comparison script `src/compare_step6_predictions.py` was initially not present in the project. | Created `src/compare_step6_predictions.py` implementing fuzzy float comparison (`math.isclose` with `rel_tol=1e-9`) for numeric features and exact string matching for categorical features and predictions. | Script executed with exit code 0 and confirmed parity across all 20 features, predicted class, and intervention label. Normal prediction repeated with exact match. |

No defect was observed across normal, boundary, or invalid input execution paths. The input validator reliably intercepted corrupt inputs and provided clear, actionable error messages.

## Known limits

- **Single Validation Row Reference**: The automated CSV comparison script verifies parity between the UI export and CLI reference on the first validation record. While full pipeline integration is confirmed, individual edge predictions should continue to be inspected.
- **Unit Testing Scope**: Unit tests in `test_product_predict.py` test input validation and bounds checking; they do not evaluate model accuracy or classification fairness across diverse student subgroups.
- **Educational Decision-Support Nature**: SC03 is designed strictly as a supportive decision-assistance system for academic mentors. It does not certify academic capability, grade outcomes, or degree completion, and must never be utilized for automated punitive decisions.

## Contributions

- **Team NeuroNexus (Devashmitha)**:
  - Designed the comprehensive test plan covering normal, boundary, invalid, missing-model, and parity tests (T01–T10).
  - Authored and verified `src/compare_step6_predictions.py` for automated parity checking.
  - Executed all 10 test procedures, verified model resilience during missing-dependency simulation, and validated error handling.
  - Documented complete test evidence, verification logs, and reproducibility instructions in `docs/STEP-6.md`.
