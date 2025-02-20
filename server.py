from flask import Flask, request

app = Flask(__name__)

@app.route("/callback")
def callback():
    auth_code = request.args.get("code")
    if auth_code:
        print(f"Codice di autorizzazione ricevuto: {auth_code}")
        return f"Codice ricevuto! Ora copialo e incollalo nel terminale: {auth_code}"
    else:
        return "Errore: Nessun codice ricevuto.", 400

if __name__ == "__main__":
    app.run(port=8000)
