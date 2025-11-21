import requests
import os
import json
import csv

# Percorso di salvataggio nella cartella app-Nomadi-Digitali
cartella_destinazione = os.path.expanduser("./app-Nomadi-Digitali")
os.makedirs(cartella_destinazione, exist_ok=True)
percorso_json = os.path.join(cartella_destinazione, "coworking_osm.json")
percorso_csv = os.path.join(cartella_destinazione, "coworking_osm.csv")

# Query coworking in Italia (modifica bounding box per altre aree)
query = """
[out:json][timeout:60];
node["amenity"="coworking_space"](41.5,-8.2,47.8,17.1);
out body;
"""
overpass_url = "https://overpass-api.de/api/interpreter"

print("Richiesta a Overpass...")
response = requests.post(overpass_url, data={'data': query})
response.raise_for_status()
data = response.json()
print(f"Trovati {len(data['elements'])} coworking.")

# Salva JSON completo
with open(percorso_json, "w", encoding="utf-8") as f_json:
    json.dump(data, f_json, ensure_ascii=False, indent=2)
print(f"Salvato {percorso_json}")

# Salva CSV esteso con nuovi campi
with open(percorso_csv, "w", encoding="utf-8", newline="") as csvfile:
    fieldnames = [
        "id", "name", "address", "city", "postcode", "lat", "lon",
        "email", "website", "phone", "operator", "services", "opening_hours"
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for element in data["elements"]:
        tags = element.get("tags", {})
        writer.writerow({
            "id": element.get("id", ""),
            "lat": element.get("lat", ""),
            "lon": element.get("lon", ""),
            "name": tags.get("name", ""),
            "address": f"{tags.get('addr:street', '')} {tags.get('addr:housenumber', '')}".strip(),
            "city": tags.get("addr:city", ""),
            "postcode": tags.get("addr:postcode", ""),
            "email": tags.get("email", ""),
            "website": tags.get("website", ""),
            "phone": tags.get("phone", ""),
            "operator": tags.get("operator", ""),
            "services": tags.get("services", ""),
            "opening_hours": tags.get("opening_hours", "")
        })
print(f"Creato {percorso_csv}")