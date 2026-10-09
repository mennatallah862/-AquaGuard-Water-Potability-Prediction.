# 💧 AquaGuard — Water Potability Prediction

An interactive Machine Learning project that predicts water potability based on nine physicochemical water quality parameters.

## Overview

**AquaGuard** is a water quality classification project built using Python and Scikit-learn. It analyzes water measurements and predicts whether a water sample is classified as potable or not potable by a trained Random Forest model.

The project includes exploratory data analysis, missing-value imputation, class imbalance handling, model comparison, hyperparameter tuning, and decision-threshold optimization.

> **Disclaimer:** AquaGuard is an educational ML project. Its predictions do not certify that water is safe to drink. Laboratory testing and applicable water quality standards are necessary for real-world safety decisions.

## Dataset

The dataset contains **3,276 samples and 10 columns**, including nine input features and one target variable, `Potability`.

| Feature           | Description                          |
| ----------------- | ------------------------------------ |
| `ph`              | Acidity or alkalinity                |
| `Hardness`        | Water hardness                       |
| `Solids`          | Total dissolved solids               |
| `Chloramines`     | Chloramines concentration            |
| `Sulfate`         | Sulfate concentration                |
| `Conductivity`    | Electrical conductivity              |
| `Organic_carbon`  | Organic carbon concentration         |
| `Trihalomethanes` | Trihalomethanes concentration        |
| `Turbidity`       | Water cloudiness                     |
| `Potability`      | Target: 0 = Not Potable, 1 = Potable |

The dataset contains missing values in `ph`, `Sulfate`, and `Trihalomethanes`. No duplicate rows were found in the initial inspection.

## Machine Learning Workflow

1. **Exploratory Data Analysis (EDA):** Dataset inspection, descriptive statistics, missing-value analysis, target distribution, correlation analysis, histograms, and boxplots.
2. **Data Preparation:** Separate input features from the target and split the data into training and testing sets.
3. **Missing-Value Imputation:** Use `SimpleImputer(strategy="median")` within the model pipeline.
4. **Class Imbalance Handling:** Apply SMOTE within the training pipeline.
5. **Model Comparison:** Evaluate Logistic Regression, Random Forest, Extra Trees, Bagging, and Voting Classifier.
6. **Cross-Validation:** Compare models using stratified cross-validation.
7. **Hyperparameter Tuning:** Optimize Random Forest parameters using GridSearchCV.
8. **Threshold Optimization:** Select a decision threshold using out-of-fold training predictions.
9. **Final Evaluation:** Evaluate the selected model on the held-out test set using classification metrics, a confusion matrix, and an ROC curve.

## Model Selection

The tuned Random Forest was selected for further evaluation.

Best parameters obtained during hyperparameter tuning:

| Parameter           | Value  |
| ------------------- | ------ |
| `n_estimators`      | 300    |
| `max_depth`         | 20     |
| `min_samples_split` | 10     |
| `min_samples_leaf`  | 1      |
| `max_features`      | `sqrt` |

Best cross-validation F1-score during tuning: **0.5524**.

The selected decision threshold was **0.36**, based on the highest F1-score among the evaluated thresholds using cross-validation predictions on the training data.

The threshold changes the classification decision; it does not change the model's underlying predicted probability.

## Initial Tuned Model Performance

The following results are from the held-out test set using the default classification threshold.

| Metric                    | Score |
| ------------------------- | ----: |
| Accuracy                  |  0.66 |
| Precision (Potable class) |  0.57 |
| Recall (Potable class)    |  0.52 |
| F1-score (Potable class)  |  0.54 |

*These are baseline results for the tuned model before applying the optimized threshold. Final threshold-based test metrics should be added after evaluation.*

## Tech Stack

* **Python** — Core programming language
* **Pandas & NumPy** — Data manipulation
* **Matplotlib & Seaborn** — Data visualization
* **Scikit-learn** — Model training, evaluation, and hyperparameter tuning
* **Imbalanced-learn** — SMOTE and imbalanced-learning pipelines
* **Joblib** — Model serialization
* **Streamlit** — Planned or optional interactive web application

## Installation

Clone the repository:

```bash
git clone https://github.com/mennatallah862/aquaguard-water-potability.git
cd aquaguard-water-potability
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the training notebook to reproduce the model, or run the application if `app.py` and the saved model artifact are included.

```bash
streamlit run app.py
```

## Model Artifact

The saved model file, `water_potability_model.pkl`, is expected to contain:

```python
{
    "model": best_rf,
    "threshold": 0.36
}
```

The actual threshold should be loaded from the saved artifact rather than hardcoded independently in the application.

## Project Structure

```text
aquaguard-water-potability/
├── app.py
├── water_potability_model.pkl
├── requirements.txt
├── README.md
└── notebooks/
    └── water_Quality_project.ipynb
```

Adjust the structure to match the files actually committed to the repository.

## Future Improvements

* Develop an interactive Streamlit interface.
* Add final threshold-based test metrics.
* Improve recall and F1-score through further model evaluation.
* Add input validation and prediction explanations.
* Evaluate the model on additional, representative water quality samples.



---

💧 **AquaGuard — Water Potability Prediction with Machine Learning**
