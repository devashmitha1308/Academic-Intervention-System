# Step 3: ANN Model Development and Evaluation

## Project
Student Performance and Academic Intervention System

## Objective
To train an Artificial Neural Network (ANN) to identify students who may benefit from academic support using academic performance and engagement indicators.

## Dataset
The project uses separate training, validation, and test datasets stored in `data/processed/`.

- Training samples: 22,815
- Validation samples: 4,889
- Test samples: 4,889
- Target variable: `risk`

The `final_result` and `id_student` columns are excluded from the model inputs to avoid target leakage and unnecessary student identification.

## Model
An ANN classifier was implemented using scikit-learn's `MLPClassifier`.

- Hidden layers: 64 and 32 neurons
- Activation: ReLU
- Optimizer: Adam
- Maximum iterations: 150
- Early stopping: Enabled
- Random state: 42

## Evaluation Results

| Split | Accuracy | Precision | Recall | F1 Score |
|---|---:|---:|---:|---:|
| Validation | 0.8282 | 0.8665 | 0.7974 | 0.8305 |
| Test | 0.8374 | 0.8749 | 0.8074 | 0.8398 |

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
