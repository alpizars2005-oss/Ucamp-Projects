# Semana 15 — Consultor del clima con OpenWeather

Reto semanal del **Módulo 4 de Fundamentos de Python (UCAMP)**. El programa consulta el clima actual con OpenWeather y permite que el usuario elija entre buscar por **ciudad** o por **latitud y longitud**.

## Requisitos de la actividad cubiertos

- Pregunta primero si el usuario tiene el nombre de la ciudad o las coordenadas.
- Acepta ciudades con el formato `CIUDAD,SIGLAS_DEL_PAIS`, por ejemplo `Mexico City,MX`.
- Solicita la API key de OpenWeather al ejecutar el programa cuando no existe una variable de entorno configurada.
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

## API key: dos formas de usarla

### Opción 1 — escribirla al ejecutar

Si `OPENWEATHER_API_KEY` no está configurada, el programa la solicita con `getpass`. La clave no se muestra mientras se escribe y solo vive durante esa ejecución.

### Opción 2 — variable de entorno

Para no escribir la API key en cada ejecución, puedes guardarla como variable de entorno llamada:

```text
OPENWEATHER_API_KEY
```

El programa primero intenta leer esta variable con `os.getenv()`; si existe, la utiliza automáticamente. Python soporta variables de entorno en Windows, Linux y macOS.

En Windows puedes crearla desde:

```text
Configuración avanzada del sistema
→ Variables de entorno
→ Variables de usuario
→ Nueva
```

Nombre:

```text
OPENWEATHER_API_KEY
```

Valor:

```text
TU_API_KEY_REAL
```

Después cierra y vuelve a abrir PowerShell para que la nueva terminal herede la variable.

Para comprobar que existe sin mostrar su valor completo:

```powershell
if ($env:OPENWEATHER_API_KEY) { "API key configurada" } else { "API key no configurada" }
```

Nunca escribas la API key directamente dentro de `Semana15.py` ni la subas a GitHub.

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

- **12/12 pruebas unitarias aprobadas**.
- Validación de ciudad y siglas del país: aprobada.
- Validación de latitud y longitud: aprobada.
- Reutilización de `OPENWEATHER_API_KEY`: aprobada.
- Consulta HTTP simulada: aprobada.
- Error `401` por API key inválida: aprobado.
- Error `404` por ubicación inexistente: aprobado.
- Timeout de red: aprobado.
- Extracción y presentación de datos del clima: aprobada.
- Compilación de Python: aprobada.
- GitHub Actions: aprobada en Python 3.11 y 3.13.

## Seguridad

Nunca escribas una API key real dentro del código ni la publiques en GitHub. El programa puede leerla desde una variable de entorno o mantenerla únicamente en memoria durante la ejecución.
