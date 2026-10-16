# Guía para crear y subir Tasks a Azure DevOps

- **Comunidad:** entregables-metas
- **Alias:** README de csv_to_azure_devops, guía de carga de tareas
- **Actualizado:** 2026-10-05

## Resumen

Guía instructiva, de prerrequisitos a solución de problemas, para preparar el archivo de tareas y ejecutar el script de carga. Es el único documento real del proyecto. Está desfasada respecto del script actual: omite el modo prueba por defecto y el archivo de entrada configurable.

## Hechos

- Documento adoptado por ingeniería inversa sin modificar su contenido · desde 2026-10 · hasta vigente · [spec](../../.sdf/docs/guia-subir-tasks-azure-devops/spec.md)
- Archivo en `docs/`; la raíz conserva un README mínimo que lo enlaza · desde 2026-10 · hasta vigente · [documento](../../docs/guia-subir-tasks-azure-devops.md)
- El script arranca con `DRY_RUN=true` y no lo dice la guía · observado 2026-10-05 · desde desconocido · hasta desconocido · [script](../../upload_tasks_with_ai.py)

## Relaciones

- usa: [upload_tasks_with_ai.py](../bienes-recursos/upload-tasks-with-ai.md) — es el script que la guía explica
- usa: [Azure DevOps](../bienes-recursos/azure-devops.md) — destino de las Tasks
- usa: [DeepSeek](../empresas/deepseek.md) — IA opcional para las descripciones
- responsable de: [Paul Realpe](../personas/paul-realpe.md) — firma la guía

## Aparece en

- [guia-subir-tasks-azure-devops.md](../../docs/guia-subir-tasks-azure-devops.md)
- [README.md](../../README.md) — enlace de portada
- [project.md](../../.sdf/project.md)

## Notas e historial

- 2026-10-05 — Adoptada en [adoptar-guia-subir-tasks-azure-devops](../../.sdf/docs/guia-subir-tasks-azure-devops/changes/2026-10-05-adoptar-guia-subir-tasks-azure-devops/proposal.md). La deriva respecto del código está listada en la spec.
