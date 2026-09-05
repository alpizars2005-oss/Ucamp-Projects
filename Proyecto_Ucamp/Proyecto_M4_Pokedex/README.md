# Construye una Pokédex — UCAMP Módulo 4

Proyecto final del **Módulo 4: Manejo de Archivos, Excepciones y Consumo de APIs**. La aplicación consume **PokéAPI** desde Python usando la librería `requests`.

El usuario escribe el nombre de un Pokémon; el programa valida la respuesta HTTP, muestra la información solicitada y guarda la respuesta completa en un archivo JSON dentro de la carpeta `pokedex/`.

## Índice

1. [Requisitos de la actividad cubiertos](#requisitos-de-la-actividad-cubiertos)
2. [Correspondencia con la rúbrica](#correspondencia-con-la-rúbrica)
3. [Requisitos para ejecutar](#requisitos-para-ejecutar)
4. [Ejemplo de resultado](#ejemplo-de-resultado-squirtle)
5. [Instalación](#instalación)
6. [Ejecución](#ejecución)
7. [Estructura del proyecto](#estructura-del-proyecto)
8. [Cómo lo hice](#cómo-lo-hice)
9. [Qué aprendí](#qué-aprendí-en-este-módulo)
10. [Pruebas](#pruebas)
11. [API utilizada](#api-utilizada)

## Requisitos de la actividad cubiertos

- Consume `https://pokeapi.co/api/v2/pokemon/{nombre}` con `requests`.
- Si el Pokémon no existe, muestra un mensaje específico para el código `404`.
- Valida otros códigos HTTP y errores de conexión.
- Muestra:
  - peso;
  - tamaño;
  - movimientos;
  - habilidades;
  - tipos;
  - estadísticas base;
  - enlace de la imagen frontal.
- Abre la imagen frontal en el navegador predeterminado cuando es posible.
- Crea automáticamente la carpeta `pokedex/`.
- Guarda en JSON la respuesta completa recibida de PokéAPI y el enlace frontal.
- Usa `try/except` para entradas, red, JSON y archivos.
- Incluye pruebas unitarias que no dependen de Internet.
- El código incorpora comentarios y docstrings útiles para explicar el flujo del programa.

## Correspondencia con la rúbrica

| Criterio | Evidencia en el proyecto |
|---|---|
| **Título e índice** | Este README incluye un título principal y un índice navegable. |
| **Consumo exitoso de PokéAPI** | `consultar_pokemon()` realiza una petición GET con `requests` y procesa la respuesta JSON. |
| **Validación de status codes** | Se manejan explícitamente `404`, errores `5xx` y otros códigos diferentes de `200`. |
| **Despliegue correcto de la información** | Se muestran peso, tamaño, tipos, habilidades, movimientos, estadísticas y el enlace frontal; además se intenta abrir el sprite en el navegador. |
| **Guardar adecuadamente el archivo .json** | `guardar_pokemon()` crea `pokedex/` y guarda la respuesta completa con `json.dump()`. |
| **Repositorio de GitHub** | El proyecto incluye código, README, dependencias, ejemplo JSON, pruebas y reflexión de aprendizaje. |
| **Código comentado correctamente** | El programa incluye comentarios educativos sobre HTTP, conversiones de unidades, JSON, imágenes y persistencia, además de docstrings por función. |

## Requisitos para ejecutar

- Python **3.9 o superior**.
- `pip` para instalar dependencias.
- Biblioteca `requests`.
- Conexión a Internet para consultas reales a PokéAPI.
- Permisos de escritura en la carpeta del proyecto para crear `pokedex/<pokemon>.json`.
- Un navegador web es opcional; únicamente se utiliza para intentar abrir la imagen frontal.

**PokéAPI no requiere API key**, por lo que este proyecto no necesita credenciales ni secretos.

## Ejemplo de resultado: Squirtle

Durante la verificación manual se realizó una búsqueda real de `squirtle`. El programa obtuvo correctamente el Pokémon **#7 Squirtle**, mostró sus datos, abrió la imagen frontal y creó localmente `pokedex/squirtle.json`.

Imagen frontal devuelta por PokéAPI:

![Squirtle](https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png)

Fragmento de la salida real verificada:

```text
POKÉDEX | #7 Squirtle
Peso: 9.0 kg
Tamaño: 0.5 m
Tipos: water
Habilidades: torrent, rain-dish

Estadísticas base:
  - hp: 44
  - attack: 48
  - defense: 65
  - special-attack: 50
  - special-defense: 64
  - speed: 43

Movimientos (105):
...

Imagen frontal:
https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png

Se abrió la imagen frontal en tu navegador.
Información guardada correctamente en: .../pokedex/squirtle.json
```

También se probó un nombre inexistente (`Turtle`) y el programa respondió correctamente:

```text
Error: No se encontró ningún Pokémon llamado 'turtle'.
```

## Instalación

Desde la raíz del repositorio:

```bash
python -m pip install -r requirements.txt
```

También puede instalarse únicamente la dependencia de este proyecto desde su carpeta:

```bash
python -m pip install -r Proyecto_Ucamp/Proyecto_M4_Pokedex/requirements.txt
```

La única biblioteca externa utilizada es `requests`. `json`, `pathlib`, `textwrap` y `webbrowser` forman parte de la biblioteca estándar de Python.

## Ejecución

Desde la raíz del repositorio:

```bash
python Proyecto_Ucamp/Proyecto_M4_Pokedex/pokedex.py
```

Después escribe, por ejemplo:

```text
squirtle
```

La ejecución genera:

```text
Proyecto_Ucamp/Proyecto_M4_Pokedex/pokedex/squirtle.json
```

## Estructura del proyecto

```text
Proyecto_M4_Pokedex/
├── pokedex.py
├── requirements.txt
├── README.md
├── pokedex/
│   └── pikachu_ejemplo.json
└── tests/
    └── test_pokedex.py
```

El archivo `pokedex/pikachu_ejemplo.json` sirve como muestra versionada de la estructura. Al ejecutar una búsqueda real, el programa crea `pokedex/<nombre>.json` con la respuesta completa actual de PokéAPI y el enlace frontal.

> La ejecución manual ya generó `squirtle.json` en el equipo local. Ese archivo no se reconstruye artificialmente en el repositorio: sólo debe versionarse a partir del archivo real generado por el programa.

## ¿Cómo lo hice?

1. Solicité el nombre del Pokémon y normalicé la entrada.
2. Construí la URL del recurso `pokemon` de PokéAPI.
3. Realicé una petición HTTP GET con `requests` y un timeout.
4. Validé el `status_code` antes de procesar la respuesta.
5. Convertí el JSON recibido a estructuras de Python.
6. Extraje peso, altura, movimientos, habilidades, tipos, estadísticas e imagen.
7. Mostré la información en consola e intenté abrir la imagen frontal.
8. Creé la carpeta `pokedex/` cuando no existía.
9. Guardé toda la respuesta de la API en un archivo `.json`.
10. Añadí manejo de excepciones y pruebas unitarias con respuestas simuladas.
11. Comenté las partes importantes del código para explicar decisiones y conversiones sin llenar cada línea de comentarios redundantes.

## ¿Qué aprendí en este módulo?

Con este proyecto practiqué cómo consumir una API web desde Python, interpretar respuestas JSON y manejar diferentes códigos de estado HTTP. También reforcé el uso de listas, diccionarios, funciones y excepciones con `try/except`.

La parte de persistencia me permitió practicar la creación de carpetas y archivos desde Python y comprender cómo guardar información estructurada en JSON. Las pruebas simuladas también me ayudaron a separar la lógica del programa de la disponibilidad de una API externa.

La verificación manual me permitió comprobar la diferencia entre una respuesta válida, como `squirtle`, y un recurso inexistente, como `turtle`, y confirmar que el programa crea correctamente el archivo JSON y abre el recurso gráfico proporcionado por la API.

## Pruebas

Las pruebas no realizan llamadas reales a PokéAPI:

```bash
python -m unittest discover -s Proyecto_Ucamp/Proyecto_M4_Pokedex/tests -v
```

### Estado de verificación

- **6/6 pruebas unitarias aprobadas**.
- Normalización y validación del nombre: aprobadas.
- Consulta HTTP simulada: aprobada.
- Manejo de Pokémon inexistente con `404`: aprobado.
- Conversión de peso, altura, tipos y habilidades: aprobada.
- Creación y lectura del archivo JSON: aprobada.
- Compilación de Python: aprobada.
- Prueba manual con `squirtle`: aprobada.
- Prueba manual con recurso inexistente: aprobada.
- GitHub Actions: aprobada en Python 3.11 y 3.13 antes del último ajuste documental; el workflow se vuelve a ejecutar con cada actualización del PR.

## API utilizada

- PokéAPI: https://pokeapi.co/
- Documentación: https://pokeapi.co/docs/v2
