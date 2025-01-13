from flask import Flask, render_template, request, redirect, url_for
import folium
import pandas as pd
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Charger les lieux
lieux = pd.read_csv('lieux.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def map():
    # Créer la carte
    carte = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

    # Ajouter les lieux à la carte
    for _, lieu in lieux.iterrows():
        folium.Marker(
            [lieu['Latitude'], lieu['Longitude']],
            popup=lieu['Nom']
        ).add_to(carte)

    # Sauvegarder la carte
    carte.save('templates/map.html')
    return render_template('map.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "Aucun fichier sélectionné."
    
    file = request.files['file']
    if file.filename == '':
        return "Aucun fichier sélectionné."
    
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('results', filename=filename))

@app.route('/results/<filename>')
def results(filename):
    # Charger les réponses des joueurs
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    reponses = pd.read_csv(filepath)

    # Comparer avec les réponses correctes
    score = 0
    for _, lieu in lieux.iterrows():
        reponse = reponses[reponses['Nom'] == lieu['Nom']]
        if not reponse.empty:
            distance = ((lieu['Latitude'] - reponse['Latitude'].values[0])**2 +
                        (lieu['Longitude'] - reponse['Longitude'].values[0])**2)**0.5
            if distance < 0.01:  # Tolérance
                score += 1

    return render_template('results.html', score=score, total=len(lieux))

if __name__ == '__main__':
    app.run(debug=True)
