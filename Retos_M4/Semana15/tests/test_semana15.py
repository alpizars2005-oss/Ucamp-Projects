import os
import pathlib
import sys
import unittest
from unittest.mock import Mock, patch

import requests

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import Semana15 as semana15


DATOS_CLIMA = {
    "name": "Mexico City",
    "weather": [{"description": "muy nuboso"}],
    "main": {"temp": 21.6, "feels_like": 21.2, "humidity": 62},
}


class Semana15ValidacionesTests(unittest.TestCase):
    def test_validar_ciudad_correcta(self):
        self.assertEqual(
            semana15.validar_ciudad("Mexico City,mx"), ("Mexico City", "MX")
        )

    def test_validar_ciudad_indica_pais_incorrecto(self):
        with self.assertRaisesRegex(ValueError, "siglas del país"):
            semana15.validar_ciudad("Mexico City,MEX")

    def test_validar_latitud_fuera_de_rango(self):
        with self.assertRaisesRegex(ValueError, "latitud"):
            semana15.validar_latitud("91")

    def test_validar_longitud_no_numerica(self):
        with self.assertRaisesRegex(ValueError, "longitud"):
            semana15.validar_longitud("oeste")

    def test_parametros_por_ciudad(self):
        parametros = semana15.parametros_por_ciudad("Mexico City", "MX", "demo")
        self.assertEqual(parametros["q"], "Mexico City,MX")
        self.assertEqual(parametros["units"], "metric")
        self.assertEqual(parametros["lang"], "es")

    def test_parametros_por_coordenadas(self):
        parametros = semana15.parametros_por_coordenadas(
            "19.4326", "-99.1332", "demo"
        )
        self.assertEqual(parametros["lat"], 19.4326)
        self.assertEqual(parametros["lon"], -99.1332)

    def test_solicitar_api_key_reutiliza_variable_de_entorno(self):
        with patch.dict(
            os.environ, {semana15.VARIABLE_API_KEY: "clave-entorno"}, clear=False
        ):
            with patch.object(semana15, "getpass") as getpass_falso:
                self.assertEqual(semana15.solicitar_api_key(), "clave-entorno")
                getpass_falso.assert_not_called()


class Semana15ApiTests(unittest.TestCase):
    def test_consulta_exitosa(self):
        respuesta = Mock(status_code=200)
        respuesta.json.return_value = DATOS_CLIMA
        get_falso = Mock(return_value=respuesta)

        datos = semana15.consultar_clima(
            {"q": "Mexico City,MX", "appid": "demo"}, get_func=get_falso
        )

        self.assertEqual(datos["name"], "Mexico City")
        get_falso.assert_called_once_with(
            semana15.API_URL,
            params={"q": "Mexico City,MX", "appid": "demo"},
            timeout=semana15.TIMEOUT_SEGUNDOS,
        )

    def test_api_key_incorrecta(self):
        respuesta = Mock(status_code=401)
        with self.assertRaisesRegex(semana15.ClimaError, "API key"):
            semana15.consultar_clima({}, get_func=Mock(return_value=respuesta))

    def test_ciudad_no_encontrada(self):
        respuesta = Mock(status_code=404)
        with self.assertRaisesRegex(semana15.ClimaError, "no encontró"):
            semana15.consultar_clima({}, get_func=Mock(return_value=respuesta))

    def test_timeout(self):
        get_falso = Mock(side_effect=requests.exceptions.Timeout)
        with self.assertRaisesRegex(semana15.ClimaError, "tardó demasiado"):
            semana15.consultar_clima({}, get_func=get_falso)

    def test_extraer_clima(self):
        clima = semana15.extraer_clima(DATOS_CLIMA)
        self.assertEqual(clima["lugar"], "Mexico City")
        self.assertEqual(clima["descripcion"], "muy nuboso")
        self.assertEqual(clima["humedad"], 62)


if __name__ == "__main__":
    unittest.main()
