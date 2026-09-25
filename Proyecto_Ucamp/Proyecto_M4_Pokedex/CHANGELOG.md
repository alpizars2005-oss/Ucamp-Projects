# Cambios de la Pokédex

## Sin integrar — revisión del 25 de septiembre de 2026

Corregí el guardado para que el nombre recibido de la API no pueda elegir una ruta fuera de `pokedex/` mediante `../`, una ruta absoluta o un enlace simbólico externo ya existente. La respuesta debe ser un objeto JSON y el nombre acepta letras minúsculas ASCII, números y segmentos separados por guiones, como `mr-mime`.

Las respuestas válidas conservan el mismo contenido: `imagen_frontal` y la respuesta completa bajo `pokemon`. Si falta `name`, se mantiene `pokemon.json`. No se eliminan ni migran archivos existentes y no hay dependencias nuevas.

La comprobación de enlaces simbólicos evita seguir un destino externo que ya exista cuando se valida. No pretende aislar el programa frente a otro proceso que cambie concurrentemente el sistema de archivos.

## Verificación de esta revisión

Ejecutar desde la raíz:

```bash
python -m unittest discover -s Proyecto_Ucamp/Proyecto_M4_Pokedex/tests -v
```

Pasaron localmente 13 pruebas: las seis anteriores y siete nuevas de persistencia. Los casos de escritura se ejecutaron únicamente en directorios temporales; no se hicieron peticiones a PokéAPI ni se abrió el navegador. En sistemas que no permitan crear enlaces simbólicos, ese caso se omite explícitamente.

El apartado histórico de verificación manual del README no es evidencia de una nueva ejecución en esta revisión. El resultado de CI y la integración se deben consultar en el PR correspondiente.

Alcance y rollback: [PLAN.md](PLAN.md). La corrección se revierte con su commit de implementación; no necesita restaurar una migración de datos.
