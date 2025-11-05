import numpy as np
from src.data_loader import load_worldbank_fallback

# 1. Load Data
df = load_worldbank_fallback('NY.GDP.PCAP.CD', countries=('DE', 'IT', 'US'), start=2000, end=2023)

# 2. Change Data to NumPy-Array 
values = df[['DEU','ITA','USA']].to_numpy()

# 3. Computing means and standard deviation
means = np.mean(values, axis=0)
stds = np.std(values, axis=0)

#4. Show results
countries = ['Germany', 'Italy', 'United States']
for country, mean, std in zip(countries, means, stds):
    print(f"{country:15} | Mean GDP per capita: {mean:10.2f} | Std Dev:{std:10.2f}")
    