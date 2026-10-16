# Instrucciones para agentes de IA

**Versión del framework SDF: 6.0** (el instalador la estampa en `.sdf/project.md`; las actualizaciones comparan estampas y aplican solo las migraciones intermedias).

Este proyecto usa un sistema de especificaciones inspirado en **OpenSpec**, adaptado para producir documentos de oficina (Word, Excel, PowerPoint, PDF) en lugar de código. Cualquier herramienta de IA (Claude, Codex, Gemini, etc.) debe seguir estas reglas.

Este archivo es el **núcleo**: agnóstico al modelo, siempre cargado, deliberadamente mínimo. Seis módulos en `.sdf/reglas/` cargan lo que no toda tarea necesita (tabla "Módulos de reglas") — incluido el flujo completo de crear/actualizar/cerrar un documento. Nunca cites un nombre de modelo aquí ni en un módulo: la tabla `modelos` del arnés lo resuelve por plataforma.

## Principio central

**Ningún documento se crea o modifica sin una especificación.** La spec es la fuente de verdad; el archivo Word/Excel/PPT/PDF es solo el artefacto generado a partir de ella: siempre se regenera o actualiza el mismo documento a partir de su spec actualizada, nunca se acumulan versiones.

Corolarios:

1. Un documento "rápido, sin tanta vuelta" sigue el flujo completo pero ligero (proposal y spec breves). Nunca se omite.
2. Documento en `docs/` sin spec en `.sdf/docs/<id>/` (creado por fuera del flujo): antes de modificarlo, crear su spec por ingeniería inversa (leer el archivo, documentar su estado actual).
3. Spec y documento contradictorios: informar al usuario y resolver la discrepancia antes de continuar (normalmente regenerando el documento desde la spec).

## Estructura de carpetas

Regla de diseño: **la raíz muestra solo lo que el usuario usa** — documentos (`docs/`), conocimiento (`wiki/`), archivos fuente y el adaptador de la IA. Toda la maquinaria vive oculta en `.sdf/`.

```
<proyecto>/
├── CLAUDE.md          ← adaptador de la IA en uso (o AGENTS.md/GEMINI.md); puntero a .sdf/AGENTS.md
├── <archivos fuente>  ← insumos y referencia, en la raíz o en subcarpetas propias
├── docs/              ← SOLO documentos gobernados, planos + README — <id>.<ext> (.docx/.xlsx/.pptx/.pdf)
├── wiki/              ← conocimiento del proyecto (módulo `wiki.md`) — INDEX.md + comunidades
└── .sdf/              ← maquinaria del framework (oculta)
    ├── AGENTS.md      ← ESTE archivo: el núcleo
    ├── reglas/        ← los seis módulos (ver "Módulos de reglas")
    ├── project.md     ← contexto del proyecto (leer SIEMPRE primero) + estampa de versión
    ├── MEMORY.md      ← memoria compacta de arranque (la genera sdf-init; tope 80 líneas)
    ├── FRAMEWORK-FEEDBACK.md / REVIEW.md / usage.csv  ← colas y contador, se crean al primer hallazgo
    ├── specs/         ← SOLO las plantillas del framework + checklist.sh
    └── docs/          ← espejo de docs/: <id>/spec.md , /changes/AAAA-MM-DD-<id-cambio>/{proposal.md, tasks.md, design.md?}
```

Correspondencia por id: `docs/<id>.<ext>` ↔ spec `.sdf/docs/<id>/spec.md` ↔ historial `.sdf/docs/<id>/changes/`, sin subcarpetas por documento (planos). `docs/`, `wiki/` y `.sdf/specs/` traen `README.md`; `wiki/` y `.sdf/specs/` además una regla por ruta que carga sola al trabajar ahí (o se lee al entrar, si la plataforma no lo hace). Archivos fuente: donde el usuario quiera; el framework no los gobierna, solo los registra en `.sdf/project.md`.

**Adaptadores:** en la raíz vive únicamente el de la herramienta en uso (pueden convivir varios) — `CLAUDE.md`, `AGENTS.md` (Codex/OpenAI, convención nativa), `GEMINI.md`. Todos delgados: activan `.sdf/AGENTS.md`, la única fuente de verdad.

## Módulos de reglas

Cada módulo vive en `.sdf/reglas/<nombre>.md` y se carga SOLO cuando la tarea lo exige — nunca todos a la vez. Si una tarea toca más de una fila, cárgalos todos.

| Si la tarea es... | Carga el módulo |
|---|---|
| Crear, actualizar, retirar o renombrar un documento; cerrar cualquier cambio; iniciar un proyecto nuevo | `flujo.md` |
| Crear/actualizar una página de `wiki/`, sincronizar correo/calendario, reconciliar fuentes movidas | `wiki.md` |
| Construir, consolidar o leer `.sdf/MEMORY.md`; registrar un aprendizaje o corrección del usuario | `memoria-y-aprendizaje.md` |
| Invocar/simular un subagente, decidir modelo, evaluar un entregable, registrar tokens | `modelos-y-delegacion.md` |
| Detectar, instalar dentro de, o trabajar cerca de un sub-proyecto SDF | `anidados.md` |
| Redactar "Estructura y contenido" de una spec | `tipos-de-documento.md` |

Una consulta simple sobre la wiki (una pregunta puntual, un `status`/`lint`) no exige cargar `flujo.md`: solo entra en juego al tocar `docs/` o cerrar un cambio.

**Orden de arranque fijo:** `.sdf/MEMORY.md` → `.sdf/project.md` → este núcleo → el/los módulo(s) que la tarea exija. Nunca abras documentos, specs completas ni archivos fuente antes de agotar esa cadena.

## Convenciones

- Kebab-case: `informe-avance-q3`. `<id-documento>` nombra a la vez el archivo en `docs/` y su carpeta espejo en `.sdf/docs/`.
- Ids de cambio con verbo en infinitivo (`crear-presupuesto-2026`), carpeta con prefijo de fecha (`2026-07-24-crear-presupuesto-2026/`).
- Idioma: el de `project.md`. Fechas AAAA-MM-DD, **siempre reales, nunca deducidas** (`date +%F` o la del entorno de la sesión) al nombrar una carpeta de cambio o llenar `Fecha:`/`Actualizado:` — son historial inmutable, una fecha alucinada lo corrompe para siempre.
- Specs en markdown puro, sin dependencias de herramienta. Nunca `documento_v2_final_FINAL.docx`: un documento = un archivo + una spec.
- Un cambio en curso a la vez por documento. Cambios cerrados no se editan. Wiki en modo delta en cada cierre (módulo `wiki.md`).
- **Prefijo estable:** núcleo y adaptadores no contienen nada que cambie entre sesiones (fechas, contadores, estado) — eso vive en `MEMORY.md` y `usage.csv`. Es lo que hace útil la caché de prompts de cada proveedor.
