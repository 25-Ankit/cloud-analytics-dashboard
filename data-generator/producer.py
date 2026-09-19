import os, random, signal, time
from stream.stream import init_db, put_event

CITIES=["Mumbai","Delhi","Bengaluru","Pune","Hyderabad","Chennai"]
CATEGORIES=["Electronics","Fashion","Grocery","Home","Sports"]
running=True
def stop(signum,frame):
    global running; running=False
signal.signal(signal.SIGINT,stop); signal.signal(signal.SIGTERM,stop)
def main():
    interval=float(os.getenv("GENERATOR_INTERVAL","2")); init_db(); print(f"generator started interval={interval}s",flush=True)
    while running:
        eid=put_event(random.choice(CITIES),random.choice(CATEGORIES),round(random.uniform(100,5000),2))
        print(f"event={eid}",flush=True); time.sleep(interval)
if __name__=="__main__": main()
