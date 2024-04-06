from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler

def suma(a, b):
    return a + b

def resta(a, b):
    return a - b

def multiplicacion(a, b):
    return a * b

def division(a, b):
    if b != 0:
        return a / b
    else:
        return "Error"
    
dispatcher = SoapDispatcher(
    "soap-server",
    location="http://localhost:8000",
    action="http://localhost:8000",
    namespace="http://localhost:8000",
    trace=True,
    ns=True,
)

dispatcher.register_function(
    "Suma",
    suma,
    returns={"resultado": int},
    args={"a": int, "b": int},
)

dispatcher.register_function(
    "Resta",
    resta,
    returns={"resultado": int},
    args={"a": int, "b": int},
)

dispatcher.register_function(
    "Multiplicacion",
    multiplicacion,
    returns={"resultado": int},
    args={"a": int, "b": int},
)

dispatcher.register_function(
    "Division",
    division,
    returns={"resultado": float},
    args={"a": int, "b": int},
)

server = HTTPServer(("",8000), SOAPHandler)
server.dispatcher = dispatcher
print("Servidor SOAP iniciado en http://localhost:8000/")
server.serve_forever()