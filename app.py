from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/map')
def show_map():
    # Legge i dati dal file CSV (dev'essere nella stessa cartella!)
    df = pd.read_csv("coworking_osm.csv")
    coworkings = df.to_dict(orient="records")
    center_lat = coworkings[0]["lat"]
    center_lon = coworkings[0]["lon"]
    # Passa i dati alla pagina mappa
    return render_template("map.html", coworkings=coworkings, center_lat=center_lat, center_lon=center_lon)

if __name__ == "__main__":
    app.run(debug=True)