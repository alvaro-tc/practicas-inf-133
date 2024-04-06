from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs


pacientes = {}


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
class Paciente:
    def __init__(self):
        self.nombre = None
        self.apellido = None
        self.edad = None
        self.genero = None
        self.diagnostico = None
        self.doctor = None

    def setPaciente(self,nombre,apellido,edad,genero,diagnostico,doctor):
        self.nombre= nombre
        self.apellido= apellido
        self.edad= edad
        self.genero= genero
        self.diagnostico= diagnostico
        self.doctor= doctor
    
        
class PacienteService:
    def deletePaciente(self, paciente_ci):
        del pacientes[paciente_ci]
        return paciente_ci
    def updatePaciente(self, paciente_ci, data):
        if paciente_ci in pacientes:
            paciente = pacientes[paciente_ci]
            nombre = data.get("nombre", None)
            apellido = data.get("apellido", None)
            edad = data.get("edad", None)
            genero = data.get("genero", None)
            diagnostico = data.get("diagnostico", None)
            doctor = data.get("doctor", None)
            ci = data.get("ci", None)
            if nombre:
                paciente.nombre= nombre
            if apellido:
                paciente.apellido= apellido
            if edad:
                paciente.edad = edad
            if genero:
                paciente.genero = genero
            if diagnostico:
                paciente.diagnostico = diagnostico
            if doctor:
                paciente.doctor= doctor
            if ci:
                pacientes[ci] = pacientes.pop(paciente_ci)
            return paciente.__dict__
    def read_Pacientes():
        return {index: paciente.__dict__ for index, paciente in pacientes.items()}
    def search_Paciente(self,paciente_ci):
        paciente = pacientes.get(paciente_ci)
        return paciente.__dict__
    def search_Diagnostico(self,diagnostico):
        return {key: paciente.__dict__ for key, paciente in pacientes.items() if getattr(paciente, "diagnostico") == diagnostico}
    def search_Doctor(self,doctor):
        return {key: paciente.__dict__ for key, paciente in pacientes.items() if getattr(paciente, "doctor") == doctor}
    
    def crearPaciente(self,data):
        ci = data.get("ci", None)
        nombre = data.get("nombre", None)
        apellido = data.get("apellido", None)
        edad = data.get("edad", None)
        genero = data.get("genero", None)
        diagnostico = data.get("diagnostico", None)
        doctor = data.get("doctor", None)
        paciente = Paciente()
        paciente.setPaciente(nombre,apellido,edad,genero,diagnostico,doctor)
        pacientes[ci]=paciente
        return paciente.__dict__
    
class PacientesHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/pacientes":
            response_data = PacienteService.read_Pacientes()
            HTTPDataHandler.handle_response(self, 200, response_data)
        elif self.path.startswith("/pacientes/"):
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            if 'diagnostico' in query_params:
                diagnostico = query_params['diagnostico'][0]
                response_data = PacienteService.search_Diagnostico(self,diagnostico)
                if response_data:
                    HTTPDataHandler.handle_response(self, 200, response_data)
                else:
                    HTTPDataHandler.handle_response(self, 404, {"message": "Paciente(s) no encontrado(s)"})
            elif 'doctor' in query_params:
                doctor = query_params['doctor'][0]
                response_data = PacienteService.search_Doctor(self,doctor)
                if response_data:
                    HTTPDataHandler.handle_response(self, 200, response_data)
                else:
                    HTTPDataHandler.handle_response(self, 404, {"message": "Paciente(s) no encontrado(s)"})

            else:
                paciente=PacienteService.search_Paciente(self,int(self.path.split("/")[-1]))
                if paciente:
                    HTTPDataHandler.handle_response(self, 200, paciente)
                else:
                    HTTPDataHandler.handle_response(self, 404, {"message": "Paciente no encontrado"})
                
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})


    def do_POST(self):
        data = HTTPDataHandler.handle_reader(self)
        if self.path == "/pacientes":
            new_paciente_key=PacienteService.crearPaciente(self,data)
            HTTPDataHandler.handle_response(self,201,new_paciente_key)
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})


    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            paciente_ci = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            response_data = PacienteService.updatePaciente(self,paciente_ci,data)
            if response_data:
                HTTPDataHandler.handle_response(self,200,response_data)
            else:
                HTTPDataHandler.handle_response(self,404,{"message": "Paciente no encontrado"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})

    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            paciente_ci = int(self.path.split("/")[-1])
            if paciente_ci in pacientes:
                response_data=PacienteService.deletePaciente(self,paciente_ci)
                HTTPDataHandler.handle_response(self,200,{"message": "Paciente eliminado"})
            else:
                HTTPDataHandler.handle_response(self,404,{"message": "Paciente no encontrado"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})


def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, PacientesHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()


if __name__ == "__main__":
    main()