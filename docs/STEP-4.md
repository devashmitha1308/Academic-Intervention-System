
# Step 4: Baseline Comparison

## Objective

Compare a simple assessment-based threshold baseline with the previously trained Artificial Neural Network (ANN) on the same validation and test splits.

## Dataset

- Training rows: 22,815
- Validation rows: 4,889
- Test rows: 4,889
- Target column: `risk`
- Positive class: `1` (at-risk student)
- Negative class: `0` (not classified as at-risk)

## Baseline Rule

The baseline predicts risk class `1` when `assessment_average` is less than or equal to 50. Otherwise, it predicts class `0`.

The threshold is fixed at 50 and is not tuned using validation or test outcomes.

## Validation Results

| Metric | Threshold Baseline | ANN |
|---|---:|---:|
| Accuracy | 0.7208 | 0.8282 |
| Precision | 0.9170 | 0.8665 |
| Recall | 0.5180 | 0.7974 |
| F1 Score | 0.6620 | 0.8305 |
| False Positives | 121 | 317 |
| False Negatives | 1244 | 523 |

## Test Results

| Metric | Threshold Baseline | ANN |
|---|---:|---:|
| Accuracy | 0.7231 | 0.8374 |
| Precision | 0.9165 | 0.8749 |
| Recall | 0.5231 | 0.8074 |
| F1 Score | 0.6660 | 0.8398 |
| False Positives | 123 | 298 |
| False Negatives | 1231 | 497 |

## Interpretation

The ANN achieves higher accuracy, recall, and F1 score on both validation and test splits. The threshold baseline has higher precision but misses more at-risk students.

On the test split, the baseline has 1,231 false negatives compared with 497 for the ANN. For an academic-support tool, missed at-risk students are important to monitor.

These results support further evaluation of the ANN as a screening aid. They do not establish that either model is fair or suitable for automated high-stakes decisions.

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
