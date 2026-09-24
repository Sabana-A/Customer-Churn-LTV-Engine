from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd

from src.api.batch_prediction import router as batch_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(batch_router)

# =========================
# LOAD TRAINED MODELS
# =========================

churn_model = joblib.load("models/churn_model.pkl")
ltv_model = joblib.load("models/ltv_model.pkl")


# =========================
# CHURN INPUT DATA
# =========================

class CustomerData(BaseModel):
    SeniorCitizen: int
    tenure: int
    MonthlyCharges: float
    TotalCharges: float

    gender_Male: int
    Partner_Yes: int
    Dependents_Yes: int
    PhoneService_Yes: int

    MultipleLines_No_phone_service: int
    MultipleLines_Yes: int

    InternetService_Fiber_optic: int
    InternetService_No: int

    OnlineSecurity_No_internet_service: int
    OnlineSecurity_Yes: int

    OnlineBackup_No_internet_service: int
    OnlineBackup_Yes: int

    DeviceProtection_No_internet_service: int
    DeviceProtection_Yes: int

    TechSupport_No_internet_service: int
    TechSupport_Yes: int

    StreamingTV_No_internet_service: int
    StreamingTV_Yes: int

    StreamingMovies_No_internet_service: int
    StreamingMovies_Yes: int

    Contract_One_year: int
    Contract_Two_year: int

    PaperlessBilling_Yes: int

    PaymentMethod_Credit_card_automatic: int
    PaymentMethod_Electronic_check: int
    PaymentMethod_Mailed_check: int


# =========================
# LTV INPUT DATA
# =========================

class LTVData(BaseModel):
    SeniorCitizen: int
    tenure: int
    MonthlyCharges: float

    gender_Male: int
    Partner_Yes: int
    Dependents_Yes: int
    PhoneService_Yes: int

    MultipleLines_No_phone_service: int
    MultipleLines_Yes: int

    InternetService_Fiber_optic: int
    InternetService_No: int

    OnlineSecurity_No_internet_service: int
    OnlineSecurity_Yes: int

    OnlineBackup_No_internet_service: int
    OnlineBackup_Yes: int

    DeviceProtection_No_internet_service: int
    DeviceProtection_Yes: int

    TechSupport_No_internet_service: int
    TechSupport_Yes: int

    StreamingTV_No_internet_service: int
    StreamingTV_Yes: int

    StreamingMovies_No_internet_service: int
    StreamingMovies_Yes: int

    Contract_One_year: int
    Contract_Two_year: int

    PaperlessBilling_Yes: int

    PaymentMethod_Credit_card_automatic: int
    PaymentMethod_Electronic_check: int
    PaymentMethod_Mailed_check: int

    TenureGroup_13_24_Months: int
    TenureGroup_25_48_Months: int
    TenureGroup_49_72_Months: int


# =========================
# HOME
# =========================

@app.get("/")
def home():
    return {"message": "API is running"}


# =========================
# CHURN PREDICTION
# =========================

@app.post("/predict-churn")
def predict_churn(customer: CustomerData):

    data = customer.model_dump()

    input_data = pd.DataFrame([data])

    input_data = input_data.rename(columns={

        "MultipleLines_No_phone_service":
            "MultipleLines_No phone service",

        "InternetService_Fiber_optic":
            "InternetService_Fiber optic",

        "OnlineSecurity_No_internet_service":
            "OnlineSecurity_No internet service",

        "OnlineBackup_No_internet_service":
            "OnlineBackup_No internet service",

        "DeviceProtection_No_internet_service":
            "DeviceProtection_No internet service",

        "TechSupport_No_internet_service":
            "TechSupport_No internet service",

        "StreamingTV_No_internet_service":
            "StreamingTV_No internet service",

        "StreamingMovies_No_internet_service":
            "StreamingMovies_No internet service",

        "Contract_One_year":
            "Contract_One year",

        "Contract_Two_year":
            "Contract_Two year",

        "PaymentMethod_Credit_card_automatic":
            "PaymentMethod_Credit card (automatic)",

        "PaymentMethod_Electronic_check":
            "PaymentMethod_Electronic check",

        "PaymentMethod_Mailed_check":
            "PaymentMethod_Mailed check"
    })

    input_data = input_data[churn_model.feature_names_in_]

    prediction = churn_model.predict(input_data)[0]

    probability = churn_model.predict_proba(input_data)[0][1]

    if prediction == 1:
        result = "Churn"
    else:
        result = "No Churn"

    return {
        "prediction": result,
        "churn_probability": round(float(probability), 4)
    }


# =========================
# LTV PREDICTION
# =========================

