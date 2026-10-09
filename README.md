
💧 AquaGuard — Water Potability Prediction
PythonStreamlitscikit-learnimbalanced-learn

An interactive Machine Learning project that predicts water potability based on nine physicochemical water quality parameters.

📑 Table of Contents
Overview
Dataset
Machine Learning Workflow
Model Selection
Model Performance
Web Application
Tech Stack
Installation
Model Artifact
Project Structure
Future Improvements
Overview
AquaGuard is a water quality classification project built using Python and Scikit-learn. It analyzes water measurements and predicts whether a water sample is classified as potable or not potable by a trained Random Forest model.

The project includes exploratory data analysis, missing-value imputation, class imbalance handling, model comparison, hyperparameter tuning, and decision-threshold optimization — all wrapped in an interactive Streamlit application.

Disclaimer: AquaGuard is an educational ML project. Its predictions do not certify that water is safe to drink. Laboratory testing and applicable water quality standards are necessary for real-world safety decisions.

Dataset
The dataset contains 3,276 samples and 10 columns, including nine input features and one target variable, Potability.

Feature	Description
ph	Acidity or alkalinity
Hardness	Water hardness
Solids	Total dissolved solids
Chloramines	Chloramines concentration
Sulfate	Sulfate concentration
Conductivity	Electrical conductivity
Organic_carbon	Organic carbon concentration
Trihalomethanes	Trihalomethanes concentration
Turbidity	Water cloudiness
Potability	Target: 0 = Not Potable, 1 = Potable
The dataset contains missing values in ph, Sulfate, and Trihalomethanes. No duplicate rows were found in the initial inspection.

Machine Learning Workflow
Exploratory Data Analysis (EDA): Dataset inspection, descriptive statistics, missing-value analysis, target distribution, correlation analysis, histograms, and boxplots.
Data Preparation: Separate input features from the target and split the data into training and testing sets.
Missing-Value Imputation: Use SimpleImputer(strategy="median") within the model pipeline.
Class Imbalance Handling: Apply SMOTE within the training pipeline.
Model Comparison: Evaluate Logistic Regression, Random Forest, Extra Trees, Bagging, and Voting Classifier.
Cross-Validation: Compare models using stratified cross-validation.
Hyperparameter Tuning: Optimize Random Forest parameters using GridSearchCV.
Threshold Optimization: Select a decision threshold using out-of-fold training predictions.
Final Evaluation: Evaluate the selected model on the held-out test set using classification metrics, a confusion matrix, and an ROC curve.
Model Selection
The tuned Random Forest was selected for further evaluation.

Best parameters obtained during hyperparameter tuning:

Parameter	Value
n_estimators	300
max_depth	20
min_samples_split	10
min_samples_leaf	1
max_features	sqrt
Best cross-validation F1-score during tuning: 0.5524.

The selected decision threshold was 0.36, based on the highest F1-score among the evaluated thresholds using cross-validation predictions on the training data.

The threshold changes the classification decision; it does not change the model's underlying predicted probability.

Model Performance
Results from the held-out test set using the default classification threshold (0.50):

Metric	Score
Accuracy	0.66
Precision (Potable class)	0.57
Recall (Potable class)	0.52
F1-score (Potable class)	0.54
📌 Threshold-based test metrics (using the optimized threshold of 0.36) will be added after final evaluation.

💻 Web Application
The project ships with an interactive Streamlit application (app.py) featuring:

Feature
🎛️	9 validated inputs organized into Basic, Chemical, and Additional property groups
📊	Probability gauge visualizing the safety score against the decision threshold
🎯	Threshold marker displayed on the probability bar for transparent decisions
📋	Result details including prediction, probability, and margin from threshold
📱	Responsive design with an ocean-themed animated UI
Run it locally:

streamlit run app.py
Tech Stack
Python — Core programming language
Pandas & NumPy — Data manipulation
Matplotlib & Seaborn — Data visualization
Scikit-learn — Model training, evaluation, and hyperparameter tuning
Imbalanced-learn — SMOTE and imbalanced pipeline handling
Joblib — Model serialization
Streamlit — Interactive web application
Plotly — Gauge chart visualization (optional)
Installation
Clone the repository:

bash

git clone https://github.com/mennatallah862/aquaguard-water-potability.git
cd aquaguard-water-potability
Install the required packages:

bash

pip install -r requirements.txt
Run the training notebook to reproduce the model:

bash

jupyter notebook notebooks/water_Quality_project.ipynb
Or launch the web application (requires the saved model artifact):

bash

streamlit run app.py
Model Artifact
The saved model file, water_potability_model.pkl, is expected to contain:

python

{
    "model": best_rf,
    "threshold": 0.36
}
The actual threshold is loaded from the saved artifact at runtime rather than hardcoded in the application.

Project Structure
text

aquaguard-water-potability/
├── app.py                          # Streamlit web application
├── water_potability_model.pkl      # Trained model + threshold
├── requirements.txt
├── README.md
└── notebooks/
    └── water_Quality_project.ipynb
Future Improvements
Add final threshold-based test metrics using the optimized threshold.
Improve recall and F1-score through further feature engineering and model evaluation.
Add batch prediction support (CSV upload for multiple samples).
Add prediction explanations using model interpretability tools (e.g., SHAP).
Deploy the application to Streamlit Community Cloud.
Evaluate the model on additional, representative water quality samples.
<div align="center">

💧 AquaGuard — Water Potability Prediction with Machine Learning

</div>
```
