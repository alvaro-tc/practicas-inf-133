from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random
from urllib.parse import parse_qs, urlparse

partidas = {}

class Player:
    _instance = None
 
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.elemento = None
        return cls._instance
    
    def to_dict(self):
        return {"elemento": self.elemento}
class Partida:
    def __init__(self):
        self.elemento = None
        self.elemento_servidor = None
        self.resultado = None

    def __str__(self):
        return f"elemento: {self.elemento}, elemento_servidor: {self.elemento_servidor}, resultado: {self.resultado}"
    
    def jugarPartida(self,elemento):
        self.elemento=elemento
        self.elemento_servidor= random.choice(["piedra", "papel", "tijera"])
        if self.elemento_servidor == self.elemento:
            self.resultado = "empató"
        elif (self.elemento_servidor == "piedra" and self.elemento == "tijera") or \
                (self.elemento_servidor == "papel" and self.elemento == "piedra") or \
                (self.elemento_servidor == "tijera" and self.elemento == "papel"):
            self.resultado = "perdió"
        else:
            self.resultado = "ganó"

class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))


        
class PartidaService:
    def read_Partidas(self):
        return {index: partida.__dict__ for index, partida in partidas.items()}
    def search_Partidas(self,query_params):
        if "resultado" in query_params:
            resultado = query_params["resultado"][0]
        else:
            resultado = None
        if resultado:
            return {key: partida.__dict__ for key, partida in partidas.items() if getattr(partida, "resultado") == resultado}
        else:
            return {}
 
    def crear_Partida(self, post_data):
        elemento = post_data.get("elemento",None)
        partida = Partida()
        partida.jugarPartida(elemento)
       
        if partidas:
            new_id =max(partidas.keys()) + 1
        else:
            new_id=1
        partidas[new_id] = partida
        
        return {"id": new_id, **partidas[new_id].__dict__}




class PartidaHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        global player
        player = Player()
        self.partidas_service = PartidaService()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == "/partidas":
            data = self.partidas_service.read_Partidas()
            HTTPDataHandler.handle_response(self, 200, data)
        elif self.path.startswith("/partidas/"):
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            if query_params:
                response_data = self.partidas_service.search_Partidas(query_params)
                if response_data:
                    HTTPDataHandler.handle_response(self, 200, response_data)
                else:
                    HTTPDataHandler.handle_response(self, 404, {"message": "Partida(s) no encontrada(s)"})
            else:
                HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})

    def do_POST(self):
        if self.path == "/partidas":
            post_data = HTTPDataHandler.handle_reader(self)
            data = self.partidas_service.crear_Partida(post_data)
            HTTPDataHandler.handle_response(self, 201, data)
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})


def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, PartidaHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()


if __name__ == "__main__":
    main()
