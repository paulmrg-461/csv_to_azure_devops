# Módulo: Memoria y aprendizaje continuo

Cárgalo al construir o consolidar `.sdf/MEMORY.md`, al registrar una corrección del usuario como aprendizaje permanente, o al ejecutar la pasada de conocimiento de `sdf-lint`. El núcleo ya dice CUÁNDO se toca la memoria dentro del cierre; este módulo cubre CÓMO.

## Memoria del proyecto (.sdf/MEMORY.md)

`.sdf/MEMORY.md` es la memoria compacta de arranque: el mapa del mapa. Cada sesión la lee al inicio para heredar en ~800 tokens lo esencial del proyecto. Reglas:

- **Contenido:** qué es el proyecto (3 frases), estado actual (qué se trabaja, qué viene), decisiones vigentes que moldean el trabajo (con enlace al detalle), 10-15 entidades clave (una línea + enlace a su página), y aprendizajes/preferencias del usuario. La jerga NO va aquí: vive en el Glosario de `project.md`. Plantilla: `.sdf/specs/memoria.md`.
- **Tope duro: 80 líneas.** Cuando se llene NO se agranda: se CONSOLIDA — fusionar entradas, podar lo obsoleto, empujar el detalle a las páginas de la wiki (la memoria extendida). Registrar la fecha de última consolidación en su cabecera.
- **Mantenimiento delta:** se actualiza como parte del cierre de cada cambio (junto con la wiki, mismo subagente). Solo se toca lo que cambió: estado actual, decisión nueva, entidad nueva relevante, aprendizaje.
- **Se genera, no se instala:** la crea `sdf-init` (a partir de `project.md` y la wiki inicial) y la regenera `sdf-graph full`. Si no existe en un proyecto en marcha, crearla en el próximo cierre.
- **Enlaces relativos a `.sdf/`:** MEMORY vive en `.sdf/`, así que sus enlaces a la wiki llevan `../` (`../wiki/decisiones/<slug>.md`) y los enlaces a specs son directos (`docs/<id>/spec.md`, porque `.sdf/docs/` es su vecina).
- Ante discrepancia, mandan las specs y las páginas de la wiki: MEMORY es un índice de acceso rápido, no la fuente de verdad.

## Aprendizaje continuo (volverse experto en el proyecto)

El objetivo es que la expertise quede COMPILADA en archivos que toda sesión futura hereda, no en la memoria de una conversación. Tres mecanismos, ejecutados en el cierre de cada cambio:

1. **Descubrimientos:** preguntarse "¿qué aprendí trabajando esto que la wiki no sabía?" — un dato, una relación, un matiz del negocio. Destilarlo: página nueva o actualizada (usar `conceptos/` si la extensión está activa — ver módulo `wiki.md`), término nuevo al glosario de `project.md`, o línea en MEMORY si es estructural.
2. **Correcciones del usuario:** cuando el usuario corrija tono, formato, criterio o contenido, esa preferencia NO se queda en la conversación: registrarla en los Estándares de `project.md` (si es transversal) o en la spec del documento (si es puntual), y en "Aprendizajes" de MEMORY si conviene tenerla siempre presente. El siguiente documento debe nacer ya corregido.
3. **Consolidación periódica:** `sdf-lint` incluye una pasada de conocimiento — detectar temas repetidos en varias páginas que merecen destilarse, y entradas de MEMORY obsoletas o vencidas.
