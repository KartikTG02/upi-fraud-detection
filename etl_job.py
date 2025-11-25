import pandas as pd
from sqlalchemy import create_engine
import time

print("--- Step 1: Generating Data")
import generate_upi_data

print("--- Step 2: Connecting to Docker Database ---")
db_engine = create_engine(
    'postgresql://admin:password123@localhost:5432/bank_data')
print("--- Step 3: Reading CSV ---")
df = pd.read_csv("upi_transactions_batch.csv")

print(f"-- Step 4: Uploading {len(df)} rows to PostgreSQL ---")
df.to_sql('transactions', db_engine, if_exists='replace', index=False)

print("✅ Success! Data is now inside the Database")