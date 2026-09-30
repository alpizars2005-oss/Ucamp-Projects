# Simulación de Sprint e Incremento — Semana 4

**Proyecto:** Mochi Monchi — sistema digital de pedidos e inventario.  
**Autor:** Angel Alfredo. **Preparación:** 30 de septiembre de 2026.

## Naturaleza del ejercicio

Simulación académica individual de un Sprint de una semana, representado en cinco jornadas virtuales (J1–J5). Las jornadas son un guion de inspección y adaptación construido para el ejercicio: no son cinco días transcurridos ni actas de reuniones con personas que no participaron. Las responsabilidades de Product Owner, Scrum Master y Developer se representan por separado. Los resultados técnicos sí proceden de ejecuciones de la aplicación y de sus pruebas. La redacción reflexiva se propone para revisión del estudiante.

El punto de partida es el Product Vision Board de Semana 2 y las historias US-01 a US-10 de Semana 3. En esta carpeta no había un incremento ejecutable. No se reemplaza la visión original: se entrega una aplicación local accesible desde navegador como implementación inicial, no una versión de producción ni un ejecutable autónomo.

## Objetivo del Sprint

Permitir que un operador registre un pedido una sola vez, revise su total, lo confirme y vea el descuento correcto de ingredientes y empaques; al cierre podrá consultar pedidos del día y registrar feedback. Si falta un insumo, la operación debe rechazarse sin alterar pedidos ni existencias.

## Equipo y responsabilidades simuladas

| Responsabilidad | Representación | Decisión que le corresponde |
|---|---|---|
| Product Owner | Angel Alfredo | Ordenar el valor del MVP y decidir qué queda fuera. |
| Scrum Master | Angel Alfredo | Facilitar la inspección, hacer visibles impedimentos y cuidar los acuerdos. |
| Developer | Angel Alfredo | Planear e implementar la solución y comprobar su calidad. |

No se presentan estas responsabilidades como un equipo real de tres integrantes. La simulación individual no reproduce la colaboración de un Scrum Team completo.

## Product Backlog y Sprint Backlog

Las diez historias del MVP se seleccionan para un recorrido completo con datos mínimos. No se usa una velocidad histórica inventada ni se estiman puntos como si existiera un equipo observado.

| ID | Historia / resultado | Criterio de aceptación | Evidencia |
|---|---|---|---|
| US-01 | Abrir catálogo y precios | Se muestran fresa y mango a $35.00 y matcha a $40.00; importes sintéticos en MXN. | Catálogo; 01_pedido_revision.png |
| US-02 | Consultar stock inicial | Cada ingrediente muestra cantidad, unidad y umbral; la disponibilidad usa la receta completa. | Inventario; tests de disponibilidad |
| US-03 | Crear un pedido | Admite varios productos y cantidades enteras de 1 a 99; rechaza entradas inválidas. | Carrito; validación de líneas |
| US-04 | Añadir una nota breve | Guarda hasta 240 caracteres como texto; no modifica la receta ni admite sustituciones automáticas. | Pedido confirmado; prueba de HTML |
| US-05 | Revisar el total | El carrito muestra $110.00 para 2 fresa y 1 matcha; el servidor recalcula antes de guardar. | 01_pedido_revision.png |
| US-06 | Confirmar y guardar | La venta permanece tras reabrir la base; repetir el mismo envío no duplica pedidos. | Persistencia e idempotencia |
| US-07 | Descontar la receta | Una transacción descuenta ingredientes y empaques; si falta un insumo no guarda ni descuenta nada. | Atomicidad y concurrencia |
| US-08 | Actualizar existencias y alertas | Tras la segunda venta quedan 80 g de masa, 40 g de crema y 20 g de fresa; aparecen tres alertas. | 03_inventario_alertas.png |
| US-09 | Consultar el resumen diario | El cierre muestra 2 pedidos y $460.00 de ventas de prueba, filtrados por fecha local del servidor. | 04_cierre_y_feedback.png |
| US-10 | Registrar feedback del turno | Persiste una valoración entera de 1 a 5 y comentario opcional; el dato 4/5 de la demo no es opinión de un cliente. | 04_cierre_y_feedback.png |

**Estado al cierre del ejercicio:** US-01 a US-10 terminadas dentro del alcance académico local comprobado. “Terminada” no significa lista para operar públicamente ni validada en el mercado.

**Fuera del Sprint:** edición/cancelación, pagos y tickets, configuración de umbrales, ajustes de inventario con historial, usuarios/permisos y exportaciones (Release 2); nube, multi-sucursal e integraciones (futuro). Estas funciones siguen en el backlog de Semana 3.

