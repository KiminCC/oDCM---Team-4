import requests
import json
import os

API_URL = "http://127.0.0.1:5001/scrape_user_tracks"

try:
    print("📂 Cartella corrente:", os.getcwd())  # Mostra la cartella attuale
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        file_path = os.path.join(os.getcwd(), "soundcloud_data.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ Dati salvati in '{file_path}'")
    else:
        print(f"❌ Errore durante il recupero dei dati: {response.status_code}")
except Exception as e:
    print(f"❌ Eccezione: {e}")
