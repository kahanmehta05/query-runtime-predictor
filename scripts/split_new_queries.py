import os

input_file = "db/newextend_queries.sql"
output_dir = "db/queries_extended"
os.makedirs(output_dir, exist_ok=True)

start_index = 23  # because we already have 1–22

with open(input_file, "r") as f:
    content = f.read()

# Split on semicolon, remove empty chunks
queries = [q.strip() + ";" for q in content.split(";") if q.strip()]

for i, query in enumerate(queries, start=start_index):
    filename = os.path.join(output_dir, f"{i}.sql")
    with open(filename, "w") as f:
        f.write(query)

print(f"✅ Split {len(queries)} queries into {output_dir}/")
