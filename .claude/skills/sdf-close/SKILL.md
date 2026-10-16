---
name: sdf-close
description: Cierra los cambios que quedaron en curso - spec, project.md, wiki, checklist
---

Busca proposals con `Estado: en curso` en `.sdf/docs/*/changes/*/` y ciérralos según el módulo `.sdf/reglas/flujo.md` (secciones "Flujo de trabajo obligatorio" y "Checklist de validación"):

1. Para cada cambio abierto: verifica que el documento en `docs/` refleje lo pedido; completa la spec; actualiza la tabla de Documentos activos de `.sdf/project.md`; lanza EN PARALELO (mismo turno) `wiki-graph` (wiki + MEMORY delta) y `evaluator` (si es documento nuevo o cambio mayor); luego la verificación en dos capas: `bash .sdf/specs/checklist.sh <id>` + los 3 puntos de juicio del módulo `.sdf/reglas/flujo.md`. Si cierras varios documentos, lote: un solo wiki-graph con todos los deltas y los evaluators en paralelo; marca tareas de `tasks.md` y pon `Estado: cerrado`.
2. Si un cambio no puede cerrarse porque falta una decisión del usuario, pregúntala (sección "Pendientes / supuestos" del proposal).
3. Reporta: cambios cerrados y qué se completó en cada uno, más las entradas nuevas o pendientes de `.sdf/REVIEW.md` (contradicciones, entidades dudosas, relaciones fuera de vocabulario) para que el usuario decida cuando quiera. No bloquean el cierre.
