import psycopg2
import time
import json
import os
from datetime import datetime
import platform
import psutil
import subprocess

def get_hardware_info():
    return {
        "cpu_cores": psutil.cpu_count(logical=False),
        "cpu_threads": psutil.cpu_count(logical=True),
        "cpu_freq_mhz": psutil.cpu_freq().max if psutil.cpu_freq() else None,
        "ram_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "disk_type": "SSD" if platform.system() == "Darwin" else "Unknown",
        "os": platform.system()
    }

def run_query_with_json_output(query_path, db_name, output_dir):
    with open(query_path, 'r') as f:
        query = f.read()

    conn = psycopg2.connect(dbname=db_name, user="darshmehta", password="", host="localhost", port="5432")
    cur = conn.cursor()

    print(f"\n[Running] {query_path}")
    start_time = time.time()
    cur.execute("EXPLAIN (ANALYZE, FORMAT JSON) " + query)
    end_time = time.time()

    plan = cur.fetchone()[0][0]

    result = {
        "query": query,
        "execution_time": round(end_time - start_time, 3),
        "timestamp": datetime.now().isoformat(),
        "plan": plan,
        "hardware": get_hardware_info()
    }

    os.makedirs(output_dir, exist_ok=True)
    query_id = os.path.basename(query_path).replace(".sql", "")
    output_file = os.path.join(output_dir, f"{query_id}_plan.json")
    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)

    print(f"[✓] Saved: {output_file}")
    cur.close()
    conn.close()

if __name__ == "__main__":
    DB_NAME = "tpch"
    OUTPUT_DIR = "data/processed"
    MISSING_QUERIES = ["15", "17", "20", "21"]

    for qid in MISSING_QUERIES:
        path = f"db/queries/{qid}.sql"
        if os.path.exists(path):
            try:
                run_query_with_json_output(path, DB_NAME, OUTPUT_DIR)
            except Exception as e:
                print(f"[✗] Failed {qid}: {e}")
        else:
            print(f"[!] Missing file: {path}")
