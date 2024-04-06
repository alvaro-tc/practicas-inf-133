import requests
url = "http://localhost:8000/mensajes"
headers = {'Content-type': 'application/json'}

# POST /mensajes
data = {
    "contenido": "hola mundo",
}
response2 = requests.post(url, json=data, headers=headers)
print("Crear Mensaje:",response2.text)

# GET /mensajes
response = requests.get(url=url)
print("Mostrar mensajes:",response.json())


# GET /mensajes/{mensaje_id}
response = requests.get(url=url+"/1")
print("Mostrar mensaje por id:",response.json())


# PUT /mensajes/{mensaje_id}
data_update = {
    "contenido": "hoal mundz",
}
response2 = requests.put(url=url+"/1", json=data_update, headers=headers)
print("Update Mensaje:",response2.text)

# GET /mensajes/{mensaje_id}
response = requests.get(url=url+"/1")
print("Mostrar Mensajes:",response.json())

# DELETE /mensajes/{mensaje_id}
response3 = requests.delete(url=url+"/1")
print("Eliminar Mensaje:",response3.text)

# GET /mensajes
response = requests.get(url=url)
print("Mostrar Mensajes:",response.text)

