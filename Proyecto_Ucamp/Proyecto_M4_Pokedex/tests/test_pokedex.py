import json
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import Mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import pokedex


POKEMON_EJEMPLO = {
    "id": 25,
    "name": "pikachu",
    "height": 4,
    "weight": 60,
    "types": [{"type": {"name": "electric"}}],
    "abilities": [
        {"ability": {"name": "static"}},
        {"ability": {"name": "lightning-rod"}},
    ],
    "moves": [
        {"move": {"name": "thunder-shock"}},
        {"move": {"name": "quick-attack"}},
    ],
    "stats": [
        {"base_stat": 35, "stat": {"name": "hp"}},
        {"base_stat": 55, "stat": {"name": "attack"}},
    ],
    "sprites": {
        "front_default": (
            "https://raw.githubusercontent.com/PokeAPI/sprites/"
            "master/sprites/pokemon/25.png"
        )
    },
}


class TestPokedex(unittest.TestCase):
    def test_normalizar_nombre(self):
        self.assertEqual(pokedex.normalizar_nombre("  Mr Mime  "), "mr-mime")

    def test_nombre_vacio(self):
        with self.assertRaises(ValueError):
            pokedex.normalizar_nombre("   ")

    def test_consulta_exitosa(self):
        respuesta = Mock(status_code=200)
        respuesta.json.return_value = POKEMON_EJEMPLO
        get_falso = Mock(return_value=respuesta)

        datos = pokedex.consultar_pokemon("pikachu", get_func=get_falso)

        self.assertEqual(datos["id"], 25)
        get_falso.assert_called_once_with(
            pokedex.API_URL.format("pikachu"), timeout=pokedex.TIMEOUT_SEGUNDOS
        )

    def test_pokemon_no_encontrado(self):
        respuesta = Mock(status_code=404)

        with self.assertRaises(pokedex.PokemonNoEncontradoError):
            pokedex.consultar_pokemon(
                "no-existe", get_func=Mock(return_value=respuesta)
            )

    def test_extraer_resumen(self):
        resumen = pokedex.extraer_resumen(POKEMON_EJEMPLO)
        self.assertEqual(resumen["peso_kg"], 6.0)
        self.assertEqual(resumen["altura_m"], 0.4)
        self.assertEqual(resumen["tipos"], ["electric"])
        self.assertEqual(resumen["habilidades"][0], "static")

    def test_guardar_json(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta_original = pokedex.CARPETA_POKEDEX
            try:
                pokedex.CARPETA_POKEDEX = pathlib.Path(carpeta)
                ruta = pokedex.guardar_pokemon(POKEMON_EJEMPLO)
                self.assertTrue(ruta.exists())

                contenido = json.loads(ruta.read_text(encoding="utf-8"))
                self.assertEqual(contenido["pokemon"]["name"], "pikachu")
                self.assertIn("imagen_frontal", contenido)
            finally:
                pokedex.CARPETA_POKEDEX = ruta_original


if __name__ == "__main__":
    unittest.main()
