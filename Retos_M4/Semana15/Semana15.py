"""Reto semanal UCAMP: consultor del clima con OpenWeather.

Permite consultar el clima por ciudad o por coordenadas usando Current Weather
API. La API key se solicita al ejecutar el programa y nunca se guarda en disco.
"""

from getpass import getpass

import requests

API_URL = "https://api.openweathermap.org/data/2.5/weather"
TIMEOUT_SEGUNDOS = 10


class ClimaError(Exception):
    """Error controlado relacionado con la consulta del clima."""


def validar_ciudad(valor):
    """Valida CIUDAD,SIGLAS_DEL_PAIS y devuelve ciudad y país."""
    if not isinstance(valor, str):
        raise ValueError("La ciudad debe escribirse como texto.")

    partes = [parte.strip() for parte in valor.split(",")]

    if len(partes) != 2:
        raise ValueError(
            "La ciudad debe tener el formato CIUDAD,SIGLAS_DEL_PAIS, "
            "por ejemplo: Mexico City,MX."
        )

    ciudad, pais = partes

    if not ciudad:
        raise ValueError("El nombre de la ciudad está vacío.")

    if not pais:
        raise ValueError("Las siglas del país están vacías.")

    if len(pais) != 2 or not pais.isalpha():
        raise ValueError(
            "Las siglas del país deben contener exactamente 2 letras, por ejemplo: MX."
        )

    return ciudad, pais.upper()


def validar_latitud(valor):
    """Convierte y valida una latitud entre -90 y 90."""
    try:
        latitud = float(valor)
    except (TypeError, ValueError) as error:
        raise ValueError("La latitud debe ser un número.") from error

    if not -90 <= latitud <= 90:
        raise ValueError("La latitud debe estar entre -90 y 90.")

    return latitud


def validar_longitud(valor):
    """Convierte y valida una longitud entre -180 y 180."""
    try:
        longitud = float(valor)
    except (TypeError, ValueError) as error:
        raise ValueError("La longitud debe ser un número.") from error

    if not -180 <= longitud <= 180:
        raise ValueError("La longitud debe estar entre -180 y 180.")

    return longitud


def validar_api_key(api_key):
    """Comprueba que se haya proporcionado una API key."""
    api_key = api_key.strip()
    if not api_key:
        raise ValueError("La API key de OpenWeather no puede estar vacía.")
    return api_key


def parametros_por_ciudad(ciudad, pais, api_key):
    """Construye los parámetros para buscar por ciudad."""
    return {
        "q": f"{ciudad},{pais}",
        "appid": validar_api_key(api_key),
        "units": "metric",
        "lang": "es",
    }


def parametros_por_coordenadas(latitud, longitud, api_key):
    """Construye los parámetros para buscar por coordenadas."""
    return {
        "lat": validar_latitud(latitud),
        "lon": validar_longitud(longitud),
        "appid": validar_api_key(api_key),
        "units": "metric",
        "lang": "es",
    }


def consultar_clima(parametros, get_func=requests.get):
    """Consulta OpenWeather y devuelve la respuesta JSON validada."""
    try:
        respuesta = get_func(API_URL, params=parametros, timeout=TIMEOUT_SEGUNDOS)
    except requests.exceptions.Timeout as error:
        raise ClimaError("La consulta tardó demasiado tiempo en responder.") from error
    except requests.exceptions.ConnectionError as error:
        raise ClimaError(
            "No fue posible conectarse a OpenWeather. Revisa tu conexión a Internet."
        ) from error
    except requests.exceptions.RequestException as error:
        raise ClimaError(f"Ocurrió un error al consultar OpenWeather: {error}") from error

    if respuesta.status_code == 401:
        raise ClimaError("La API key de OpenWeather es incorrecta o todavía no está activa.")

    if respuesta.status_code == 404:
        raise ClimaError("OpenWeather no encontró la ciudad o ubicación indicada.")

    if respuesta.status_code == 429:
        raise ClimaError(
            "Se alcanzó el límite de consultas de OpenWeather. Intenta de nuevo más tarde."
        )

    if respuesta.status_code != 200:
        try:
            detalle = respuesta.json().get("message", "Error desconocido")
        except (ValueError, AttributeError):
            detalle = "Error desconocido"
        raise ClimaError(
            f"OpenWeather respondió con el código HTTP {respuesta.status_code}: {detalle}."
        )

    try:
        return respuesta.json()
    except ValueError as error:
        raise ClimaError("OpenWeather devolvió una respuesta JSON inválida.") from error


def extraer_clima(datos):
    """Extrae los datos necesarios para mostrarlos al usuario."""
    try:
        return {
            "lugar": datos.get("name") or "la ubicación indicada",
            "descripcion": str(datos["weather"][0]["description"]),
            "temperatura": float(datos["main"]["temp"]),
            "sensacion": float(datos["main"]["feels_like"]),
            "humedad": int(datos["main"]["humidity"]),
        }
    except (KeyError, IndexError, TypeError, ValueError) as error:
        raise ClimaError(
            "La API respondió, pero faltan datos del clima esperados."
        ) from error


def mostrar_clima(clima):
    """Muestra el mensaje solicitado y datos adicionales del clima."""
    print("\n" + "=" * 58)
    print(f"El clima en {clima['lugar']} es {clima['descripcion']}.")
    print(f"Temperatura: {clima['temperatura']:.1f} °C")
    print(f"Sensación térmica: {clima['sensacion']:.1f} °C")
    print(f"Humedad: {clima['humedad']}%")
    print("=" * 58)


def solicitar_api_key():
    """Solicita la API key sin mostrarla en la terminal."""
    return validar_api_key(getpass("Introduce tu API key de OpenWeather: "))


def main():
    """Controla la interacción principal del reto semanal."""
    print("\nCONSULTOR DEL CLIMA — UCAMP")
    print("1. Tengo el nombre de la ciudad")
    print("2. Tengo la latitud y la longitud")

    try:
        opcion = input(
            "\n¿Tienes las coordenadas o el nombre de la ciudad? [1/2]: "
        ).strip()
        api_key = solicitar_api_key()

        if opcion == "1":
            entrada = input(
                "Escribe la ciudad en formato CIUDAD,SIGLAS_DEL_PAIS "
                "(ej. Mexico City,MX): "
            )
            ciudad, pais = validar_ciudad(entrada)
            parametros = parametros_por_ciudad(ciudad, pais, api_key)
        elif opcion == "2":
            latitud = input("Latitud: ").strip()
            longitud = input("Longitud: ").strip()
            parametros = parametros_por_coordenadas(latitud, longitud, api_key)
        else:
            raise ValueError("La opción es incorrecta. Debes escribir 1 o 2.")

        datos = consultar_clima(parametros)
        clima = extraer_clima(datos)
        mostrar_clima(clima)

    except (ValueError, ClimaError) as error:
        print(f"\nError: {error}")
    except KeyboardInterrupt:
        print("\nConsulta cancelada por el usuario.")


if __name__ == "__main__":
    main()
