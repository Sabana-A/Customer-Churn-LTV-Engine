import joblib

# Load models
churn_model = joblib.load("models/churn_model.pkl")
ltv_model = joblib.load("models/ltv_model.pkl")

print("===== CHURN MODEL =====")
print("Model:", type(churn_model))
print("Number of features:", churn_model.n_features_in_)

if hasattr(churn_model, "feature_names_in_"):
    print("Features:")
    print(churn_model.feature_names_in_)

print()

print("===== LTV MODEL =====")
print("Model:", type(ltv_model))
print("Number of features:", ltv_model.n_features_in_)

if hasattr(ltv_model, "feature_names_in_"):
    print("Features:")
    print(ltv_model.feature_names_in_)