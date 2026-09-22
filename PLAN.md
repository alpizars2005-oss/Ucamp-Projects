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

---

# Módulo 5 — SCRUM — Semana 1 — 2026-09-10

## Objetivo

Resolver el reto **Definición del Caso de Estudio** seleccionando un proyecto real, justificando su abordaje con Scrum y mapeando las responsabilidades de Product Owner, Scrum Master y Development Team.

Se adopta `Retos_M5/` como continuación conservadora de la estructura existente del repositorio. El caso de estudio será **Mochi Monchi - Sistema digital de pedidos e inventario**.

## Commits planeados

15. **Documentar plan del reto Scrum semana 1**
   - Registrar alcance, criterio de organización y verificación antes de integrar la entrega.

16. **Añadir caso de estudio Scrum semana 1**
   - Documentar el producto seleccionado.
   - Incluir una justificación de Scrum de máximo 200 palabras.
   - Crear la matriz inicial de responsabilidades del Scrum Team.
   - Mantener explícita la separación de responsabilidades aun cuando el proyecto sea individual.

17. **Documentar módulo Scrum**
   - Crear el README del Módulo 5 con alcance, entregables y trazabilidad de la rúbrica.

18. **Integrar módulo Scrum al índice principal**
   - Actualizar la estructura y la sección de retos del README raíz.
   - Añadir Scrum, Product Backlog, sprints e iteración incremental a las habilidades en progreso.

## Verificación

- La justificación de Scrum debe tener 200 palabras o menos.
- El proyecto debe describir un producto o servicio concreto.
- La justificación debe mencionar explícitamente incertidumbre/complejidad, retroalimentación e iteración.
- Deben distinguirse correctamente Product Owner, Scrum Master y Development Team.
- No se modifica código ejecutable ni dependencias; las pruebas automatizadas no aplican a esta entrega documental.
- La versión DOCX/PDF se revisa visualmente antes de entrega.

## Riesgo y rollback

Riesgo mínimo: cambios exclusivamente documentales. Cada commit puede revertirse de forma independiente sin afectar los ejercicios de Python ni el CI existente.


---

# Módulo 5 — SCRUM — Semana 3 — 2026-09-22

## Objetivo

Resolver el reto **User Story Mapping y MVP** continuando con el caso de estudio **Mochi Monchi - Sistema digital de pedidos e inventario**.

La entrega debe visualizar el recorrido del usuario, separar claramente el MVP del resto del backlog y dejar explícita la forma en que la primera versión permitirá obtener retroalimentación real.

## Commits planeados

19. **Documentar plan del reto Scrum semana 3**
   - Registrar recorrido de usuario, hipótesis a validar y criterio de separación entre MVP y backlog.

20. **Añadir User Story Mapping y MVP**
   - Mapear el recorrido desde la revisión del turno hasta el cierre.
   - Identificar historias necesarias para registrar pedidos y mantener inventario actualizado.
   - Marcar visualmente las historias incluidas en Release 1.
   - Definir backlog priorizado y funciones posteriores.

21. **Documentar validación y feedback**
   - Explicar el criterio de éxito del MVP.
   - Registrar qué datos y comentarios se usarán para decidir las siguientes prioridades.
   - Actualizar la documentación del Módulo 5 y el índice principal.

## Verificación

- El mapa debe mostrar un recorrido de usuario comprensible de principio a fin.
- El MVP debe estar visualmente diferenciado del resto del backlog.
- El MVP debe incluir una forma concreta de recolectar feedback de uso.
- La solución debe mantener continuidad con el Product Vision Board de Semana 2.
- La entrega DOCX/PDF debe revisarse visualmente antes de subirla.
- No hay código ejecutable ni dependencias nuevas; no aplican pruebas unitarias.

## Riesgo y rollback

Riesgo mínimo. Los cambios son documentales y pueden revertirse de forma independiente sin afectar los ejercicios de programación ni el CI.
