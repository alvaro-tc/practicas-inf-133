from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from graphene import ObjectType, String,Boolean, Int, List, Schema, Field, Mutation

class Planta(ObjectType):
    id = Int()
    nombreComun = String()
    especie = String()
    edad = Int()
    altura = Int()
    fruto = Boolean()

plantas = [
    Planta(
        id=1, 
        nombreComun="margarita", 
        especie="margaritus alboreasis", 
        edad=3,
        altura=5,
        fruto = True
    )
]

class CrearPlanta(Mutation):
    class Arguments:
        id = Int()
        nombreComun = String()
        especie = String()
        edad = Int()
        altura = Int()
        fruto = Boolean()

    planta = Field(Planta)
    def mutate(root, info, nombreComun,especie,edad,altura,fruto):
        nueva_planta = Planta(
            id= plantas[-1].id +1,
            nombreComun=nombreComun, 
            especie=especie, 
            edad=edad,
            altura=altura,
            fruto=fruto
        )
        plantas.append(nueva_planta)
        return CrearPlanta(planta=nueva_planta)

class DeletePlanta(Mutation):
    class Arguments:
        id = Int()
    planta = Field(Planta)
    def mutate(root, info, id):
        for i, planta in enumerate(plantas):
            if planta.id == id:
                plantas.pop(i)
                return DeletePlanta(planta=planta)
        return None

 
class PutPlanta(Mutation):
    class Arguments:
        id = Int()
        nombreComun = String()
        especie = String()
        edad = Int()
        altura = Int()
        fruto = Boolean()
        
    planta =Field(Planta)

    def mutate(root, info, id, nombreComun,especie,edad,altura,fruto):
        for i, planta in enumerate(plantas):
            if planta.id ==id:
                planta.nombreComun=nombreComun
                planta.especie=especie
                planta.edad=edad
                planta.altura=altura
                planta.fruto=fruto
                return PutPlanta(planta=planta)
        return None


class Query(ObjectType):
    plantas= List(Planta)
    def resolve_plantas(root,info):
        return(plantas)
    
    planta_por_id = Field(Planta, id=Int())
    planta_por_nombreComun_y_especie = Field(Planta, nombreComun=String(), especie=String())
    planta_por_especie = List(Planta, especie=String())

    def resolve_planta_por_id(root, info, id):
        for planta in plantas:
            if planta.id == id:
                return planta
        return None
    
    def resolve_planta_por_nombreComun_y_especie(root, info, nombreComun, especie):
        for planta in plantas:
            if planta.nombreComun == nombreComun and planta.especie == especie:
                return planta
        return None
    
    def resolve_planta_por_especie(root, info, especie):
        lPlantas=[]
        for planta in plantas:
            if planta.especie == especie:
                lPlantas.append(planta)
        return lPlantas
    def resolve_plantas_por_fruto(root, info, fruto):
        lPlantas=[]
        for planta in plantas:
            if planta.fruto == fruto:
                lPlantas.append(planta)
        return lPlantas
    
    


class Mutations(ObjectType):
    crear_planta = CrearPlanta.Field()
    delete_planta = DeletePlanta.Field()
    put_planta = PutPlanta.Field()
  

schema = Schema(query=Query, mutation=Mutations)



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







class GraphQLHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path == "/graphql":
            data = HTTPDataHandler.handle_reader(self)
            result = schema.execute(data["query"])
            HTTPDataHandler.handle_response(self, 200, result.data)
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no existente"})


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, GraphQLHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()