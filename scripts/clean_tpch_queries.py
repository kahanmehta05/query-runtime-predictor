import os
import re

QUERY_DIR = "db/queries"

# Replace TPC-H parameter placeholders with actual values
REPLACEMENTS = {
    r":x": "",
    r":o": "",
    r":n": "",
    r":1": "90",
    r":2": "AUTOMOBILE",
    r":3": "15",
    r":4": "'1997-07-01'",
    r":5": "'ASIA'",
    r":6": "'FRANCE'",
    r":7": "1",
    r":8": "'BRAZIL'",
    r":9": "'green'",
    r"-1": "1",   # handle stray negative literals
    r"\b100\b": "100"  # prevent random loose 100s from failing
}

def clean_query_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    # Remove lines like ":x", ":o", etc.
    content = re.sub(r"^\s*:[a-z0-9]+\s*$", "", content, flags=re.MULTILINE)

    # Apply defined replacements
    for pattern, replacement in REPLACEMENTS.items():
        content = re.sub(pattern, replacement, content)

    with open(file_path, "w") as f:
        f.write(content)

    print(f"[✓] Cleaned {file_path}")

if __name__ == "__main__":
    for i in range(1, 23):
        path = os.path.join(QUERY_DIR, f"{i}.sql")
        if os.path.exists(path):
            clean_query_file(path)
        else:
            print(f"[!] Missing file: {path}")
