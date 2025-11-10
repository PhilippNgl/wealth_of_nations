# analysis/02_final/app_dashboard.py
from __future__ import annotations
import os
from typing import List, Dict

import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Wealth of Nations – Mini Dashboard",
    page_icon="🌍",
    layout="wide",
)

# -----------------------------
# Data paths
# -----------------------------
RAW_FEATURES = "analysis/02_final/_data/features_country_year.csv"
ZS_FEATURES = "analysis/02_final/_data/features_country_year_zscored.csv"

# Indicator pretty labels (for display only)
INDICATOR_LABELS: Dict[str, str] = {
    "gdp_per_capita_usd": "GDP per capita (current US$)",
    "life_expectancy_years": "Life Expectancy (years)",
    "health_exp_pc_usd": "Health Expenditure per capita (US$)",
    "child_mortality_per_1000": "Child Mortality (per 1,000)",
    "fertility_rate_births_per_woman": "Fertility Rate (births per woman)",
    "co2_tons_per_capita": "CO₂ emissions (tons per capita)",
    "urban_population_pct": "Urban population (% of total)",
}

# ISO3 to short name (optional convenience for subtitles/legends)
COUNTRY_NAMES = {
    "DEU": "Germany",
    "ITA": "Italy",
    "USA": "United States",
    "JPN": "Japan",
    "CHN": "China",
    "IND": "India",
    "BRA": "Brazil",
    "NGA": "Nigeria",
    "FRA": "France",
    "GBR": "United Kingdom",
}

# -----------------------------
# Data loading
# -----------------------------
@st.cache_data
def load_features(raw_path: str, z_path: str):
    """Loads raw and z-scored feature matrices indexed by (country, year)."""
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Missing file: {raw_path}")
    if not os.path.exists(z_path):
        raise FileNotFoundError(f"Missing file: {z_path}")
    raw = pd.read_csv(raw_path).set_index(["country", "year"]).sort_index()
    zsc = pd.read_csv(z_path).set_index(["country", "year"]).sort_index()
    return raw, zsc

raw_df, z_df = load_features(RAW_FEATURES, ZS_FEATURES)

# Determine global year range from data
all_years = raw_df.index.get_level_values("year").unique()
year_min, year_max = int(all_years.min()), int(all_years.max())

# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.title("⚙️ Controls")

countries = sorted(raw_df.index.get_level_values("country").unique())
indicators = [c for c in raw_df.columns if c in INDICATOR_LABELS] or list(raw_df.columns)

selected_countries: List[str] = st.sidebar.multiselect(
    "Countries",
    options=countries,
    default=["DEU", "CHN"] if "DEU" in countries and "CHN" in countries else countries[:2],
)

selected_indicators: List[str] = st.sidebar.multiselect(
    "Indicators",
    options=indicators,
    format_func=lambda k: INDICATOR_LABELS.get(k, k.replace("_", " ").title()),
    default=[i for i in ["gdp_per_capita_usd", "life_expectancy_years"] if i in indicators] or indicators[:2],
)

year_range = st.sidebar.slider(
    "Year range",
    min_value=year_min, max_value=year_max,
    value=(max(year_min, 2000), year_max),
    step=1,
)

use_zscore = st.sidebar.toggle("Standardize values (z-score)", value=False,
                               help="If enabled, charts and heatmap use z-scored features.")

st.sidebar.markdown("---")
show_data_table = st.sidebar.checkbox("Show filtered data preview", value=False)
st.sidebar.markdown("Tip: Use the download buttons below to export the filtered data.")

# -----------------------------
# Header / KPI ribbon
# -----------------------------
st.title("🌍 Wealth of Nations — Mini Dashboard")
st.caption("Interactive exploration of socio-economic indicators by country and year")

cA, cB, cC = st.columns(3)
cA.metric("Countries in dataset", f"{len(countries)}")
cB.metric("Indicators available", f"{raw_df.shape[1]}")
cC.metric("Years covered", f"{year_min}–{year_max}")

