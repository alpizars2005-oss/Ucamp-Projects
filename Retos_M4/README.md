# Retos del Módulo 4

Esta carpeta contiene los retos semanales correspondientes al **Módulo 4: Manejo de Archivos, Excepciones y Consumo de APIs** del bootcamp de Fundamentos de Python de UCAMP.

## Contenido

| Semana | Descripción | Archivo |
|---|---|---|
| **13** | Programa para registrar alumnos y calificaciones, calcular promedios y evitar que entradas incorrectas detengan la ejecución mediante validaciones y manejo de excepciones. | [`Semana13.py`](Semana13.py) |
| **14** | Programa que lee contactos desde un archivo, los muestra numerados, permite modificar nombre, teléfono y correo, y guarda los cambios sin detenerse ante opciones incorrectas. | [`Semana14/`](Semana14/) |
| **15** | Consultor del clima con OpenWeather Current Weather API. Permite buscar por ciudad en formato `CIUDAD,SIGLAS_DEL_PAIS` o por latitud/longitud y solicita la API key durante la ejecución. | [`Semana15/`](Semana15/) |

## Ejecutar la semana 13

Desde la raíz del repositorio:

```bash
python Retos_M4/Semana13.py
```

## Ejecutar la semana 14

La carpeta incluye tanto el programa como el archivo de contactos utilizado por el ejercicio:

```text
Semana14/
├── Semana14.py
└── contactos.txt
```

Desde la raíz del repositorio:

```bash
python Retos_M4/Semana14/Semana14.py
```

El archivo `contactos.txt` utiliza el formato `nombre|telefono|correo`. Al modificar un contacto desde el programa, los cambios se guardan directamente en ese archivo.

## Ejecutar la semana 15

La semana 15 consume **OpenWeather Current Weather API** mediante una petición GET.

Primero instala las dependencias declaradas en la raíz del repositorio:

```bash
python -m pip install -r requirements.txt
```

Después ejecuta:

```bash
python Retos_M4/Semana15/Semana15.py
```

El programa pregunta si deseas consultar por:

1. ciudad, usando el formato `CIUDAD,SIGLAS_DEL_PAIS`, por ejemplo `Mexico City,MX`; o
2. latitud y longitud.

También solicita la API key de OpenWeather mediante `getpass`. La clave no se muestra mientras se escribe y no se guarda en archivos ni en el repositorio.

La documentación completa del reto está en [`Semana15/README.md`](Semana15/README.md).

Para ejecutar sus pruebas sin realizar llamadas reales a OpenWeather:

```bash
python -m unittest discover -s Retos_M4/Semana15/tests -v
```

En algunos sistemas puede ser necesario utilizar `python3`.
