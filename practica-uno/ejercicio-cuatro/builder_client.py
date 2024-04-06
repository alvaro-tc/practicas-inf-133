import requests
url = "http://localhost:8000/pacientes"
headers = {'Content-type': 'application/json'}

# POST /pacientes
data = {
    "ci": 12925767,
    "nombre": "Alvaro Ariel",
    "apellido": "Torrez Calle",
    "edad": 20,
    "genero": "masculino",
    "diagnostico": "Diabetes",
    "doctor": "Pedro Perez",
}
response2 = requests.post(url, json=data, headers=headers)
print("Crear paciente:",response2.text)

# GET /pacientes
response = requests.get(url=url)
print("Listar pacientes:",response.json())


# GET /pacientes/{ci}
response = requests.get(url=url+"/12925767")
print("Mostrar paciente:",response.json())


# GET /pacientes/?diagnostico={diagnostico}
response = requests.get(url=url+"/?diagnostico=Diabetes")
print("Mostrar pacientes POR:",response.json())

# GET /pacientes/?doctor={doctor}
response = requests.get(url=url+"/?doctor=Pedro Perez")
print("Mostrar pacientes POR:",response.json())


# PUT /pacientes/{ci}
data_update = {
    "ci": 12925768,
    "nombre": "Alvaro Ariel",
    "apellido": "Torrez Calle",
    "edad": 18,
    "genero": "masculino",
    "diagnostico": "bueno",
    "doctor": "Pepito Primero",
}
response2 = requests.put(url=url+"/12925767", json=data_update, headers=headers)
print("Cambiar paciente:",response2.text)


# DELETE /pacientes/{ci}
response3 = requests.delete(url=url+"/12925768")
print("Eliminar paciente:",response3.text)

# GET /pacientes
response = requests.get(url=url)
print("Monstra pacientes:",response.text)

