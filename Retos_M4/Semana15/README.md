# Semana 15 — Consulta del clima con OpenWeather

Este reto consume **OpenWeather One Call API 3.0** mediante una petición HTTP GET para consultar el clima actual de una localidad a partir de su latitud y longitud.

## Qué practica este reto

- Consumo de una API REST mediante HTTP GET.
- Construcción de una URL con parámetros de consulta.
- Lectura e interpretación de respuestas JSON.
- Validación de latitud y longitud.
- Manejo de errores HTTP, de red y de datos inesperados.
- Protección de credenciales mediante variables de entorno.
- Pruebas unitarias con respuestas simuladas, sin consumir la API real.

## Configurar la API key

Primero crea una cuenta en OpenWeather y obtén una API key. OpenWeather puede requerir activar el producto correspondiente a **One Call API 3.0**, así que conviene revisar la documentación oficial antes de ejecutar el reto.

La clave **no debe escribirse dentro de `Semana15.py` ni subirse a GitHub**. El programa la lee desde la variable de entorno `OPENWEATHER_API_KEY`.

### Windows PowerShell

```powershell
$env:OPENWEATHER_API_KEY="TU_API_KEY"
python Retos_M4/Semana15/Semana15.py
```

### Windows CMD

```cmd
set OPENWEATHER_API_KEY=TU_API_KEY
python Retos_M4\Semana15\Semana15.py
```

### Linux / macOS

```bash
export OPENWEATHER_API_KEY="TU_API_KEY"
python3 Retos_M4/Semana15/Semana15.py
```

## Coordenadas

El programa solicita:

- **Latitud:** valor entre `-90` y `90`.
- **Longitud:** valor entre `-180` y `180`.

Puedes obtener coordenadas con el sitio sugerido por UCAMP o con cualquier servicio de mapas confiable.

## Datos mostrados

El programa imprime:

- Condición del clima.
- Temperatura en °C.
- Sensación térmica en °C.
- Humedad.
- Velocidad del viento.
- Zona horaria devuelta por OpenWeather.

## Ejecutar las pruebas

Las pruebas usan datos simulados y no necesitan conexión a Internet ni una API key real.

Desde la raíz del repositorio:

```bash
python -m unittest discover -s Retos_M4/Semana15/tests -v
```

## Seguridad

Nunca publiques una API key real en un commit, captura de pantalla o archivo compartido. Si una clave se expone accidentalmente, revócala desde tu cuenta de OpenWeather y genera una nueva.
