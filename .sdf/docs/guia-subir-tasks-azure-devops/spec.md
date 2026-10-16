# Spec: Guía para crear y subir Tasks a Azure DevOps

> **Spec por ingeniería inversa (adopción 2026-10-05).** Describe la guía tal como estaba en el `README.md`; el contenido no se modificó.

- **Id:** guia-subir-tasks-azure-devops
- **Archivo:** `docs/guia-subir-tasks-azure-devops.md`
- **Formato:** Markdown
- **Estado:** vigente, con deriva respecto del código (ver Decisiones)
- **Creado:** 2026-10-05 (la guía es anterior; fecha original no determinada. Firma "Paul Realpe" al final)
- **Última actualización:** 2026-10-05

## Propósito

Guiar paso a paso la instalación de dependencias, la preparación del archivo de tareas y la ejecución de `upload_tasks_with_ai.py`, que crea un Work Item de tipo Task por fila, lo enlaza a su User Story y enriquece la descripción con IA.

## Audiencia

Quien sube tareas de planificación a Azure DevOps (hoy, Paul Realpe y quien lo releve).

## Requisitos

- La guía DEBE listar prerrequisitos: Python, organización y proyecto de Azure DevOps, PAT con permiso Work Items (Read & Write), clave de IA opcional.
- La guía DEBE declarar las columnas obligatorias del archivo de tareas y sus lineamientos (`Priority` = 1, formato de `Sprint`, `Module` con frente, `AssignedTo` con correo corporativo).
- La guía NO DEBE contener credenciales reales; solo marcadores (`tu_pat`, `tu_api_key_deepseek`). Verificado al adoptar: cumple.
- La guía DEBERÍA reflejar el comportamiento real del script (hoy no lo hace; ver Decisiones).

## Estructura y contenido

1. **Prerrequisitos.**
2. **Instalación de dependencias:** entorno global o virtual; dependencias citadas: `pandas`, `requests`, `openpyxl`.
3. **Configurar credenciales:** variables de `.env` (`ORGANIZATION`, `PROJECT`, `AZURE_DEVOPS_PAT`/`PAT`, `AZURE_DEVOPS_URL`, `DEEPSEEK_API_KEY`) con ejemplo de relleno.
4. **Crear primero el User Story (Key Result)** y obtener su ID numérico.
5. **Preparar `tasks.xlsx`:** ocho columnas (`Title`, `Module`, `Description`, `Priority`, `UserStoryID`, `Sprint`, `AssignedTo`, `OriginalEstimate`), lineamientos y una fila de ejemplo.
6. **Ejecutar el script:** qué hace (crea Tasks, enlaza con `Hierarchy-Reverse`, genera descripción con módulo, texto de IA y horas con 30 % de Unit Testing, exporta `created_tasks.xlsx`).
7. **Verificación y solución de problemas:** Sprint existente, usuario válido, errores 401/403, enlace a User Story, lectura del archivo.
8. **Buenas prácticas al redactar tareas.**

## Formato y estilo

Markdown con listas y bloques de código; firma `Paul Realpe` al final. Incluye una ruta absoluta de Windows (`c:\Users\paulm\...\BlackNBlue\csv_to_azure_devops`) que no corresponde a la ubicación actual del proyecto.

## Fuentes de datos

Cotejada con [`upload_tasks_with_ai.py`](../../../upload_tasks_with_ai.py) (versión con cambios sin commitear, leída sin tocarla), [`requirements.txt`](../../../requirements.txt) y [`.env.example`](../../../.env.example). No se ejecutó ningún script ni se contactó Azure DevOps.

## Decisiones

- **2026-10-05 — Movida a `docs/` con README mínimo en la raíz:** es el único documento real del proyecto. Se movió como pide el framework; se dejó un README de tres líneas porque la raíz de un repositorio sin README pierde su portada. Se descartó dejar la guía en la raíz porque el checklist exige `docs/<id>.*`.
- **2026-10-05 — Deriva anotada, no corregida (corolario 3).** Frente al código actual (versión con cambios sin commitear):
  1. El script arranca en **modo prueba**: `DRY_RUN` vale `true` por defecto y hay que poner `DRY_RUN=false` para crear Work Items. La guía no lo menciona.
  2. Archivo de entrada: el script lee `INPUT_FILE` (por defecto `tasks.csv`, separador TAB; admite `.xlsx`, listas separadas por coma y patrones glob). La guía habla solo de `tasks.xlsx`.
  3. `DEEPSEEK_MODEL`, `CSV_SEPARATOR`, `INPUT_FILE` y `DRY_RUN` no figuran en la guía; `.env.example` trae `INPUT_FILE` y `CSV_SEPARATOR`.
  4. La guía omite `python-dotenv`, que sí está en `requirements.txt`.
  5. El ejemplo de sprint dice `Sprint 57`; `tasks.csv` usa `Sprint 61`.
  6. Corregirlo es un cambio `actualizar-guia-subir-tasks-azure-devops`, posterior a que se commiteen las modificaciones del script (el script se leyó en su estado de trabajo).
- **2026-10-05 — Datos personales:** la guía lista correos corporativos de tres responsables por rol. La spec no los repite.

## Registro de cambios

| Fecha | Cambio (carpeta en changes/) | Resumen |
|-------|------------------------------|---------|
| 2026-10-05 | 2026-10-05-adoptar-guia-subir-tasks-azure-devops | Adopción por ingeniería inversa; guía movida a `docs/` |
