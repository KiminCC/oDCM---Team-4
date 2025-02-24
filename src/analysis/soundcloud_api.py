import requests

ACCESS_TOKEN = '2-299933-1508724076-Ws5ZCyeqd31Bp'  # inserisci qui il token ottenuto prima
API_URL = 'https://api.soundcloud.com/me'  # endpoint per recuperare informazioni sul tuo account

headers = {
    'Authorization': f'OAuth {ACCESS_TOKEN}',
    'Accept': 'application/json'
}

response = requests.get(API_URL, headers=headers)

if response.status_code == 200:
    user_info = response.json()
    print("Informazioni sull'utente ottenute con successo:")
    print(user_info)
else:
    print(f"Errore nella richiesta: {response.status_code}")
    print(response.json())
