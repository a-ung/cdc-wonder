import pandas as pd
import numpy as np

IN_PATH = "data/processed/combined_raw.csv"
OUT_PATH = "data/processed/clean_heart_disease_county_age_year_1999_2020.csv"


df = pd.read_csv(IN_PATH)
df.columns = [c.strip() for c in df.columns]


# --- Keep only true data rows (Year must be numeric) 
df["Year_num"] = pd.to_numeric(df["Year"], errors="coerce")
df = df[df["Year_num"].notna()].copy()
df["Year"] = df["Year_num"].astype(int)
df = df.drop(columns=["Year_num"])


# --- Standardize/rename columns
df = df.rename(columns={
    "State": "state",
    "State Code": "state_fips",
    "County": "county",
    "County Code": "county_code",
    "Ten-Year Age Groups": "age_group",
    "Ten-Year Age Groups Code": "age_group_code",
    "Year": "year",
    "Year Code": "year_code",
    "Deaths": "deaths_raw",
    "Population": "population_raw",
    "Crude Rate": "crude_rate_raw",
    "Notes": "notes",
})


# --- Build county_fips (state_fips 2 digits + county_code 3 digits)
df["state_fips"] = df["state_fips"].astype(str).str.strip().str.zfill(2)
df["county_code"] = df["county_code"].astype(str).str.strip().str.zfill(3)
df["county_fips"] = df["state_fips"] + df["county_code"]


# --- Deaths: keep 0, mark Suppressed as NA
df["suppressed"] = df["deaths_raw"].astype(str).str.contains("suppressed", case=False, na=False)
df["deaths"] = pd.to_numeric(df["deaths_raw"].where(~df["suppressed"], np.nan), errors="coerce")


# --- Population: numeric (should not be suppressed)
df["population"] = pd.to_numeric(
    df["population_raw"].astype(str).str.replace(",", "", regex=False).str.strip(),
    errors="coerce"
)


# --- Crude rate: numeric when possible; 'Unreliable' becomes NA
df["crude_rate"] = pd.to_numeric(
    df["crude_rate_raw"].astype(str).str.replace(",", "", regex=False).str.strip(),
    errors="coerce"
)


# --- Type cleanup
df["year"] = df["year"].astype(int)
df["age_group"] = df["age_group"].astype(str).str.strip()
df["age_group_code"] = df["age_group_code"].astype(str).str.strip()
df["year_code"] = df["year_code"].astype(str).str.strip()



out = df[[
    "state", "state_fips",
    "county", "county_fips",
    "age_group", "age_group_code",
    "year", "year_code",
    "deaths", "population", "crude_rate",
    "suppressed",
    "notes"
]].copy()


# --- Sanity checks
print("Rows:", len(out))
print("States:", out["state"].nunique())
print("Unique county_fips:", out["county_fips"].nunique())
print("Year range:", out["year"].min(), "-", out["year"].max())
print("Suppressed rows:", int(out["suppressed"].sum()))
print("Population missing:", int(out["population"].isna().sum()))
print("Deaths missing (includes suppressed):", int(out["deaths"].isna().sum()))


# --- Warn if population missing
if out["population"].isna().any():
    print("WARNING: Some population values are missing. Check raw exports.")



out.to_csv(OUT_PATH, index=False)
print("Saved:", OUT_PATH)

