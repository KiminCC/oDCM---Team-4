CLIENT_ID = "tcgOlBvvbQxa9w2fbg4B2reO57im5vkn"
CLIENT_SECRET = "SUNBc6ffHzrm1QZvYdPCxDdlIM1v4X1Q"

import requests

def get_token():
    req=requests.post('https://api.soundcloud.com/oauth2/token', params = {'Content-Type': 'application/x-www-form-urlencoded',
                                                                  'client_id': CLIENT_ID,
                                                                  'client_secret' : CLIENT_SECRET,
                                                                      'grant_type' : 'client_credentials'})
    return(req.json())
    
auth_data = get_token()
token = auth_data['access_token']
print(token)

auth_data['expires_in']

# Example: Search for tracks with "lofi"
search_query = "lofi"
response = requests.get(
    "https://api.soundcloud.com/tracks",
    headers={"Authorization": "Bearer 2-299933--dJea6JYHyzLrLWSwti713ve"},
    params = {"q": search_query}
)

result = response.json()

for data in result:
    title = data.get('title')
    print(f'title: {title}')


token


req.json()