# Step 5 - Product V1

## Team and project
- Team name: NeuroNexus
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
- Student overlap audit:
  ```powershell
  python src/audit_student_split.py
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
- **Input Form Interface**: [01_app_form.png](file:///c:/Users/devas/Downloads/Academic-Intervention-System-main/Academic-Intervention-System-main/docs/evidence/step5/01_app_form.png)
  - Displays loaded validation sample with all 20 indicators pre-filled, organized into demographic and engagement columns.
- **Prediction Result & Decision Support**: [02_prediction_result.png](file:///c:/Users/devas/Downloads/Academic-Intervention-System-main/Academic-Intervention-System-main/docs/evidence/step5/02_prediction_result.png)
  - Displays the predicted class (`1`), high-risk alert badge, risk probability (`96.76%`), concrete supportive action steps, result table, and `Download this result as CSV` button.
- **Input Validation & Error Handling**: [03_validation_error.png](file:///c:/Users/devas/Downloads/Academic-Intervention-System-main/Academic-Intervention-System-main/docs/evidence/step5/03_validation_error.png)
  - Demonstrates rejection of an out-of-range value (`assessment_average = 105.0`) with clear inline guidance without unhandled tracebacks.
- **Automated Unit Testing Evidence**: `Ran 5 tests in 0.001s, OK` via `python -m unittest test_product_predict -v`.
- **Reference Prediction Output**: Saved to `data/reports/step5_ui_reference_prediction.csv`.

## Student Data Leakage & Split Audit (Response to NeuroNexus Feedback)

In response to instructor feedback: *"explain how you checked that the same student does not appear in both training and test data"*:

### 1. Analysis of Dataset Granularity
In the Open University Learning Analytics Dataset (OULAD), the primary unit of observation is a **course-module registration** indexed by `(id_student, code_module, code_presentation)`, rather than an isolated student record. 
- A single student frequently enrolls in more than one module (e.g. taking module `AAA` and module `BBB`, or retaking a presentation).
- Total records: **32,593** registrations across **28,785** unique students.
- **3,538 students (12.3%)** are registered in more than one course.

### 2. Overlap Verification Procedure
We created an automated audit tool ([`src/audit_student_split.py`](file:///c:/Users/devas/Downloads/Academic-Intervention-System-main/Academic-Intervention-System-main/src/audit_student_split.py)) that computes the set intersection of unique `id_student` values across all splits:
```python
train_ids = set(train_df["id_student"].unique())
test_ids = set(test_df["id_student"].unique())
val_ids = set(val_df["id_student"].unique())

overlap_train_test = train_ids & test_ids
overlap_train_val = train_ids & val_ids
```
**Audit Output (`data/reports/student_split_audit.json`):**
- Training: 22,815 rows | 20,939 unique students
- Validation: 4,889 rows | 4,799 unique students
- Test: 4,889 rows | 4,804 unique students
- **Train & Test Overlap**: 812 students (16.9% of test students have a separate course enrollment in the training set).
- **Train & Validation Overlap**: 803 students.
- **Validation & Test Overlap**: 171 students.

### 3. Impact & Grouped Splitting Mitigation
- **Current Formulation (Course-Level Screening)**: The current split evaluates how accurately the model predicts intervention risk for an *individual course enrollment* given that specific course's assessment grades and VLE interaction logs.
- **Strict Student-Level Generalization**: To guarantee 100% student-level isolation where no student ID appears across splits, we implemented [`src/demo_group_split.py`](file:///c:/Users/devas/Downloads/Academic-Intervention-System-main/Academic-Intervention-System-main/src/demo_group_split.py) using `sklearn.model_selection.GroupShuffleSplit`:
  ```python
  gss = GroupShuffleSplit(n_splits=1, test_size=0.30, random_state=42)
  train_idx, test_idx = next(gss.split(df, groups=df["id_student"]))
  ```
  Verification confirmed that `GroupShuffleSplit` achieves **0 overlapping students (0.00%)** between training and evaluation partitions.

## Earlier feedback addressed
- Added visual evidence screenshots (`01_app_form.png`, `02_prediction_result.png`, `03_validation_error.png`) under `docs/evidence/step5/`.
- Conducted and documented a complete student-level data leakage audit between training and test sets using set intersection metrics.
- Kept model training and hyperparameter search strictly isolated in Step 3; Product V1 performs inference only on the saved model artifact.
- Implemented comprehensive input validation guarding against missing fields, negative counts, non-finite values, and out-of-bounds percentages before pipeline ingestion.
- Ensured absolute parity between CLI reference predictions and interactive Streamlit execution.

## Limitations and responsible use
- The system is an educational screening aid created to assist faculty mentors with proactive early intervention. It does not certify academic capability, grade outcomes, or degree completion.
- Automated punitive decisions, penalties, or negative administrative actions must never be triggered based on this system's predictions.
- Dataset constraints: The model was trained on historical data from the Open University Learning Analytics Dataset (OULAD). Patterns may reflect specific course designs and cohort distributions that require institutional recalibration before cross-institution use.

## Team contributions
- **Team NeuroNexus (Devashmitha)**:
  - Designed and implemented the Product V1 Streamlit interface (`app.py`).
  - Developed the robust inference and validation module (`src/product_predict.py`).
  - Built automated unit test suites (`test_product_predict.py`).
  - Implemented verification scripts (`src/check_product_prediction.py`).
  - Conducted the student overlap and data split audit (`src/audit_student_split.py`, `src/demo_group_split.py`).
  - Generated visual evidence and authored the comprehensive Step 5 documentation (`docs/STEP-5.md`).
