import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score

from xgboost import XGBClassifier


# ==========================================
# 1. LOAD DATASET
# ==========================================

file_path = "data/telco_churn_cleaned.csv"

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Rows:", len(df))
print("Columns:", len(df.columns))


# ==========================================
# 2. REMOVE CUSTOMER ID
# ==========================================

if "customerID" in df.columns:
    df = df.drop(columns=["customerID"])


# ==========================================
# 3. CONVERT TARGET
# ==========================================

df["Churn"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
})


# ==========================================
# 4. SEPARATE FEATURES AND TARGET
# ==========================================

X = df.drop(columns=["Churn"])
y = df["Churn"]


# ==========================================
# 5. ONE-HOT ENCODING
# ==========================================

X = pd.get_dummies(
    X,
    drop_first=True,
    dtype=int
)


print("Encoded features:", len(X.columns))


# ==========================================
# 6. TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))


# ==========================================
# 7. LOGISTIC REGRESSION
# ==========================================

logistic_model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

logistic_model.fit(X_train, y_train)

logistic_prediction = logistic_model.predict(X_test)


# ==========================================
# 8. RANDOM FOREST
# ==========================================

random_forest_model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

random_forest_model.fit(X_train, y_train)

random_forest_prediction = random_forest_model.predict(X_test)


# ==========================================
# 9. XGBOOST
# ==========================================

xgb_model = XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    eval_metric="logloss"
)

xgb_model.fit(X_train, y_train)

xgb_prediction = xgb_model.predict(X_test)


# ==========================================
# 10. MODEL EVALUATION FUNCTION
# ==========================================

def evaluate_model(model_name, y_true, y_pred):

    precision = precision_score(
        y_true,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_true,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_true,
        y_pred,
        zero_division=0
    )

    print("\n" + "=" * 45)
    print(model_name)
    print("=" * 45)

    print("Precision:", round(precision, 4))
    print("Recall   :", round(recall, 4))
    print("F1 Score :", round(f1, 4))

    return {
        "Model": model_name,
        "Precision": precision,
        "Recall": recall,
        "F1_Score": f1
    }


# ==========================================
# 11. EVALUATE ALL MODELS
# ==========================================

results = []

results.append(
    evaluate_model(
        "Logistic Regression",
        y_test,
        logistic_prediction
    )
)

results.append(
    evaluate_model(
        "Random Forest",
        y_test,
        random_forest_prediction
    )
)

results.append(
    evaluate_model(
        "XGBoost",
        y_test,
        xgb_prediction
    )
)


# ==========================================
# 12. CREATE RESULTS TABLE
# ==========================================

results_df = pd.DataFrame(results)

print("\n")
print("MODEL COMPARISON")
print("=" * 60)
print(results_df.to_string(index=False))


# ==========================================
# 13. SAVE XGBOOST MODEL
# ==========================================

joblib.dump(
    xgb_model,
    "models/xgboost_churn_model.pkl"
)

print("\nXGBoost model saved successfully!")

print(
    "File: models/xgboost_churn_model.pkl"
)


# ==========================================
# 14. SAVE MODEL RESULTS
# ==========================================

results_df.to_csv(
    "models/churn_model_comparison.csv",
    index=False
)

print(
    "Model comparison saved successfully!"
)

print(
    "File: models/churn_model_comparison.csv"
)