---
name: sdf-adopt
description: Adopta un archivo existente como entregable gobernado (spec por ingenieria inversa)
---

Adopta el archivo indicado (o pregunta cuál, listando candidatos de la raíz/subcarpetas) según el paso 0.1 del módulo `.sdf/reglas/flujo.md`:

1. Lee el archivo (delegar la lectura y el borrador de spec al subagente `ingestor-fuentes` si el archivo es extenso) y propone al usuario: id en kebab-case, propósito y audiencia detectados.
2. Crea la carpeta espejo `.sdf/docs/<id>/` y dentro el cambio `.sdf/docs/<id>/changes/AAAA-MM-DD-adoptar-<id>/` (proposal + tasks).
3. Crea la spec por ingeniería inversa en `.sdf/docs/<id>/spec.md`: estructura y contenido ACTUALES, sección por sección/hoja/slide; en Decisiones, anota que nació fuera del flujo.
4. Mueve el archivo a `docs/<id>.<ext>` (plano, sin subcarpeta) y regístralo en Documentos activos de `.sdf/project.md`.
5. Quítalo de Fuentes de información en `.sdf/project.md` si estaba listado ahí.
6. Cierra el cambio completo (wiki y MEMORY delta + evaluación independiente si aplica + checklist + Estado: cerrado).
