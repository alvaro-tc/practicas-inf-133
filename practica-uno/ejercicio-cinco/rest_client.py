import requests
url = "http://localhost:8000/animales"
headers = {'Content-type': 'application/json'}

# POST /animales
data = {
    "nombre": "Polkis",
    "especie": "Perro",
    "genero": "masculino",
    "edad": 20, 
    "peso": 69
}
response2 = requests.post(url, json=data, headers=headers)
print("Crear animal:",response2.text)

# GET /animales
response = requests.get(url=url)
print("Mostrar animales:",response.json())


# GET /animales/{animal_id}
response = requests.get(url=url+"/1")
print("Mostrar animal:",response.json())


# GET /animales/?especie={especie}
response = requests.get(url=url+"/?especie=Perro")
print("Mostrar animales POR:",response.json())

# GET /animales/?genero={genero}
response = requests.get(url=url+"/?genero=masculino")
print("Mostrar animales POR:",response.json())


# PUT /animales/{animal_id}
data_update = {
    "nombre": "Polkis",
    "especie": "Perro",
    "genero": "femenino",
    "edad": 20,
    "peso": 69
}
response2 = requests.put(url=url+"/1", json=data_update, headers=headers)
print("Cambiar animal:",response2.text)


# DELETE /animales/{animal_id}
response3 = requests.delete(url=url+"/1")
print("Eliminar animal:",response3.text)

# GET /animales
response = requests.get(url=url)
print("Mostrar animales:",response.text)

