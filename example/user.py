from flask import Flask, request, jsonify
import requests
import random
from datetime import datetime

app = Flask(__name__)

# Inserisci le tue credenziali SoundCloud
CLIENT_ID = "tcgOlBvvbQxa9w2fbg4B2reO57im5vkn"
CLIENT_SECRET = "SUNBc6ffHzrm1QZvYdPCxDdlIM1v4X1Q"

def get_token():
    """
    Ottiene un token di accesso tramite il grant_type client_credentials.
    """
    url = "https://api.soundcloud.com/oauth2/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"Errore token: {response.status_code}, {response.text}")
        return None

@app.route('/scrape_user_tracks', methods=['GET'])
def scrape_user_tracks():
    """
    Endpoint per cercare utenti su SoundCloud, ottenere le loro tracce e calcolare la frequenza di pubblicazione.
    """
    token = get_token()
    if not token:
        return jsonify({"error": "Impossibile ottenere il token di accesso"}), 500
    
    # Ottenere un campione casuale di utenti Pro
    url = "https://api.soundcloud.com/users"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"limit": 200}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        return jsonify({"error": "Errore durante il recupero degli utenti", "status": response.status_code}), response.status_code
    
    users = response.json()
    pro_users = [user for user in users if user.get("plan", "").lower().startswith("pro")]
    random_sample = random.sample(pro_users, min(len(pro_users), 50))
    
    # Per ogni utente, ottenere tutte le tracce e calcolare la frequenza
    all_user_data = []
    for user in random_sample:
        user_id = user.get("id")
        if not user_id:
            continue
        track_url = f"https://api.soundcloud.com/users/{user_id}/tracks"
        track_response = requests.get(track_url, headers=headers)

        if track_response.status_code == 200:
            tracks = track_response.json()
            # Calcolare la frequenza delle pubblicazioni basata sulle date di creazione delle tracce
            track_dates = []
            for track in tracks:
                created_at = track.get("created_at")
                if created_at:
                    try:
                        date_obj = datetime.strptime(created_at, "%Y/%m/%d %H:%M:%S %z")
                        track_dates.append(date_obj)
                    except ValueError as e:
                        print(f"Errore parsing data: {created_at} - {e}")

            # Calcolare la frequenza delle tracce per anno e mese
            frequency = {}
            for date in track_dates:
                year_month = date.strftime("%Y-%m")
                if year_month not in frequency:
                    frequency[year_month] = 0
                frequency[year_month] += 1
            
            all_user_data.append({
                "user_id": user_id,
                "username": user.get("username"),
                "tracks": tracks,
                "frequency": frequency
            })
    
    return jsonify({"users_data": all_user_data}), 200

@app.route('/', methods=['GET'])
def home():
    """
    Endpoint di test per verificare che il server Flask sia attivo.
    """
    return "Server Flask è attivo!", 200

@app.route('/routes', methods=['GET'])
def list_routes():
    """
    Elenca tutti gli endpoint disponibili nell'app Flask.
    """
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(str(rule))
    return jsonify({"available_routes": routes}), 200

if __name__ == '__main__':
    app.run(debug=True)
