"""La respuesta de una API no debe elegir una ruta fuera de la Pokédex."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pokedex


class TestGuardadoSeguro(unittest.TestCase):
    def setUp(self):
        temporal = tempfile.TemporaryDirectory()
        self.addCleanup(temporal.cleanup)
        self.base = Path(temporal.name)
        self.carpeta = self.base / "pokedex"
        cambio = patch.object(pokedex, "CARPETA_POKEDEX", self.carpeta)
        cambio.start()
        self.addCleanup(cambio.stop)

    def test_rechaza_ruta_relativa_sin_sobrescribir_archivo_externo(self):
        externo = self.base / "fuera.json"
        externo.write_text("conservar", encoding="utf-8")
        with self.assertRaises(ValueError):
            pokedex.guardar_pokemon({"name": "../fuera", "sprites": {}})
        self.assertEqual(externo.read_text(encoding="utf-8"), "conservar")

    def test_rechaza_ruta_absoluta_dentro_del_directorio_temporal(self):
        externo = self.base / "absoluto.json"
        with self.assertRaises(ValueError):
            pokedex.guardar_pokemon({"name": str(externo.with_suffix("")), "sprites": {}})
        self.assertFalse(externo.exists())

    def test_rechaza_nombres_no_validos_antes_de_crear_archivos(self):
        for nombre in (None, 1, [], {}, "", "..\\fuera", "sub/pikachu", "pikachu:extra"):
            with self.subTest(nombre=nombre), self.assertRaises(ValueError):
                pokedex.guardar_pokemon({"name": nombre, "sprites": {}})
        self.assertFalse(self.carpeta.exists())

    def test_conserva_nombre_datos_y_formato_de_respuestas_validas(self):
        for nombre in ("pikachu", "mr-mime", "deoxys-normal", "porygon2"):
            with self.subTest(nombre=nombre):
                datos = {"name": nombre, "sprites": {"front_default": None}, "extra": [1, "á"]}
                original = copy.deepcopy(datos)
                ruta = pokedex.guardar_pokemon(datos)
                self.assertEqual(ruta, self.carpeta / (nombre + ".json"))
                self.assertEqual(datos, original)
                self.assertEqual(json.loads(ruta.read_text(encoding="utf-8")), {
                    "imagen_frontal": None, "pokemon": original,
                })

    def test_rechaza_enlace_simbolico_que_sale_de_la_carpeta(self):
        self.carpeta.mkdir()
        externo = self.base / "externo.json"
        externo.write_text("conservar", encoding="utf-8")
        try:
            (self.carpeta / "pikachu.json").symlink_to(externo)
        except (OSError, NotImplementedError):
            self.skipTest("El entorno no permite crear enlaces simbólicos")
        with self.assertRaises(ValueError):
            pokedex.guardar_pokemon({"name": "pikachu", "sprites": {}})
        self.assertEqual(externo.read_text(encoding="utf-8"), "conservar")

    def test_conserva_nombre_predeterminado_si_falta_name(self):
        ruta = pokedex.guardar_pokemon({"sprites": {}})
        self.assertEqual(ruta.name, "pokemon.json")

    def test_rechaza_respuesta_que_no_es_objeto(self):
        for datos in (None, [], 1, "pikachu"):
            with self.subTest(datos=datos), self.assertRaises(ValueError):
                pokedex.guardar_pokemon(datos)
        self.assertFalse(self.carpeta.exists())


if __name__ == "__main__":
    unittest.main()
