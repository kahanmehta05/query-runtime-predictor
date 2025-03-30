import os
import json
import psutil
import platform
import pandas as pd

INPUT_DIR = "data/processed"
OUTPUT_CSV = "data/final_features_sample.csv"

def get_hardware_features():
    try:
        io = psutil.disk_io_counters()
        disk_speed = round(io.read_time + io.write_time, 2)
    except Exception:
        disk_speed = "Unknown"

    return {
        "cpu_cores": psutil.cpu_count(logical=False),
        "cpu_threads": psutil.cpu_count(logical=True),
        "ram_gb": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        "cpu_freq_mhz": round(psutil.cpu_freq().max if psutil.cpu_freq() else 0, 2),
        "os": platform.system(),
        "disk_speed_ms": disk_speed
    }

def count_plan_nodes(plan, node_counts, additional_features):
    node_type = plan.get("Node Type")
    if node_type:
        node_counts[node_type] = node_counts.get(node_type, 0) + 1

    if node_type == "Sort" and "Sort Method" in plan:
        additional_features["sort_method"] = plan["Sort Method"]

    if "Actual Rows" in plan:
        additional_features["actual_rows"] = plan["Actual Rows"]
    if "Actual Loops" in plan:
        additional_features["actual_loops"] = plan["Actual Loops"]
    if "Startup Cost" in plan:
        additional_features["startup_cost"] = plan["Startup Cost"]
    if "Plan Rows" in plan:
        additional_features["plan_rows"] = plan["Plan Rows"]

    if "Plans" in plan:
        for subplan in plan["Plans"]:
            count_plan_nodes(subplan, node_counts, additional_features)

data = []

for filename in sorted(os.listdir(INPUT_DIR)):
    if not filename.endswith("_plan.json"):
        continue

    path = os.path.join(INPUT_DIR, filename)

    try:
        with open(path, "r") as f:
            json_data = json.load(f)

        plan_root = json_data["plan"].get("Plan")
        if not plan_root:
            raise ValueError("No root 'Plan' node found")

        query_id = filename.split("_")[0].strip()
        runtime = json_data.get("execution_time", None)
        timestamp = json_data.get("timestamp", "")
        raw_query = json_data.get("query", "").strip()
        raw_plan_tree = json.dumps(plan_root, indent=2)

        node_counts = {}
        additional = {
            "actual_rows": 0,
            "actual_loops": 0,
            "startup_cost": 0,
            "plan_rows": 0,
            "sort_method": "None"
        }
        count_plan_nodes(plan_root, node_counts, additional)

        plan_rows = additional["plan_rows"] or 1
        card_error = round(additional["actual_rows"] / plan_rows, 4)

        features = {
            "query_id": f"Q{query_id}",
            "execution_time": runtime,
            "timestamp": timestamp,
            "query_text": raw_query,
            "plan_tree": raw_plan_tree,
            "total_cost": plan_root.get("Total Cost", 0),
            "Seq Scan_count": node_counts.get("Seq Scan", 0),
            "Index Scan_count": node_counts.get("Index Scan", 0),
            "Index Only Scan_count": node_counts.get("Index Only Scan", 0),
            "Nested Loop_count": node_counts.get("Nested Loop", 0),
            "Hash Join_count": node_counts.get("Hash Join", 0),
            "Merge Join_count": node_counts.get("Merge Join", 0),
            "Sort_count": node_counts.get("Sort", 0),
            "Aggregate_count": node_counts.get("Aggregate", 0),
            "actual_rows": additional["actual_rows"],
            "actual_loops": additional["actual_loops"],
            "startup_cost": additional["startup_cost"],
            "plan_rows": plan_rows,
            "cardinality_error": card_error,
            "sort_method": additional["sort_method"]
        }

        features.update(get_hardware_features())
        data.append(features)
        print(f"✅ Extracted: {filename}")

    except Exception as e:
        print(f"❌ Could not read plan from {path}: {e}")

# Save output CSV
os.makedirs("data", exist_ok=True)
df = pd.DataFrame(data)
df.to_csv(OUTPUT_CSV, index=False)
print(f"\n✅ Final features saved to {OUTPUT_CSV}")
