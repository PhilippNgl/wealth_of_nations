import os
import pandas as pd

# -----------------------------
# Configuration
# -----------------------------
RAW_DIR = "data/raw"
OUT_DIR = "analysis/02_final/_data"

FILES = {
    "gdp_per_capita_usd": "API_NY.GDP.PCAP.CD_DS2_en_csv_v2_",
    "life_expectancy_years": "API_SP.DYN.LE00.IN_DS2_en_csv_v2_",
    "co2_tons_per_capita": "API_EN.ATM.CO2E.PC_DS2_en_csv_v2_",
    "health_exp_pc_usd": "API_SH.XPD.CHEX.PC.CD_DS2_en_csv_v2_",
    "fertility_rate": "API_SP.DYN.TFRT.IN_DS2_en_csv_v2_",
    "child_mortality": "API_SH.DYN.MORT_DS2_en_csv_v2_",
    "urban_population_pct": "API_SP.URB.TOTL.IN.ZS_DS2_en_csv_v2_"
}


COUNTRIES = ["DEU", "ITA", "FRA", "GBR", "USA", "CHN", "JPN", "NGA", "IND", "BRA"]
START_YEAR, END_YEAR = 2000, 2023

# -----------------------------
# Load and reshape each indicator
# -----------------------------
frames = []
for indicator_name, prefix in FILES.items():
    file = next((f for f in os.listdir(RAW_DIR) if f.startswith(prefix) and f.endswith(".csv")), None)
    if not file:
        print(f"⚠️ Missing file for {indicator_name}")
        continue

    path = os.path.join(RAW_DIR, file)
    df = pd.read_csv(path, skiprows=4)

    df = df[df["Country Code"].isin(COUNTRIES)]
    df = df.melt(
        id_vars=["Country Code"],
        var_name="year",
        value_name="value"
    )
    df["indicator"] = indicator_name
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df = df[(df["year"] >= START_YEAR) & (df["year"] <= END_YEAR)]
    frames.append(df[["Country Code", "indicator", "year", "value"]])

# -----------------------------
# Combine + save
# -----------------------------
if not frames:
    raise RuntimeError("No data loaded. Check CSV file names and RAW_DIR path.")

combined = pd.concat(frames, ignore_index=True)
combined = combined.rename(columns={"Country Code": "country"})
combined = combined.sort_values(["indicator", "country", "year"])

# Wide version
wide = (
    combined.pivot_table(
        index=["year", "indicator"],
        columns="country",
        values="value"
    )
    .sort_index()
    .sort_index(axis=1)
)
wide.columns.name = None

os.makedirs(OUT_DIR, exist_ok=True)
p_long = os.path.join(OUT_DIR, "wb_long_panel.csv")
p_wide = os.path.join(OUT_DIR, "wb_wide_year_indicator_by_country.csv")

combined.to_csv(p_long, index=False)
wide.to_csv(p_wide)

print(f"\n✅ Saved long-format: {p_long}")
print(f"✅ Saved wide-format: {p_wide}")
print("\nPreview (wide):")
print(wide.tail(10))


