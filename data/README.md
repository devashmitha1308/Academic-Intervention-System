# Data Documentation

## Dataset

This project uses the Open University Learning Analytics Dataset (OULAD).

OULAD contains student demographic information, assessment records, registration information, virtual learning environment interactions, course information, and assessment metadata.

The dataset contains more than 10,000 real student-course records and is used as the primary dataset for the Student Performance & Academic Intervention System.

## Raw Data

The original downloaded OULAD archive is stored in:

data/raw/open+university+learning+analytics+dataset.zip

The archive was extracted for inspection and processing into:

data/raw/oulad_check/

The original dataset files are not modified.

## Main Source Tables

### studentInfo.csv

Contains student-course level information including:

- Student ID
- Module
- Presentation
- Gender
- Region
- Highest education
- IMD band
- Age band
- Previous attempts
- Studied credits
- Disability
- Final result

### studentAssessment.csv

Contains student assessment submissions and scores.

### assessments.csv

Contains assessment metadata including:

- Assessment ID
- Module
- Presentation
- Assessment type
- Assessment date
- Assessment weight

### studentVle.csv

Contains student interactions with virtual learning environment resources.

### vle.csv

Contains information about learning resources and activity types.

### courses.csv

Contains course and presentation information.

### studentRegistration.csv

Contains student registration information.

## Preprocessing

The preprocessing pipeline is implemented in:

src/prepare_data.py

The raw data is not modified.

Assessment scores and dates containing invalid or unknown values are converted to numeric values and invalid records are excluded from the corresponding assessment features.

Only TMA and CMA assessment records are used for early intervention features.

Exam records are excluded from the early intervention assessment features because exam dates may be unavailable and exams occur later in the academic process.

## Intervention Cutoff

The project defines day 90 as the intervention cutoff.

Only assessment and VLE activity occurring from day 0 through day 90 is used to create early intervention features.

The final academic outcome is retained as the target used for supervised learning.

This cutoff is a project-defined modelling decision and is not an official OULAD intervention boundary.

## Target Definition

The original OULAD final_result contains four categories:

- Pass
- Distinction
- Fail
- Withdrawn

For the academic-risk classification task, these categories are mapped to a binary target:

- Risk = 1: Fail or Withdrawn
- Risk = 0: Pass or Distinction

The original final_result column is retained for auditing and interpretation.

It must not be used as an input feature during model training because the risk target is derived from it.

## Feature Engineering

Assessment features include:

- assessment_average
- assessment_count
- assessment_weighted_average
- assessment_max
- assessment_min

Virtual learning environment engagement features include:

- total_clicks
- average_clicks
- maximum_clicks
- active_days
- unique_resources

Student information features include:

- gender
- region
- highest_education
- imd_band
- age_band
- num_of_prev_attempts
- studied_credits
- disability

## Missing Values

After preprocessing, the processed dataset contains zero missing values.

When a student-course record has no recorded assessment or VLE activity before the intervention cutoff, the corresponding aggregate activity features are represented as zero.

This represents absence of recorded activity rather than an unknown measurement.

## Duplicate Handling

The final processed dataset contains one record per student-course-presentation combination.

Duplicate student-course-presentation records are removed after feature aggregation and validated before saving the processed dataset.

## Dataset Split

The processed dataset is divided using stratified random splitting:

- Training: 70%
- Validation: 15%
- Test: 15%

Random state:

42

The split is stratified using the binary risk target to preserve the class distribution.

## Generated Files

The preprocessing pipeline creates:

data/processed/train.csv

data/processed/validation.csv

data/processed/test.csv

data/processed/academic_intervention_dataset.csv

results/data_quality_report.json

## Reproducibility

Run the preprocessing pipeline from the project root using:

python src/prepare_data.py

The pipeline uses a fixed random state of 42 for reproducible train, validation, and test splits.

## Data Quality

The latest processed dataset contains:

- 32,593 student-course records
- 23 columns
- 0 missing processed values
- 0 duplicate student-course-presentation records
- 17,208 risk records
- 15,385 non-risk records

The generated quality report is stored at:

results/data_quality_report.json
