# analysis/02_final/plot_correlation.py
from __future__ import annotations
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# -----------------------------
# Configuration
# -----------------------------
IN_FILE = "analysis/02_final/_data/features_country_year_zscored.csv"
OUT_DIR = "analysis/02_final/_plots"
CORR_METHOD = "pearson"  # alternatives: "spearman", "kendall"

# -----------------------------
# Main pipeline
# -----------------------------
def main() -> None:
    if not os.path.exists(IN_FILE):
        raise FileNotFoundError(f"Input file not found: {IN_FILE}")
    os.makedirs(OUT_DIR, exist_ok=True)

    # 1) Load standardized data
    df = pd.read_csv(IN_FILE, index_col=["country", "year"])
    print(f"Loaded standardized feature set: {df.shape[0]} rows × {df.shape[1]} columns")

    # 2) Compute correlation matrix
    corr = df.corr(method=CORR_METHOD)

    # 3) Plot heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        cbar_kws={"label": "Correlation"},
        square=True,
    )
    plt.title(f"Feature Correlation Heatmap ({CORR_METHOD.title()} correlation)", pad=16)
    plt.tight_layout()

    # 4) Save and show
    out_path = os.path.join(OUT_DIR, f"heatmap_{CORR_METHOD}.png")
    plt.savefig(out_path, dpi=300)
    print(f"✅ Saved heatmap: {out_path}")
    plt.show()


if __name__ == "__main__":
    main()
