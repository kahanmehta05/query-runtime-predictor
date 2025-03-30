import os
import psycopg2
import json
import time
from datetime import datetime

def run_query_with_plan(db_name, query_path, output_dir, user="darshmehta", password=""):
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()

        with open(query_path, 'r') as f:
            query = f.read()

        print(f"\n[Running] {query_path}")
        start_time = time.time()
        cur.execute("EXPLAIN (ANALYZE, FORMAT JSON) " + query)
        end_time = time.time()

        plan = cur.fetchone()[0][0]

        result = {
            "query": query,
            "execution_time": end_time - start_time,
            "timestamp": datetime.now().isoformat(),
            "plan": plan
        }

        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.basename(query_path).replace('.sql', '')
        output_file = os.path.join(output_dir, f"{base_name}_plan.json")
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)

        print(f"[✓] Saved {output_file} (runtime: {end_time - start_time:.3f}s)")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"[✗] Failed to run {query_path}: {e}")

if __name__ == "__main__":
    QUERY_DIR = "db/queries"
    OUTPUT_DIR = "data/processed"

    for i in range(1, 23):
        sql_file = os.path.join(QUERY_DIR, f"{i}.sql")
        if os.path.exists(sql_file):
            run_query_with_plan(
                db_name="tpch",
                query_path=sql_file,
                output_dir=OUTPUT_DIR
            )
        else:
            print(f"[!] Query file missing: {sql_file}")
