import pandas as pd
import random
import time
from datetime import datetime, timedelta

banks = ['@okhdfc', '@oksbi','@paytm', '@ybl', '@axl']
apps = ['GooglePay', 'PhonePay', 'PayTm', 'Cred']
locations = ['Mumbai', 'Delhi', 'Bangalore', 'Pune', 'Hyderabad', 'Chennai', 'Kolkata']
fraud_locations = ['Jamtara', 'Mewat', 'Bharatpur']

def generate_vpa():
    names = ['rahul', 'mehul', 'swapnil', 'tommy', 'rajesh', 'amit', 'sneha', 'vikram', 'anita', 'rohit', 'meera']
    return f"{random.choice(names)}{random.randint(1,999)}{random.choice(banks)}"

def generate_transaction():
    is_fraud = random.random() < 0.05

    if is_fraud:
        amount = random.randint(10000, 100000)
        location = random.choice(fraud_locations) if random.random() > 0.5 else random.choice(locations)
        category = "Phishing"
    else:
        amount = random.randint(10, 5000)
        location = random.choice(locations)
        category = random.choice(['Groceries', 'Food', 'Travel', 'Utilities'])
    
    return {
        "transaction_id": f"TXN{int(time.time()*10000)}",
        "timestamp": datetime.now().isoformat(),
        "sender_vpa": generate_vpa(),
        "amount_inr": amount,
        "location": location,
        "app_used": random.choice(apps),
        "is_fraud_flag": 1 if is_fraud else 0
    }

data = []
print("generating 1000 UPI transactions...")
for _ in range(1000):
    data.append(generate_transaction())

df = pd.DataFrame(data)
df.to_csv("upi_transactions_batch.csv", index=False)
print("Data saved to 'upi_transactions_batch.csv'")
print(df.head())