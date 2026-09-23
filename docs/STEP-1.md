# Step 1 Project Contract

## Team and Responsibilities

- Repository - Create folders, add members, and test clone/run steps
- Data - Define fields, prepare sample data, and record sources
- Baseline - Write simple rules and expected results
- Testing/UI - Build validation, prepare the screen sketch, and collect evidence

## One-Sentence Problem

Given anonymous academic indicators, estimate a risk band and suggest a supportive intervention.

## User of the Product

A faculty mentor who wants early, supportive academic intervention information.

## Inputs and Units

| Field | Meaning | Type / Unit | Starter Rule |
|---|---|---|---|
| record_id | Anonymous row identifier | Text | STU-001, STU-002, ... |
| attendance_pct | Classes attended | Percentage | 0 to 100 |
| assessment_pct | Assessment marks | Percentage | 0 to 100 |
| assignment_pct | Assignment marks | Percentage | 0 to 100 |
| engagement_score | Participation indicator | Number, 0 to 10 | 0 to 10 |
| prior_performance_pct | Earlier academic performance | Percentage | 0 to 100 |
| risk_label | Expected academic-risk label | Category | low, medium, high |

## Outputs and Units

- Risk category: low, medium, or high
- Intervention: monitor, mentoring/study plan, or faculty follow-up

The final decision must remain with a human faculty mentor.

## Baseline Method

1. Calculate a visible score:
   - 30% attendance
   - 30% assessment
   - 20% assignment
   - 10% engagement
   - 10% prior performance
2. Convert engagement_score to a percentage before using it.
3. Temporary risk bands:
   - Below 50: high risk
   - 50 to 69: medium risk
   - 70 or more: low risk
4. Map:
   - Low risk → monitor
   - Medium risk → mentoring/study plan
   - High risk → faculty follow-up
5. A human makes the final decision.

These thresholds are temporary and will be evaluated later.

## Soft Computing Method for M1

One transparent neural classifier and a simple score baseline, shown in a risk and intervention screen.

## Advanced Method for M2

Compare Perceptron, ADALINE, and Backpropagation; study errors, imbalance, fairness, and deploy the application.

## Dataset / Scenario Sources

A public anonymized dataset will be selected and documented with its URL, licence, columns, target, original size, and privacy limitations.

No names, phone numbers, or other directly identifying student information will be collected.

## Five Mandatory Test Cases

| Case | Attendance | Assessment | Assignment | Engagement | Prior Performance | Expected Label |
|---|---:|---:|---:|---:|---:|---|
| STU-001 | 92 | 84 | 88 | 8 | 81 | low |
| STU-002 | 42 | 75 | 78 | 7 | 74 | medium |
| STU-003 | 55 | 35 | 30 | 3 | 40 | high |
| STU-004 | 78 | 48 | 52 | 9 | 45 | medium |
| STU-005 | 70 | 60 | 60 | 5 | 60 | medium |

These cases will be checked against the baseline and validation program.

## Product V1 Screen Sketch

To be added after the initial screen sketch is created.

## Risks and Assumptions

- The data must remain anonymous.
- Temporary thresholds may change after testing.
- Missing or invalid values must be rejected or handled according to documented validation rules.
- Simulated data, if used, must be clearly identified as simulated.
- Dataset limitations and assumptions will be documented.
- The system provides decision support and does not automatically punish or take adverse action against students.

## Step 1 Completion Evidence

The following evidence will be added during Step 1:

- Repository and collaborator evidence
- Dataset documentation
- Starter sample data
- Validation output
- Baseline rules and expected results
- Product V1 screen sketch
- Git commit history
- Links to relevant project files
