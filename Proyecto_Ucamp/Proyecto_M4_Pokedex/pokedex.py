"""Proyecto final del Módulo 4 de UCAMP: Pokédex usando PokéAPI."""

import json
import textwrap
import webbrowser
from pathlib import Path

import requests

API_URL = "https://pokeapi.co/api/v2/pokemon/{}"
TIMEOUT_SEGUNDOS = 10
CARPETA_POKEDEX = Path(__file__).resolve().parent / "pokedex"


class PokemonNoEncontradoError(Exception):
    """Se usa cuando PokéAPI devuelve 404 para el Pokémon solicitado."""


def normalizar_nombre(nombre):
    """Limpia y valida el nombre escrito por el usuario."""
    nombre = nombre.strip().lower().replace(" ", "-")

    if not nombre:
        raise ValueError("Debes escribir el nombre de un Pokémon.")

    permitido = nombre.replace("-", "")
    if not permitido.isalnum():
        raise ValueError("El nombre del Pokémon contiene caracteres no válidos.")

    return nombre


def consultar_pokemon(nombre, get_func=requests.get):
    """Consulta un Pokémon y valida los códigos de estado HTTP."""
    url = API_URL.format(nombre)

    try:
        respuesta = get_func(url, timeout=TIMEOUT_SEGUNDOS)
    except requests.exceptions.Timeout as error:
        raise ConnectionError("PokéAPI tardó demasiado tiempo en responder.") from error
    except requests.exceptions.ConnectionError as error:
        raise ConnectionError(
            "No fue posible conectarse a PokéAPI. Revisa tu conexión a Internet."
        ) from error
    except requests.exceptions.RequestException as error:
        raise ConnectionError(f"Ocurrió un error al consultar PokéAPI: {error}") from error

    if respuesta.status_code == 404:
        raise PokemonNoEncontradoError(
            f"No se encontró ningún Pokémon llamado '{nombre}'."
        )

    if respuesta.status_code >= 500:
        raise ConnectionError(
            f"PokéAPI tiene un problema temporal (HTTP {respuesta.status_code})."
        )

    if respuesta.status_code != 200:
        raise ConnectionError(
            f"PokéAPI respondió con un código inesperado: HTTP {respuesta.status_code}."
        )

    try:
        return respuesta.json()
    except ValueError as error:
        raise ConnectionError("PokéAPI devolvió una respuesta JSON inválida.") from error


def extraer_resumen(datos):
    """Obtiene de la respuesta los datos solicitados por la actividad."""
    try:
        return {
            "id": datos["id"],
            "nombre": datos["name"].replace("-", " ").title(),
            "peso_kg": datos["weight"] / 10,
            "altura_m": datos["height"] / 10,
            "tipos": [elemento["type"]["name"] for elemento in datos["types"]],
            "habilidades": [
                elemento["ability"]["name"] for elemento in datos["abilities"]
            ],
            "movimientos": [elemento["move"]["name"] for elemento in datos["moves"]],
            "estadisticas": {
                elemento["stat"]["name"]: elemento["base_stat"]
                for elemento in datos["stats"]
            },
            "imagen": datos["sprites"]["front_default"],
        }
    except (KeyError, TypeError) as error:
        raise ValueError("PokéAPI respondió sin alguno de los datos esperados.") from error


def mostrar_resumen(resumen):
    """Imprime de forma legible los datos principales del Pokémon."""
    print("\n" + "=" * 70)
    print(f"POKÉDEX | #{resumen['id']} {resumen['nombre']}")
    print("=" * 70)
    print(f"Peso: {resumen['peso_kg']:.1f} kg")
    print(f"Tamaño: {resumen['altura_m']:.1f} m")
    print(f"Tipos: {', '.join(resumen['tipos'])}")
    print(f"Habilidades: {', '.join(resumen['habilidades'])}")

    print("\nEstadísticas base:")
    for nombre, valor in resumen["estadisticas"].items():
        print(f"  - {nombre}: {valor}")

    movimientos = ", ".join(resumen["movimientos"])
    print(f"\nMovimientos ({len(resumen['movimientos'])}):")
    print(textwrap.fill(movimientos, width=70, subsequent_indent="  "))

    print(f"\nImagen frontal: {resumen['imagen'] or 'No disponible'}")
    print("=" * 70)


def mostrar_imagen(url):
    """Abre en el navegador la imagen frontal proporcionada por PokéAPI."""
    if not url:
        print("PokéAPI no proporcionó una imagen frontal para este Pokémon.")
        return

    try:
        abierto = webbrowser.open(url)
        if abierto:
            print("Se abrió la imagen frontal en tu navegador.")
        else:
            print(
                "No pude abrir el navegador automáticamente; "
                "usa el enlace mostrado arriba."
            )
    except webbrowser.Error:
        print(
            "No pude abrir el navegador automáticamente; "
            "usa el enlace mostrado arriba."
        )


def guardar_pokemon(datos):
    """Guarda toda la respuesta y el enlace frontal dentro de /pokedex."""
    CARPETA_POKEDEX.mkdir(exist_ok=True)

    nombre = datos.get("name", "pokemon")
    ruta = CARPETA_POKEDEX / f"{nombre}.json"

    contenido = {
        "imagen_frontal": datos.get("sprites", {}).get("front_default"),
        "pokemon": datos,
    }

    try:
        with ruta.open("w", encoding="utf-8") as archivo:
            json.dump(contenido, archivo, indent=4, ensure_ascii=False)
    except OSError as error:
        raise OSError(f"No fue posible guardar el archivo JSON: {error}") from error

    return ruta


def main():
    """Ejecuta la Pokédex interactiva."""
    print("\nPOKÉDEX — UCAMP")
    print("Consulta información usando PokéAPI.\n")

    try:
        nombre = normalizar_nombre(input("Escribe el nombre de un Pokémon: "))
        datos = consultar_pokemon(nombre)
        resumen = extraer_resumen(datos)

        mostrar_resumen(resumen)
        mostrar_imagen(resumen["imagen"])

        ruta = guardar_pokemon(datos)
        print(f"Información guardada correctamente en: {ruta}")

    except PokemonNoEncontradoError as error:
        print(f"\nError: {error}")
    except (ValueError, ConnectionError, OSError) as error:
        print(f"\nError: {error}")
    except KeyboardInterrupt:
        print("\nConsulta cancelada por el usuario.")


if __name__ == "__main__":
    main()
