import time
import json
from kafka import KafkaProducer
from generate_upi_data import generate_transaction # We reuse your Level 1 code!

# --- TEACHING MOMENT: The Setup ---
# bootstrap_servers: Tells Python where Docker is running.
# value_serializer: The "Packer". It turns our Dictionary into Bytes.
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

print("--- 🚀 UPI Payment Stream Started ---")
print("Press Ctrl+C to stop.")

try:
    while True:
        # 1. Generate fake data
        transaction = generate_transaction()
        
        # 2. Send to Kafka
        # We send it to the topic named 'upi_transactions'
        producer.send('upi_transactions', value=transaction)
        
        # Print so we know it's working
        print(f"Sent: {transaction['transaction_id']} | Amount: ₹{transaction['amount_inr']}")
        
        # 3. Sleep for 1 second (Simulates real-time traffic)
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\n--- Stream Stopped ---")
    producer.close()