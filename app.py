import os
from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd

# Créer l'application Flask
app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'

# Charger les données CSV
CSV_FILE = 'lieux.csv'

def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        # Créer un fichier CSV vide si nécessaire
        pd.DataFrame(columns=['Nom', 'Latitude', 'Longitude']).to_csv(CSV_FILE, index=False)
        return pd.read_csv(CSV_FILE)

# Page d'accueil
@app.route('/')
def home():
    data = load_data()
    lieux = data.to_dict(orient='records')
    return render_template('index.html', lieux=lieux)

# Ajouter un lieu
@app.route('/ajouter', methods=['POST'])
def ajouter_lieu():
    nom = request.form.get('nom')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    if not nom or not latitude or not longitude:
        flash("Tous les champs sont obligatoires.", "error")
        return redirect(url_for('home'))

    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        flash("Les coordonnées doivent être des nombres.", "error")
        return redirect(url_for('home'))

    # Ajouter le lieu au fichier CSV
    data = load_data()
    new_entry = {'Nom': nom, 'Latitude': latitude, 'Longitude': longitude}
    data = data.append(new_entry, ignore_index=True)
    data.to_csv(CSV_FILE, index=False)

    flash("Lieu ajouté avec succès !", "success")
    return redirect(url_for('home'))

# Supprimer un lieu
@app.route('/supprimer/<int:index>', methods=['POST'])
def supprimer_lieu(index):
    data = load_data()
    if 0 <= index < len(data):
        data = data.drop(index)
        data.to_csv(CSV_FILE, index=False)
        flash("Lieu supprimé avec succès !", "success")
    else:
        flash("Lieu introuvable.", "error")
    return redirect(url_for('home'))

# Point d'entrée principal
if __name__ == '__main__':
    # Obtenez le port défini par Render ou utilisez 5000 par défaut
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
