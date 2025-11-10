# analysis/02_final/data_preparation.py
from __future__ import annotations
import os
import pandas as pd
import numpy as np

# -----------------------------
# Configuration
# -----------------------------
IN_LONG = "analysis/02_final/_data/wb_long_panel.csv"
OUT_DIR = "analysis/02_final/_data"

# Optional: restrict to the main study window
START_YEAR = 2000
END_YEAR = 2023

# Optional: drop rows with too many missing indicator values
MIN_NON_NA_RATIO = 0.5  # keep rows with >= 50% non-NaN features


# -----------------------------
# Helpers
# -----------------------------
def zscore_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies z-score per numeric column: (x - mean) / std.
    Columns with zero variance remain NaN (no scaling possible).
    Index and non-numeric columns are preserved.
    """
    numeric = df.select_dtypes(include=[np.number]).columns
    out = df.copy()
    for col in numeric:
        series = out[col]
        mu = series.mean(skipna=True)
        sigma = series.std(skipna=True)
        # avoid division by zero
        if pd.isna(sigma) or sigma == 0:
            out[col] = np.nan
        else:
            out[col] = (series - mu) / sigma
    return out


# -----------------------------
# Main pipeline
# -----------------------------
def main() -> None:
    if not os.path.exists(IN_LONG):
        raise FileNotFoundError(f"Input not found: {IN_LONG}")

    os.makedirs(OUT_DIR, exist_ok=True)

    # 1) Load long-format panel
    df = pd.read_csv(IN_LONG)

    # Expecting columns: ['country', 'indicator', 'year', 'value']
    expected = {"country", "indicator", "year", "value"}
    missing_cols = expected - set(df.columns)
    if missing_cols:
        raise ValueError(f"Input is missing columns: {missing_cols}")

    # 2) Filter time window and basic cleaning
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df = df[(df["year"] >= START_YEAR) & (df["year"] <= END_YEAR)]
    df = df.drop_duplicates(subset=["country", "indicator", "year"]).copy()

    # 3) Pivot to features: index=(country, year), columns=indicator
    wide = (
        df.pivot_table(
            index=["country", "year"],
            columns="indicator",
            values="value",
            aggfunc="mean",
        )
        .sort_index()
    )
    wide.columns.name = None  # clean column name

    # 4) Optional row filter by completeness
    if MIN_NON_NA_RATIO is not None:
        min_non_na = int(np.ceil(MIN_NON_NA_RATIO * wide.shape[1]))
        mask_keep = wide.count(axis=1) >= min_non_na
        wide = wide.loc[mask_keep]

    # 5) Save plain features
    p_features = os.path.join(OUT_DIR, "features_country_year.csv")
    wide.to_csv(p_features)
    print(f"Saved features: {p_features} (rows={len(wide):,}, cols={wide.shape[1]})")

    # 6) Z-scored version (per indicator column)
    wide_z = zscore_columns(wide)
    p_z = os.path.join(OUT_DIR, "features_country_year_zscored.csv")
    wide_z.to_csv(p_z)
    print(f"Saved z-scored features: {p_z} (rows={len(wide_z):,}, cols={wide_z.shape[1]})")

    # 7) Quick preview
    print("\nPreview (features, tail):")
    print(wide.tail(5))
    print("\nPreview (z-scored, tail):")
    print(wide_z.tail(5))


if __name__ == "__main__":
    main()