**Tablero de la simulación:**

| Momento | Por hacer | En curso | En revisión | Terminado |
|---|---|---|---|---|
| Planning | US-01–US-10 | — | — | — |
| Jornada intermedia, estado didáctico | US-09–US-10 | US-06–US-08 | US-03–US-05 | US-01–US-02 |
| Cierre verificado | — | — | — | US-01–US-10 |

La fila intermedia representa la progresión del ejercicio; no procede de un historial externo de Jira o Miro.

## Definition of Ready (DoR)

Acuerdo de preparación del ejercicio, no un elemento obligatorio añadido al marco Scrum.

1. La historia conserva su identificador del MVP y explica usuario, necesidad y valor esperado.
2. Existe un criterio observable de aceptación y al menos un caso de error relevante.
3. Los productos, precios, unidades, recetas y umbrales necesarios están definidos como datos de prueba.
4. Las dependencias entre pedido, receta e inventario son conocidas; las líneas compartidas se acumulan antes de descontar.
5. El alcance está acotado: aplicación local; sin cobros reales, nube, usuarios avanzados ni cambio de receta por una nota.
6. La historia cabe en la capacidad de la simulación y tiene una forma concreta de comprobar su resultado.

## Definition of Done (DoD)

1. El flujo de la historia funciona en el incremento local y cumple el criterio de aceptación acordado.
2. Pedido e inventario se actualizan juntos; los errores no dejan ventas parciales ni cantidades negativas.
3. Los datos persisten y los reintentos de un mismo envío no duplican la operación.
4. Pasan las 44 pruebas de lógica/API y las nueve comprobaciones de interfaz documentadas, con sus límites de entorno visibles.
5. El código, comandos de ejecución, limitaciones, capturas y resultados se entregan de forma reproducible; no contiene credenciales reales.
6. La historia se revisa contra el objetivo del Sprint y se incorpora a la documentación; la Review no sustituye estas verificaciones.

## Sprint Planning

**Momento del guion:** inicio de J1. **Timebox propuesto:** 45 minutos; no se afirma que ese tiempo haya sido medido.

**Por qué:** comprobar la hipótesis de conectar pedido, receta e inventario sin doble captura. El resultado comercial esperado sigue siendo una hipótesis hasta trabajar con un operador real.

**Qué:** US-01 a US-10 con tres productos de prueba, recetas fijas y una sola base local. Quedan fuera cobros, cambios de receta por nota y funciones de Release 2.

**Cómo:** separar interfaz de navegador, API Python y persistencia SQLite; definir precios en centavos y cantidades enteras; construir primero el flujo pedido–inventario y después cierre/feedback. La operación de venta será atómica y cada envío tendrá un identificador reutilizable en un reintento.

**Acuerdos:** revisar errores como parte de cada historia, no al final; conservar el dato original ante rechazo; tratar toda valoración y precio de demostración como sintéticos; no exponer el servidor a Internet. La capacidad se reserva al recorrido mínimo y a su comprobación, sin nuevas integraciones.

**Salida:** objetivo del Sprint, diez historias seleccionadas, DoR/DoD y plan de trabajo visibles en este documento.

## Daily Scrum — registro de cinco jornadas virtuales

**Timebox propuesto:** diez minutos por jornada. La inspección se centra en avanzar hacia el objetivo y ajustar el plan, no en rendir cuentas a un jefe. No se inventan horarios ni asistentes.

### J1 — Inspección del alcance

**Inspección:** La visión incluía un sistema amplio, pero el MVP ya tenía diez historias delimitadas.

**Adaptación acordada:** Usar tres productos y recetas sintéticas; trabajar el recorrido completo antes de añadir funciones de Release 2.

**Impedimento o límite:** No hay cifras reales de costos, recetas o tiempo de operación. Se mantienen como hipótesis no verificadas.

### J2 — Pedido y preparación

**Inspección:** Una nota puede interpretarse como un cambio de ingredientes, aunque la receta del sistema es fija.

**Adaptación acordada:** Aclarar en la interfaz que la nota es informativa; validar cantidades y recalcular el total en el servidor.

**Impedimento o límite:** Las sustituciones quedan fuera del incremento. No se promete descontar una receta que el sistema no conoce.

### J3 — Integridad del inventario

**Inspección:** Varias líneas pueden consumir el mismo ingrediente; además, un usuario puede repetir una confirmación.

**Adaptación acordada:** Agrupar requerimientos y ejecutar una transacción; usar un identificador por envío y añadir pruebas de concurrencia.

