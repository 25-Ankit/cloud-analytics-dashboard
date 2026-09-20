import os
import random
import signal
import time

from stream.stream import init_db, put_event

CITIES = ["Mumbai", "Delhi", "Bengaluru", "Pune", "Hyderabad", "Chennai"]
CATEGORIES = ["Electronics", "Fashion", "Grocery", "Home", "Sports"]

running = True


def stop_handler(signum, frame):
    global running
    running = False


signal.signal(signal.SIGINT, stop_handler)
signal.signal(signal.SIGTERM, stop_handler)


def main():
    interval = float(os.getenv("GENERATOR_INTERVAL", "2"))
    init_db()
    print(f"generator started; interval={interval}s", flush=True)

    while running:
        city = random.choice(CITIES)
        category = random.choice(CATEGORIES)
        amount = round(random.uniform(100, 5000), 2)
        event_id = put_event(city, category, amount)
        print(f"event={event_id} city={city} category={category} amount={amount}", flush=True)
        time.sleep(interval)

    print("generator stopped", flush=True)


if __name__ == "__main__":
    main()
