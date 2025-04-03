import os
import json
import psutil
import platform
import subprocess
import pandas as pd
import tempfile
import time

INPUT_DIR = "../data/processed"
OUTPUT_CSV = "../data/final_features_sample.csv"

# ✅ Disk write speed estimation (MB/s)
def estimate_disk_speed():
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            start = time.time()
            tmp.write(os.urandom(100 * 1024 * 1024))  # Write 100MB
            tmp.flush()
            os.fsync(tmp.fileno())
            end = time.time()
        os.remove(tmp.name)
        return round(100 / (end - start), 2)
    except:
        return 0.0

# ✅ Disk type: SSD or HDD
def detect_disk_type():
    try:
        system = platform.system()
        if system == "Darwin":
            return "SSD"
        elif system == "Linux":
            for device in os.listdir("/sys/block"):
                rotational_path = f"/sys/block/{device}/queue/rotational"
                if os.path.exists(rotational_path):
                    with open(rotational_path, "r") as f:
                        if f.read().strip() == "0":
                            return "SSD"
                        else:
                            return "HDD"
        elif system == "Windows":
            result = subprocess.run(
                ["powershell", "-Command", "Get-PhysicalDisk | Select-Object MediaType"],
                capture_output=True, text=True
            )
            if "SSD" in result.stdout:
                return "SSD"
            elif "HDD" in result.stdout:
                return "HDD"
    except:
        pass
    return "Unknown"

def get_cpu_freq_mhz():
    try:
        if platform.system() == "Darwin":
            if platform.machine() == "arm64":
                return 3200.0
            else:
                out = subprocess.check_output(["sysctl", "-n", "hw.cpufrequency"]).decode()
                return round(int(out.strip()) / 1_000_000, 2)
        elif psutil.cpu_freq() and psutil.cpu_freq().max:
            return round(psutil.cpu_freq().max, 2)
    except:
        pass
    return 0.0

# ✅ RAM, CPU, disk info
def get_hardware_features():
    return {
        "cpu_cores": psutil.cpu_count(logical=False),
        "cpu_threads": psutil.cpu_count(logical=True),
        "ram_gb": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        "available_ram_gb": round(psutil.virtual_memory().available / (1024 ** 3), 2),
        "cpu_freq_mhz": get_cpu_freq_mhz(),
        "os": platform.system(),
        "disk_speed_MBps": estimate_disk_speed(),
        "disk_type": detect_disk_type(),
        "cpu_util_percent": psutil.cpu_percent(interval=1)
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

# ✅ Extract features from all query JSONs
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

# ✅ Save to CSV
os.makedirs("data", exist_ok=True)
df = pd.DataFrame(data)
df.to_csv(OUTPUT_CSV, index=False)
print(f"\n✅ Final features saved to {OUTPUT_CSV}")