**Impedimento o límite:** La operación no debe quedar a medias cuando falta un ingrediente o se pierde la respuesta.

### J4 — Interfaz y revisión técnica

**Inspección:** Dos pantallas necesitan leer una sola base; dos copias independientes no se sincronizan.

**Adaptación acordada:** Conservar un servidor local con SQLite y clientes de navegador; consultar cambios cada cinco segundos.

**Impedimento o límite:** La prueba local del navegador usa un puente HTTP por restricciones de navegación del entorno. No demuestra una red física.

### J5 — Cierre y evidencia

**Inspección:** El flujo ya permite registrar, descontar y revisar. Faltaba separar resultados técnicos de validación comercial.

**Adaptación acordada:** Comprobar DoD, conservar logs y seis capturas; documentar el feedback 4/5 como sintético.

**Impedimento o límite:** Pendiente una sesión con un operador real y la revisión personal de las reflexiones antes de Community.

## Sprint Review

**Momento del guion:** fin de J5. **Timebox propuesto:** 25 minutos. Participan las perspectivas simuladas de PO, desarrollo y operador; no hubo aprobación de un cliente real.

Se recorre el incremento y se contrastan las historias con su criterio de aceptación. La Review inspecciona el resultado y adapta el backlog; no es una autorización que sustituya la DoD.

| Paso de la demostración | Resultado observado |
|---|---|
| Revisar 2 mochi de fresa y 1 de matcha | Total $110.00 MXN antes de confirmar. |
| Confirmar el primer pedido | 1 pedido; quedan 480 g de masa, 240 g de crema, 170 g de fresa, 200 g de mango, 65 g de matcha y 17 empaques. |
| Confirmar 10 mochi de fresa | 2 pedidos, $460.00 MXN acumulados; masa 80 g, crema 40 g y fresa 20 g provocan tres alertas. |
| Intentar vender 3 mochi de matcha | Rechazo por stock insuficiente; el estado completo permanece igual. |
| Registrar cierre y feedback | Se guarda una valoración sintética de 4/5 con comentario de prueba. No es satisfacción de un cliente. |
| Reintentar un envío cuya respuesta se perdió | Una sola venta y un solo descuento, aun al restaurar la sesión y reenviar el mismo identificador. |

**Qué se acepta en la simulación:** las diez historias dentro del alcance descrito y los resultados de sus pruebas. **Qué no se concluye:** reducción real de tiempo, exactitud de recetas del negocio, facturación real, satisfacción de usuarios o aptitud productiva.

**Adaptación del Product Backlog:** priorizar prueba con operador real y cancelación con devolución de inventario; definir respaldo/restauración y permisos antes del uso operativo. El comentario 4/5 sirve para probar la captura de feedback, no para justificar comercialmente una prioridad.

## Sprint Retrospective

**Momento del guion:** después de la Review. **Timebox propuesto:** 20 minutos. Técnica: Empezar / Dejar / Continuar. El foco es mejorar la forma de trabajar, no volver a demostrar el producto.

| Acción | Mejora | Responsable simulado | Comprobación siguiente |
|---|---|---|---|
| Empezar | Prueba con un operador real sobre cinco pedidos de prueba. | PO / Angel Alfredo | Próximo Sprint: registrar tiempo, correcciones y comentario; comparar con una línea base manual, sin fijar mejoras inventadas. |
| Empezar | Diseñar cancelación con devolución exacta de inventario. | Developer / Angel Alfredo | Próximo Sprint: criterios y pruebas de doble cancelación, stock restituido y total del día corregido. |
| Dejar | Confundir una nota de preparación con una modificación de receta. | PO / Angel Alfredo | Mantener la advertencia visible y no aceptar sustituciones hasta definir su impacto en ingredientes. |
| Continuar | Probar errores antes de considerar una historia terminada. | SM y Developer / Angel Alfredo | Mantener idempotencia, atomicidad y concurrencia en la suite; ninguna regresión aceptada. |
| Empezar | Planear respaldo/restauración y permisos antes del uso operativo. | Developer / Angel Alfredo | Definir prueba de restauración y modelo de acceso antes de datos reales o exposición fuera de una red confiable. |

## Lecciones aprendidas como Scrum Master

### ¿Cómo te fue?

La simulación permitió pasar de una visión y un mapa de historias a un recorrido que puede comprobarse. El trabajo más importante no fue añadir pantallas, sino mantener consistente el pedido con sus ingredientes cuando ocurre un error.

### ¿Qué aprendiste?

