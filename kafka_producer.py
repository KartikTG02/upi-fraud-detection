import time
import json
from kafka import KafkaProducer
from generate_upi_data import generate_transaction 

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

print("--- 🚀 UPI Payment Stream Started ---")
print("Press Ctrl+C to stop.")

try:
    while True:

        transaction = generate_transaction()
        producer.send('upi_transactions', value=transaction)
        print(f"Sent: {transaction['transaction_id']} | Amount: ₹{transaction['amount_inr']}")
        time.sleep(1)

except KeyboardInterrupt:
    print("\n--- Stream Stopped ---")
    producer.close()