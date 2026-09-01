from flask import Flask, jsonify, render_template
import sqlite3
import json
import os

app = Flask(__name__)

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "stream",
    "events.db"
)


def get_analytics():
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
        if total_orders
        else 0
    )

    return {
        "total_orders": total_orders,
        "total_sales": total_sales,
        "average_order": average_order,
        "city_sales": city_sales,
        "category_sales": category_sales
    }


@app.route("/")
def dashboard():
    return render_template("index.html")


@app.route("/api/analytics")
def analytics():
    return jsonify(get_analytics())


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
