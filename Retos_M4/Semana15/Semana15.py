"""Reto semanal: consultar el clima con OpenWeather Current Weather API.

La API key se obtiene de la variable de entorno ``OPENWEATHER_API_KEY`` para
no guardar credenciales dentro del código ni del repositorio.
"""

import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

API_URL = "https://api.openweathermap.org/data/2.5/weather"
TIMEOUT_SEGUNDOS = 10


class ClimaError(Exception):
    """Error controlado al consultar o interpretar datos del clima."""


def obtener_api_key():
    """Obtiene la API key desde una variable de entorno."""
    api_key = os.getenv("OPENWEATHER_API_KEY", "").strip()

    if not api_key:
        raise ClimaError(
            "No se encontró la variable OPENWEATHER_API_KEY. "
            "Configúrala antes de ejecutar el programa."
        )

    return api_key


def validar_coordenadas(latitud, longitud):
    """Valida que las coordenadas estén dentro de los rangos permitidos."""
    if not -90 <= latitud <= 90:
        raise ValueError("La latitud debe estar entre -90 y 90.")

    if not -180 <= longitud <= 180:
        raise ValueError("La longitud debe estar entre -180 y 180.")


def construir_url(latitud, longitud, api_key):
    """Construye la URL GET para OpenWeather Current Weather API."""
    validar_coordenadas(latitud, longitud)

    if not api_key or not api_key.strip():
        raise ValueError("La API key no puede estar vacía.")

    parametros = {
        "lat": latitud,
        "lon": longitud,
        "appid": api_key.strip(),
        "units": "metric",
        "lang": "es",
    }

    return f"{API_URL}?{urlencode(parametros)}"


def formatear_desfase_utc(segundos):
    """Convierte un desfase horario en segundos a un texto UTC±HH:MM."""
    try:
        segundos = int(segundos)
    except (TypeError, ValueError) as error:
        raise ClimaError("OpenWeather devolvió un desfase horario inválido.") from error

    signo = "+" if segundos >= 0 else "-"
    segundos = abs(segundos)
    horas, resto = divmod(segundos, 3600)
    minutos = resto // 60
    return f"UTC{signo}{horas:02d}:{minutos:02d}"


def interpretar_respuesta(datos):
    """Extrae los datos principales del clima desde la respuesta JSON."""
    try:
        principal = datos["main"]
        viento = datos["wind"]
        descripcion = datos["weather"][0]["description"]
        sistema = datos.get("sys") or {}

        return {
            "localidad": str(datos.get("name") or "No disponible"),
            "pais": str(sistema.get("country") or "No disponible"),
            "temperatura": float(principal["temp"]),
            "sensacion": float(principal["feels_like"]),
            "humedad": int(principal["humidity"]),
            "viento": float(viento["speed"]),
            "descripcion": str(descripcion).capitalize(),
            "zona_horaria": formatear_desfase_utc(datos.get("timezone", 0)),
        }
    except (KeyError, IndexError, TypeError, ValueError) as error:
        raise ClimaError(
            "La respuesta de OpenWeather no contiene los datos esperados."
        ) from error


def consultar_clima(latitud, longitud, api_key, urlopen_func=urlopen):
    """Consulta OpenWeather y devuelve los datos principales del clima."""
    url = construir_url(latitud, longitud, api_key)

    try:
        with urlopen_func(url, timeout=TIMEOUT_SEGUNDOS) as respuesta:
            contenido = respuesta.read().decode("utf-8")
            datos = json.loads(contenido)

    except HTTPError as error:
        if error.code == 401:
            mensaje = "OpenWeather rechazó la API key. Verifica que sea válida."
        elif error.code == 429:
            mensaje = "Se alcanzó el límite de solicitudes de OpenWeather."
        else:
            mensaje = f"OpenWeather respondió con el error HTTP {error.code}."
        raise ClimaError(mensaje) from error

    except URLError as error:
        raise ClimaError(
            "No fue posible conectarse con OpenWeather. Revisa tu conexión."
        ) from error

    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ClimaError("OpenWeather devolvió una respuesta inválida.") from error

    return interpretar_respuesta(datos)


def solicitar_coordenada(nombre, minimo, maximo):
    """Solicita una coordenada numérica hasta recibir un valor válido."""
    while True:
        try:
            valor = float(input(f"Escribe la {nombre} ({minimo} a {maximo}): "))

            if minimo <= valor <= maximo:
                return valor

            print(f"La {nombre} debe estar entre {minimo} y {maximo}.")

        except ValueError:
            print("Entrada inválida. Escribe un número, por ejemplo: 19.4326")


def mostrar_clima(clima, latitud, longitud):
    """Muestra en consola los datos obtenidos de OpenWeather."""
    print("\n" + "=" * 52)
    print("CLIMA ACTUAL")
    print("=" * 52)
    print(f"Localidad: {clima['localidad']} ({clima['pais']})")
    print(f"Coordenadas: {latitud:.4f}, {longitud:.4f}")
    print(f"Condición: {clima['descripcion']}")
    print(f"Temperatura: {clima['temperatura']:.1f} °C")
    print(f"Sensación térmica: {clima['sensacion']:.1f} °C")
    print(f"Humedad: {clima['humedad']} %")
    print(f"Velocidad del viento: {clima['viento']:.1f} m/s")
    print(f"Zona horaria: {clima['zona_horaria']}")


def ejecutar_programa():
    """Controla la ejecución interactiva del reto de la semana 15."""
    print("Consulta del clima con OpenWeather Current Weather API")
    print("Ingresa las coordenadas de la localidad que deseas consultar.\n")

    latitud = solicitar_coordenada("latitud", -90, 90)
    longitud = solicitar_coordenada("longitud", -180, 180)

    try:
        api_key = obtener_api_key()
        clima = consultar_clima(latitud, longitud, api_key)
        mostrar_clima(clima, latitud, longitud)
    except ClimaError as error:
        print(f"\nNo se pudo obtener el clima: {error}")


if __name__ == "__main__":
    ejecutar_programa()
