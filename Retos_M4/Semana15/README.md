# Semana 15 — Consultor del clima con OpenWeather

Reto semanal del **Módulo 4 de Fundamentos de Python (UCAMP)**. El programa consulta el clima actual con OpenWeather y permite que el usuario elija entre buscar por **ciudad** o por **latitud y longitud**.

## Requisitos de la actividad cubiertos

- Pregunta primero si el usuario tiene el nombre de la ciudad o las coordenadas.
- Acepta ciudades con el formato `CIUDAD,SIGLAS_DEL_PAIS`, por ejemplo `Mexico City,MX`.
- Solicita la API key de OpenWeather al ejecutar el programa.
- Valida ciudad, país, latitud, longitud y API key con mensajes que indican el dato incorrecto.
- Usa `try/except` para manejar errores de entrada, red y respuesta de la API.
- Informa cuando OpenWeather no encuentra la ciudad o ubicación.
- Muestra un resultado del tipo: `El clima en Mexico City es muy nuboso.`
- Añade temperatura, sensación térmica y humedad como información complementaria.

## Requisitos para ejecutar

- Python **3.9 o superior**.
- `pip` para instalar dependencias.
- Biblioteca `requests` instalada mediante el `requirements.txt` del repositorio.
- Conexión a Internet para realizar consultas reales.
- Una cuenta gratuita de **OpenWeather**.
- Una **API key de OpenWeather** válida y activa.

La API key se solicita durante la ejecución con `getpass`; **no debe escribirse dentro del código ni guardarse en GitHub**.

## API utilizada

Se utiliza **OpenWeather Current Weather API**:

```text
https://api.openweathermap.org/data/2.5/weather
```

Esta API admite consultas por nombre de ciudad o por coordenadas y devuelve JSON.

## Instalación

Desde la raíz del repositorio:

```bash
python -m pip install -r requirements.txt
```

## Ejecución

Desde la raíz del repositorio:

```bash
python Retos_M4/Semana15/Semana15.py
```

El programa pide la API key en la terminal usando `getpass`, por lo que la clave **no se muestra mientras se escribe y no se guarda en el repositorio**.

Ejemplo de ciudad:

```text
Mexico City,MX
```

Ejemplo de coordenadas de Ciudad de México:

```text
Latitud: 19.4326
Longitud: -99.1332
```

## Pruebas

Las pruebas usan respuestas simuladas; no necesitan Internet ni una API key real.

```bash
python -m unittest discover -s Retos_M4/Semana15/tests -v
```

### Estado de verificación

- **11/11 pruebas unitarias aprobadas**.
- Validación de ciudad y siglas del país: aprobada.
- Validación de latitud y longitud: aprobada.
- Consulta HTTP simulada: aprobada.
- Error `401` por API key inválida: aprobado.
- Error `404` por ubicación inexistente: aprobado.
- Timeout de red: aprobado.
- Extracción y presentación de datos del clima: aprobada.
- Compilación de Python: aprobada.
- GitHub Actions: aprobada en Python 3.11 y 3.13.

## Seguridad

Nunca escribas una API key real dentro del código ni la publiques en GitHub. El programa solo la mantiene en memoria durante la ejecución.
