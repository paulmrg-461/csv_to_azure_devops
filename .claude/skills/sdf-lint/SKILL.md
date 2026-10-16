---
name: sdf-lint
description: Revision de calidad de la wiki - vigencia de hechos, contradicciones, vocabulario, huerfanas
---

Pasada de salud sobre `wiki/` (inspirada en la operación "lint" del patrón LLM Wiki). Delegar la detección al subagente `auditor` si está disponible. Busca y reporta:

1. **Hechos sin sellar:** líneas de la sección "Hechos" sin `desde` o sin enlace a fuente; datos datables (cargos, tarifas, estados, cifras, vigencias) que siguen sueltos en la prosa del Resumen y deberían bajar a "Hechos". Páginas de la convención anterior (sin sección "Hechos") se actualizan en modo delta a medida que se tocan — reportarlas, no reescribir la wiki entera.
2. **Contradicciones** entre páginas o contra las specs (fechas, roles, cifras que no cuadran). Por cada una, proponer una de las tres salidas de "Hechos, vigencia y contradicciones" del módulo `.sdf/reglas/wiki.md` — sucesión, coexistencia o rechazo — con su razón. Lo que no se pueda decidir sin el usuario va a `.sdf/REVIEW.md`, no se adivina.
3. **Intervalos mal formados:** dos hechos del mismo tipo `vigente` a la vez en una misma página; `hasta` anterior a `desde`; `hasta vigente` sostenido por una fuente que otra posterior ya superó; fechas inventadas con más precisión que la fuente.
4. **Relaciones fuera de vocabulario:** relaciones genéricas (`relacionado con`, `asociado a`) o términos que no están ni en el vocabulario cerrado del módulo `.sdf/reglas/wiki.md` ni en la línea "Relaciones de la wiki" de `.sdf/project.md`. Proponer el reemplazo del vocabulario, o llevar el término a `.sdf/REVIEW.md` para que el usuario lo apruebe.
5. **Entidades posiblemente duplicadas:** páginas de nombre, sigla o alias parecidos que podrían ser la misma entidad. NUNCA fusionar por cuenta propia: proponer la fusión al usuario o dejarla en `.sdf/REVIEW.md`.
6. **Páginas huérfanas:** sin ningún enlace entrante desde otras páginas ni desde INDEX.md.
7. **Enlaces rotos:** enlaces markdown a páginas o archivos que no existen.
8. **Entidades faltantes:** conceptos mencionados repetidamente en varias páginas que merecen página propia.
9. **Conocimiento sin destilar:** temas repetidos en varias páginas que merecen página propia o entrada en MEMORY; entradas de `MEMORY.md` obsoletas, vencidas o que exceden el tope.
10. **INDEX.md desalineado:** páginas que existen pero no están en el índice, o al revés.
11. **Cola de revisión:** entradas `pendiente` de `.sdf/REVIEW.md` (si existe), con su antigüedad. Recordar al usuario que decidir una entrada libera conocimiento que hoy está congelado. No son bloqueantes.

Presenta los hallazgos clasificados (bloqueante/menor) y pide confirmación antes de corregir. Las correcciones se delegan al subagente `wiki-graph`.

Al terminar: registra el consumo de esta acción en `.sdf/usage.csv` (acción `lint`; subagentes medidos por sus notificaciones, orquestador estimado — ver "Contabilidad de tokens" en el módulo `modelos-y-delegacion.md`).
