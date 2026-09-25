# User Story Mapping y MVP — SCRUM Semana 3

## Caso de estudio

**Mochi Monchi - Sistema digital de pedidos e inventario**

Esta semana continúa el mismo producto trabajado en el Product Vision Board de la Semana 2. El objetivo es representar el recorrido principal del usuario, ordenar las historias por valor y separar el conjunto mínimo que permita validar si conectar pedidos, recetas e inventario mejora la operación diaria.

## Usuario principal

**Operador de Mochi Monchi:** persona que inicia el turno, registra pedidos, consulta existencias y necesita cerrar la operación con información suficiente para detectar problemas.

El dueño o administrador funciona como stakeholder principal y utiliza el resumen de operación y el feedback del usuario para decidir qué mejorar en la siguiente iteración.

## Hipótesis a validar

> Si el operador registra un pedido una sola vez y el sistema descuenta automáticamente los ingredientes según la receta, disminuirá la doble captura y será más fácil saber qué productos pueden seguir vendiéndose durante el turno.

## Backbone del recorrido

1. **Revisar turno**
2. **Registrar pedido**
3. **Confirmar venta**
4. **Actualizar operación**
5. **Cerrar y aprender**

## User Story Mapping

| Actividad | Release 1 — MVP | Release 2 — Siguiente prioridad | Más adelante |
|---|---|---|---|
| **1. Revisar turno** | **US-01:** Como operador, quiero abrir el catálogo con precios vigentes para comenzar a vender sin revisar varias fuentes. **US-02:** Como operador, quiero ver el stock y alertas básicas para identificar productos con riesgo de faltante. | Como administrador, quiero configurar umbrales de stock por ingrediente. | Pronóstico de demanda y compras sugeridas. |
| **2. Registrar pedido** | **US-03:** Como operador, quiero crear un pedido agregando productos y cantidades para registrar la venta una sola vez. **US-04:** Como operador, quiero añadir una nota breve al pedido para registrar ajustes simples. | Editar o cancelar pedidos antes del cierre y devolver inventario cuando corresponda. | Pedidos en línea y sincronización con canales externos. |
| **3. Confirmar venta** | **US-05:** Como operador, quiero revisar el total antes de confirmar para detectar errores. **US-06:** Como operador, quiero confirmar y guardar el pedido para que quede registrado en la operación del día. | Métodos de pago y ticket/recibo. | Integración con terminales de pago. |
| **4. Actualizar operación** | **US-07:** Como operador, quiero que al confirmar el pedido se descuenten automáticamente los ingredientes definidos en la receta para evitar doble captura. **US-08:** Como operador, quiero consultar existencias actualizadas y alertas simples para saber qué productos siguen disponibles. | Sugerencia de compra y ajuste manual de inventario con historial. | Multi-sucursal y sincronización en la nube. |
| **5. Cerrar y aprender** | **US-09:** Como operador, quiero ver un resumen básico de pedidos del día para revisar el turno. **US-10:** Como operador, quiero registrar una valoración rápida de 1 a 5 y un comentario opcional para reportar fricciones o mejoras. | Reportes exportables y filtros por fecha/producto. | Analítica avanzada, promociones y notificaciones. |

## MVP — Release 1

El MVP reúne únicamente lo necesario para completar el recorrido de principio a fin y validar la hipótesis principal:

- catálogo básico de productos y precios;
- consulta de stock y alertas simples;
- creación de pedidos con productos, cantidades y nota breve;
- cálculo, revisión y confirmación del pedido;
- recetas con ingredientes y cantidades;
- descuento automático de inventario al confirmar;
- existencias actualizadas después de cada venta;
- resumen básico de pedidos del día; y
- valoración de 1 a 5 con comentario opcional al cierre del turno.

### Por qué estas funciones sí forman parte del MVP

El valor que queremos comprobar no es tener un sistema completo de punto de venta, sino demostrar que una sola captura del pedido puede alimentar el inventario y reducir trabajo manual. Por eso quedan fuera del MVP funciones útiles pero no indispensables para probar esa hipótesis, como pagos, tickets, promociones, exportaciones, usuarios avanzados o pedidos en línea.

## Release 2 / Backlog priorizado

1. edición y cancelación de pedidos con devolución de inventario;
2. métodos de pago y ticket;
3. umbrales configurables y sugerencia de compra;
4. ajustes de inventario con historial;
5. usuarios y permisos;
6. exportación de reportes.

## Backlog futuro

- promociones y combos;
- pedidos en línea;
- sincronización en la nube;
- soporte multi-sucursal;
- notificaciones a clientes;
- integraciones externas;
- analítica avanzada.

## Feedback y criterio de éxito

Durante una prueba real de operación se observarán cuatro señales:

1. **Tiempo de registro:** cuánto tarda el operador en capturar y confirmar un pedido.
2. **Correcciones:** cuántas veces necesita corregir un pedido antes de confirmarlo.
3. **Faltantes detectados:** si las alertas ayudan a identificar insumos insuficientes antes de aceptar más ventas.
4. **Percepción del usuario:** valoración de 1 a 5 y comentario opcional al cierre del turno.

El MVP cumple su objetivo si permite completar el flujo sin duplicar información, actualiza el inventario de forma automática y genera evidencia suficiente para decidir qué elemento del backlog debe priorizarse en la siguiente iteración.

## Evidencia visual

El tablero visual versionado está en:

- [Tablero_User_Story_Mapping.svg](Tablero_User_Story_Mapping.svg)

La guía para montarlo en una herramienta colaborativa y tomar las capturas solicitadas está en:

- [GUIA_ENTREGA.md](GUIA_ENTREGA.md)

## Trazabilidad de la rúbrica

- **Experiencia del usuario:** el backbone muestra un recorrido continuo desde revisar el turno hasta cerrar y aprender.
- **MVP diferenciado:** Release 1 está separado de Release 2 y del backlog futuro.
- **Feedback del mercado:** el MVP permite observar tiempos, correcciones y faltantes, además de capturar una valoración y comentario del operador.
- **Coherencia con Semana 2:** las historias se derivan de la propuesta de valor que conecta pedidos, recetas e inventario real de Mochi Monchi.

## Verificación

Entrega documental y visual. No modifica código ejecutable ni dependencias. La revisión consiste en comprobar que el tablero sea legible, que el MVP esté visualmente separado del backlog y que las capturas finales provengan de la herramienta colaborativa utilizada para la entrega.
