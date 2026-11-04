# Step 5 - Product V1

## Team and project
- Team name: Devashmitha
- Project code and title: SC03: Student Performance and Academic Intervention System
- Branch and commit: `step-5-product-v1`

## User task
The user of this product is a faculty mentor or academic advisor who wishes to evaluate student progress indicators early in an academic semester to identify students who may require supportive academic intervention. 

The mentor enters 20 anonymous indicators across four key areas:
1. Student demographics and educational background (`gender`, `region`, `highest_education`, `imd_band`, `age_band`, `disability`).
2. Course registration details (`code_module`, `code_presentation`, `studied_credits`, `num_of_prev_attempts`).
3. Assessment marks (`assessment_average`, `assessment_count`, `assessment_max`, `assessment_min`, `assessment_weighted_average`).
4. Learning environment engagement (`total_clicks`, `average_clicks`, `maximum_clicks`, `active_days`, `unique_resources`).

The application validates all inputs, evaluates the indicators against the trained Step 3 Artificial Neural Network (ANN), and outputs:
- The predicted academic risk category (`0`: Lower Risk / Standard Progress, or `1`: Higher Risk / Intervention Recommended).
- An estimated risk probability percentage.
- Concrete, supportive intervention recommendations (e.g., faculty consultation, personalized study schedule, deadline reminders).
- An explicit ethical notice reminding the user that this tool provides supportive decision assistance and must never replace human judgment or be used for automated punitive actions.

## Interface and method
- Interface type: Streamlit Web Application
- Entry file: `app.py`
- Saved model/controller/optimiser: `models/ann_model.pkl` (scikit-learn `Pipeline` containing `ColumnTransformer` with `SimpleImputer`, `StandardScaler`, `OneHotEncoder`, and `MLPClassifier` neural network) and metadata in `models/ann_model_metadata.json`.
- Input schema and units:
  - `code_module`: Course module code (e.g., AAA, BBB, CCC, DDD)
  - `code_presentation`: Presentation cohort (e.g., 2013J, 2014B, 2014J)
  - `gender`: Gender code (`M` or `F`)
  - `region`: Geographic region (e.g., East Anglian Region, London)
  - `highest_education`: Qualification level (e.g., Lower Than A Level, HE Qualification)
  - `imd_band`: Index of Multiple Deprivation band (e.g., 30-40%, 70-80%)
  - `age_band`: Age cohort (e.g., 0-35, 35-55, 55<=)
  - `num_of_prev_attempts`: Previous module attempts (integer count >= 0)
  - `studied_credits`: Cumulative module credits (integer >= 0)
  - `disability`: Disability declared (`Y` or `N`)
  - `assessment_average`: Average assessment score (percentage, 0.0 to 100.0)
  - `assessment_count`: Number of completed assessments (integer count >= 0)
  - `assessment_max`: Highest assessment score (percentage, 0.0 to 100.0)
  - `assessment_min`: Lowest assessment score (percentage, 0.0 to 100.0)
  - `assessment_weighted_average`: Credit-weighted assessment score (percentage, 0.0 to 100.0)
  - `total_clicks`: Virtual Learning Environment interaction clicks (count >= 0)
  - `average_clicks`: Mean clicks per learning resource (number >= 0)
  - `maximum_clicks`: Peak clicks on single activity (number >= 0)
  - `active_days`: Number of distinct active days on learning platform (integer count >= 0)
  - `unique_resources`: Number of unique course materials accessed (integer count >= 0)
- Output labels, units and meaning:
  - `predicted_class`: Integer binary label (`0` = Lower Risk, `1` = Higher Risk)
  - `label`: Plain-language status: "Higher Risk (Academic Intervention Recommended)" or "Lower Risk (Standard Academic Progress)"
  - `risk_probability`: Estimated model posterior probability of student needing support (0.0 to 1.0)
  - `recommendation`: Actionable guidance for proactive mentor outreach
  - `notice`: Mandatory ethical use statement
