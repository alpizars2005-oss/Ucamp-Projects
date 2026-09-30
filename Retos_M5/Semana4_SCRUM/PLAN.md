# Sprint 1: plan de implementación

Caso de estudio: Mochi Monchi. Se conserva el MVP US-01 a US-10 de Semana 3.

1. Implementar un servicio local de Python y SQLite, sin dependencias externas, y una interfaz web adaptable.
2. Probar el recorrido completo y los errores que afectarían pedidos o inventario: cantidades inválidas, falta de insumos, doble envío y concurrencia.
3. Separar la simulación académica de los resultados observados. No inventar asistentes, reuniones, satisfacción del negocio ni mejoras de tiempo.
4. Completar una copia de la plantilla oficial de Semana 4 y recuperar la entrega original de Semana 2.
5. Capturar la aplicación en ejecución, consolidar documentos, publicar en el mismo repositorio y verificar el resultado remoto.

Decisión de alcance: interfaz web local sobre una sola base de datos. Facilita usar el mismo incremento desde distintos navegadores de una red confiable; no equivale a sincronización en la nube ni a un ejecutable autónomo. Pagos, edición/cancelación, usuarios y reportes avanzados siguen fuera del Sprint.

Riesgo y reversión: sólo se añade Semana4_SCRUM y documentación/CI relacionada. No se borran ni reescriben los ejercicios anteriores. Los datos operativos nunca se versionan.
