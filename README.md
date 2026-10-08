# 🏠 Bengaluru House Price Predictor

An end-to-end **Machine Learning regression project** that predicts residential property prices in Bengaluru using property characteristics such as location, area, BHK, bathrooms, balconies, and area type.

The project focuses on the complete ML workflow:

**Data Cleaning → EDA → Feature Engineering → Model Training → Evaluation → Model Persistence → Deployment**

🔗 **Live App:** https://bengaluru-house-price-predictor-cdahquhwxd2wgn7dxxvkeu.streamlit.app/

---

# 🤖 Machine Learning

The core of this project is a **regression-based machine learning pipeline** for predicting house prices.

### What I used

- Supervised Machine Learning
- Regression
- Linear Regression as a baseline
- Random Forest Regression
- Train/Test Split
- Categorical Encoding
- `OneHotEncoder`
- `ColumnTransformer`
- Scikit-learn `Pipeline`
- Log transformation of the target variable
- Random Forest ensemble learning
- MAE, RMSE and R² for evaluation
- Permutation Feature Importance
- Error Analysis
- Joblib model serialization

---

## 🧠 ML Pipeline

The final prediction pipeline follows:

```text
Raw Property Data
        ↓
Data Cleaning
        ↓
EDA
        ↓
Feature Engineering
        ↓
Train / Test Split
        ↓
Categorical Encoding
        ↓
Preprocessing Pipeline
        ↓
Random Forest Regression
        ↓
Log-Transformed Target
        ↓
Prediction
        ↓
Inverse Transformation
        ↓
Estimated House Price
