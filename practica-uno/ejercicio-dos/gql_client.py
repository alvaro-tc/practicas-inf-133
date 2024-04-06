import requests
url = 'http://localhost:8000/graphql'

query_get= """
    { 
        plantas{
            id
            nombreComun
            especie
            edad
            altura
            fruto
        }
    }
"""

response_mutation = requests.post(url, json={'query': query_get})
print(response_mutation.text)

query_crear = """
mutation {
        crearPlanta(nombreComun: "margarota", especie: "margaritus alboreasis", edad:3, altura :5,fruto:false) {
            planta {
                id
                nombreComun
                especie
                edad
                altura
                fruto
            }
        }
    }
"""
response_mutation = requests.post(url, json={'query': query_crear})
print(response_mutation.text)


query_poner= """
mutation {
        putPlanta(id : 2,nombreComun: "margarota", especie: "margaritus alboreasis", edad:3, altura :15,fruto:false) {
            planta {
                id
                nombreComun
                especie
                edad
                altura
                fruto
            }
        }
    }
"""
response_mutation = requests.post(url, json={'query': query_poner})
print(response_mutation.text)


query_get= """
    {
        plantas{
            id
            nombreComun
            especie
            edad
            altura
            fruto
        }
    }
"""

response_mutation = requests.post(url, json={'query': query_get})
print(response_mutation.text)


query_especie = """
    {
        plantaPorEspecie(especie: "margaritus alboreasis"){
            id
            nombreComun
            especie
            edad
            altura
            fruto
        }
    }
"""

response_mutation = requests.post(url, json={'query': query_especie})
print(response_mutation.text)
