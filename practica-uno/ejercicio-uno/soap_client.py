from zeep import Client
client = Client('http://localhost:8000')

# SUMA
result_suma = client.service.Suma(10, 5)
print("Suma:", result_suma)

# RESTA
result_resta = client.service.Resta(10, 5)
print("Resta:", result_resta)

# MULTIPLICACION
result_multiplicacion = client.service.Multiplicacion(10, 5)
print("Multiplicación:", result_multiplicacion)

# DIVISION
result_division = client.service.Division(10, 5)
print("División:", result_division)
