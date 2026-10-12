# Perceptron and ADALINE Model Comparison

## Objective

The objective is to implement and compare Perceptron and ADALINE neural learning algorithms for student academic-risk classification.

## Dataset

The models use the project's processed student dataset, divided into training, validation, and testing sets.

## Models Implemented

* **Perceptron:** A supervised learning algorithm that updates weights when a prediction is incorrect.
* **ADALINE:** An adaptive linear neuron that learns by minimizing the error between target values and its linear output.

## Test Results

| Model      | Accuracy | Precision | Recall | F1 Score |
| ---------- | -------: | --------: | -----: | -------: |
| Perceptron |   0.7805 |    0.8035 | 0.7733 |   0.7882 |
| ADALINE    |   0.2677 |    0.3248 | 0.3588 |   0.3409 |

## Results Analysis

Perceptron achieved an accuracy of 78.05% and an F1-score of 0.7882. ADALINE achieved an accuracy of 26.77% and an F1-score of 0.3409 on the test set.

Perceptron performed better on all four reported metrics. ADALINE's comparatively low scores suggest that its learning rate, feature scaling, or training convergence may need further investigation.

## Evaluation Methods

The models were evaluated using accuracy, precision, recall, F1-score, confusion matrices, and classification reports. The detailed results are saved in `perceptron_adaline_test_results.csv`, and the comparison chart is saved in `perceptron_adaline_comparison.png`.

## Responsible Use

Model predictions should be treated as academic-support signals rather than definitive judgments about students. Faculty should review predictions before making decisions. Data leakage, class imbalance, and fairness must be assessed before practical use.

## Limitations

Performance depends on preprocessing, feature selection, class distribution, and hyperparameters. The low ADALINE score should be investigated before drawing conclusions about its suitability.
