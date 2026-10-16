---
name: sdf-feedback
description: Revisa las propuestas de mejora del framework acumuladas en el proyecto y aplicalas a la fuente canonica del skill SDF (flujo del dueno del framework)
---

Flujo de mejora continua del framework (ver sección "Mejora continua del framework" en el módulo `.sdf/reglas/flujo.md`):

1. Lee `.sdf/FRAMEWORK-FEEDBACK.md`. Si no existe o no tiene entradas pendientes, informa y termina.
2. Presenta las propuestas pendientes agrupadas por regla/archivo implicado, cada una con: síntoma observado, mejora propuesta, y tu análisis honesto de si vale la pena (algunas serán ruido — dilo).
3. Para las que el usuario apruebe: se aplican SOLO en la fuente canónica del skill SDF — la carpeta donde vive su `SKILL.md` con sus `assets/` (p. ej. `SDF-Skill/sdf/`), esté donde esté. Si no está conectada a la sesión, pide conectarla. NUNCA edites las reglas del framework dentro del proyecto.
4. Tras aplicar: marca las entradas como `Estado: aplicado (AAAA-MM-DD)` en `.sdf/FRAMEWORK-FEEDBACK.md`, y recuerda al usuario re-empaquetar el skill (package_skill sobre la carpeta del skill) y redistribuir el `.skill` — los proyectos existentes se ponen al día con "actualiza el framework".
5. Si quien corre el comando no es el dueño del framework: solo consolida el log y ofrécele exportarlo para enviárselo al dueño.
