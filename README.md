
# Guía: Crear y subir actividades (Tasks) a Azure DevOps

Esta guía documenta el paso a paso para instalar dependencias, preparar el archivo `tasks.xlsx` y ejecutar el script para subir actividades (Tasks) a Azure DevOps. Incluye lineamientos obligatorios y buenas prácticas para evitar errores.

## 1) Prerrequisitos

- Python 3.x instalado.
- Organización y proyecto en Azure DevOps.
- Personal Access Token (PAT) con permisos: Work Items (Read & Write).
- (Opcional) API Key del proveedor de IA (para descripciones enriquecidas).

## 2) Instalación de dependencias

1. Abre la terminal en la carpeta del proyecto:
   
   ```bash
   cd c:\Users\paulm\Documents\dev-projects\IAAplicada\BlackNBlue\csv_to_azure_devops
   ```

2. Instala los requisitos:
   
   - Entorno global:
     ```bash
     pip install -r requirements.txt
     ```
   - Entorno virtual (recomendado):
     ```bash
     python -m venv .venv
     .\.venv\Scripts\activate
     pip install -r requirements.txt
     ```

Dependencias usadas: `pandas`, `requests`, `openpyxl`.

## 3) Configurar credenciales

Configura en el script o mediante variables de entorno:

- Organización (`organization`) y proyecto (`project`).
- PAT para Azure DevOps.
- (Opcional) API Key del proveedor de IA.

El script carga el archivo `.env` ubicado en la misma carpeta del script y soporta nombres de variables en mayúsculas y minúsculas. Si no defines `AZURE_DEVOPS_URL`, se construye automáticamente con `ORGANIZATION` y `PROJECT`.

Ejemplo de `.env` (ponerlo en la misma carpeta del script):

```dotenv
# Organización y Proyecto
ORGANIZATION=tu-organizacion
PROJECT=tu-proyecto

# Token de acceso personal (PAT)
AZURE_DEVOPS_PAT=tu_pat
# También se acepta: PAT=tu_pat

# Endpoint para crear Tasks (opcional). Si no lo defines, se construye automáticamente.
AZURE_DEVOPS_URL=https://dev.azure.com/tu-organizacion/tu-proyecto/_apis/wit/workitems/$Task?api-version=6.0

# Clave de IA (opcional). Si no está presente, la IA se deshabilita.
DEEPSEEK_API_KEY=tu_api_key_deepseek
```

Variables soportadas en `.env` (mayúsculas/minúsculas):
- ORGANIZATION / organization
- PROJECT / project
- AZURE_DEVOPS_PAT / PAT / azure_devops_pat / pat
- AZURE_DEVOPS_URL / azure_devops_url
- DEEPSEEK_API_KEY / deepseek_api_key

## 4) Crear primero el User Story (Key Result)

Antes de subir tareas, crea el User Story en Azure DevOps y obtén su ID (numérico). Ese ID se coloca en la columna `UserStoryID` de cada fila de `tasks.xlsx`.

- Puedes crearlo manualmente en Boards.
- O con tu script de creación de User Stories.

## 5) Preparar el archivo tasks.xlsx

El script lee `tasks.xlsx` y espera las siguientes columnas:

- `Title`
- `Module`
- `Description`
- `Priority`
- `UserStoryID`
- `Sprint`
- `AssignedTo`
- `OriginalEstimate`

Lineamientos obligatorios:

- `Priority`: siempre `1`.
- `Sprint`: exactamente con barra invertida, por ejemplo `Black and Blue\Sprint 57`.
- `Module`: debe indicar el módulo y el frente, por ejemplo:
  - `Playbacks Frontend`, `Playbacks Backend`
  - `Auth Backend`
  - `LiveViews Frontend`
  - `LocalCoreAPI Backend`
  - `Recording Service Backend`
  - `Go2RTC Backend`
  - `Code Quality Frontend/Backend`
- `AssignedTo`: correo corporativo del responsable (todos terminan en `@blacknblue.app`). Roles típicos:
  - `abdiel.arias@blacknblue.app` — Desarrollador Frontend Flutter (BnB Client).
  - `victor.rodriguez@blacknblue.app` — Backend Python/Golang (CoreAPI, LocalCoreAPI, Recording Service, Go2RTC).
  - `samir.millan@blacknblue.app` — Reconocimiento (OpenCV, YOLO, Python).
- `OriginalEstimate`: horas totales estimadas (entero o decimal). El script calcula automáticamente 30% para Unit Testing y desglosa horas en la descripción final.

Ejemplo de fila en `tasks.xlsx`:

- `Title`: Reemplazar magic numbers y strings por constantes
- `Module`: Playbacks Frontend
- `Description`: Definir constantes estáticas para valores como z-index, spacing y borderRadius, mejorando legibilidad y mantenibilidad del código.
- `Priority`: 1
- `UserStoryID`: 2035
- `Sprint`: Black and Blue\Sprint 57
- `AssignedTo`: abdiel.arias@blacknblue.app
- `OriginalEstimate`: 1

## 6) Ejecutar el script

Desde la carpeta del proyecto, ejecuta:

```bash
python upload_tasks_with_ai.py
```

Qué hace el script:

- Lee `tasks.xlsx` y crea un Work Item de tipo Task por cada fila.
- Enlaza cada Task al User Story mediante `Hierarchy-Reverse` usando `UserStoryID`.
- Genera la descripción final incluyendo:
  - Módulo y descripción base.
  - Descripción y sugerencia generadas por IA (si la API responde).
  - Detalle de horas: Tarea, Unit Testing (30%) y Total.
- Exporta un resumen a `created_tasks.xlsx` con ID, Sprint, AssignedTo y fecha de creación.

## 7) Verificación y solución de problemas

- `Sprint` (IterationPath) debe existir en Azure DevOps; si no, la API fallará.
- `AssignedTo` debe ser un usuario válido del proyecto; usa su correo corporativo.
- Errores 401/403: revisa PAT, permisos y que `organization`/`project` coincidan.
- Enlace al User Story: verifica que `UserStoryID` exista y sea accesible.
- Lectura de `tasks.xlsx`: valida nombres de columnas, hoja principal y ubicación del archivo.

## 8) Buenas prácticas al redactar tareas

- `Title`: claro y conciso (ej.: "Reemplazar magic numbers por constantes en Playbacks").
- `Module`: siempre módulo + frente (Frontend/Backend/etc.).
- `Description`: técnica y específica del cambio.
- `Priority`: 1.
- `UserStoryID`: el ID del entregable creado previamente.
- `Sprint`: `Black and Blue\Sprint 57`.
- `AssignedTo`: correo del responsable en Azure DevOps.
- `OriginalEstimate`: horas totales (el script calcula automáticamente el 30% para Unit Testing).

---

Con esta guía podrás preparar `tasks.xlsx` y ejecutar `upload_tasks_with_ai.py` para subir eficientemente tus tareas a Azure DevOps con descripciones enriquecidas y enlace al User Story correspondiente.

##### `Paul Realpe`
