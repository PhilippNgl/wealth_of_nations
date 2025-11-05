import matplotlib.pyplot as plt
from src.data_loader import load_worldbank_fallback

# Load Data
df = load_worldbank_fallback('NY.GDP.PCAP.CD', countries=('DE', 'IT', 'US'), start=2000, end=2023)

# Draw Diagramm
ax = df.plot(x='Year', y=[c for c in df.columns if c != 'Year'], figsize=(9, 5))
ax.set_title("GDP per capita (current US$), 2000–2023")
ax.set_ylabel("US-Dollar pro Kopf")
ax.grid(True)

# Save Diagramm (instead of showing)
plt.tight_layout()
plt.savefig("reports/gdp_per_capita_DE_IT_US.png", dpi=160)
print("✅ Diagramm gespeichert: reports/gdp_per_capita_DE_IT_US.png")
