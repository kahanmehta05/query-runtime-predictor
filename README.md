
# 🚀 Query Runtime Predictor

A machine learning-based system to predict the runtime of SQL queries executed on PostgreSQL, built using TPC-H benchmark queries.

---

## 📦 Project Structure

```
query-runtime-predictor/
├── data/
│   ├── final_features_sample.csv        # Extracted features from queries
│   ├── final_features_extended.csv      # Features from extended queries
│   ├── final_features_all.csv           # Merged dataset (1–222 queries)
│   └── processed/                       # JSON plan files (1–22)
│   └── processed_extended/              # JSON plan files (23–222)
├── db/
│   ├── create_tpch_schema.sql
│   ├── load_tpch_data.sql
│   └── queries/                         # All SQL queries (Q1 to Q222)
├── scripts/
│   ├── extract_runtime_features.py      # Runs query and logs plan (JSON)
│   ├── extract_features_sample.py       # Extracts features → CSV
│   ├── run_all_queries.py
│   ├── run_missing_queries.py
│   └── split_new_queries.py
├── notebooks/
│   └── ...                              # For model training/analysis
├── models/
│   └── ...                              # Trained models or saved checkpoints
└── venv/                                # Python virtual environment
```

---

## 🔧 Setup Instructions (Any System)

### 1. 📥 Clone the Repository
```bash
git clone https://github.com/kahanmehta05/query-runtime-predictor.git
cd query-runtime-predictor
```

### 2. 🐍 Setup Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 📦 Install Dependencies
```bash
pip install pandas psycopg2-binary psutil
```

If `requirements.txt` exists:
```bash
pip install -r requirements.txt
```

---

## 🛠 PostgreSQL Setup

### 1. Launch PostgreSQL and Create Database
```sql
CREATE DATABASE tpch;
```

### 2. Create Schema and Load Data
Inside `psql`:
```bash
\i db/create_tpch_schema.sql
\i db/load_tpch_data.sql
```

---

## 📤 Run Scripts

### 1. Extract Runtime & Plan (for selected queries)
```bash
python scripts/extract_runtime_features.py --queries 1 2 3
```

### 2. Extract Features into CSV
```bash
python scripts/extract_features_sample.py
```

This generates `data/final_features_sample.csv`.

---

## ⚙️ Features Extracted

Includes both query-level and hardware-level features:
- Total cost
- Node counts (Seq Scan, Nested Loop, etc.)
- Cardinality error
- Actual vs estimated rows
- Query text
- Plan tree
- CPU cores, threads, RAM, frequency, disk I/O

---

## 🌐 Running on Another Machine

1. Clone the repo
2. Setup virtual env
3. Run:
   ```bash
   python scripts/extract_runtime_features.py
   python scripts/extract_features_sample.py
   ```
4. Push changes:
   ```bash
   git add data/final_features_sample.csv
   git commit -m "Added features from M2 Mac"
   git push
   ```

---

## 🤝 Contributing
1. Fork the repo
2. Create a new branch
3. Push and create a PR

---

## 👨‍🔬 Authors
- Kahan Mehta
- [Any collaborators here]

---

## 🧠 Research Goal
To build a machine-learning model that predicts query runtime across:
- Different hardware
- Different datasets
- Different query complexities

---

## 📄 License
MIT License (optional)

---
