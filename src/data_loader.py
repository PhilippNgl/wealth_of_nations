print(">> USING FALLBACK LOADER")  # nur zum Prüfen

import requests
import pandas as pd

def load_worldbank_fallback(indicator='NY.GDP.PCAP.CD',
                            countries=('DE','IT','US'),
                            start=2000, end=2023):
    """
    Holt Daten direkt von der World-Bank-Webseite.
    Ergebnis: Tabelle mit Spalten Year, DE, IT, US
    """
    cc = ';'.join(countries)  # "DE;IT;US"
    url = f'https://api.worldbank.org/v2/country/{cc}/indicator/{indicator}'
    params = {'date': f'{start}:{end}', 'format': 'json', 'per_page': 20000}
    r = requests.get(url, params=params)
    r.raise_for_status()
    js = r.json()          # Antwort in „echte“ Daten umwandeln
    data = js[1] or []     # js[0] = Überschrift, js[1] = richtige Liste
    df = pd.DataFrame(data)[['countryiso3code', 'date', 'value']]
    df = df.rename(columns={'countryiso3code': 'country', 'date': 'Year'})
    df['Year'] = df['Year'].astype(int)
    df = df.pivot(index='Year', columns='country', values='value').sort_index()
    df.reset_index(inplace=True)
    df.columns.name = None
    return df

# Dieser Teil läuft, wenn du die Datei startest
if __name__ == "__main__":
    demo = load_worldbank_fallback()
    print(demo.head())


