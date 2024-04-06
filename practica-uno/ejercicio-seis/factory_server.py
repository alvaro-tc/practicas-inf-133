from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

animales ={}

class Animales:
    def __init__(self, especie, nombre, genero, edad, peso):
        self.nombre = nombre
        self.especie = especie
        self.genero = genero
        self.edad = edad
        self.peso = peso

class Mamifero(Animales):
    def __init__(self, nombre, genero, edad, peso):
        super().__init__("mamifero",nombre, genero, edad, peso)
class Ave(Animales):
    def __init__(self, nombre, genero, edad, peso):
        super().__init__("ave", nombre, genero, edad, peso)
class Reptil(Animales):
    def __init__(self, nombre, genero, edad, peso):
        super().__init__("reptil", nombre, genero, edad, peso)
class Anfibio(Animales):
    def __init__(self, nombre, genero, edad, peso):
        super().__init__("anfibio", nombre, genero, edad, peso)
class Pez(Animales):
    def __init__(self, nombre, genero, edad, peso):
        super().__init__("pez", nombre, genero, edad, peso)

class AnimalFactory:
    @staticmethod
    def createAnimal(nombre,especie, genero, edad, peso):
        if especie == "mamifero":
            return Mamifero(nombre, genero, edad, peso)
        elif especie == "ave":
            return Ave(nombre, genero, edad, peso)
        elif especie == "reptil":
            return Reptil(nombre, genero, edad, peso)
        elif especie == "anfibio":
            return Anfibio(nombre, genero, edad, peso)
        elif especie == "pez":
            return Pez(nombre, genero, edad, peso)
        else:
            return None

class HTTPDataHandler:
    @staticmethod
    def handle_response(handler,status,data):
        handler.send_response(status)
        handler.send_header("Content-type","applicacion/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))

class AnimalService:
    def __init__(self):
        self.factory = AnimalFactory()

    def crearAnimal(self,data):
        nombre= data.get("nombre",None)
        especie= data.get("especie",None)
        genero= data.get("genero",None)
        edad= data.get("edad",None)
        peso= data.get("peso",None)
        
        animal = self.factory.createAnimal(
            nombre,especie,genero,edad,peso
        )
        if animal:
            if animales:
                animales[max(animales.keys())+1]=animal
            else:
                animales[1] = animal
            return animal
        else:
            return {"Message":"Especie no valido"}
        
        
    def readAnimales(self):
        return {index: animal.__dict__ for index, animal in animales.items()}
    def updateAnimal(self, animal_id, data):
        if animal_id in animales:
            animal = animales[animal_id]
            nombre = data.get("nombre", None)
            genero = data.get("genero", None)
            edad = data.get("edad", None)
            peso = data.get("peso", None)
            if nombre:
                animal.nombre = nombre
            if genero:
                animal.genero = genero
            if edad:
                animal.edad = edad
            if peso:
                animal.peso = peso    
            return animal
        else:
            return None
    def deleteAnimal(self, animal_id):
        if animal_id in animales:
            del animales[animal_id]
            return {"message": "Animal eliminado"}
        else:
            return None
    def search(self, atribute, query_params):
        if atribute in query_params:
            query = query_params[atribute][0]
        else:
            query = None
        if query:
            if (atribute == "especie"):
                return {key: animal.__dict__ for key, animal in animales.items() if getattr(animal, atribute) == query}
            if (atribute == "genero"):
                return {key: animal.__dict__ for key, animal in animales.items() if getattr(animal, atribute) == query}
        else:
            return None
    def searchAnimal(self,animal_id):
        animal = animales.get(animal_id)
        return animal
    
class AnimalesHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.animal_service = AnimalService()
        super().__init__(*args,*kwargs)
    def do_GET(self):
        if self.path == "/animales":
            response_data = self.animal_service.readAnimales()
            HTTPDataHandler.handle_response(self,200,response_data)
        elif self.path.startswith("/animales/"):
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            if query_params:
                response_especie_data = self.animal_service.search("especie",query_params)
                response_genero_data = self.animal_service.search("genero",query_params)
                if response_especie_data:
                    HTTPDataHandler.handle_response(self, 200, response_especie_data)
                elif response_genero_data:
                    HTTPDataHandler.handle_response(self, 200, response_genero_data)
                else:
                    HTTPDataHandler.handle_response(self, 404, {"message": "Animal no encontrado"})
            else:
                animal = self.animal_service.searchAnimal(int(self.path.split("/")[-1]))
                if animal:
                    HTTPDataHandler.handle_response(self, 200, animal.__dict__)
                else:
                    HTTPDataHandler.handle_response(self, 404, {"message": "Animal no encontrado"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})
    def do_POST(self): 
        # POST request to create a new patient
        data = HTTPDataHandler.handle_reader(self)
        if self.path == "/animales":
            new_animal = self.animal_service.crearAnimal(data)
            HTTPDataHandler.handle_response(self, 201, new_animal.__dict__)
        else:

            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})

    def do_PUT(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.animal_service.updateAnimal(animal_id, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(self, 404, {"message": "Animal no encontrado"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})

    def do_DELETE(self):

        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            if animal_id in animales:
                response_data = self.animal_service.deleteAnimal(animal_id)
                HTTPDataHandler.handle_response(self, 200, {"message": "Animal eliminado"})
            else:
                HTTPDataHandler.handle_response(self, 404, {"message": "Animal no encontrado"})
        else:

            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})

        
def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, AnimalesHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()


if __name__ == "__main__":
    main()