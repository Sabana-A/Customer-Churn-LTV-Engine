import pandas as pd
from database import engine

# CSV file path
file_path = "data/telco_churn_cleaned.csv"

# Read cleaned dataset
df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Rows:", len(df))
print("Columns:", len(df.columns))

# Load data into PostgreSQL
df.to_sql(
    "telco_customer_churn",
    engine,
    if_exists="replace",
    index=False
)

print("Data loaded into PostgreSQL successfully!")
print("Table name: telco_customer_churn")