- Data flow: `app.py` Form Input -> `src/product_predict.py::validate_inputs` (type, range, and presence checks) -> `models/ann_model.pkl::predict_one` (feature alignment, preprocessing, inference) -> Streamlit Display + CSV Export (`step5_prediction.csv`).

## Run instructions
- Tested Python version: `Python 3.13.5`
- Dependency installation:
  ```powershell
  python -m pip install -r requirements-product-v1.txt
  ```
- Working directory: repository root (`Academic-Intervention-System`)
- Start command:
  ```powershell
  python -m streamlit run app.py
  ```
- Expected local address: `http://localhost:8501`
- Automated checks:
  ```powershell
  python -m unittest test_product_predict -v
  ```
- Prediction consistency verification:
  ```powershell
  python src/check_product_prediction.py
  ```

## Actual test evidence

| Case | Actual input or evidence path | Expected behaviour | Observed behaviour | Pass/Fail |
|---|---|---|---|---|
| Normal | Row 0 of `data/processed/validation.csv` (Module DDD, 2014J, score 62.5%, clicks 152) | Passes validation; returns class 1, probability 0.9676, and supportive outreach recommendation | Returned class 1, label "Higher Risk (Academic Intervention Recommended)", probability 0.9676, actionable plan | Pass |
| Boundary | `assessment_average` tested at 0.0% and 100.0% | Passes validation as valid edge values; model executes prediction successfully | Both 0.0% and 100.0% accepted without errors; valid prediction output generated | Pass |
| Invalid or missing input | `assessment_average = "-5"`, `assessment_average = "105"`, `code_module = ""`, missing features | Rejects invalid input with descriptive `ValueError`; prevents model execution | Raised `ValueError: assessment_average: score must be between 0 and 100.` and `missing required feature.` | Pass |
| Missing model/service | `MODEL_PATH` pointed to non-existent file | Raises clear `FileNotFoundError` prompting user to restore Step 3 model artifacts | Raised `FileNotFoundError: Saved model or metadata is missing. Restore your Step 3 files.` | Pass |
| Same input through UI and inference code | Comparison between `python src/check_product_prediction.py` and UI "Load one existing example" | Output values, predicted class (1), and probability (0.9676) must match exactly | `data/reports/step5_ui_reference_prediction.csv` matched UI output identically across all fields | Pass |

## Screenshots and evidence
- Unit testing evidence: `Ran 5 tests in 0.001s, OK` via `python -m unittest test_product_predict -v`.
- Reference prediction output saved to: `data/reports/step5_ui_reference_prediction.csv`.
- Interactive application tested at `http://localhost:8501` with:
  1. One-click loading of real validation samples via "Load one existing example".
  2. Input form with explicit labels, units, and clear sections.
  3. Interactive risk classification and tailored recommendation card.
  4. CSV export functionality via `Download this result as CSV`.
  5. Expandable architecture explanation describing the underlying fitted pipeline and lack of retraining during inference.

## Earlier feedback addressed
- Kept model training and hyperparameter search strictly isolated in Step 3; Product V1 performs inference only on the saved model artifact.
- Implemented comprehensive input validation guarding against missing fields, negative counts, non-finite values, and out-of-bounds percentages before pipeline ingestion.
- Ensured absolute parity between CLI reference predictions and interactive Streamlit execution.

## Limitations and responsible use
- The system is an educational screening aid created to assist faculty mentors with proactive early intervention. It does not certify academic capability, grade outcomes, or degree completion.
- Automated punitive decisions, penalties, or negative administrative actions must never be triggered based on this system's predictions.
- Dataset constraints: The model was trained on historical data from the Open University Learning Analytics Dataset (OULAD). Patterns may reflect specific course designs and cohort distributions that require institutional recalibration before cross-institution use.

## Team contributions
- Devashmitha: Designed and implemented the Product V1 Streamlit interface (`app.py`), developed the robust inference and validation module (`src/product_predict.py`), built automated unit test suites (`test_product_predict.py`), implemented verification scripts (`src/check_product_prediction.py`), and completed the Step 5 documentation.
