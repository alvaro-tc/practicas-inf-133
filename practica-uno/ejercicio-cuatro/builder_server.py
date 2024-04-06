from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

pacientes = {}

class Paciente:
    def __init__(self):
        self.nombre = None
        self.apellido = None
        self.edad = None
        self.genero = None
        self.diagnostico= None
        self.doctor = None
    def __str__(self):
        return f"nombre: {self.nombre}, apellido: {self.apellido}, edad: {self.edad}, genero: {self.genero}, diagnostico: {self.diagnostico}, doctor: {self.doctor}"
    #Lista: {', '.join(self.lista)

class PacienteBuilder:
    def __init__(self):
        self.paciente = Paciente()
    
    def set_nombre(self,nombre):
        self.paciente.nombre = nombre

    def set_apellido(self,apellido):
        self.paciente.apellido = apellido

    def set_edad(self,edad):
        self.paciente.edad = edad
    
    def set_genero(self,genero):
        self.paciente.genero = genero
    
    def set_diagnostico(self,diagnostico):
        self.paciente.diagnostico = diagnostico
    
    def set_doctor(self,doctor):
        self.paciente.doctor = doctor

    def get_paciente(self):
        return self.paciente
    
class Pacientes:
    def __init__(self,builder):
        self.builder = builder
    
    def create_paciente(self,nombre,apellido,edad,genero,diagnostico,doctor):
        self.builder.set_nombre(nombre)
        self.builder.set_apellido(apellido)
        self.builder.set_edad(edad)
        self.builder.set_genero(genero)
        self.builder.set_diagnostico(diagnostico)
        self.builder.set_doctor(doctor)
        return self.builder.get_paciente()
        
    
class PacienteService:
    def __init__(self):
        self.builder = PacienteBuilder()
        self.pacientes = Pacientes(self.builder)

    def create_paciente(self, post_data):
        ci = post_data.get('ci', None)
        nombre = post_data.get('nombre', None)
        apellido = post_data.get('apellido', None)
        edad = post_data.get('edad', None)
        genero = post_data.get('genero', None)
        diagnostico = post_data.get('diagnostico', None)
        doctor = post_data.get('doctor', None)

        paciente = self.pacientes.create_paciente(nombre,apellido,edad,genero,diagnostico,doctor)
        pacientes[ci]=paciente
        
        return {
            "nombre": nombre,
            "apellido": apellido,
            "edad": edad,
            "genero": genero,
            "diagnostico": diagnostico,
            "doctor": doctor
        }

    
    def read_pacientes(self):
        return {index: paciente.__dict__ for index, paciente in pacientes.items()}
    
    def search_paciente(self,ci):
        paciente = next((paciente for index, paciente in pacientes.items() if index == ci), None)
        if paciente:
            return paciente.__dict__
        else:
            return None
        
    def search_diagnostico(self,diagnostico):
        pacientes_con_diagnostico = {}

        for indice, paciente in pacientes.items():
            if paciente.diagnostico == diagnostico:
                pacientes_con_diagnostico[indice] = paciente.__dict__

        return pacientes_con_diagnostico
    
    def search_doctor(self,doctor):
        pacientes_con_doctor = {}

        for indice, paciente in pacientes.items():
            if paciente.doctor == doctor:
                pacientes_con_doctor[indice] = paciente.__dict__

        return pacientes_con_doctor
    
    def update_paciente(self, paciente_ci, post_data):
        if paciente_ci in pacientes:
            paciente = pacientes[paciente_ci]
            ci = post_data.get('ci', None)
            nombre = post_data.get('nombre', None)
            apellido = post_data.get('apellido', None)
            edad = post_data.get('edad', None)
            genero = post_data.get('genero', None)
            diagnostico = post_data.get('diagnostico', None)
            doctor = post_data.get('doctor', None)
            if nombre:
                paciente.nombre = nombre
            if apellido:
                paciente.apellido = apellido
            if edad:
                paciente.edad = edad
            if genero:
                paciente.genero = genero
            if diagnostico:
                paciente.diagnostico = diagnostico
            if doctor:
                paciente.doctor = doctor
            if ci:
                pacientes[ci] = pacientes.pop(paciente_ci)
            return paciente
        else:
            return None
        
    def delete_paciente(self, paciente_ci):
        if paciente_ci in pacientes:
            return pacientes.pop(paciente_ci)
        else:
            return None
        

class HTTPDataHandler:
    @staticmethod
    def handle_response(handler,status,data):
        handler.send_response(status)
        handler.send_header("Content-type","application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
    @staticmethod
    def handle_reader(handler):
        content_lenght = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_lenght)
        return json.loads(post_data.decode("utf-8"))
class PacienteHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controller = PacienteService()
        super().__init__(*args, **kwargs)
    

    def do_POST(self):
        if self.path == '/pacientes':
            data = HTTPDataHandler.handle_reader(self)
            response_data= self.controller.create_paciente(data)
            HTTPDataHandler.handle_response(self, 201, response_data)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_GET(self):
        if self.path == "/pacientes":
            response_data = PacienteService.read_pacientes(self)
            HTTPDataHandler.handle_response(self, 200, response_data)
        elif self.path.startswith("/pacientes/"):
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            if 'diagnostico' in query_params:
                diagnostico = query_params['diagnostico'][0]
                response_data = PacienteService.search_diagnostico(self,diagnostico)
                if response_data:
                    HTTPDataHandler.handle_response(self, 200, response_data)
                else:
                    HTTPDataHandler.handle_response(self, 404, {"message": "Paciente(s) no encontrado(s)"})
            elif 'doctor' in query_params:
                doctor = query_params['doctor'][0]
                response_data = PacienteService.search_doctor(self,doctor)
                if response_data:
                    HTTPDataHandler.handle_response(self, 200, response_data)
                else:
                    HTTPDataHandler.handle_response(self, 404, {"message": "Paciente(s) no encontrado(s)"})

            else:
                paciente=PacienteService.search_paciente(self,int(self.path.split("/")[-1]))
                if paciente:
                    HTTPDataHandler.handle_response(self, 200, paciente)
                else:
                    HTTPDataHandler.handle_response(self, 404, {"message": "Paciente no encontrado"})
                
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})



    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            index = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.update_paciente(index, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "Índice de paciente no válido"}
                )
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            index = int(self.path.split("/")[-1])
            deleted_pizza = self.controller.delete_paciente(index)
            if deleted_pizza:
                HTTPDataHandler.handle_response(
                    self, 200, {"message": "Paciente eliminado correctamente"}
                )
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "Indice de paciente no valido"}
                )
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})


def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, PacienteHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()


if __name__ == "__main__":
    main()