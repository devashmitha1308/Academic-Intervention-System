# Step 3: ANN Model Development and Evaluation

## Project
Student Performance and Academic Intervention System (Team NeuroNexus)

## Objective
To train an Artificial Neural Network (ANN) to identify students who may benefit from academic support using academic performance and engagement indicators.

## Dataset
The project uses separate training, validation, and test datasets stored in `data/processed/`, partitioned with **strict student-level group isolation** using `GroupShuffleSplit` on `id_student`.

- Training samples: 22,842 (20,149 unique students)
- Validation samples: 4,857 (4,318 unique students)
- Test samples: 4,894 (4,318 unique students)
- Target variable: `risk`
- Student ID overlap across splits: **0 (0.00%)**

The `final_result` and `id_student` columns are excluded from the model inputs to avoid target leakage and unnecessary student identification.

## Model
An ANN classifier was implemented using an end-to-end scikit-learn `Pipeline` combining `ColumnTransformer` (scaling numerical features and one-hot encoding categorical features) and `MLPClassifier`.

- Hidden layers: 64 and 32 neurons
- Activation: ReLU
- Optimizer: Adam
- Maximum iterations: 150
- Early stopping: Enabled
- Random state: 42

## Evaluation Results

| Split | Accuracy | Precision | Recall | F1 Score |
|---|---:|---:|---:|---:|
| Validation | 0.8209 | 0.9008 | 0.7429 | 0.8143 |
| Test | 0.8277 | 0.8949 | 0.7659 | 0.8254 |

## Generated Outputs

- `results/step3_ann_loss_curve.png`
- `results/step3_ann_validation_confusion_matrix.png`
- `results/step3_ann_test_confusion_matrix.png`
- `data/reports/step3_ann_metrics.csv`
- `data/reports/step3_ann_validation_predictions.csv`
- `data/reports/step3_ann_test_predictions.csv`
- `models/ann_model.pkl`
- `models/ann_model_metadata.json`

## Responsible Use
Predictions are intended to support academic intervention, not to punish or label students permanently. Model results should be reviewed alongside context, data quality, and fairness considerations.
