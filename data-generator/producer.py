import json
import random
import time
import os
import sys

from datetime import datetime, timezone
from faker import Faker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from stream.stream import put_event

fake = Faker()

PRODUCTS = [
    ("Laptop", "Electronics", 55000),
    ("Smartphone", "Electronics", 25000),
    ("Headphones", "Accessories", 3000),
    ("Monitor", "Electronics", 18000),
    ("Keyboard", "Accessories", 2500),
    ("Mouse", "Accessories", 1200),
    ("Tablet", "Electronics", 22000),
    ("Smartwatch", "Wearables", 8000),
]

CITIES = [
    "Mumbai",
    "Delhi",
    "Bangalore",
    "Pune",
    "Hyderabad",
    "Chennai",
]


def generate_sale():
    product, category, price = random.choice(PRODUCTS)
    quantity = random.randint(1, 5)

    sale = {
        "transaction_id": fake.uuid4(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "product": product,
        "category": category,
        "quantity": quantity,
        "price": price,
        "total_amount": quantity * price,
        "city": random.choice(CITIES),
    }

    return sale


if __name__ == "__main__":
    print("Starting Cloud Analytics Data Generator...")
    print("Sending events to Local Kinesis Stream...")
    print("Press CTRL+C to stop.\n")

    try:
        while True:
            sale = generate_sale()

            # Send event to our local stream
            put_event(sale)

            print("Event sent:")
            print(json.dumps(sale, indent=2))
            print("-" * 50)

            time.sleep(2)

    except KeyboardInterrupt:
        print("\nData generator stopped.")