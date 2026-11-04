"""SC03 Step 5: Student Performance and Academic Intervention System Product V1.

Run with: python -m streamlit run app.py
"""

from pathlib import Path
import pandas as pd
import streamlit as st

from src.product_predict import FEATURES, ROOT, load_model, predict_one

st.set_page_config(
    page_title="SC03 Academic Intervention System - Product V1",
    layout="wide",
)

st.title("Student Performance & Academic Intervention System")
st.subheader("Product V1 - Decision-Support Interface")
st.write(
    "Enter the student academic and engagement indicators below to assess "
    "academic risk and obtain early supportive intervention recommendations."
)
st.warning(
    "Teaching & Decision-Support Example Only. "
    "A model prediction assists faculty mentors in proactive outreach and does NOT "
    "replace educator judgment, nor should it be used for automated punitive decisions."
)

LABELS = {
    "code_module": "Course Module Code (e.g., AAA, BBB, CCC, DDD)",
    "code_presentation": "Presentation Cohort (e.g., 2013J, 2014B, 2014J)",
    "gender": "Gender (M / F)",
    "region": "Geographic Region (e.g., East Anglian Region, London)",
    "highest_education": "Highest Education (e.g., A Level or Equivalent, HE Qualification)",
    "imd_band": "Index of Multiple Deprivation Band (e.g., 30-40%, 70-80%)",
    "age_band": "Age Band (e.g., 0-35, 35-55, 55<=)",
    "num_of_prev_attempts": "Number of Previous Course Attempts (integer >= 0)",
    "studied_credits": "Total Studied Credits (e.g., 60, 120)",
    "disability": "Disability Declared (Y / N)",
    "assessment_average": "Assessment Average Score (0-100 %)",
    "assessment_count": "Number of Assessments Submitted (integer >= 0)",
    "assessment_max": "Maximum Assessment Score (0-100 %)",
    "assessment_min": "Minimum Assessment Score (0-100 %)",
    "assessment_weighted_average": "Weighted Assessment Score (0-100 %)",
    "total_clicks": "VLE Virtual Learning Environment Total Clicks (>= 0)",
    "average_clicks": "Average Clicks per Activity (>= 0)",
    "maximum_clicks": "Maximum Clicks on a Single Activity (>= 0)",
    "active_days": "Active Online Learning Days (integer >= 0)",
    "unique_resources": "Unique Course Resources Accessed (integer >= 0)",
}


@st.cache_resource
def saved_model():
    return load_model()


try:
    model = saved_model()
except Exception as error:
    st.error(f"The saved model could not be loaded: {error}")
    st.info("Ensure the Step 3 trained model and metadata are present in models/.")
    st.stop()

# Option to pre-load a real validation case
if st.button("Load one existing example"):
    try:
        example = pd.read_csv(ROOT / "data" / "processed" / "validation.csv", nrows=1)
        for name in FEATURES:
            st.session_state[name] = str(example.iloc[0][name])
        st.success("Loaded validation sample into form fields successfully.")
    except Exception as error:
        st.error(f"Example could not be loaded: {error}")

with st.form("academic_indicators_form"):
    st.markdown("### Student Indicators Form")
    col1, col2 = st.columns(2)

    values = {}
    half = len(FEATURES) // 2

    with col1:
        st.markdown("#### Student Demographics & Course Profile")
        for name in FEATURES[:half]:
            values[name] = st.text_input(LABELS[name], key=name)

    with col2:
        st.markdown("#### Academic Performance & VLE Engagement")
        for name in FEATURES[half:]:
            values[name] = st.text_input(LABELS[name], key=name)

    submitted = st.form_submit_button("Predict Academic Risk & Supportive Action")

if submitted:
    try:
        result = predict_one(model, values)
    except ValueError as error:
        st.error(str(error))
    except Exception as error:
        st.error(f"Prediction could not be completed: {error}")
    else:
        st.markdown("---")
        st.subheader("Intervention Decision-Support Result")

        if result["predicted_class"] == 1:
            st.error(f"**Predicted Status**: {result['label']}")
            st.warning(f"**Action Recommended**: {result['recommendation']}")
        else:
            st.success(f"**Predicted Status**: {result['label']}")
            st.info(f"**Action Recommended**: {result['recommendation']}")

        st.metric("Estimated Risk Probability", f"{result['risk_probability'] * 100:.2f}%")
        st.caption(result["notice"])

        output = pd.DataFrame([result])
        st.dataframe(output)

        st.download_button(
            label="Download this result as CSV",
            data=output.to_csv(index=False).encode("utf-8"),
            file_name="step5_prediction.csv",
            mime="text/csv",
        )

with st.expander("How this demonstration works"):
    st.write(
        "1. The interface collects 20 student indicators spanning demographic, "
        "course registration, assessment marks, and virtual learning environment engagement."
    )
    st.write(
        "2. Inputs are strictly validated to check for non-blank fields, numeric datatypes, "
        "percentage bounds (0-100%), and non-negative counts."
    )
    st.write(
        "3. Validated features are fed directly into the saved Step 3 scikit-learn pipeline "
        "(fitted SimpleImputer, StandardScaler, OneHotEncoder, and MLPClassifier ANN). "
        "No retraining occurs during inference."
    )
    st.write(
        "4. The system produces a risk classification, probability, and tailored supportive action plan."
    )
