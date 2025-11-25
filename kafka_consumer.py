import json
import redis
from kafka import KafkaConsumer
from sqlalchemy import create_engine, text

r = redis.Redis(host='localhost', port=6379, db=0)
db_engine = create_engine('postgresql://admin:password123@localhost:5432/bank_data')

consumer = KafkaConsumer(
    'upi_transactions',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')) # The "Unpacker"
)

print("--- 🕵️ Fraud Detector Listening... ---")

for message in consumer:
    txn = message.value
    user_id = txn['sender_vpa']
    amount = txn['amount_inr']
    txn_id = txn['transaction_id']
    
    risk_score = 0
    reasons = []

    if (r.get(user_id)):
        risk_score += 50
        reasons.append("Velocity Alert")
    r.setex(user_id, 10, "active")

    if amount > 50000:
        risk_score += 50
        reasons.append("High Amount")

    if risk_score >= 50:
        print(f"🚨 FRAUD: {txn_id} ({reasons})")
        with db_engine.connect() as conn:
            query = text(f"""
                INSERT INTO transactions (transaction_id, timestamp, sender_vpa, amount_inr, location, app_used, is_fraud_flag, flag_reason)
                VALUES ('{txn_id}', '{txn['timestamp']}', '{user_id}', '{amount}', '{txn['location']}', '{txn['app_used']}', 1, '{", ".join(reasons)}')
                """)
            conn.execute(query)
            conn.commit()

    else:
        print(f"✅ Safe: {txn_id}")