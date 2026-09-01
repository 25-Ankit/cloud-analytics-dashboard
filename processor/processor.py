import sqlite3
import json
import os

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "stream",
    "events.db"
)


def process_events():
    conn = sqlite3.connect(DB_PATH)

    rows = conn.execute("""
        SELECT event_data
        FROM events
        ORDER BY id
    """).fetchall()

    conn.close()

    total_orders = len(rows)
    total_sales = 0
    city_sales = {}
    category_sales = {}

    for row in rows:
        event = json.loads(row[0])

        amount = event["total_amount"]
        city = event["city"]
        category = event["category"]

        total_sales += amount

        city_sales[city] = city_sales.get(city, 0) + amount
        category_sales[category] = category_sales.get(category, 0) + amount

    average_order = (
        total_sales / total_orders
        if total_orders > 0
        else 0
    )

    print("\n========== CLOUD ANALYTICS ==========")
    print(f"Total Orders      : {total_orders}")
    print(f"Total Sales       : ₹{total_sales:,.2f}")
    print(f"Average Order     : ₹{average_order:,.2f}")

    print("\nSales by City:")
    for city, sales in city_sales.items():
        print(f"  {city}: ₹{sales:,.2f}")

    print("\nSales by Category:")
    for category, sales in category_sales.items():
        print(f"  {category}: ₹{sales:,.2f}")

    print("======================================")


if __name__ == "__main__":
    process_events()