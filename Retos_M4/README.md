# Retos del Módulo 4

Esta carpeta contiene los retos semanales correspondientes al **Módulo 4: Manejo de Archivos, Excepciones y Consumo de APIs** del bootcamp de Fundamentos de Python de UCAMP.

## Contenido

| Semana | Descripción | Archivo |
|---|---|---|
| **13** | Programa para registrar alumnos y calificaciones, calcular promedios y evitar que entradas incorrectas detengan la ejecución mediante validaciones y manejo de excepciones. | [`Semana13.py`](Semana13.py) |
| **14** | Programa que lee contactos desde un archivo, los muestra numerados, permite modificar nombre, teléfono y correo, y guarda los cambios sin detenerse ante opciones incorrectas. | [`Semana14/`](Semana14/) |

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

En algunos sistemas puede ser necesario utilizar `python3`.
