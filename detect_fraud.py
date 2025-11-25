import pandas as pd

df = pd.read_csv("upi_transactions_batch.csv")

def apply_fraud_rules(row):
    reasons = []
    risk_score = 0

    suspicious_locations = ['Jamtara', 'Mewat', 'Bharatpur']
    if row['location'] in suspicious_locations:
        risk_score += 50
        reasons.append(f"High Risk Location ({row['location']})")

    if row['amount_inr'] > 50000:
        risk_score += 30
        reasons.append("High Transaction Amount")
    
    return risk_score, '; '.join(reasons)

df[['risk_score', 'flag_reason']] = df.apply(
    lambda row: pd.Series(apply_fraud_rules(row)), axis=1
)

suspected_fraud = df[df['risk_score'] > 40]

print(f"Total Transactions Scanned:{len(df)}")
print(f"Suspected Fraud Cases: {len(suspected_fraud)}")
print("\n--- FLAG REPORT ---")
print(suspected_fraud[['transaction_id', 'amount_inr', 'location', 'flag_reason']])
suspected_fraud.to_csv('suspected_fraud_list.csv', index=False)