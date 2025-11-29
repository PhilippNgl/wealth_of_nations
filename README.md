# Wealth of Nations – Python Project  
**Master in Data Science for Economics and Health – Università degli Studi di Milano**

Final project for the Python module.  
This project explores how key socioeconomic indicators (GDP, Life Expectancy, Health Expenditure, Fertility, CO₂ Emissions, etc.) evolve across major world economies using World Bank data.  
A Streamlit web dashboard was developed as a **bonus feature (+3 points)**.

---

## Project Structure

wealth_of_nations/
├── analysis/
│ ├── 01_preliminary/ # Early analysis and drafts
│ └── 02_final/ # Final scripts and app
│ ├── _data/ # Processed datasets (CSV)
│ ├── _plots/ # Generated figures (PNG)
│ ├── app_dashboard.py # Streamlit dashboard (bonus)
│ ├── data_integration.py # Data loading and merging
│ ├── data_preparation.py # Cleaning, reshaping, z-scoring
│ ├── plot_correlation.py # Correlation heatmap
│ └── plot_timeseries.py # Time series comparison
├── src/
│ ├── data_loader.py # API and CSV loaders
│ ├── plot_stats.py # Shared plotting utilities
│ └── init.py
├── data/ # Raw or external datasets (optional)
├── reports/ # Output charts for documentation
├── requirements.txt
└── README.md


---

## Concept & Data

Data were sourced from the **World Bank Open Data** API (`wbgapi`) and corresponding bulk CSV exports for reproducibility.  
Indicators were selected to represent both **economic** and **demographic** dimensions.

**Indicators**
- GDP per capita (NY.GDP.PCAP.CD)  
- Life expectancy (SP.DYN.LE00.IN)  
- Health expenditure per capita (SH.XPD.CHEX.PC.CD)  
- Child mortality (SH.DYN.MORT)  
- Fertility rate (SP.DYN.TFRT.IN)  
- CO₂ emissions per capita (EN.ATM.CO2E.PC)  
- Urban population (% of total) (SP.URB.TOTL.IN.ZS)

**Countries (example subset)**  
DEU, ITA, USA, JPN, CHN, IND, BRA, NGA  
**Years**: 2000–2023

---

## Installation

```bash
# 1. Clone repository
git clone https://github.com/<your-username>/wealth_of_nations.git
cd wealth_of_nations

# 2. Create & activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

-----------------------------------------------------------------------------------------------------------------------------------------------------------

## Analysis Overview

**Data Acquisition**

Primary access via wbgapi (World Bank API).

Fallback implemented with requests for stability (src/data_loader.py).

Data reshaped into panel format (year × country × indicator).

**Data Preparation**

Cleaning, merging, and z-score normalization across indicators.

Stored in _data/features_country_year_zscored.csv.

**Correlation Heatmap**

Heatmap visualizes cross-indicator relationships.

Red → positive correlation (e.g., GDP ↔ Life Expectancy)

Blue → negative correlation (e.g., GDP ↔ Fertility Rate)

White → weak or no correlation.

**Time Series Comparison**

Line plots comparing temporal trends between countries (e.g., DEU vs CHN).

Saved in _plots/timeseries_DEU_CHN.png.

## Web Dashboard (Bonus)

A lightweight interactive Streamlit dashboard provides real-time visualization.

Run locally: streamlit run analysis/02_final/app_dashboard.py

**Features:**

Select countries and indicators dynamically.

Display time-series charts and correlation comparisons.

Enables intuitive exploration of economic and demographic trends.

## Troubleshooting & Stability Notes

Context.
The World Bank API (wbgapi) occasionally triggers JSONDecodeError or HTTP 429 (rate limits) for large queries.

Solution.
A custom fallback function (load_worldbank_fallback()) was implemented using direct REST calls with requests.get().
This ensures stability and reproducibility during large-scale pulls.

Implementation.
Located in src/data_loader.py, the fallback converts JSON responses into clean pandas DataFrames, reshapes them (year × country), and saves them locally as CSV.

Evaluation Criteria Checklist
Criterion	Implemented	Evidence
1. GitHub Usage	->	.gitignore, structured commits, detailed README
2. Project Organization	->	Modular structure (src/, analysis/), clear functions, docstrings
3. Input/Output	->	API + CSV fallback, consistent loading/saving
4. Data Manipulation	->	Pandas cleaning, merging, reshaping, z-scoring
5. Scientific Computing	->	Correlation analysis (Pearson), numerical aggregation
6. Visualization	->	Matplotlib & Seaborn (heatmap, time series)
7. BONUS – Web Application	->	Streamlit dashboard with user interaction

## References

World Bank Open Data

wbgapi Python package

Matplotlib Documentation

Streamlit Documentation

## personal Details

Author: Philipp Neglein
Course: Data Science for Economics and Health (Python Laboratory)
University: Unviersita degli studi di Milano
Date: November 2025
Repository: [github.com/philipp-neglein/wealth_of_nations](https://github.com/philipp-neglein/wealth_of_nations)
