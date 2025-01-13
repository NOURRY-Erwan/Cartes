from flask import Flask, render_template, send_file, request
import pandas as pd
import os
import folium

# Initialisation de l'application Flask
app = Flask(__name__)

# Chemin du fichier CSV
CSV_FILE = 'lieux.csv'

# Création du fichier CSV s'il n'existe pas
def create_csv():
    if not os.path.exists(CSV_FILE):
        data = {
            "Nom": ["Collège A", "Collège B", "Collège C"],
            "Latitude": [48.8566, 48.8584, 48.853],
            "Longitude": [2.3522, 2.2945, 2.349]
        }
        pd.DataFrame(data).to_csv(CSV_FILE, index=False)

# Appel de la fonction pour créer le CSV au démarrage
create_csv()

# Charger les données depuis le fichier CSV
lieux = pd.read_csv(CSV_FILE)

@app.route('/')
def index():
    # Création de la carte avec Folium
    carte = folium.Map(location=[48.8566, 2.3522], zoom_start=13)

    # Ajouter les marqueurs à la carte
    for _, row in lieux.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=row['Nom'],
        ).add_to(carte)

    # Sauvegarde la carte dans un fichier HTML temporaire
    map_path = os.path.join('templates', 'map.html')
    carte.save(map_path)

    return render_template('map.html')

@app.route('/download')
def download():
    # Permettre le téléchargement du fichier CSV
    return send_file(CSV_FILE, as_attachment=True)

@app.route('/add', methods=['POST'])
def add_location():
    # Ajouter un lieu depuis un formulaire
    nom = request.form.get('nom')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    if nom and latitude and longitude:
        new_row = {
            "Nom": nom,
            "Latitude": float(latitude),
            "Longitude": float(longitude)
        }
        global lieux
        lieux = lieux.append(new_row, ignore_index=True)
        lieux.to_csv(CSV_FILE, index=False)
        return "Lieu ajouté avec succès !"
    else:
        return "Veuillez fournir toutes les informations."

if __name__ == '__main__':
    app.run(debug=True)
