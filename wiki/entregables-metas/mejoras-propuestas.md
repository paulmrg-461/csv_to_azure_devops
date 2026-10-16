# Mejoras propuestas de csv_to_azure_devops

- **Comunidad:** entregables-metas
- **Alias:** mejoras-propuestas
- **Actualizado:** 2026-10-05

## Resumen

Documento con 21 hallazgos sobre los scripts de carga y extracción, con archivo y línea. Lo más importante: un fallo de red en una carga LIVE pierde el registro de lo creado y repetirla duplica tareas; tres scripts piden pegar el PAT en el código; los datos del backlog se envían a DeepSeek incluso en modo prueba. No se encontraron secretos expuestos.

Archivo: [mejoras-propuestas.md](../../docs/mejoras-propuestas.md) · Spec: [spec](../../.sdf/docs/mejoras-propuestas/spec.md)

## Hechos

- La exportación de lo creado ocurre solo al final del bucle y las llamadas a Azure DevOps no tienen manejo de errores de red · observado 2026-10-05 · desde desconocido · hasta vigente · [upload_tasks_with_ai.py](../../upload_tasks_with_ai.py)
- Tres scripts mantienen la variable del token vacía para pegarlo en el código · observado 2026-10-05 · desde desconocido · hasta vigente · [create_user_stories.py](../../create_user_stories.py)
- La llamada a la IA ocurre antes de la comprobación de modo prueba · observado 2026-10-05 · desde desconocido · hasta vigente · [upload_tasks_with_ai.py](../../upload_tasks_with_ai.py)
- `.gitignore` solo excluye `.env`; el repo versiona `venv/` · observado 2026-10-05 · desde desconocido · hasta vigente · [.gitignore](../../.gitignore)

## Relaciones

- responsable de: [upload_tasks_with_ai.py](../bienes-recursos/upload-tasks-with-ai.md) — revisa su código.
- depende de: [Extractores de Azure DevOps](../bienes-recursos/extractores-azure-devops.md) — cubre sus cuatro scripts hermanos.
- usa: [Guía para subir Tasks](guia-subir-tasks-azure-devops.md) — señala su deriva respecto del script.

## Aparece en

- [mejoras-propuestas.md](../../docs/mejoras-propuestas.md) — el documento mismo.

## Notas e historial

- 2026-10-05 — Creado. Las líneas de los dos archivos con cambios sin commitear son del árbol de trabajo.
- Los valores de `.env` se comprobaron sin imprimirlos: no aparecen en otros archivos.
