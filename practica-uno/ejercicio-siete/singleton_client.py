import requests
url = "http://localhost:8000/partidas"
headers = {'Content-type': 'application/json'}

# GET /partidas
response = requests.get(url=url)
print("Mostrar partidas:",response.json())

# POST /partidas
data = {
    "elemento": "piedra"
}

response2 = requests.post(url, json=data, headers=headers)
print("Crear partida:",response2.text)

# GET /partidas
response = requests.get(url=url+"/?resultado=pierdo")
print("Mostrar partidas:",response.json())

