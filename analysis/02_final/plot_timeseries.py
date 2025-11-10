# analysis/02_final/plot_timeseries.py
from __future__ import annotations
import os
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Configuration
# -----------------------------
IN_FILE = "analysis/02_final/_data/features_country_year.csv"
OUT_DIR = "analysis/02_final/_plots"

# Choose indicators and countries for comparison
INDICATORS = [
    ("gdp_per_capita_usd", "GDP per capita (current US$)"),
    ("life_expectancy_years", "Life Expectancy (years)"),
]

COUNTRY_PAIRS = [
    ("DEU", "CHN"),  # Germany vs China
    ("USA", "NGA"),  # USA vs Nigeria
]

# -----------------------------
# Helper function
# -----------------------------
def plot_timeseries(df: pd.DataFrame, country_a: str, country_b: str, indicators: list[tuple[str, str]]) -> None:
    """
    Plots selected indicators over time for two countries.
    Each indicator gets its own subplot.
    """
    fig, axes = plt.subplots(len(indicators), 1, figsize=(10, 6 * len(indicators)), sharex=True)

    if len(indicators) == 1:
        axes = [axes]

    for ax, (col, label) in zip(axes, indicators):
        for country, style in zip([country_a, country_b], ["-o", "-s"]):
            subset = df.xs(country, level="country")[col].dropna()
            ax.plot(subset.index, subset.values, style, label=country)
        ax.set_title(label, fontsize=13)
        ax.set_ylabel("Value")
        ax.grid(True, alpha=0.3)
        ax.legend(title="Country")

    axes[-1].set_xlabel("Year")
    plt.tight_layout()

    fname = f"timeseries_{country_a}_{country_b}.png"
    out_path = os.path.join(OUT_DIR, fname)
    os.makedirs(OUT_DIR, exist_ok=True)
    plt.savefig(out_path, dpi=300)
    print(f"✅ Saved: {out_path}")
    plt.show()


# -----------------------------
# Main pipeline
# -----------------------------
def main() -> None:
    if not os.path.exists(IN_FILE):
        raise FileNotFoundError(f"Input file not found: {IN_FILE}")

    df = pd.read_csv(IN_FILE)
    df = df.set_index(["country", "year"]).sort_index()

    for country_a, country_b in COUNTRY_PAIRS:
        print(f"\n=== Plotting {country_a} vs {country_b} ===")
        plot_timeseries(df, country_a, country_b, INDICATORS)


if __name__ == "__main__":
    main()
