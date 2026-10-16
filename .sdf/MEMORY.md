# MEMORY del proyecto: csv_to_azure_devops

> Memoria compacta de arranque. TOPE DURO: 80 líneas.
> Última consolidación: 2026-10-16

## Qué es este proyecto

Scripts Python para subir Tasks a Azure DevOps desde `tasks.csv`/`tasks.xlsx` con texto generado por IA, y para extraer Work Items a Excel. Este SDF gobierna solo la guía de uso. Propietario: Paul Realpe. Ver [project.md](project.md).

## Estado actual

- Un documento adoptado el 2026-10-05: [guía](docs/guia-subir-tasks-azure-devops/spec.md).
- 2026-10-05: creado [mejoras-propuestas](docs/mejoras-propuestas/spec.md) (21 hallazgos; sin secretos expuestos; prioridad: resiliencia de la carga LIVE).
- 2026-10-16: `upload_tasks_with_ai.py` con proveedor de IA seleccionable (DeepSeek/Groq); trabajo en la rama `feature/groq-provider`.
- 2026-10-16: cargadas Tasks en Azure DevOps — épica 02 (14 Tasks, IDs 3706-3719 → US 3705) y épica 03 (15 Tasks, IDs 3721-3735 → US 3720).
- Pendiente: actualizar la guía (sigue sin `DRY_RUN`, `INPUT_FILE` ni el proveedor seleccionable).

## Decisiones vigentes que moldean el trabajo

- 2026-10-05 — Guía movida a `docs/`; el README raíz queda como enlace ([spec](docs/guia-subir-tasks-azure-devops/spec.md)).
- 2026-10-05 — `venv/` y `.env` no se leen ni se documentan.
- 2026-10-16 — IA por proveedor: `AI_PROVIDER` elige `deepseek` (default del repo) o `groq`; en el `.env` local se usa `groq` con `openai/gpt-oss-120b`.
- 2026-10-16 — Fuera del índice de git: `venv/`, estado local (`.omc/`, `.marscode/`, `.obsidian/`, `.DS_Store`) y salidas (`created_tasks.xlsx`, `azure_devops_work_items.xlsx`); ver `.gitignore`.

## Entidades clave

- [upload_tasks_with_ai.py](../wiki/bienes-recursos/upload-tasks-with-ai.md) — el script de carga; proveedor IA seleccionable (DeepSeek/Groq), `DRY_RUN=true` por defecto.
- [Extractores](../wiki/bienes-recursos/extractores-azure-devops.md) — scripts auxiliares sin documentar.
- [Azure DevOps](../wiki/bienes-recursos/azure-devops.md) — destino; organización BlacknBlue.
- [Mejoras propuestas](../wiki/entregables-metas/mejoras-propuestas.md) — hallazgos por archivo y línea.
- [Backlog de docs](../wiki/proyectos-relacionados/docs-backlog.md) — insumo previsto.

## Aprendizajes y preferencias del usuario

- Español; lo indeterminable se declara (origen: encargo 2026-10-05).
- `.env` contiene credenciales: nunca reproducirlas (origen: encargo 2026-10-05).
- 2026-10-16 — En la cuenta Groq del proyecto el modelo válido es `openai/gpt-oss-120b` (`llama-3.3-70b-versatile` da 404 `model_not_found`).
- 2026-10-16 — `created_tasks.xlsx` se sobrescribe en cada corrida (hallazgo 18): guardar copia por épica si importa el historial de IDs.
