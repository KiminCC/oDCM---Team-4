from flask import Flask, request, jsonify
import requests

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

def get_user_info(user_id, token):
    """
    Recupera le informazioni di un utente dato il suo user_id.
    """
    url = f"https://api.soundcloud.com/users/{user_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Errore utente {user_id}: {response.status_code}, {response.text}")
        return None

@app.route('/pro_users', methods=['GET'])
def pro_users():
    """
    Endpoint personalizzato per filtrare gli utenti Pro.
    Si aspetta un parametro query 'user_ids' con una lista separata da virgole.
    """
    user_ids_param = request.args.get('user_ids')
    if not user_ids_param:
        return jsonify({"error": "Parametro 'user_ids' non fornito"}), 400

    # Convertiamo la stringa in una lista di ID
    user_ids = [uid.strip() for uid in user_ids_param.split(',')]
    
    token = get_token()
    if not token:
        return jsonify({"error": "Impossibile ottenere il token di accesso"}), 500

    pro_users_list = []
    for user_id in user_ids:
        user_data = get_user_info(user_id, token)
        if user_data:
            plan = user_data.get("plan", "").lower()
            if plan.startswith("pro"):
                pro_users_list.append(user_data)

    return jsonify({"pro_users": pro_users_list}), 200

if __name__ == '__main__':
    app.run(debug=True)
