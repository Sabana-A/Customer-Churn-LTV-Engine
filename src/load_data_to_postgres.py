import pandas as pd
from src.database import engine

# Read cleaned CSV
file_path = "data/telco_churn_cleaned.csv"
df = pd.read_csv(file_path)

print("CSV loaded successfully!")
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