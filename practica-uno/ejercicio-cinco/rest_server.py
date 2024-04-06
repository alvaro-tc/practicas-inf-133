from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

animales = {}
class Animal:
    def __init__(self):
        self.nombre = None
        self.especie = None
        self.genero = None
        self.edad = None
        self.peso = None

    def setAnimal(self,nombre,especie,genero,edad,peso):
        self.nombre= nombre
        self.especie= especie
        self.genero= genero
        self.edad= edad
        self.peso= peso
    
class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type","application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
    @staticmethod
    def handle_reader(handler):
        content_length = int (handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))

class AnimalService:
    def crearAnimal(self,data):
        nombre =data.get("nombre",None)
        especie =data.get("especie",None)
        genero =data.get("genero",None)
        edad =data.get("edad",None)
        peso =data.get("peso",None)
        animal = Animal()
        animal.setAnimal(nombre,especie,genero,edad,peso)

        if not animales:
            animales[1]=animal
        else:
            animales[max(animales.keys()) +1]=animal

        return animal.__dict__
    def readAnimales(self):
        return {index: animal.__dict__ for index, animal in animales.items()}
    
    def updateAnimal(self, animal_id, data):
        if animal_id in animales:

            animal = animales[animal_id]
            nombre = data.get("nombre", None)
            especie = data.get("especie", None)
            genero = data.get("genero", None)
            edad = data.get("edad", None)
            peso = data.get("peso", None)
            if nombre:
                animal.nombre= nombre
            if especie:
                animal.especie= especie
            if genero:
                animal.genero = genero
            if edad:
                animal.edad = edad
            if peso:
                animal.peso = peso
            return animal.__dict__
        else:
            return None
    def search_Especie (self,query_params):
        if "especie" in query_params:
            especie = query_params["especie"][0]
        else:
            especie = None
        if especie:
            return {key: animal.__dict__ for key, animal in animales.items() if getattr(animal, "especie") == especie}
        else:
            return {}
    def search_Genero (self,query_params):
        if "genero" in query_params:
            genero = query_params["genero"][0]
        else:
            genero = None
        if genero:
            return {key: animal.__dict__ for key, animal in animales.items() if getattr(animal, "genero") == genero}
        else:
            return {}
    
    def searchAnimal(self,animal_id):
        animal = animales.get(animal_id)
        return animal.__dict__
    def deleteAnimal(self,animal_id):
        del animales[animal_id]
        return animal_id

class AnimalesHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/animales":
            response_data = AnimalService.readAnimales(self)
            HTTPDataHandler.handle_response(self,200,response_data)
        elif self.path.startswith("/animales/"):
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            if query_params:
                response_especie_data = AnimalService.search_Especie(self,query_params)
                response_genero_data = AnimalService.search_Genero(self,query_params)
                if response_especie_data:
                    HTTPDataHandler.handle_response(self, 200, response_especie_data)
                elif response_genero_data:
                    HTTPDataHandler.handle_response(self, 200, response_genero_data)
                else:
                    HTTPDataHandler.handle_response(self, 404, {"message": "Animal no encontrado"})
            else:
                animal = AnimalService.searchAnimal(self,int(self.path.split("/")[-1]))
                if animal:
                    HTTPDataHandler.handle_response(self, 200, animal)
                else:
                    HTTPDataHandler.handle_response(self, 404, {"message": "Animal no encontrado"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})
    def do_POST(self):
        # POST request to create a new patient
        data = HTTPDataHandler.handle_reader(self)
        if self.path == "/animales":
            new_animal = AnimalService.crearAnimal(self,data)
            HTTPDataHandler.handle_response(self, 201, new_animal)
        else:

            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})

    def do_PUT(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            response_data = AnimalService.updateAnimal(self,animal_id, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(self, 404, {"message": "Animal no encontrado"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})

    def do_DELETE(self):

        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            if animal_id in animales:
                response_data = AnimalService.deleteAnimal(self,animal_id)
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