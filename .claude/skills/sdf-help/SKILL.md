---
name: sdf-help
description: Lista los verbos del framework SDF y para que sirve cada uno; con "guiado" ensena el flujo completo sobre un documento propio
---

Si te invocan con el argumento `guiado`, salta directo a la sección "Modo guiado" de abajo — no muestres primero la tabla completa. Sin argumento, muestra al usuario esta guía rápida (y confirma contra los skills instalados por si hay verbos adicionales):

| Verbo | Qué hace |
|---------|----------|
| `sdf-init` | Inicializa el proyecto: entrevista para `project.md`, extensiones de la wiki, inventario de contenido, wiki inicial y `MEMORY.md`. |
| `sdf-graph [full]` | Refresca la wiki y `MEMORY.md` en modo delta (con `full`: reconstrucción completa). Incluye reconciliación de fuentes movidas. |
| `sdf-sync` | Trae correos y reuniones del proyecto desde los conectores de correo/calendario (incluye transcripciones). |
| `sdf-status` | Reporte de salud (solo lectura): cambios abiertos, huérfanos, memoria, feedback pendiente, fuentes. |
| `sdf-lint` | Calidad de la wiki: contradicciones, huérfanas, enlaces rotos, datos obsoletos, conocimiento sin destilar. |
| `sdf-close` | Cierra los cambios que quedaron con Estado: en curso (incluye evaluación independiente si aplica). |
| `sdf-adopt <archivo>` | Adopta un archivo existente como documento gobernado (documento plano en docs/ + spec espejo en .sdf/docs/<id>/). |
| `sdf-feedback` | Revisa propuestas de mejora del framework y las aplica al skill (dueño del framework). |
| `sdf-migrate` | Completa los pasos pendientes de una migración del framework — de `.sdf-migracion/` (SDF Manager) o, si no hay, del manifiesto del arnés cuando esté accesible. |
| `sdf-help` | Esta guía. |

Recuerda: todo se puede pedir igual en lenguaje natural; las reglas completas viven en `.sdf/AGENTS.md` (núcleo) y sus módulos en `.sdf/reglas/`. Cómo se invoca cada verbo depende de la herramienta (`/sdf-<verbo>` en Claude Code y Antigravity, `$sdf-<verbo>` en Codex) — usa la sintaxis de la sesión actual.

## Modo guiado

Objetivo: que un usuario nuevo termine la sesión (~15 minutos) habiendo hecho el ciclo completo UNA vez, con un documento suyo de verdad — no un ejemplo de juguete. No es un verbo aparte: es este mismo skill enseñando mientras trabaja.

1. **No empieces preguntando teoría.** Pregunta directo: "¿qué documento de oficina necesitas ahora mismo — uno nuevo, o uno que ya tengas y quieras que gobierne el framework?". Si no tiene ninguno en mente, sugiere algo pequeño y real de su propio contexto (un documento que haya mencionado, algo de la carpeta) — nunca "un informe de ejemplo" genérico.
2. **Si `.sdf/project.md` sigue siendo plantilla**, la entrevista de `sdf-init` (paso 0 del módulo `.sdf/reglas/flujo.md`) es un prerrequisito — hazla, pero rápido: lo mínimo para arrancar (propósito, idioma, propietario), sin agotar cada campo opcional. Explica en una frase por qué existe `project.md` (contexto que no se vuelve a preguntar) antes de seguir.
3. **Ejecuta el flujo real sobre ESE documento** (crear uno nuevo o adoptar el existente, según lo que haya pedido — módulo `flujo.md` completo), narrando en 1-2 frases el PORQUÉ de cada paso a medida que ocurre, no antes: "esto es la spec — la fuente de verdad; el Word que ves después se genera a partir de ella, así que si algo no cuadra, se corrige aquí y se regenera, nunca se edita el Word a mano." No expliques subagentes, políticas de modelo ni contabilidad de tokens a menos que pregunte — eso es detalle de implementación, no parte del aprendizaje de hoy.
4. **Cierra el cambio de verdad** (checklist en dos capas incluido) y señala, cuando pase, el momento exacto en que la wiki y `MEMORY.md` se actualizaron solas — es el punto que más cuesta creer sin verlo.
5. **Cierra la sesión con el resumen del ciclo**, en una frase memorable: "proponer → generar → cerrar — así es cada documento de aquí en adelante, con o sin mí explicando." Señala `sdf-help` (sin argumento) como referencia para cuando necesite otro verbo, y sigue de largo si el usuario ya quiere seguir trabajando — el modo guiado no es una pantalla aparte que haya que "cerrar".

Si el usuario se desvía a una pregunta de fondo (por qué existe tal regla, qué pasa en tal otro caso), respóndela brevemente y vuelve al documento — el aprendizaje real ocurre haciendo, no en una explicación larga antes de empezar.
