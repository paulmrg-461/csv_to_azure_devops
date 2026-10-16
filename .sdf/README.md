# SDF — Spec Driven Framework

Plantilla de proyecto para producir documentos de oficina (Word, Excel, PowerPoint, PDF) con IA de forma gobernada: **cada documento nace de una especificación** que captura sus requisitos, estructura y el razonamiento detrás de cada decisión. Inspirado en OpenSpec, adaptado de código a documentos.

Desde la v5, la carpeta del proyecto queda limpia: en la raíz solo se ven `docs/` (los documentos), `wiki/` (el conocimiento), los archivos fuente del usuario y el adaptador de su herramienta de IA. Toda la maquinaria del framework — este README incluido — vive en la carpeta oculta `.sdf/`.

## Cómo usar esta plantilla

1. Instalar el framework en la carpeta del proyecto (skill SDF o SDF Manager), eligiendo el adaptador de la herramienta de IA que se usa (Claude → `CLAUDE.md`, Codex → `AGENTS.md`, Gemini → `GEMINI.md`).
2. En la primera sesión, pedir a la IA que diligencie `project.md` (es una plantilla con placeholders; hará una entrevista corta).
3. Pedir documentos normalmente. La IA seguirá el flujo de `AGENTS.md`: propuesta → documento → spec → cierre del cambio.

¿La carpeta ya tiene contenido (Words, Exceles, PDFs, imágenes)? Funciona igual: en la primera sesión pide a la IA que haga el inventario. Clasificará cada archivo como **fuente de información** (se queda donde está, se lista en `project.md`) o como **entregable a adoptar** (se le crea spec por ingeniería inversa, el archivo pasa a `docs/` y su spec a `.sdf/docs/<id>/`). Ver "Proyecto con contenido preexistente" en `AGENTS.md`.

## Qué hay aquí

| Ruta | Qué es |
|------|--------|
| `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` (raíz) | Adaptador de la herramienta de IA en uso: puntero delgado que activa `.sdf/AGENTS.md`. |
| `docs/` | Los documentos gobernados, PLANOS (`<id>.<ext>`), más su README. Nada más: la carpeta que la gente navega. |
| `wiki/` | Wiki de conocimiento del proyecto: páginas legibles por comunidad interconectadas con enlaces clicables a páginas y archivos. Núcleo fijo (Personas, Empresas, Bienes/recursos, Entregables/metas, Reuniones, Correos) + extensiones activables por proyecto (Lugares, Decisiones, Conceptos, Riesgos, Normas, Bitácora semanal). La IA la mantiene sola al cierre de cada cambio; correos y reuniones se pueblan desde los conectores al pedir "sincroniza la wiki". |
| Raíz / subcarpetas propias | Archivos fuente: insumos y material de referencia. |
| `.sdf/AGENTS.md` | Reglas del flujo para cualquier IA. La pieza central. |
| `.sdf/project.md` | Contexto del proyecto (plantilla a diligenciar) + estampa de versión del framework. |
| `.sdf/MEMORY.md` | Memoria compacta de arranque (~80 líneas): la genera `/sdf-init`, la lee cada sesión al iniciar y se mantiene sola al cierre de cada cambio. |
| `.sdf/docs/<id>/` | Espejo de `docs/`: la `spec.md` y el historial `changes/` de cada documento. |
| `.sdf/specs/` | Las 12 plantillas del framework (spec-documento, proposal, tasks, design, entidad, reunion, correo, riesgo, bitacora, memoria, feedback, review) + `checklist.sh`. Solo plantillas: las specs reales viven en `.sdf/docs/<id>/`. |
| `.sdf/usage.csv` | (Derivado) Contador de consumo de tokens por documento, acción, agente y modelo; lo alimenta cada cierre. Resumen en `/sdf-status`. |
| `.sdf/FRAMEWORK-FEEDBACK.md` | Log de propuestas de mejora del framework (lo crea la IA al primer hallazgo; se procesa con `/sdf-feedback`). |
| `.sdf/REVIEW.md` | Cola de revisión: contradicciones entre fuentes, entidades dudosas y relaciones fuera de vocabulario que la IA no resuelve sola (lo crea al primer hallazgo). No bloquea cierres; se reporta en `/sdf-status` y `/sdf-lint`. |
| `graphify-out/` | (Opcional, derivado) Índice de fuentes generado por el usuario con graphify en su máquina; el framework solo lo consume para localizar datos en fuentes crudas. |
| `.claude/agents/` | Subagentes del framework: `wiki-graph` (Sonnet, mantiene la wiki), `ingestor-fuentes` (Haiku, lee crudo y devuelve destilado), `auditor` (Sonnet, solo lectura: checklist/status/lint) y `evaluator` (Sonnet, contexto limpio: juzga los entregables antes del cierre). |
| `.claude/commands/` | Comandos slash del framework (SDF = Spec Driven Framework), ver abajo. |

