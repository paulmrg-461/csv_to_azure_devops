# MEMORY del proyecto: csv_to_azure_devops

> Memoria compacta de arranque. TOPE DURO: 80 líneas.
> Última consolidación: 2026-10-05

## Qué es este proyecto

Scripts Python para subir Tasks a Azure DevOps desde `tasks.csv`/`tasks.xlsx` con texto generado por IA, y para extraer Work Items a Excel. Este SDF gobierna solo la guía de uso. Propietario: Paul Realpe. Ver [project.md](project.md).

## Estado actual

- Un documento adoptado el 2026-10-05: [guía](docs/guia-subir-tasks-azure-devops/spec.md).
- 2026-10-05: creado [mejoras-propuestas](docs/mejoras-propuestas/spec.md) (21 hallazgos; sin secretos expuestos; prioridad: resiliencia de la carga LIVE).
- Pendiente: actualizar la guía cuando se commiteen los cambios de `upload_tasks_with_ai.py` (modo prueba por defecto, `INPUT_FILE`).

## Decisiones vigentes que moldean el trabajo

- 2026-10-05 — Guía movida a `docs/`; el README raíz queda como enlace ([spec](docs/guia-subir-tasks-azure-devops/spec.md)).
- 2026-10-05 — `upload_tasks_with_ai.py` y `tasks_bugs_extractor.py` no se tocan mientras tengan cambios sin commitear.
- 2026-10-05 — `venv/` y `.env` no se leen ni se documentan.

## Entidades clave

- [upload_tasks_with_ai.py](../wiki/bienes-recursos/upload-tasks-with-ai.md) — el script de carga; `DRY_RUN=true` por defecto.
- [Extractores](../wiki/bienes-recursos/extractores-azure-devops.md) — scripts auxiliares sin documentar.
- [Azure DevOps](../wiki/bienes-recursos/azure-devops.md) — destino; organización BlacknBlue.
- [Mejoras propuestas](../wiki/entregables-metas/mejoras-propuestas.md) — hallazgos por archivo y línea.
- [Backlog de docs](../wiki/proyectos-relacionados/docs-backlog.md) — insumo previsto.

## Aprendizajes y preferencias del usuario

- Español; lo indeterminable se declara (origen: encargo 2026-10-05).
- `.env` contiene credenciales: nunca reproducirlas (origen: encargo 2026-10-05).
