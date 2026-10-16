# Proyecto: csv_to_azure_devops

## Propósito

Conjunto de scripts Python que suben Tasks a Azure DevOps desde un archivo de tareas (`tasks.csv` o `tasks.xlsx`), con descripciones enriquecidas por IA, y que extraen Work Items (Tasks, Bugs, Issues) a Excel. Su guía de uso es el documento central. (Fuentes: [README.md](../README.md), [guía](../docs/guia-subir-tasks-azure-devops.md).)

Este proyecto SDF **gobierna la documentación**, no el código. Resultado esperado: que la guía de carga tenga spec e historial y que su deriva respecto del script quede registrada hasta corregirse.

### Alcance

- **Incluido:** la guía de carga de Tasks.
- **Excluido:** los scripts (`*.py`), los datos (`tasks.csv`, `tasks.xlsx`, `user_stories.csv`, `*.xlsx` generados), `.env` y la carpeta `venv/` (no se lee ni se documenta). El código no se modifica desde este proyecto.
- **No gobernados por decisión:** los archivos de datos; son insumos y salidas, no documentos.

## Contexto

- **Propietario:** Paul Realpe (Paul.Realpe@sig.systems)
- **Organización / equipo:** SIG Systems / SLC Enterprise
- **Creado:** 2026-10-05 (gobierno SDF); primer commit del código: ver historial git (rama `main`)
- **Idioma de trabajo:** español
- **Versión del framework SDF:** 6.0 — actualizado 2026-10-05 (instalado 2026-10-05)
- **Entregables típicos:** Markdown (`.md`).
- **Estado del repositorio al adoptar:** `main`, con cambios sin commitear en `tasks_bugs_extractor.py` y `upload_tasks_with_ai.py`; esos archivos no se tocaron.

## Audiencias y stakeholders

| Audiencia | Rol | Qué necesita |
|-----------|-----|--------------|
| Quien sube tareas de planificación | ejecutor | pasos exactos y reglas del archivo de entrada |
| Responsables asignados en las tareas | lector | saber que las tareas se crean con su correo corporativo |

## Estándares de los documentos

- **Tono y estilo:** instructivo, español, segunda persona.
- **Marca / plantilla visual:** no determinada.
- **Formato de fechas:** AAAA-MM-DD
- **Moneda y unidades:** horas (estimación original de cada tarea).
- **Confidencialidad:** contiene datos de acceso. Nunca reproducir ni citar valores de `.env`: contiene credenciales (PAT de Azure DevOps y clave de IA); no se reproducen aquí. `.env` está en `.gitignore`.
- **Verbosidad del chat:** respuestas breves por defecto.

## Convenciones del proyecto

- Sistema de especificaciones estilo OpenSpec (ver `AGENTS.md`).
- Cada entregable vive plano en `docs/<id>.md`; spec e historial en `.sdf/docs/<id>/`.
- La raíz conserva un `README.md` mínimo que enlaza a la guía.
- **Comunidades de la wiki:** núcleo + extensiones activas: ninguna.
- **Relaciones de la wiki:** vocabulario cerrado de `AGENTS.md`; ampliaciones aprobadas: ninguna.
- Los archivos con cambios sin commitear no se modifican hasta que el propietario los commitee.

## Fuentes de información

- [upload_tasks_with_ai.py](../upload_tasks_with_ai.py) — script de carga (cambios sin commitear).
- [tasks_bugs_extractor.py](../tasks_bugs_extractor.py) — extrae Tasks/Bugs/Issues a `azure_devops_work_items.xlsx` (cambios sin commitear).
- [tasks_extractor.py](../tasks_extractor.py), [issues_extractor.py](../issues_extractor.py) — extractores anteriores; llevan `organization`/`project` fijos y `pat` vacío en el código.
- [create_user_stories.py](../create_user_stories.py) — crea User Stories ("[KeyResult]") desde `user_stories.csv`.
- [tasks.csv](../tasks.csv), [tasks.xlsx](../tasks.xlsx), [user_stories.csv](../user_stories.csv) — entradas de ejemplo/trabajo.
- [created_tasks.xlsx](../created_tasks.xlsx), [azure_devops_work_items.xlsx](../azure_devops_work_items.xlsx) — salidas generadas.
- [requirements.txt](../requirements.txt), [.env.example](../.env.example) — dependencias y plantilla de variables.
- `.env` — credenciales, no se lee ni se reproduce.
- Azure DevOps (organización BlacknBlue) y API de DeepSeek — servicios externos.

## Glosario

| Término | Significado |
|---------|-------------|
| Task | Work Item de tarea que crea el script en Azure DevOps |
| User Story / Key Result | Work Item padre al que se enlaza cada Task; se crea antes con el título `[KeyResult]: …` |
| PAT | Personal Access Token de Azure DevOps (permiso Work Items Read & Write) |
| `UserStoryID` | Columna con el ID numérico del User Story padre |
| Sprint (IterationPath) | Ruta de iteración con barra invertida, p. ej. `Black and Blue\Sprint 61` |
| `DRY_RUN` | Variable del script; por defecto `true` (no crea Work Items) |
| `Hierarchy-Reverse` | Tipo de enlace con el que la Task apunta a su User Story |
| Unit Testing 30 % | Parte de la estimación que el script separa de las horas de la tarea |
| DeepSeek | Proveedor de IA que genera descripción, actividades y criterios de aceptación |

## Documentos activos

| Id | Archivo | Formato | Descripción | Estado |
|----|---------|---------|-------------|--------|
| guia-subir-tasks-azure-devops | `docs/guia-subir-tasks-azure-devops.md` | Markdown | Guía para preparar el archivo de tareas y subirlas a Azure DevOps | vigente |
| mejoras-propuestas | `docs/mejoras-propuestas.md` | Markdown | Hallazgos de seguridad, correcciones, refactor, pruebas y futuro, con archivo y línea | vigente |