## Comandos

| Comando | Qué hace |
|---------|----------|
| `/sdf-init` | Inicializa el proyecto: entrevista para `project.md`, inventario de contenido existente, wiki inicial. |
| `/sdf-graph [full]` | Refresca la wiki en modo delta; con `full`, reconstrucción completa. |
| `/sdf-sync` | Sincroniza correos y reuniones desde los conectores de correo/calendario. |
| `/sdf-status` | Reporte de salud: cambios abiertos, huérfanos, wiki al día. Solo lectura. |
| `/sdf-lint` | Revisión de calidad de la wiki: contradicciones, páginas huérfanas, enlaces rotos, datos obsoletos. |
| `/sdf-close` | Cierra los cambios que quedaron con Estado: en curso. |
| `/sdf-adopt <archivo>` | Adopta un archivo existente como entregable gobernado con su spec. |
| `/sdf-feedback` | Revisa propuestas de mejora del framework acumuladas y las aplica al skill (dueño del framework). |
| `/sdf-help` | Guía rápida de todos los comandos. |

Los comandos son atajos: todo se puede pedir igual en lenguaje natural ("inicializa el framework", "refresca la wiki"). En Claude Desktop/Cowork no aparecen en el autocompletado del prompt (eso es de Claude Code CLI), pero funcionan igual al escribirlos: el adaptador de la raíz instruye a la IA para reconocer cualquier mensaje que empiece con `/sdf-` y ejecutar el comando correspondiente.

## Actualizar el framework en un proyecto existente

Cuando el framework evolucione y quieras llevar la versión nueva a un proyecto que ya está andando:

1. Lo más fácil: dile al skill SDF *"actualiza el framework de esta carpeta"* (o usa el SDF Manager, que detecta proyectos desactualizados y aplica las migraciones con vista previa y rollback). Manual: reemplaza solo los archivos del framework — `.sdf/AGENTS.md`, `.sdf/README.md`, `.sdf/specs/` completa (solo contiene plantillas), el adaptador de la raíz, la carpeta `.claude/` completa, y los `README.md` de `docs/` y `wiki/` (+ `CLAUDE.md` de `wiki/`).
2. **No toques** lo que contiene tu trabajo: `.sdf/project.md` (ya diligenciado), tus documentos en `docs/`, sus specs e historiales en `.sdf/docs/<id>/`, `.sdf/MEMORY.md` ni las páginas ya creadas en `wiki/`.
3. Abre una sesión en ese proyecto y di: *"Actualicé el framework a la versión nueva: reconcilia el proyecto"*. La IA correrá `/sdf-status`, completará lo que la versión nueva espera y te propondrá activar extensiones si aplican.

## Economía de créditos (guía rápida)

El framework ya optimiza lo suyo (memoria compacta, zoom, deltas, cierre paralelo con script, Haiku para ingesta). Los hábitos del usuario multiplican el ahorro:

1. **Sesión en Sonnet** para el trabajo documental diario (el mayor ahorro individual; Opus solo para tareas puntuales que lo ameriten).
2. **Una tarea = una sesión**: cierra la conversación al cerrar el documento — el historial largo se re-cobra en cada turno; MEMORY repone el contexto por ~1.000 tokens.
3. **Poda plugins y conectores** que no uses (Configuración de Claude): cada uno inyecta su peaje en todas las sesiones.
4. **No pegues archivos al chat**: déjalos en la carpeta; el framework los lee selectivamente.

## Beneficios

- Un documento = un archivo + una spec. Sin `_v2_final_FINAL`.
- La carpeta que ve la gente está limpia: documentos en `docs/`, conocimiento en `wiki/`; el andamiaje (specs, historiales, memoria, plantillas) vive oculto en `.sdf/`.
- El historial y el porqué de cada documento viven junto a su spec, no en la memoria de nadie.
- Cualquier IA (o persona) puede retomar el proyecto y regenerar o modificar documentos con contexto completo.
- La wiki `wiki/` da una vista de conocimiento del proyecto navegable por humanos, y es compatible con [graphify](https://github.com/Graphify-Labs/graphify) para quien quiera el grafo visual interactivo.
