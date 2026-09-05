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

---

# Auditoría general del repositorio — 2026-08-26

## Objetivo

Convertir el repositorio de ejercicios en un portafolio académico verificable sin reescribir soluciones históricas ni ocultar la progresión de aprendizaje.

## Hallazgos

- Ya existen pruebas unitarias para Semana 15, pero no hay CI a nivel raíz que las ejecute automáticamente.
- El repositorio contiene ejercicios independientes de varias semanas; una verificación de sintaxis con `compileall` aporta cobertura amplia sin ejecutar código interactivo.
- Faltan convenciones raíz de editor/archivos temporales, aunque algunos subdirectorios ya tienen `.gitignore` propios.

## Commits planeados

6. **Añadir CI académico reproducible**
   - Compilar los ejercicios Python sin ejecutarlos.
   - Ejecutar las pruebas de Semana 15 sin red ni credenciales reales.
   - Fijar las GitHub Actions a SHAs inmutables y usar permisos `contents: read`.

7. **Normalizar higiene del repositorio**
   - Añadir `.editorconfig` y `.gitignore` raíz conservadores.
   - No mover ni renombrar ejercicios entregados.

8. **Documentar verificación**
   - Actualizar README con comandos de comprobación local y estado de CI.

## Riesgo y rollback

Riesgo bajo: no se cambia la lógica de los retos. CI y archivos de higiene pueden revertirse de forma independiente.

---

# Cierre del Módulo 4 — reto OpenWeather y proyecto Pokédex — 2026-09-04

## Objetivo

Alinear el reto semanal de OpenWeather con la consigna final de UCAMP y añadir el proyecto integrador del Módulo 4 (Pokédex) sin perder el enfoque educativo del repositorio.

## Commits planeados

9. **Alinear reto de clima con la consigna final**
   - Permitir consulta por ciudad o por latitud/longitud.
   - Solicitar la API key durante la ejecución sin guardarla en el repositorio.
   - Validar entradas y códigos HTTP con mensajes claros.
   - Mantener pruebas unitarias sin llamadas reales a OpenWeather.

10. **Añadir proyecto Pokédex del Módulo 4**
   - Consumir PokéAPI con `requests`.
   - Mostrar peso, tamaño, movimientos, habilidades, tipos, estadísticas e imagen frontal.
   - Guardar la respuesta completa en JSON dentro de `pokedex/`.
   - Incluir README, ejemplo y pruebas unitarias.

11. **Integrar documentación y CI del Módulo 4**
   - Actualizar README raíz y README del módulo.
   - Declarar `requests` como dependencia.
   - Ejecutar en CI las pruebas del reto de clima y de la Pokédex.

## Verificación

- Ejecutar las pruebas del reto de clima sin conexión ni API key real.
- Ejecutar las pruebas de la Pokédex sin conexión.
- Compilar los archivos Python modificados.
- Confirmar que no se almacena ninguna API key.
- Verificar que los README permiten explicar y ejecutar cada entrega.

## Riesgo y rollback

Riesgo bajo. Los cambios están limitados al cierre del Módulo 4, documentación y CI. El rollback consiste en revertir los commits 9–11 de forma independiente.


---

# Blindaje final de rúbrica — Pokédex Módulo 4 — 2026-09-04

## Objetivo

Cerrar los puntos interpretables de la rúbrica de entrega sin cambiar el comportamiento funcional ya verificado.

## Commits planeados

12. **Añadir índice y trazabilidad de la rúbrica**
   - Incorporar un índice navegable al README del proyecto.
   - Hacer explícita la relación entre cada criterio y la evidencia del repositorio.
   - Conservar instrucciones de instalación, ejecución, pruebas y reflexión.

13. **Reforzar comentarios educativos del código**
   - Añadir comentarios útiles en las partes clave del flujo HTTP, conversiones de unidades, despliegue de imagen y persistencia JSON.
   - Evitar comentarios redundantes o que dificulten explicar el código línea por línea.
   - Mantener intacto el comportamiento funcional.

14. **Verificar CI y evidencia de ejecución**
   - Ejecutar nuevamente las pruebas y compilación mediante GitHub Actions.
   - Mantener el JSON de ejemplo versionado.
   - No inventar ni reconstruir el archivo `squirtle.json` generado localmente; se añadirá sólo si se dispone del archivo real producido por la ejecución manual.

## Riesgo y rollback

Riesgo mínimo: documentación y comentarios, sin cambios esperados de lógica. Cada commit puede revertirse de forma independiente.
