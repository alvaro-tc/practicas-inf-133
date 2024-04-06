from http.server import BaseHTTPRequestHandler, HTTPServer
import json

mensajes ={}


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

class Mensaje:
    def __init__(self):
        self.contenido = None
        self.contenido_encriptado = None

    def setMensaje(self,contenido):
        self.contenido= contenido
        self.contenido_encriptado = ''
        for i in contenido:
            if i==" ":
                self.contenido_encriptado= self.contenido_encriptado+ " "
            elif i == "x":
                self.contenido_encriptado= self.contenido_encriptado+ "a"
            elif i == "y":
                self.contenido_encriptado= self.contenido_encriptado+ "b"
            elif i == "z":
                self.contenido_encriptado= self.contenido_encriptado+ "c"
            else:
                self.contenido_encriptado = self.contenido_encriptado+ str(chr((ord(i)+3)))


class MensajeService:
        
    def deleteMensaje(self, mensaje_id):
        del mensajes[mensaje_id]
        return mensaje_id

    def read_Mensajes(self):
        return {index: mensaje.__dict__ for index, mensaje in mensajes.items()}
    def search_Mensajes(self,mensaje_id):
        mensaje = mensajes.get(mensaje_id)
        if mensaje:
            return mensaje.__dict__
        else:
            return None
    def update_Mensaje(self,mensaje_id,data):
        if mensaje_id in mensajes:
            contenido = data.get("contenido", None)
            if contenido:
                mensaje = Mensaje()
                mensaje.setMensaje(contenido)
                mensajes[mensaje_id]= mensaje
                return mensaje.__dict__
            else:
                return {}
        else:
            return None
    def crearMensaje(self,post_data):
        contenido = post_data.get("contenido", None)
        mensaje = Mensaje()
        mensaje.setMensaje(contenido)

        if mensajes:
            new_id = [max(mensajes.keys())]
        else:
            new_id=1
        mensajes[new_id]=mensaje
        return mensajes[new_id].__dict__

class MensajesHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.mensajes_service = MensajeService()
        super().__init__(*args,*kwargs)
    def do_GET(self):
        if self.path == "/mensajes":
            response_data = self.mensajes_service.read_Mensajes()
            HTTPDataHandler.handle_response(self,200,response_data)
        elif self.path.startswith("/mensajes/"):
            mensaje = self.mensajes_service.search_Mensajes(int(self.path.split("/")[-1]))
            if mensaje:
                HTTPDataHandler.handle_response(self, 200, mensaje)
            else:
                HTTPDataHandler.handle_response(self, 404, {"message": "Mensaje no encontrado"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})
    def do_POST(self):
        
        if self.path == "/mensajes":
            data = HTTPDataHandler.handle_reader(self)
            new_mensaje = self.mensajes_service.crearMensaje(data)
            HTTPDataHandler.handle_response(self, 201, new_mensaje)
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})

    def do_PUT(self):
        if self.path.startswith("/mensajes/"):
            mensaje_id = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.mensajes_service.update_Mensaje(mensaje_id, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(self, 404, {"message": "Mensaje no encontrado"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})

    def do_DELETE(self):

        if self.path.startswith("/mensajes/"):
            mensaje_id = int(self.path.split("/")[-1])
            if mensaje_id in mensajes:
                response_data = self.mensajes_service.deleteMensaje(mensaje_id)
                HTTPDataHandler.handle_response(self, 200, {"message": "Mensaje eliminado correctamente"})
            else:
                HTTPDataHandler.handle_response(self, 404, {"message": "Mensaje no encontrado"})
        else:

            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})

        
def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, MensajesHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()


if __name__ == "__main__":
    main()
    