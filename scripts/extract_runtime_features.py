import psycopg2
import json
import time
import os
from datetime import datetime

def run_query_with_plan(db_name, query_path, output_dir):
    # ✅ PostgreSQL connection - using your actual macOS username
    conn = psycopg2.connect(
        dbname=db_name,
        user='darshmehta',     # ✅ Update here
        password='',            # ✅ Leave blank if no password
        host='localhost',
        port='5432'
    )

    cur = conn.cursor()

    # Read SQL query from file
    with open(query_path, 'r') as f:
        query = f.read()

    print(f"\n[Running] {query_path}")
    
    # Run query with EXPLAIN ANALYZE and time it
    start_time = time.time()
    cur.execute("EXPLAIN (ANALYZE, FORMAT JSON) " + query)
    end_time = time.time()

    plan = cur.fetchone()[0][0]  # Get the actual plan

    # Build result
    result = {
        "query": query,
        "execution_time": end_time - start_time,
        "timestamp": datetime.now().isoformat(),
        "plan": plan
    }

    # Ensure output folder exists
    os.makedirs(output_dir, exist_ok=True)

    # Save result
    base_name = os.path.basename(query_path).replace('.sql', '')
    output_file = os.path.join(output_dir, f"{base_name}_plan.json")
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"[✓] Saved plan + runtime to {output_file}")
    print(f"[✓] Execution Time: {end_time - start_time:.3f} seconds")

    # Clean up
    cur.close()
    conn.close()

# Run example (23 o 223)
if __name__ == "__main__":
    folder = "db/queries_extended"
    output_dir = "data/processed_extended"
    os.makedirs(output_dir, exist_ok=True)

    for file in sorted(os.listdir(folder)):
        if file.endswith(".sql"):
            query_path = os.path.join(folder, file)
            run_query_with_plan(
                db_name="tpch",
                query_path=query_path,
                output_dir=output_dir
            )


