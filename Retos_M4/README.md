# Retos del Módulo 4

Esta carpeta contiene los retos semanales correspondientes al **Módulo 4: Manejo de Archivos, Excepciones y Consumo de APIs** del bootcamp de Fundamentos de Python de UCAMP.

## Contenido

| Semana | Descripción | Archivo |
|---|---|---|
| **13** | Programa para registrar alumnos y calificaciones, calcular promedios y evitar que entradas incorrectas detengan la ejecución mediante validaciones y manejo de excepciones. | [`Semana13.py`](Semana13.py) |
| **14** | Programa que lee contactos desde un archivo, los muestra numerados, permite modificar nombre, teléfono y correo, y guarda los cambios sin detenerse ante opciones incorrectas. | [`Semana14/`](Semana14/) |
| **15** | Consulta el clima actual mediante OpenWeather Current Weather API usando latitud, longitud y una API key protegida mediante variable de entorno. | [`Semana15/`](Semana15/) |

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

La semana 15 consume **OpenWeather Current Weather API** mediante una petición GET. La consigna original menciona One Call API 3.0, pero ese producto requiere una suscripción de facturación separada; esta variante conserva el objetivo académico usando el endpoint oficial incluido en el acceso gratuito de OpenWeather.

La API key no se guarda en el repositorio; debe configurarse en la variable de entorno `OPENWEATHER_API_KEY`.

### Windows PowerShell

```powershell
$env:OPENWEATHER_API_KEY="TU_API_KEY"
python Retos_M4/Semana15/Semana15.py
```

### Linux / macOS

```bash
export OPENWEATHER_API_KEY="TU_API_KEY"
python3 Retos_M4/Semana15/Semana15.py
```

La documentación completa del reto y sus pruebas está en [`Semana15/README.md`](Semana15/README.md).

Para ejecutar las pruebas sin realizar llamadas reales a OpenWeather:

```bash
python -m unittest discover -s Retos_M4/Semana15/tests -v
```

En algunos sistemas puede ser necesario utilizar `python3`.
