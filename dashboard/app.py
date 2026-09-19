from flask import Flask, jsonify, render_template
from stream.stream import get_snapshot, init_db

app=Flask(__name__)
init_db()
@app.get("/")
def index(): return render_template("index.html")
@app.get("/api/health")
def health():
    try: init_db(); return jsonify({"status":"ok"})
    except Exception as exc: return jsonify({"status":"error","error":str(exc)}),500
@app.get("/api/analytics")
def analytics(): return jsonify(get_snapshot())
@app.get("/api/analytics/cities")
def cities(): return jsonify(get_snapshot()["cities"])
@app.get("/api/analytics/categories")
def categories(): return jsonify(get_snapshot()["categories"])
if __name__=="__main__": app.run(host="0.0.0.0",port=5000,debug=False)