# -----------------------------
# Filter data according to selections
# -----------------------------
def filter_data(df: pd.DataFrame, sel_countries: List[str], sel_indicators: List[str], y0: int, y1: int) -> pd.DataFrame:
    """Returns a filtered dataframe by country list, indicator list, and inclusive year window."""
    if not sel_countries or not sel_indicators:
        return pd.DataFrame()
    sub = df.loc[df.index.get_level_values("country").isin(sel_countries), sel_indicators].copy()
    sub = sub.reset_index()
    sub = sub[(sub["year"] >= y0) & (sub["year"] <= y1)]
    sub = sub.set_index(["country", "year"]).sort_index()
    return sub

working_df = z_df if use_zscore else raw_df
filt_df = filter_data(working_df, selected_countries, selected_indicators, year_range[0], year_range[1])

if filt_df.empty:
    st.warning("Please pick at least one country, one indicator, and a valid year window.")
    st.stop()

# -----------------------------
# Tabs: Time series & Correlation
# -----------------------------
tab_ts, tab_corr = st.tabs(["📈 Time Series", "🔥 Correlation"])

# === Time Series Tab ===
with tab_ts:
    st.subheader("Time Series")
    st.caption(
        "Lines show the selected indicators over time for the chosen countries. "
        "Enable z-score in the sidebar to compare indicators on a common scale."
    )

    # For each indicator, create a separate chart
    for ind in selected_indicators:
        pretty = INDICATOR_LABELS.get(ind, ind.replace("_", " ").title())
        fig, ax = plt.subplots(figsize=(9, 4.5))

        for country in selected_countries:
            # Extract series for the country; drop NAs
            s = filt_df.xs(country, level="country")[ind].dropna()
            if s.empty:
                continue
            ax.plot(s.index, s.values, marker="o", linewidth=2, label=COUNTRY_NAMES.get(country, country))

        ax.set_title(pretty, pad=10)
        ax.set_xlabel("Year")
        ax.set_ylabel("Standardized value (z-score)" if use_zscore else "Value")
        ax.grid(True, alpha=0.3)
        ax.legend(loc="best", title="Country")
        st.pyplot(fig)

    # Data preview + download (optional)
    if show_data_table:
        st.markdown("#### Filtered data (long format)")
        preview = filt_df.reset_index().melt(id_vars=["country", "year"], var_name="indicator", value_name="value")
        st.dataframe(preview, use_container_width=True, hide_index=True)

    col_dl1, col_dl2 = st.columns([1, 1])
    long_export = filt_df.reset_index().melt(id_vars=["country", "year"], var_name="indicator", value_name="value")
    col_dl1.download_button(
        "⬇️ Download filtered (long CSV)",
        data=long_export.to_csv(index=False).encode("utf-8"),
        file_name="filtered_long.csv",
        mime="text/csv",
    )
    col_dl2.download_button(
        "⬇️ Download filtered (wide CSV)",
        data=filt_df.to_csv().encode("utf-8"),
        file_name="filtered_wide.csv",
        mime="text/csv",
    )

# === Correlation Tab ===
with tab_corr:
    st.subheader("Correlation Heatmap")
    st.caption(
        "Pearson correlation across the selected indicators within the filtered subset. "
        "For meaningful interpretation, enable z-score in the sidebar."
    )

    # Build matrix over indicators only
    wide_for_corr = filt_df.reset_index().pivot_table(
        index=["country", "year"], values=selected_indicators
    )

    corr = wide_for_corr.corr(method="pearson")
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        square=True,
        cbar_kws={"label": "Correlation"},
        ax=ax,
    )
    ax.set_title("Correlation of selected indicators", pad=10)
    plt.tight_layout()
    st.pyplot(fig)

# -----------------------------
# Footer note
# -----------------------------
st.markdown("---")
st.caption(
    "Data source: World Development Indicators (World Bank, bulk CSV). "
    "This dashboard is a lightweight Streamlit app for exploratory analysis."
)
