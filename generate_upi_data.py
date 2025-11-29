import random
import time
from datetime import datetime

users = [
    {'vpa': 'amit@oksbi', 'name': 'Amit'},
    {'vpa': 'priya@paytm', 'name': 'Priya'},
    {'vpa': 'raj@axl', 'name': 'Raj'}
]

apps = ['GooglePay', 'PhonePe', 'PayTm']
locations = ['Mumbai', 'Delhi', 'Bangalore']

def generate_transaction():
    user = random.choice(users)
    amount = random.randint(500, 60000)

    return {
        "transaction_id": f"TXN{int(time.time()*1000)}",
        "timestamp": datetime.now().isoformat(),
        "sender_vpa": user['vpa'],
        "amount_inr": amount,
        "location": random.choice(locations),
        "app_used": random.choice(apps)
    }