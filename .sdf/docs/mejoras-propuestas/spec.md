# Spec: Mejoras propuestas de csv_to_azure_devops

- **Id:** mejoras-propuestas
- **Archivo:** `docs/mejoras-propuestas.md` ([abrir](../../../docs/mejoras-propuestas.md))
- **Formato:** Markdown (desviación declarada en `project.md`)
- **Estado:** vigente
- **Creado:** 2026-10-05
- **Última actualización:** 2026-10-05

## Propósito

Reunir, con archivo y línea, las mejoras propuestas a los scripts que suben Tasks a Azure DevOps y extraen work items: seguridad (manejo del PAT y de los datos enviados a la IA), correcciones, refactor, pruebas y funciones por terminar.

## Audiencia

El propietario de los scripts, que decide qué arreglar primero y qué eliminar.

## Requisitos

- El documento DEBE dar archivo y línea de cada hallazgo y marcar "no verificado" lo que depende de ejecución.
- Cada hallazgo DEBE llevar dónde, qué pasa, por qué importa, propuesta, esfuerzo, prioridad y riesgo de no hacerlo; con "Contra" cuando la propuesta lo tenga.
- El documento NO DEBE contener el valor de ningún PAT, clave de IA ni contraseña.
- El documento DEBE aclarar que las líneas de `upload_tasks_with_ai.py` y `tasks_bugs_extractor.py` son del árbol de trabajo (con cambios sin commitear).
- El documento NO DEBE analizar ni citar el contenido de `venv/`.

## Estructura y contenido

1. **Cabecera y resumen:** fecha, rama, alcance, conteo por categoría y prioridad, los tres hallazgos principales y el estado de los secretos.
2. **Seguridad (1-5):** PAT escrito en el código, datos enviados a DeepSeek, repo con `venv/` y estado de herramientas, permisos del PAT, datos de personas versionados.
3. **Correcciones (6-14):** resiliencia y duplicados, timeouts, respuestas no JSON, HTML sin escapar, lotes fallidos silenciosos, deriva de la guía, ID decimal, valores por defecto, prompt desactualizado.
4. **Refactor (15-18), Pruebas (19), Futuro (20-21).**
5. **Orden sugerido y no verificado.**

## Fuentes de datos

Lectura de los cinco scripts, `requirements.txt`, `.gitignore`, `.env.example`, la guía y las cabeceras de los archivos de datos el 2026-10-05 en la rama `main`. Comprobación sin impresión de que los valores de `.env` no aparecen en otros archivos. Contraste del prompt de la IA con `../bnb-auth`.

## Decisiones

- **2026-10-05 — No tocar los archivos con cambios sin commitear:** se leyeron y se citan líneas del árbol de trabajo; se descartó proponer cambios con diff porque cambiarían bajo los pies del propietario.
- **2026-10-05 — `venv/` solo se cuenta, no se analiza:** por indicación; el conteo sale de `git ls-files`.
- **2026-10-05 — No reescribir historial:** se recomienda lo contrario porque no se encontró un secreto en `venv/` ni en `.omc/` (tampoco se abrieron).

## Registro de cambios

| Fecha | Cambio (carpeta en changes/) | Resumen |
|-------|------------------------------|---------|
| 2026-10-05 | 2026-10-05-crear-mejoras-propuestas | Creación inicial |
