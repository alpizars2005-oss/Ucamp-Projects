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

## Criterios de verificación

- Las pruebas unitarias deben ejecutarse sin conexión y sin API key real.
- El código no debe exponer credenciales ni imprimir la API key.
- El reto debe poder ejecutarse en Windows y Linux con Python 3.
- No se agregarán dependencias externas innecesarias; se utilizará la biblioteca estándar de Python.

## Riesgo y rollback

Riesgo bajo. Los cambios se limitan a una nueva semana del Módulo 4 y documentación. Para revertir, se puede revertir cada commit de forma independiente.
