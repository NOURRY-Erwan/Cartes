from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

# Nom du fichier CSV
CSV_FILE = 'lieux.csv'

# Vérifier si le fichier existe, sinon le créer
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=['Nom', 'Latitude', 'Longitude']).to_csv(CSV_FILE, index=False)

@app.route('/')
def index():
    lieux = pd.read_csv(CSV_FILE)
    return render_template('index.html', lieux=lieux.to_dict(orient='records'))

@app.route('/ajouter', methods=['POST'])
def ajouter_lieu():
    nom = request.form.get('nom')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    # Vérification des champs
    if not nom or not latitude or not longitude:
        return "Tous les champs sont requis.", 400

    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return "Latitude et Longitude doivent être des nombres.", 400

    # Ajouter le lieu dans le fichier CSV
    lieux = pd.read_csv(CSV_FILE)
    lieux = lieux.append({'Nom': nom, 'Latitude': latitude, 'Longitude': longitude}, ignore_index=True)
    lieux.to_csv(CSV_FILE, index=False)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
