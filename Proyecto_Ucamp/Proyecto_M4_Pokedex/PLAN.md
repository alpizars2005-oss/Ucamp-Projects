# Revisión del guardado de la Pokédex — 2026-09-25

El plan histórico del curso se conserva en `../../PLAN.md`. Esta revisión afecta únicamente el guardado de JSON del proyecto del Módulo 4; no modifica las entregas de Scrum ni otros proyectos.

## Lo que encontré

`guardar_pokemon()` utiliza directamente el campo `name` recibido de la API para construir el archivo. En una prueba con datos sintéticos, `../fuera` escribió fuera de `pokedex/`. Un archivo de destino que ya era un enlace simbólico también podía dirigir la escritura fuera de esa carpeta.

La reproducción se hizo exclusivamente en directorios temporales. No demuestra una respuesta maliciosa real de PokéAPI ni una explotación del equipo. Es una validación faltante en el límite entre datos externos y archivos locales.

## Commits

1. Registrar la reproducción y el alcance.
2. Validar el nombre de archivo, comprobar el destino resuelto y añadir regresiones sin cambiar el JSON que se guarda para respuestas válidas.
3. Documentar el comportamiento y comprobar el CI existente de Python 3.11/3.13.

## Pruebas

Los archivos locales de código y tests existentes coinciden con sus hashes Git en `a6a18ceadcb6be5bf27bc8046c40f93209b685b1`. Las seis pruebas originales pasaron. Las siete pruebas nuevas incluyen rutas relativas/absolutas, tipos inválidos, un enlace simbólico externo y conservación de datos válidos. Las rutas de prueba están dentro de un único directorio temporal, incluso cuando se prueba una salida fuera de la subcarpeta `pokedex/`.

No se consulta Internet, no se abre el navegador y no se usa información personal.

## Compatibilidad y límites

Conservar la respuesta completa, `imagen_frontal`, la carpeta configurada, el nombre predeterminado `pokemon` cuando falta `name`, la salida de consola y los objetivos de la rúbrica. No añadir bibliotecas ni capas nuevas.

Aceptar nombres formados por letras ASCII minúsculas, números y segmentos separados por guiones. Rechazar nombres que pretendan ser rutas. Comprobar también enlaces simbólicos ya existentes. Esto no es un sandbox para un sistema de archivos modificado concurrentemente por un atacante local.

## Riesgo y rollback

Bajo para las respuestas normales usadas en el proyecto. Los nombres malformados dejan de generar archivos. Revertir el commit de implementación; no hay migración ni eliminación de los JSON existentes.
