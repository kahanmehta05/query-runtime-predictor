import psycopg2
import json
import time
import os
from datetime import datetime

def run_query_with_plan(db_name, query_path, output_dir):
    # ✅ PostgreSQL connection — adjust username if needed
    conn = psycopg2.connect(
        dbname=db_name,
        user='darshmehta',
        password='',
        host='localhost',
        port='5432'
    )

    cur = conn.cursor()

    with open(query_path, 'r') as f:
        query = f.read()

    print(f"\n[Running] {query_path}")

    try:
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

        print(f"[✓] Saved plan + runtime to {output_file}")
        print(f"[✓] Execution Time: {end_time - start_time:.3f} seconds")

    except Exception as e:
        print(f"❌ Error running query {query_path}: {e}")

    finally:
        cur.close()
        conn.close()


# ✅ Run all queries except 17 & 21
if __name__ == "__main__":
    folder = "db/queries"
    output_dir = "data/processed"
    os.makedirs(output_dir, exist_ok=True)

    for file in sorted(os.listdir(folder), key=lambda x: int(x.replace(".sql", ""))):
        if file.endswith(".sql"):
            query_num = int(file.replace(".sql", ""))
            if query_num in {17, 21}:
                print(f"⏭️  Skipping Query {query_num}")
                continue
            query_path = os.path.join(folder, file)
            run_query_with_plan(
                db_name="tpch",
                query_path=query_path,
                output_dir=output_dir
            )



