import requests
import os
import json
import csv

# Percorso di salvataggio nella cartella app-Nomadi-Digitali
cartella_destinazione = os.path.expanduser("~/app-Nomadi-Digitali")
os.makedirs(cartella_destinazione, exist_ok=True)
percorso_json = os.path.join(cartella_destinazione, "coworking_osm.json")
percorso_csv = os.path.join(cartella_destinazione, "coworking_osm.csv")

# Query: coworking per l'Italia (modifica coordinate per altre zone)
query = """
[out:json][timeout:60];
node["amenity"="coworking_space"](41.5,8.2,47.1,18.1);
out;
"""

overpass_url = "https://overpass-api.de/api/interpreter"

print("Richiesta a Overpass...")
response = requests.post(overpass_url, data={'data': query})
response.raise_for_status()
data = response.json()
print(f"Trovati {len(data['elements'])} coworking.")

# Salva il JSON
with open(percorso_json, "w", encoding="utf-8") as f_json:
    json.dump(data, f_json, ensure_ascii=False, indent=2)
print(f"Salvato {percorso_json}")

# Salva il CSV
with open(percorso_csv, "w", encoding="utf-8", newline="") as csvfile:
    fieldnames = ["id", "lat", "lon", "name"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for element in data["elements"]:
        name = element.get("tags", {}).get("name", "")
        writer.writerow({
            "id": element["id"],
            "lat": element["lat"],
            "lon": element["lon"],
            "name": name
        })
print(f"Creato {percorso_csv}")