Un incremento no se demuestra con una lista de funciones. Necesita criterios observables: cuánto debe descontarse, qué debe permanecer igual al rechazar una venta y qué ocurre al reenviar una confirmación.

### ¿Qué rescatas de este ejercicio?

Separar las responsabilidades ayudó a decidir con más claridad. La perspectiva de PO cuidó el valor; la de SM hizo visibles los impedimentos; la de desarrollo se concentró en una solución comprobable.

### ¿Cómo te sentiste realizando este ejercicio?

La parte que generó más incertidumbre fue el manejo de errores, porque una pantalla correcta puede ocultar un inventario inconsistente. Comprobar el rechazo sin cambios y el reintento sin duplicados dio una base más concreta para confiar en el resultado. Esta reflexión personal se propone para revisión del estudiante.

### ¿Cuál es ahora tu opinión de Scrum?

Scrum tiene sentido cuando inspeccionar un resultado cambia lo que se hará después. La simulación individual ayuda a comprender esa lógica, pero no reemplaza la colaboración ni la retroalimentación de un equipo y usuarios reales.

## Incremento, pruebas y límites

La aplicación usa Python 3.11 o posterior, biblioteca estándar y SQLite. No necesita instalar un framework ni servicios externos para funcionar. El servidor se inicia en el equipo y se utiliza desde el navegador. La clave temporal de acceso cambia al reiniciar; no equivale a un sistema de usuarios o permisos.

Resultados locales: **44 pruebas de lógica/API aprobadas**, **nueve comprobaciones de interfaz aprobadas**, **seis capturas** y **cero errores de JavaScript observados**. La ejecución local de interfaz renderiza el código real en memoria y utiliza un puente a la API HTTP real por una restricción de navegación del entorno. Usa almacenamiento de sesión de prueba. No debe describirse como una prueba nativa completa de navegador, de CSP o de dos dispositivos físicos. El script también incluye un modo nativo para ejecutarlo en un entorno sin esa restricción. El archivo `evidencias/verificacion_navegador.json` identifica el modo exacto de cada ejecución.

La persistencia, los códigos HTTP, la autenticación por clave, el tamaño de las peticiones, el rechazo de rutas no permitidas, la concurrencia y la idempotencia se verifican además mediante pruebas independientes. Estas comprobaciones no certifican seguridad para producción.

La conexión entre dispositivos requiere que todos apunten al mismo servidor; no se sincronizan copias independientes. No hay nube ni uso público seguro. La fecha del cierre es la del sistema operativo del servidor. No hay editor de recetas, reposición de stock ni cancelación en esta versión. La base inicial y todas las cifras de la evidencia son sintéticas.

## Consolidado de entrega

| Criterio | Puntos de la rúbrica | Evidencia entregada |
|---|---:|---|
| Eventos Scrum documentados | 3 | Planning, cinco Daily virtuales, Review y Retrospective; objetivo y duración del Sprint. |
| Incremento tangible o funcional | 3 | Código ejecutable, instrucciones, pruebas, seis capturas y trazabilidad US-01–US-10. |
| Reflexiones y aprendizajes | 2 | Retrospectiva con acciones verificables y cinco respuestas de reflexión. |
| Ambas plantillas | 2 | Semana 2 recuperada y Semana 4 completada sobre la plantilla oficial, con anexos. |

La tabla muestra cobertura documental, no una calificación otorgada. La evaluación corresponde al curso.

Los archivos finales están en `documentos/`: ambas plantillas en DOCX/PDF y `UCAMP_SCRUM_Consolidado.pdf`. El paquete ZIP incluye además código, evidencias y documentación. `ENTREGA_COMMUNITY.txt` contiene un texto de acompañamiento. Antes de publicar en Community, el estudiante debe revisar sus reflexiones y cargar los archivos; este repositorio no demuestra un envío a la plataforma.

## Fuentes y continuidad

- Semana 2: `../Semana2_SCRUM/Product_Vision_Board.md`, y plantilla completada recuperada de la entrega anterior.
- Semana 3: `../Semana3_SCRUM/User_Story_Mapping_MVP.md`.
- Plantilla oficial Semana 4: https://docs.google.com/document/d/1d07cLEUY9ldEh5usOPw_lTNAoIRd36x3mDNNMCkRFlU/edit
- Schwaber, K. y Sutherland, J. (2020). The Scrum Guide: https://scrumguides.org/scrum-guide.html
- Python Software Foundation. sqlite3: https://docs.python.org/3/library/sqlite3.html
- Python Software Foundation. http.server (limitaciones de seguridad): https://docs.python.org/3/library/http.server.html
