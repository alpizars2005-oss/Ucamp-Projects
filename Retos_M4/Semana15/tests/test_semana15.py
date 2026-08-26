import importlib.util
import json
import os
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlparse
import unittest
from unittest.mock import patch

MODULO_PATH = Path(__file__).resolve().parents[1] / "Semana15.py"
SPEC = importlib.util.spec_from_file_location("semana15", MODULO_PATH)
semana15 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(semana15)


class RespuestaFalsa:
    def __init__(self, datos):
        self._contenido = json.dumps(datos).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return self._contenido


class Semana15Tests(unittest.TestCase):
    def setUp(self):
        self.datos_api = {
            "coord": {"lon": -99.1332, "lat": 19.4326},
            "weather": [{"description": "nubes dispersas"}],
            "main": {
                "temp": 22.4,
                "feels_like": 22.1,
                "humidity": 61,
            },
            "wind": {"speed": 3.2},
            "sys": {"country": "MX"},
            "timezone": -21600,
            "name": "Ciudad de México",
        }

    def test_validar_coordenadas_acepta_limites(self):
        semana15.validar_coordenadas(-90, -180)
        semana15.validar_coordenadas(90, 180)

    def test_validar_coordenadas_rechaza_latitud_invalida(self):
        with self.assertRaises(ValueError):
            semana15.validar_coordenadas(90.1, 0)

    def test_validar_coordenadas_rechaza_longitud_invalida(self):
        with self.assertRaises(ValueError):
            semana15.validar_coordenadas(0, -180.1)

    def test_construir_url_incluye_parametros_requeridos(self):
        url = semana15.construir_url(19.4326, -99.1332, "clave-prueba")
        partes = urlparse(url)
        parametros = parse_qs(partes.query)

        self.assertEqual(
            f"{partes.scheme}://{partes.netloc}{partes.path}", semana15.API_URL
        )
        self.assertEqual(parametros["lat"], ["19.4326"])
        self.assertEqual(parametros["lon"], ["-99.1332"])
        self.assertEqual(parametros["appid"], ["clave-prueba"])
        self.assertEqual(parametros["units"], ["metric"])
        self.assertEqual(parametros["lang"], ["es"])
        self.assertNotIn("exclude", parametros)

    def test_interpretar_respuesta_extrae_datos(self):
        clima = semana15.interpretar_respuesta(self.datos_api)

        self.assertEqual(clima["localidad"], "Ciudad de México")
        self.assertEqual(clima["pais"], "MX")
        self.assertEqual(clima["temperatura"], 22.4)
        self.assertEqual(clima["humedad"], 61)
        self.assertEqual(clima["descripcion"], "Nubes dispersas")
        self.assertEqual(clima["zona_horaria"], "UTC-06:00")

    def test_interpretar_respuesta_rechaza_datos_incompletos(self):
        with self.assertRaises(semana15.ClimaError):
            semana15.interpretar_respuesta({"main": {}})

    def test_formatear_desfase_utc(self):
        self.assertEqual(semana15.formatear_desfase_utc(19800), "UTC+05:30")
        self.assertEqual(semana15.formatear_desfase_utc(-21600), "UTC-06:00")

    def test_consultar_clima_usa_respuesta_simulada(self):
        def urlopen_falso(url, timeout):
            self.assertIn("appid=clave-prueba", url)
            self.assertIn("/data/2.5/weather?", url)
            self.assertEqual(timeout, semana15.TIMEOUT_SEGUNDOS)
            return RespuestaFalsa(self.datos_api)

        clima = semana15.consultar_clima(
            19.4326, -99.1332, "clave-prueba", urlopen_func=urlopen_falso
        )

        self.assertEqual(clima["sensacion"], 22.1)
        self.assertEqual(clima["viento"], 3.2)

    def test_consultar_clima_convierte_http_401_en_error_claro(self):
        def urlopen_falso(url, timeout):
            raise HTTPError(url, 401, "Unauthorized", hdrs=None, fp=None)

        with self.assertRaisesRegex(semana15.ClimaError, "API key"):
            semana15.consultar_clima(
                19.4326, -99.1332, "clave-invalida", urlopen_func=urlopen_falso
            )

    def test_obtener_api_key_lee_variable_de_entorno(self):
        with patch.dict(os.environ, {"OPENWEATHER_API_KEY": "abc123"}, clear=False):
            self.assertEqual(semana15.obtener_api_key(), "abc123")

    def test_obtener_api_key_rechaza_variable_ausente(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(semana15.ClimaError, "OPENWEATHER_API_KEY"):
                semana15.obtener_api_key()


if __name__ == "__main__":
    unittest.main()
