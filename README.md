# Customer Churn & LTV Engine

A machine learning project that predicts customer churn and estimates Customer Lifetime Value (LTV) using the Telco Customer Churn dataset.

## Project Overview

This project combines data analysis, machine learning, SQL, PostgreSQL, FastAPI, Docker, and Metabase to build an end-to-end customer churn analytics system.

The system helps identify customers who are likely to churn and provides insights into customer value.

## Dataset

- Dataset: Telco Customer Churn
- Total Customers: 7,043
- Churned Customers: 1,869
- Overall Churn Rate: 26.54%

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- SHAP
- PostgreSQL
- SQLAlchemy
- FastAPI
- Docker
- Metabase
- Power BI
- Git & GitHub

## Machine Learning

The project includes:

- Exploratory Data Analysis
- Data preprocessing
- Feature engineering
- Logistic Regression
- Random Forest
- XGBoost
- Model evaluation
- SHAP explainability
- Churn prediction
- Customer Lifetime Value estimation

## Database

Customer data is stored in PostgreSQL using Docker.

Database:

- PostgreSQL
- Database: `churn_db`
- Table: `telco_customer_churn`

## API

FastAPI is used to provide churn prediction through an API.

The API accepts customer information and returns a churn prediction.

## Dashboard

A Metabase dashboard was created to analyze customer churn.

Dashboard includes:

- Total Customers
- Churned Customers
- Churn Rate
- Churn by Contract
- Churn by Payment Method
- Churn by Internet Service
- Churn by Tech Support
- Churn by Online Security
- Churn by Senior Citizen

## Key Insights

- Overall churn rate is 26.54%.
- Month-to-month contract customers account for the largest number of churned customers.
- Electronic check has the highest number of churned customers among payment methods.
- Fiber optic customers account for the largest number of churned customers among internet service types.
- Customers without Tech Support show a high number of churned customers.

## Project Structure

```text
Customer-Churn-LTV-Engine/
│
├── data/
├── src/
├── models/
├── notebooks/
├── frontend/
├── README.md
└── requirements.txt