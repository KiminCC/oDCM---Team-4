import requests
import base64
import hashlib
import os
import webbrowser
from urllib.parse import urlencode
from flask import Flask, request
import threading

# Configurazione
CLIENT_ID = "tcgOlBvvbQxa9w2fbg4B2reO57im5vkn"
CLIENT_SECRET = "SUNBc6ffHzrm1QZvYdPCxDdlIM1v4X1Q"
REDIRECT_URI = "http://localhost:8000/callback"
AUTH_URL = "https://secure.soundcloud.com/authorize"
TOKEN_URL = "https://secure.soundcloud.com/oauth/token"

# Generazione del codice PKCE
def generate_pkce():
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('utf-8')).digest()
    ).rstrip(b'=').decode('utf-8')
    return code_verifier, code_challenge

code_verifier, code_challenge = generate_pkce()

# Creazione dell'URL di autorizzazione
params = {
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "response_type": "code",
    "code_challenge": code_challenge,
    "code_challenge_method": "S256",
    "state": os.urandom(16).hex()
}
auth_url = f"{AUTH_URL}?{urlencode(params)}"

# Flask Server per intercettare il codice
auth_code = None
app = Flask(__name__)

@app.route("/callback")
def callback():
    global auth_code
    auth_code = request.args.get("code")
    return "Autenticazione completata. Puoi chiudere questa finestra."

def run_flask():
    app.run(port=8000, debug=False, use_reloader=False)

# Avvio del server Flask in un thread
thread = threading.Thread(target=run_flask)
thread.start()

# Apertura dell'URL nel browser
print("Apri il seguente URL nel browser per autenticarti:")
print(auth_url)
webbrowser.open(auth_url)

# Attendi il codice
while auth_code is None:
    pass

# Scambio del codice per un access token
data = {
    "grant_type": "authorization_code",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "code": auth_code,
    "code_verifier": code_verifier
}
headers = {
    "Accept": "application/json; charset=utf-8",
    "Content-Type": "application/x-www-form-urlencoded"
}

response = requests.post(TOKEN_URL, data=data, headers=headers)

if response.status_code == 200:
    access_token = response.json().get("access_token")
    print("Access Token ottenuto:", access_token)
else:
    print("Errore nell'ottenimento del token:", response.json())
