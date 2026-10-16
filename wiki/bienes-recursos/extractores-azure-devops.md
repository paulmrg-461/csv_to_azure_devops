# Extractores de Azure DevOps

- **Comunidad:** bienes-recursos
- **Alias:** tasks_bugs_extractor.py, tasks_extractor.py, issues_extractor.py, create_user_stories.py
- **Actualizado:** 2026-10-05

## Resumen

Cuatro scripts auxiliares. `tasks_bugs_extractor.py` (el vigente) extrae Tasks, Bugs e Issues a `azure_devops_work_items.xlsx`. `tasks_extractor.py` e `issues_extractor.py` son versiones anteriores que escriben `azure_devops_tasks.xlsx` y `azure_devops_issues_bugs_with_comments.xlsx`. `create_user_stories.py` crea User Stories desde `user_stories.csv`. La guía no los cubre.

## Hechos

- `tasks_bugs_extractor.py` toma `PAT`, `ORGANIZATION` y `PROJECT` del `.env` · observado 2026-10-05 · desde desconocido · hasta desconocido · [script](../../tasks_bugs_extractor.py)
- Los otros tres llevan `organization` y `project` escritos en el código y `pat` vacío · observado 2026-10-05 · desde desconocido · hasta desconocido · [create_user_stories.py](../../create_user_stories.py)
- `create_user_stories.py` antepone `[KeyResult]:` al título · observado 2026-10-05 · desde desconocido · hasta desconocido · [script](../../create_user_stories.py)

## Relaciones

- usa: [Azure DevOps](azure-devops.md) — lee y crea Work Items

## Aparece en

- [project.md](../../.sdf/project.md)

## Notas e historial

- 2026-10-05 — `tasks_bugs_extractor.py` tiene cambios sin commitear. Ninguno de estos scripts está gobernado: solo documentación.
