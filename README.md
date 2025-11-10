
## Troubleshooting & Data Loading Notes

**Context.** Initially, I attempted to fetch World Bank data via the Python package `wbdata`.  
However, repeated calls resulted in `JSONDecodeError` and invalid responses for some queries.

**Symptom.**

**Cause (likely).** The World Bank endpoint occasionally returns a non-JSON response for certain
queries/parameters, which breaks `wbdata`’s JSON parsing.

**Solution (fallback).** I implemented a direct REST call using `requests.get()` to the official
World Bank API (e.g. `/v2/country/{DE;IT;US}/indicator/{NY.GDP.PCAP.CD}` with query parameters
for `date`, `format=json`, `per_page`), then converted the resulting list into a clean
pandas DataFrame and reshaped it (Year as rows, countries as columns).  
This approach has been stable and reproducible.

**Indicator example used.** `NY.GDP.PCAP.CD` (GDP per capita, current US$).  
**Countries used in examples.** `DE`, `IT`, `US`.  
**Years.** 2000–2023.

**Why I kept it this way.** The fallback is explicit, transparent, and independent of the higher-level
wrapper. It also makes error handling and debugging straightforward. The code is in `src/data_loader.py`
(function `load_worldbank_fallback`).

# Data acquisition

Data were sourced from the official World Bank bulk CSV exports (identical indicators to the API).
Direct API access (wbgapi) initially failed due to rate limiting (HTTP 429) during large-scale pulls.
For reproducibility and stability, indicators were downloaded once as CSV and processed locally.

# Indicators & scope

Countries (example subset): DEU, ITA, USA, JPN, CHN, IND, BRA, NGA
Indicators: GDP per capita (NY.GDP.PCAP.CD), Life expectancy (SP.DYN.LE00.IN), Health expenditure per capita (SH.XPD.CHEX.PC.CD), Child mortality (SH.DYN.MORT), Fertility rate (SP.DYN.TFRT.IN), CO₂ per capita (EN.ATM.CO2E.PC), Urban population (% total) (SP.URB.TOTL.IN.ZS).
Time window used in the analysis: 2000–2023.

# Known issues & fixes

Attempting to fetch 8×7 indicators via API triggered repeated HTTP 429 responses.
Mitigation: switched to bulk CSV download, unified long-format, pivoted to features per (country, year), and created a z-scored feature set for correlation analysis.

# Correlation Heatmap 
The correlation heatmap shows how strongly each socioeconomic indicator is associated with others across countries and years.
Strong positive values (red) indicate that both variables increase together (e.g., GDP per capita ↔ Life Expectancy), while strong negative values (blue) suggest inverse relationships (e.g., Fertility Rate ↔ GDP per capita).
Near-zero correlations imply weak or no linear relationship.

# Web Application (Bonus Section)
A lightweight interactive dashboard was developed using Streamlit.
Users can select countries and indicators to visualize time series trends and explore correlations.
This provides an intuitive interface for exploring economic and demographic relationships across nations.