@app.post("/predict-ltv")
def predict_ltv(customer: LTVData):

    data = customer.model_dump()

    input_data = pd.DataFrame([data])

    input_data = input_data.rename(columns={

        "MultipleLines_No_phone_service":
            "MultipleLines_No phone service",

        "InternetService_Fiber_optic":
            "InternetService_Fiber optic",

        "OnlineSecurity_No_internet_service":
            "OnlineSecurity_No internet service",

        "OnlineBackup_No_internet_service":
            "OnlineBackup_No internet service",

        "DeviceProtection_No_internet_service":
            "DeviceProtection_No internet service",

        "TechSupport_No_internet_service":
            "TechSupport_No internet service",

        "StreamingTV_No_internet_service":
            "StreamingTV_No internet service",

        "StreamingMovies_No_internet_service":
            "StreamingMovies_No internet service",

        "Contract_One_year":
            "Contract_One year",

        "Contract_Two_year":
            "Contract_Two year",

        "PaymentMethod_Credit_card_automatic":
            "PaymentMethod_Credit card (automatic)",

        "PaymentMethod_Electronic_check":
            "PaymentMethod_Electronic check",

        "PaymentMethod_Mailed_check":
            "PaymentMethod_Mailed check",

        "TenureGroup_13_24_Months":
            "TenureGroup_13-24 Months",

        "TenureGroup_25_48_Months":
            "TenureGroup_25-48 Months",

        "TenureGroup_49_72_Months":
            "TenureGroup_49-72 Months"
    })

    input_data = input_data[ltv_model.feature_names_in_]

    ltv_prediction = ltv_model.predict(input_data)[0]

    return {
        "predicted_ltv": round(float(ltv_prediction), 2)
    }
# =========================
# COMBINED CHURN + LTV
# =========================

@app.post("/predict")
def predict(customer: LTVData):

    data = customer.model_dump()

    # -------------------------
    # CHURN PREDICTION
    # -------------------------

    churn_data = data.copy()

    # LTV input does not contain TotalCharges.
    # Use MonthlyCharges × tenure as an approximate TotalCharges
    churn_data["TotalCharges"] = (
        churn_data["MonthlyCharges"] * churn_data["tenure"]
    )

    churn_input = pd.DataFrame([churn_data])

    churn_input = churn_input.rename(columns={
        "MultipleLines_No_phone_service":
            "MultipleLines_No phone service",

        "InternetService_Fiber_optic":
            "InternetService_Fiber optic",

        "OnlineSecurity_No_internet_service":
            "OnlineSecurity_No internet service",

        "OnlineBackup_No_internet_service":
            "OnlineBackup_No internet service",

        "DeviceProtection_No_internet_service":
            "DeviceProtection_No internet service",

        "TechSupport_No_internet_service":
            "TechSupport_No internet service",

        "StreamingTV_No_internet_service":
            "StreamingTV_No internet service",

        "StreamingMovies_No_internet_service":
            "StreamingMovies_No internet service",

        "Contract_One_year":
            "Contract_One year",

        "Contract_Two_year":
            "Contract_Two year",

        "PaymentMethod_Credit_card_automatic":
            "PaymentMethod_Credit card (automatic)",

        "PaymentMethod_Electronic_check":
            "PaymentMethod_Electronic check",

        "PaymentMethod_Mailed_check":
            "PaymentMethod_Mailed check"
    })

    # Remove LTV-only columns
    churn_input = churn_input.drop(columns=[
        "TenureGroup_13_24_Months",
        "TenureGroup_25_48_Months",
        "TenureGroup_49_72_Months"
    ])

    churn_input = churn_input[churn_model.feature_names_in_]

    churn_prediction = churn_model.predict(churn_input)[0]

    churn_probability = churn_model.predict_proba(churn_input)[0][1]

    if churn_prediction == 1:
        churn_result = "Churn"
    else:
        churn_result = "No Churn"

    # -------------------------
    # LTV PREDICTION
    # -------------------------

    ltv_input = pd.DataFrame([data])

    ltv_input = ltv_input.rename(columns={
        "MultipleLines_No_phone_service":
            "MultipleLines_No phone service",

        "InternetService_Fiber_optic":
            "InternetService_Fiber optic",

        "OnlineSecurity_No_internet_service":
            "OnlineSecurity_No internet service",

        "OnlineBackup_No_internet_service":
            "OnlineBackup_No internet service",

        "DeviceProtection_No_internet_service":
            "DeviceProtection_No internet service",

        "TechSupport_No_internet_service":
            "TechSupport_No internet service",

        "StreamingTV_No_internet_service":
            "StreamingTV_No internet service",

        "StreamingMovies_No_internet_service":
            "StreamingMovies_No internet service",

        "Contract_One_year":
            "Contract_One year",

        "Contract_Two_year":
            "Contract_Two year",

        "PaymentMethod_Credit_card_automatic":
            "PaymentMethod_Credit card (automatic)",

        "PaymentMethod_Electronic_check":
            "PaymentMethod_Electronic check",

        "PaymentMethod_Mailed_check":
            "PaymentMethod_Mailed check",

        "TenureGroup_13_24_Months":
            "TenureGroup_13-24 Months",

        "TenureGroup_25_48_Months":
            "TenureGroup_25-48 Months",

        "TenureGroup_49_72_Months":
            "TenureGroup_49-72 Months"
    })

    ltv_input = ltv_input[ltv_model.feature_names_in_]

    ltv_prediction = ltv_model.predict(ltv_input)[0]

    # -------------------------
    # FINAL RESPONSE
    # -------------------------

    return {
        "churn_prediction": churn_result,
        "churn_probability": round(float(churn_probability), 4),
        "predicted_ltv": round(float(ltv_prediction), 2)
    }