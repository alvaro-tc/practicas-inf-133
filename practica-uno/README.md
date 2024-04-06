# PRACTICA PRIMER PARCIAL
## Antes de empezar:
Completa tus datos personales en la siguiente tabla:
-------------------------
| Nombres  | Apellidos  | CI   |
| -------- | ---------- | ---- |
| `Alvaro Ariel` | `Torrez Calle` | `12925767` |

## Ejercicio 1
Construye un servidor con el protocolo SOAP que permita a un cliente realizar las operaciones de suma, resta, multiplicación y división de dos números enteros.

## Ejercicio 2
Construye un API con GraphQL para gestionar el seguimiento de las plantas de un vivero. La API debe permitir:
- Crear una planta
- Listar todas las plantas
- Buscar plantas por especie
- Buscar las plantas que tienen frutos
- Actualizar la información de una planta
- Eliminar una planta

De las plantas se debe almacenar la siguiente información:
- ID (identificador único)
- Nombre común (nombre popular)
- Especie (nombre científico)
- Edad (en meses)
- Altura (en cm)
- Frutos (booleano)

**Rutas esperadas:**
- `/graphql`

## Ejercicio 3
Aplicando los principios de desarrollo de Software DRY, KISS, YAGNI y la S de SOLID construye un API RESTful para gestionar la información de los pacientes de un hospital. La API debe permitir:
- Crear un paciente
- Listar todos los pacientes
- Buscar pacientes por CI
- Listar a los pacientes que tienen diagnostico de `Diabetes`
- Listar a los pacientes que atiende el Doctor `Pedro Pérez`
- Actualizar la información de un paciente
- Eliminar un paciente

De los pacientes se debe almacenar la siguiente información:
- CI (identificador único)
- Nombre
- Apellido
- Edad
- Género
- Diagnóstico
- Doctor (nombre del doctor que atiende al paciente)

**Rutas esperadas:**
- POST `/pacientes`
- GET `/pacientes`
- GET `/pacientes/{ci}`
- GET `/pacientes/?diagnostico={diagnostico}`
- GET `/pacientes/?doctor={doctor}`
- PUT `/pacientes/{ci}`
- DELETE `/pacientes/{ci}`

## Ejercicio 4
Aplica el patron de diseño BUILDER al ejercicio 3.

## Ejercicio 5
Construye una API RESTful para gestionar la información del los animales de un zoologico. La API debe permitir:

- Crear un animal
- Listar todos los animales
- Buscar animales por especie
- Buscar animales por género
- Actualizar la información de un animal
- Eliminar un animal

De los animales se debe almacenar la siguiente información:
- ID (identificador único)
- Nombre
- Especie
- Género
- Edad
- Peso

**Rutas esperadas:**
- POST `/animales`
- GET `/animales`
- GET `/animales?especie={especie}`
- GET `/animales/?genero={genero}`
- PUT `/animales/{id}`
- DELETE `/animales/{id}`

## Ejercicio 6
Aplica el patron de diseño FACTORY al ejercicio 5 considerando que los animales pueden ser de tipo `Mamífero`, `Ave`, `Reptil`, `Anfibio` o `Pez`.

## Ejercicio 7
Aplicando los principios de desarrollo de Software DRY, KISS, YAGNI y la S de SOLID construye un API RESTful con el patron de diseño SINGLETON para jugar piedra, papel o tijera con el servidor. La API debe permitir:

- Crear una partida
- Listar todas las partidas
- Listar partidas perdidas
- Listar partidas ganadas

De las partidas se debe almacenar la siguiente información:
- ID (identificador único)
- Elemento del jugador (piedra, papel o tijera)
- Elemento del servidor (piedra, papel o tijera)
- Resultado (ganó, perdió o empató)

**Rutas esperadas:**
- POST `/partidas`
- GET `/partidas`
- GET `/partidas?resultado={resultado}`

El servidor debe seleccionar aleatoriamente el elemento a jugar y el resultado debe ser calculado en base a las reglas del juego.

Reglas del juego:
- Piedra gana a tijera
- Tijera gana a papel
- Papel gana a piedra
- Si ambos jugadores eligen el mismo elemento, la partida es un empate.

Ejemplo de la solicitud POST `/partidas`:
```json
{
  "elemento": "piedra"
}
```

Ejemplo de la respuesta POST `/partidas`:
```json
{
  "id": 1,
  "elemento": "piedra",
  "elemento_servidor": "tijera",
  "resultado": "ganó"
}
```

## Ejercicio 8
Aplicando los principios de desarrollo de Software DRY, KISS, YAGNI y la S de SOLID construye una API RESTful para encriptar mensajes, la API debe permitir:

- Crear un mensaje
- Listar todos los mensajes
- Buscar mensajes por ID
- Actualizar el contenido de un mensaje
- Eliminar un mensaje

De los mensajes se debe almacenar la siguiente información:
- ID (identificador único)
- Contenido (mensaje a encriptar)
- Contenido encriptado

El encriptado debe ser realizado con el algoritmo de cifrado César, donde cada letra del mensaje debe ser reemplazada por la letra que se encuentra 3 posiciones adelante en el alfabeto. Por ejemplo, la letra `a` debe ser reemplazada por la letra `d`, la letra `b` por la letra `e`, y así sucesivamente.

*Sugerencia: Utiliza los ASCII codes para realizar el encriptado.*

**Rutas esperadas:**
- POST `/mensajes`
- GET `/mensajes`
- GET `/mensajes/{id}`
- PUT `/mensajes/{id}`
- DELETE `/mensajes/{id}`


# Entrega
- Debes crear la siguiente estructura de carpetas en tu repositorio para presentar tus soluciones:
```bash
practica-uno
├── ejercicio-uno
│   ├── soap_server.py
│   └── soap_client.py
├── ejercicio-dos
│   ├── gql_server.py
│   └── gql_client.py
├── ejercicio-tres
│   ├── rest_server.py
│   └── rest_client.py
├── ejercicio-cuatro
│   ├── builder_server.py
│   └── builder_client.py
├── ejercicio-cinco
│   ├── rest_server.py
│   └── rest_client.py
├── ejercicio-seis
│   ├── factory_server.py
│   └── factory_client.py
├── ejercicio-siete
│   ├── singleton_server.py
│   └── singleton_client.py
└── ejercicio-ocho
    ├── cesar_server.py
    └── cesar_client.py
```

- Una vez que hayas completado la práctica, adjunta el enlace de tu repositorio en la tarea asignada como `PRACTICA PRIMER PARCIAL` en la plataforma Google Classroom.

- Fecha LIMITE de entrega: 06/04/2024