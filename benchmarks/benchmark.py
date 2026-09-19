import argparse
import json
import os
import random
import sqlite3
import tempfile
import time
from pathlib import Path

from stream.stream import get_connection, get_db_path, init_db, put_event, get_snapshot
from processor.processor import process_once

def seed(n:int):
    cities=["Mumbai","Pune","Delhi","Bengaluru","Chennai"]
    cats=["Electronics","Grocery","Fashion","Home"]
    for _ in range(n): put_event(random.choice(cities),random.choice(cats),random.uniform(10,5000))

def full_rescan():
    with get_connection() as conn:
        return conn.execute("SELECT city,category,COUNT(*) AS orders,SUM(amount) AS sales FROM events GROUP BY city,category").fetchall()

def run(n:int=5000):
    with tempfile.TemporaryDirectory() as td:
        os.environ["ANALYTICS_DB_PATH"]=str(Path(td)/"bench.db")
        init_db(); seed(n)
        t0=time.perf_counter(); full_rescan(); full_ms=(time.perf_counter()-t0)*1000
        t0=time.perf_counter(); processed=0
        while True:
            c=process_once(500); processed+=c
            if c==0: break
        inc_ms=(time.perf_counter()-t0)*1000
        result={"events":n,"full_rescan_ms":round(full_ms,3),"incremental_ms":round(inc_ms,3),"incremental_processed":processed,"snapshot":get_snapshot()}
        out=Path("benchmarks/results/latest.json"); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2))
        return result

if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--events",type=int,default=5000); a=p.parse_args(); print(json.dumps(run(a.events),indent=2))
