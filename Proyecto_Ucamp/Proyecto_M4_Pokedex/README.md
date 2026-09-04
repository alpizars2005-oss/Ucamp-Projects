# Construye una Pokédex — UCAMP Módulo 4

Proyecto final del **Módulo 4: Manejo de Archivos, Excepciones y Consumo de APIs**. La aplicación consume **PokéAPI** desde Python usando la librería `requests`.

El usuario escribe el nombre de un Pokémon; el programa valida la respuesta HTTP, muestra la información solicitada y guarda la respuesta completa en un archivo JSON dentro de la carpeta `pokedex/`.

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

## Requisitos para ejecutar

- Python **3.9 o superior**.
- `pip` para instalar dependencias.
- Biblioteca `requests`.
- Conexión a Internet para consultas reales a PokéAPI.
- Permisos de escritura en la carpeta del proyecto para crear `pokedex/<pokemon>.json`.
- Un navegador web es opcional; únicamente se utiliza para intentar abrir la imagen frontal.

**PokéAPI no requiere API key**, por lo que este proyecto no necesita credenciales ni secretos.

## Ejemplo de resultado: Pikachu

Imagen frontal devuelta por PokéAPI:

![Pikachu](https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png)

Ejemplo de salida:

```text
POKÉDEX | #25 Pikachu
Peso: 6.0 kg
Tamaño: 0.4 m
Tipos: electric
Habilidades: static, lightning-rod
Imagen frontal: https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png
Información guardada correctamente en: pokedex/pikachu.json
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
pikachu
```

La ejecución genera:

```text
Proyecto_Ucamp/Proyecto_M4_Pokedex/pokedex/pikachu.json
```

## Estructura

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

## ¿Qué aprendí en este módulo?

Con este proyecto practiqué cómo consumir una API web desde Python, interpretar respuestas JSON y manejar diferentes códigos de estado HTTP. También reforcé el uso de listas, diccionarios, funciones y excepciones con `try/except`.

La parte de persistencia me permitió practicar la creación de carpetas y archivos desde Python y comprender cómo guardar información estructurada en JSON. Las pruebas simuladas también me ayudaron a separar la lógica del programa de la disponibilidad de una API externa.

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
- GitHub Actions: aprobada en Python 3.11 y 3.13.

## API utilizada

- PokéAPI: https://pokeapi.co/
- Documentación: https://pokeapi.co/docs/v2
