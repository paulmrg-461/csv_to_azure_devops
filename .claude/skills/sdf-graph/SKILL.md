---
name: sdf-graph
description: Refresca la wiki de wiki/ (delta por defecto; usar "full" para reconstruccion completa)
---

Refresca la wiki `wiki/` según el módulo `.sdf/reglas/wiki.md`. Si te indican `full`, hace reconstrucción completa; sin argumento, hace delta.

- Sin argumento (delta): detecta qué cambió desde la última actualización registrada en `wiki/INDEX.md` — documentos en `docs/` sin página o con spec más reciente que su página, fuentes registradas en `.sdf/project.md` sin indexar — y actualiza SOLO esas páginas. Delega la escritura al subagente `wiki-graph`.
- Siempre (delta y full): los subárboles con `.sdf/` propio — o `AGENTS.md` en su raíz, si son instalaciones v4 o anteriores — son sub-proyectos SDF (caja negra): si aparece uno nuevo, registrarlo como fuente especial y ejecutar el protocolo de TRASPASO del módulo `.sdf/reglas/anidados.md` (ceder las fuentes internas del subárbol, anotar la cesión en las páginas del padre que lo citaban, actualizar MEMORY). Jamás ingestar su interior. Luego ejecutar la "Reconciliación de fuentes" del módulo `wiki.md` — inventario del árbol con bash, detectar rutas rotas por archivos movidos o carpetas renombradas (reparar rutas en `.sdf/project.md` y wiki sin re-ingestar), y listar archivos/subcarpetas nuevos proponiendo cuáles registrar e ingestar.
- Siempre (delta y full): las subcarpetas con `.sdf-dev.json` son sub-arneses de **desarrollo** (Spec Kit u OpenSpec, caja negra igual de estricta que un SDF anidado, pero con framework distinto): si aparece uno nuevo o cambió su `.sdf-dev.json`, crea o actualiza su página en `wiki/entregables-metas/<nombre-app>.md` (plantilla `entidad.md`: qué es, para quién, estado, framework, enlace a su `README.md` y a `archivo_gobernanza`) y actualiza el campo `padre.pagina_wiki` del propio `.sdf-dev.json` si hacía falta crearla. Excluir siempre de la reconciliación de fuentes (nunca listar sus archivos internos como "nuevos sin registrar") y jamás leer su código, specs o tareas — solo `README.md` y `archivo_gobernanza`.
- Con `full`: reconstrucción completa — re-escanea fuentes, `docs/` y specs, sincroniza correo/calendario si hay conectores, y regenera `wiki/` entero y `.sdf/MEMORY.md` (pide confirmación antes, indicando cuántos archivos implica).

Siempre, al escribir: los hechos datables van sellados (`desde` / `hasta` / enlace a fuente) y NUNCA se sobrescriben — se cierra el viejo y se abre el nuevo; las relaciones salen del vocabulario cerrado; antes de crear una página se busca el nombre entre los alias existentes. Lo que no se pueda decidir sin el usuario (contradicción, entidad dudosa, término fuera de vocabulario) va a `.sdf/REVIEW.md` y el refresco continúa. Ver "Hechos, vigencia y contradicciones" en el módulo `wiki.md`.

Siempre: actualizar `.sdf/MEMORY.md` en modo delta si hubo novedades (respetando su tope de 80 líneas; módulo `memoria-y-aprendizaje.md`) e `INDEX.md` (directorio + fecha de última actualización) y reportar páginas creadas/actualizadas y entidades que no encajaron en las comunidades.

Al terminar: registra el consumo de esta acción en `.sdf/usage.csv` (acción `graph`; subagentes medidos por sus notificaciones, orquestador estimado — ver "Contabilidad de tokens" en el módulo `modelos-y-delegacion.md`).
