import pandas as pd

IN_PATH = "data/processed/clean_heart_disease_county_age_year_1999_2020.csv"
OUT_PATH = "data/processed/mastertable_heart_disease_county_age_year_1999_2020.csv"

df = pd.read_csv(IN_PATH)


# --- flag invalid population rows (do not drop)
df["population_invalid"] = df["population"].isna()

# --- flag rows unusable for rate calculations
df["rate_eligible"] = (~df["suppressed"]) & (~df["population_invalid"])


df.to_csv(OUT_PATH, index=False)

df["rate_eligible"].value_counts()
df["population_invalid"].sum()
df["suppressed"].sum()

df.groupby("state")["population_invalid"].mean().sort_values(ascending=False).head()

df.sample(20)
df[df["population_invalid"]].sample(10)
df[df["suppressed"]].sample(10)
