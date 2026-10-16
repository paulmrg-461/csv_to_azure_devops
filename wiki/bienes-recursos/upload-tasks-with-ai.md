# upload_tasks_with_ai.py

- **Comunidad:** bienes-recursos
- **Alias:** script de carga, uploader
- **Actualizado:** 2026-10-05

## Resumen

Script que lee un archivo de tareas (`.csv` con TAB o `.xlsx`), pide a DeepSeek una descripción, actividades y criterios de aceptación por tarea, crea la Task en Azure DevOps, la enlaza a su User Story y exporta `created_tasks.xlsx`. Reparte la estimación: 30 % a Unit Testing y el resto a la tarea.

## Hechos

- Modo prueba activo por defecto (`DRY_RUN=true`); para escribir en Azure DevOps hay que fijar `DRY_RUN=false` · observado 2026-10-05 · desde desconocido · hasta desconocido · [script](../../upload_tasks_with_ai.py)
- Entrada configurable con `INPUT_FILE` (por defecto `tasks.csv`; lista separada por comas o patrón glob) · observado 2026-10-05 · desde desconocido · hasta desconocido · [script](../../upload_tasks_with_ai.py)
- Modelo de IA por defecto `deepseek-v4-flash`, ajustable con `DEEPSEEK_MODEL` · observado 2026-10-05 · desde desconocido · hasta desconocido · [script](../../upload_tasks_with_ai.py)
- Tiene cambios sin commitear en el repositorio · observado 2026-10-05 · desde desconocido · hasta desconocido · [script](../../upload_tasks_with_ai.py)

## Relaciones

- usa: [Azure DevOps](azure-devops.md) — crea Work Items y enlaces
- usa: [DeepSeek](../empresas/deepseek.md) — genera el texto enriquecido
- depende de: [backlog de la carpeta docs](../proyectos-relacionados/docs-backlog.md) — su comentario sugiere cargar `../docs/backlog/saas-licencias/tasks-epic-*.csv`

## Aparece en

- [guía](../../docs/guia-subir-tasks-azure-devops.md)

## Notas e historial

- 2026-10-05 — No se ejecutó; la descripción sale de leer el código.
