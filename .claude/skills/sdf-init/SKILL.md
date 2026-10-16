---
name: sdf-init
description: Inicializa el Spec Driven Framework en esta carpeta - entrevista, inventario y wiki inicial
---

Ejecuta la inicialización del proyecto siguiendo los pasos 0 y 0.1 del módulo `.sdf/reglas/flujo.md`, en este orden:

1. Verifica que `.sdf/project.md` sea plantilla (tiene `<placeholders>`). Si ya está diligenciado, informa y pregunta si el usuario quiere re-inicializar algo puntual.
2. Entrevista guiada (paso 0 del módulo `flujo.md`): deduce lo posible de la carpeta y la conversación; pregunta el resto en tandas cortas con opciones concretas; confirma el resumen antes de dar `project.md` por terminado.
3. Extensiones de la wiki: según la naturaleza del proyecto, propone cuáles activar del catálogo (lugares, decisiones, conceptos, riesgos, normas, bitacora — ver "Comunidades" en el módulo `.sdf/reglas/wiki.md`); registra las elegidas en la línea "Comunidades de la wiki" de `.sdf/project.md` y crea SOLO esas carpetas en `wiki/`.
4. Inventario de contenido preexistente (paso 0.1): recorre raíz y subcarpetas, propone la clasificación fuente vs. entregable-a-adoptar y espera confirmación del usuario. Si el usuario quiere acotar subcarpetas, respétalo. Si una subcarpeta contiene su propia `.sdf/` (o un `AGENTS.md` en su raíz, instalación v4 o anterior), es un sub-proyecto SDF anidado: regístralo como fuente especial (enlace a su `.sdf/project.md` y `.sdf/MEMORY.md`) y NO inventaríes su interior.
5. Adopta los entregables confirmados (spec por ingeniería inversa, cambio `adoptar-<id>` con cierre completo).
6. Construye la wiki inicial en `wiki/`: el subagente `ingestor-fuentes` lee y destila cada fuente por lotes; con ese destilado, el subagente `wiki-graph` escribe las páginas. El contenido crudo nunca pasa por el contexto principal.
7. Construye `.sdf/MEMORY.md` con la plantilla `.sdf/specs/memoria.md`, destilando project.md y la wiki inicial (máximo 80 líneas).
8. Ofrece sincronizar correo/calendario (`/sdf-sync`) y programarla como tarea recurrente. Si la extensión `bitacora` está activa, ofrece también programar el recap semanal.

Al final, muestra un resumen: project.md diligenciado, extensiones activadas, N fuentes registradas, N documentos adoptados, N páginas de wiki creadas, MEMORY.md creada.

Al terminar: registra el consumo de esta acción en `.sdf/usage.csv` (acción `init`; subagentes medidos por sus notificaciones, orquestador estimado — ver "Contabilidad de tokens" en el módulo `modelos-y-delegacion.md`).
