# Propuesta: crear-mejoras-propuestas

- **Fecha:** 2026-10-05
- **Estado:** cerrado
- **Módulos:** flujo.md, tipos-de-documento.md
- **Presupuesto:** estándar ≤80k
- **Evaluación:** no aplica — la revisión independiente queda a cargo del orquestador del equipo (separación autoría/revisión)
- **Tokens:** ~55k (orquestador estimado; sin subagentes) — dentro del presupuesto
- **Tipo:** crear
- **Documento(s) afectado(s):** mejoras-propuestas (nuevo)
- **Solicitado por:** Paul Realpe (vía el orquestador del equipo)

## Qué se pide

Documento de mejoras propuestas con hallazgos concretos (archivo y línea) para los scripts de carga y extracción, ordenados por prioridad.

## Por qué

No había una revisión consolidada de los scripts, y el PAT y los datos enviados a la IA son los puntos de riesgo.

## Decisiones de la conversación

- **No modificar código ni los archivos sin commitear** (`tasks_bugs_extractor.py`, `upload_tasks_with_ai.py`); se pueden leer.
- **Ignorar `venv/`:** no se lee ni analiza.
- **Sin valores de credenciales**; fecha real 2026-10-05; sin commits ni `CLAUDE.md`.

## Pendientes / supuestos

- Supuesto: las líneas citadas de los dos archivos modificados son las del árbol de trabajo.
- No se ejecutó ningún script; comportamientos de Azure DevOps marcados como no verificados.

## Impacto

- Specs a crear: `.sdf/docs/mejoras-propuestas/spec.md`
- Archivos a generar/modificar: `docs/mejoras-propuestas.md`
- Tabla de documentos activos en `.sdf/project.md`: sí
