import pandas as pd

out = pd.read_csv("data/processed/clean_heart_disease_county_age_year_1999_2020.csv")

# Look at rows with missing population
miss = out[out["population"].isna()].copy()

print("Missing population rows:", len(miss))
print(miss[["state","county","county_fips","year","age_group","deaths","suppressed","notes"]].head(20))

# Check what "Population" looked like in the raw export for those rows
raw = pd.read_csv("data/processed/combined_raw.csv")
raw.columns = [c.strip() for c in raw.columns]
raw_miss = raw[pd.to_numeric(raw["Year"], errors="coerce").notna()].copy()
raw_miss["Year"] = pd.to_numeric(raw_miss["Year"], errors="coerce").astype(int)


# align keys
raw_miss = raw_miss.rename(columns={
    "State": "state",
    "County": "county",
    "County Code": "county_code",
    "State Code": "state_fips",
    "Ten-Year Age Groups": "age_group",
    "Year": "year",
    "Population": "population_raw",
})

raw_miss["state_fips"] = raw_miss["state_fips"].astype(str).str.zfill(2)
raw_miss["county_code"] = raw_miss["county_code"].astype(str).str.zfill(3)
raw_miss["county_fips"] = raw_miss["state_fips"] + raw_miss["county_code"]

raw_bad = raw_miss[raw_miss["population_raw"].astype(str).str.strip().isin(["", "nan", "None"])]

print("Raw rows with blank population_raw:", len(raw_bad))
print(raw_bad[["state","county","county_fips","year","age_group","population_raw"]].head(20))

# Most useful: what are the actual raw strings?
raw_miss_pop = raw_miss[raw_miss["county_fips"].isin(miss["county_fips"].unique()) & raw_miss["year"].isin(miss["year"].unique())]
print(raw_miss_pop["population_raw"].astype(str).value_counts().head(20))
