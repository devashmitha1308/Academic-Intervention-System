# Step 4: Baseline Comparison

## Objective

Compare a simple assessment-based threshold baseline with the previously trained Artificial Neural Network (ANN) on the same validation and test splits with strict student-level group isolation.

## Dataset

- Training rows: 22,842 (20,149 unique students)
- Validation rows: 4,857 (4,318 unique students)
- Test rows: 4,894 (4,318 unique students)
- Target column: `risk`
- Positive class: `1` (at-risk student needing intervention)
- Negative class: `0` (not classified as at-risk)
- Cross-split student overlap: **0 (0.00%)**

## Baseline Rule

The baseline predicts risk class `1` when `assessment_average` is less than or equal to 50. Otherwise, it predicts class `0`.

The threshold is fixed at 50 and is not tuned using validation or test outcomes.

## Validation Results

| Metric | Threshold Baseline | ANN |
|---|---:|---:|
| Accuracy | 0.7179 | 0.8209 |
| Precision | 0.9242 | 0.9008 |
| Recall | 0.5080 | 0.7429 |
| F1 Score | 0.6556 | 0.8143 |
| False Positives | 107 | 210 |
| False Negatives | 1,263 | 660 |

## Test Results

| Metric | Threshold Baseline | ANN |
|---|---:|---:|
| Accuracy | 0.7278 | 0.8277 |
| Precision | 0.9296 | 0.8949 |
| Recall | 0.5279 | 0.7659 |
| F1 Score | 0.6734 | 0.8254 |
| False Positives | 104 | 234 |
| False Negatives | 1,228 | 609 |

## Interpretation

The ANN achieves substantially higher accuracy, recall, and F1 score on both validation and test splits. While the threshold baseline has marginally higher precision, it misses nearly half of at-risk students.

On the test split, the baseline produces 1,228 false negatives compared with 609 for the ANN — meaning the ANN cuts missed at-risk students by more than half (50.4% reduction). For an early academic-support tool, minimizing missed at-risk students is critical for proactive mentoring.

These results support further evaluation of the ANN as a decision-support aid. They do not establish that either model is suitable for automated high-stakes administrative decisions.

## Reproducibility and Outputs

Run the comparison from the repository root:

```powershell
python src/compare_baseline.py
```

Generated files:

- `data/reports/step4_baseline_metrics.csv`
- `data/reports/step4_comparison.csv`
- `data/reports/step4_validation_paired_predictions.csv`
- `data/reports/step4_test_paired_predictions.csv`
- `results/step4_baseline_vs_ann.png`

The script checks that the ANN's actual labels match the split labels row by row before comparing predictions.

## Limitations

The baseline uses only assessment average. It does not account for all student circumstances and should not be used to punish or label students permanently.

The current comparison does not constitute a complete fairness audit. Additional checks across relevant student groups and review by educators are needed before real-world use.
