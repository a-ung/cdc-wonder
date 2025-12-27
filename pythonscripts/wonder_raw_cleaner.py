import pandas as pd
from glob import glob


RAW_GLOB = "data/raw/*.csv"
OUT_PATH = "data/processed/combined_raw.csv"

files = sorted(glob(RAW_GLOB))
if not files:
    raise SystemExit("No CSVs found in data/raw/")

dfs = []
for f in files:
    
    df = pd.read_csv(f)
    
    df.columns = [c.strip() for c in df.columns]

    df = df[pd.to_numeric(df["Year"], errors="coerce").notna()]

    dfs.append(df)

combined = pd.concat(dfs, ignore_index=True)

# Drop accidental repeated header rows (rare but possible)
combined = combined[combined["Year"].astype(str).str.lower() != "Year"]



combined.to_csv(OUT_PATH, index=False)
print("Files:", len(files))
print("Rows:", len(combined))
print("Saved:", OUT_PATH)



