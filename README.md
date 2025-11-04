
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