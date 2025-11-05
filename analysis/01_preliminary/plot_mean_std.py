# Purpose: Plot eans and standard deviation -s (per country) as a bar chart 
import os
import numpy as np
import matplotlib.pyplot as plt

# We are using your existing loader:
from src.data_loader import load_worldbank_fallback

# 1) Daten laden (gleicher Indikator wie eben)
df = load_worldbank_fallback('NY.GDP.PCAP.CD',countries=('DEU', 'ITA', 'USA'),start=2000,end=2023)

# 2) Changing values in NumPy-Array (only country columns)
# Attention: IS03-Codes (DEU, ITA USA), not DE/IT/US
values = df[['DEU', 'ITA', 'USA']].to_numpy()
             
# 3) Compute KPIs
# axis=0 means: we summarize ROWS and calculate column by column (country by country)
means = np.mean(values, axis=0)
stds = np.std(values, axis=0)

# 4) Labels for the plot annotation
countries_pretty = ['Germany', 'Italy', 'United States']

# 5) Ensure output directory
os.makedirs('reports', exist_ok=True)

# 6) Plot: Bar chart with error bars (standard deviation)
x = np.arange(len(countries_pretty)) # Positions 0,1,2 on x-Axis
width = 0.6                          # Width of the bars
bars = plt.bar(x, means, yerr=stds, capsize=8, color=['#ff9999','#66b3ff','#99ff99'])

# Axes & Titles
plt.xticks(x, countries_pretty)
plt.ylabel('GDP per capita (USD)')
plt.title('Average GDP per Capita (2000-2023) with Standard Deviation')

# Optional value labeling on top of the bars
for rect, m in zip(bars, means):
    height = rect.get_height()
    plt.text(rect.get_x()+rect.get_width()/2, height, f'{m:,.0f}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()

# Save and display graphic
out_path = 'reports/gdp_stats.png'
plt.savefig(out_path, dpi=150)
print(f'Plot gespeichert unter: {out_path}')
plt.show()