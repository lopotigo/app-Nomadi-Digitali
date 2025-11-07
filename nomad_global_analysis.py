import requests
import pandas as pd
import os

# Funzione per dati da Nomad List API (DEMO: molte info sono open, altre richiedono API key)
def get_nomadlist_cities():
    url = "https://nomadlist.com/api/v2/list/cities"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("result", {}).get("cities", [])
    except Exception as e:
        print("Errore chiamata NomadList API:", e)
        return []

# Funzione per dati da Numbeo API (DEMO: richiede API key - qui struttura base)
def get_numbeo_cost(city, country):
    # url = f"https://www.numbeo.com/api/city_prices?api_key=YOUR_KEY&city={city}&country={country}"
    # response = requests.get(url) ...
    # Qui restituiamo valore dummy demo
    return 1000 + hash(city) % 500

# Preparazione dei dati
def build_nomad_cities_table(nomadlist_cities):
    cities_info = []
    for item in nomadlist_cities:
        city_name = item.get("city")
        country = item.get("country")
        wifi = item.get("internet_speed", None)
        # Eventi: demo - andrebbero integrati con API Eventbrite/Meetup o scraping.
        events_nomad_next_month = None
        living_cost_usd = get_numbeo_cost(city_name, country)
        coworkings = item.get("coworkings", None)
        safety = item.get("safety", None)
        climate = item.get("climate", None)

        cities_info.append({
            "city": city_name,
            "country": country,
            "wifi_quality": wifi,
            "num_coworking": coworkings,
            "num_nomad_events": events_nomad_next_month,
            "living_cost_usd": living_cost_usd,
            "safety_index": safety,
            "climate_report": climate
        })
    return pd.DataFrame(cities_info)

# Directory e salvataggio
home = os.path.expanduser("~/app-Nomadi-Digitali")
os.makedirs(home, exist_ok=True)
csv_path = os.path.join(home, "nomad_cities_global.csv")

# Main routine
print("Scarico dati da Nomad List...")
cities_raw = get_nomadlist_cities()
print(f"Città trovate: {len(cities_raw)}")

df = build_nomad_cities_table(cities_raw)
df.sort_values("living_cost_usd", inplace=True)
df.to_csv(csv_path, index=False)
print(f"File CSV creato: {csv_path}")

# Stampa la classifica "cheap"
print("\nClassifica città più economiche:")
for _, row in df.head(10).iterrows():
    print(f'{row["city"]}, {row["country"]}: ${row["living_cost_usd"]} | Wi-Fi: {row["wifi_quality"]} | Coworking: {row["num_coworking"]}')
