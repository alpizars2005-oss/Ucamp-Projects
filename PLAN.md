# PLAN

Plan de trabajo para el reto semanal de consumo de la API de OpenWeather.

## Commits planeados

1. **Documentar plan de implementación**
   - Registrar alcance, seguridad y estrategia de pruebas antes de modificar el reto.

2. **Implementar consulta segura de clima**
   - Agregar el reto de la semana 15 usando OpenWeather One Call API 3.0.
   - Leer la API key desde `OPENWEATHER_API_KEY` sin incluir secretos en el repositorio.
   - Validar latitud y longitud.
   - Manejar errores HTTP, red y respuestas inválidas.
   - Añadir pruebas unitarias con datos simulados para evitar depender de la API real.

3. **Documentar semana 15 y verificación**
   - Actualizar `Retos_M4/README.md` y el `README.md` principal.
   - Documentar configuración de la API key, ejecución y pruebas.

## Ajuste posterior: API sin datos de pago

OpenWeather One Call API 3.0 requiere una suscripción de facturación separada. Para mantener el ejercicio académico sin solicitar una tarjeta ni asumir riesgo de cargos, se migra la semana 15 a la **Current Weather API** oficial de OpenWeather, que está incluida en el plan gratuito.

### Commits del ajuste

4. **Migrar semana 15 a Current Weather API**
   - Cambiar el endpoint a `https://api.openweathermap.org/data/2.5/weather`.
   - Conservar latitud, longitud, `appid`, unidades métricas e idioma español.
   - Adaptar el procesamiento al formato JSON de Current Weather.
   - Mantener la API key únicamente en `OPENWEATHER_API_KEY`.
   - Actualizar y ampliar las pruebas unitarias sin realizar llamadas reales.

5. **Documentar alternativa gratuita de OpenWeather**
   - Explicar por qué se usa Current Weather en lugar de One Call 3.0.
   - Actualizar los README con el endpoint, ejecución y alcance del plan gratuito.

## Criterios de verificación

- Las pruebas unitarias deben ejecutarse sin conexión y sin API key real.
- El código no debe exponer credenciales ni imprimir la API key.
- El reto debe poder ejecutarse en Windows y Linux con Python 3.
- No se agregarán dependencias externas innecesarias; se utilizará la biblioteca estándar de Python.
- La solución final no debe requerir registrar datos de pago para completar el reto.

## Riesgo y rollback

Riesgo bajo. Los cambios se limitan a la semana 15 y su documentación. La migración conserva el objetivo pedagógico del ejercicio: consumir OpenWeather mediante HTTP GET, coordenadas, API key y JSON. Para revertir, se puede regresar al commit anterior de la semana 15.
