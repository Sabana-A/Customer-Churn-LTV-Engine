import io

import joblib
import pandas as pd

from fastapi import APIRouter, UploadFile, File, HTTPException


# ==========================================
# LOAD MODELS
# ==========================================

churn_model = joblib.load("models/churn_model.pkl")
ltv_model = joblib.load("models/ltv_model.pkl")


# ==========================================
# CREATE ROUTER
# ==========================================

router = APIRouter()


# ==========================================
# BATCH PREDICTION
# ==========================================

@router.post("/predict-batch")
async def predict_batch(file: UploadFile = File(...)):

    # Check CSV file
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a CSV file."
        )

    # Read uploaded CSV
    contents = await file.read()

    try:
        df = pd.read_csv(io.BytesIO(contents))
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to read the CSV file."
        )

    if len(df) == 0:
        raise HTTPException(
            status_code=400,
            detail="CSV file is empty."
        )

    # ==========================================
    # PREPARE DATA
    # ==========================================

    data = df.copy()

    # Remove target column if present
    if "Churn" in data.columns:
        data = data.drop(columns=["Churn"])

    # Remove customer ID
    if "customerID" in data.columns:
        data = data.drop(columns=["customerID"])

    # Convert TotalCharges to numeric
    if "TotalCharges" in data.columns:
        data["TotalCharges"] = pd.to_numeric(
            data["TotalCharges"],
            errors="coerce"
        )

        data["TotalCharges"] = data["TotalCharges"].fillna(
            data["MonthlyCharges"] * data["tenure"]
        )

    # ==========================================
    # ONE-HOT ENCODING
    # ==========================================

    data = pd.get_dummies(
        data,
        drop_first=True,
        dtype=int
    )

    # ==========================================
    # CHURN INPUT
    # ==========================================

    churn_data = data.copy()

    # Add missing model columns
    for column in churn_model.feature_names_in_:
        if column not in churn_data.columns:
            churn_data[column] = 0

    # Keep only model columns in correct order
    churn_data = churn_data[
        churn_model.feature_names_in_
    ]

    # ==========================================
    # CHURN PREDICTION
    # ==========================================

    churn_predictions = churn_model.predict(
        churn_data
    )

    churn_probabilities = churn_model.predict_proba(
        churn_data
    )[:, 1]

    # ==========================================
    # LTV INPUT
    # ==========================================

    ltv_data = data.copy()

    # Add missing LTV model columns
    for column in ltv_model.feature_names_in_:
        if column not in ltv_data.columns:
            ltv_data[column] = 0

    # Keep only LTV model columns
    ltv_data = ltv_data[
        ltv_model.feature_names_in_
    ]

    # ==========================================
    # LTV PREDICTION
    # ==========================================

    ltv_predictions = ltv_model.predict(
        ltv_data
    )

    # ==========================================
    # CREATE RESULTS
    # ==========================================

    results = pd.DataFrame({
        "churn_prediction": [
            "Churn" if prediction == 1
            else "No Churn"
            for prediction in churn_predictions
        ],

        "churn_probability": [
            round(float(probability), 4)
            for probability in churn_probabilities
        ],

        "predicted_ltv": [
            round(float(ltv), 2)
            for ltv in ltv_predictions
        ]
    })

    # ==========================================
    # RETURN RESULTS
    # ==========================================

    return {
        "total_customers": len(results),
        "predictions": results.to_dict(
            orient="records"
        )
    }