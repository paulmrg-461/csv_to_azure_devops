---
name: sdf-status
description: Reporte de salud del proyecto - cambios abiertos, huerfanos, wiki al dia, curva de consumo
---

Genera un reporte de salud del framework SIN modificar nada:

Delegar la auditoría al subagente `auditor` si está disponible (auditoría tipo "salud del proyecto").

1. **Cambios abiertos:** proposals con `Estado: en curso` en `.sdf/docs/*/changes/*/`, con su antigüedad.
2. **Huérfanos:** carpetas `.sdf/docs/<id>/` sin `spec.md` o sin documento correspondiente `docs/<id>.<ext>`; documentos en `docs/` sin carpeta espejo en `.sdf/docs/`; subcarpetas de documento residuales dentro de `docs/` (estructura v4 sin migrar); specs con estado distinto de `obsoleto` cuyo documento no existe; tareas sin marcar en tasks.md de cambios cerrados.
3. **project.md (`.sdf/project.md`):** ¿tabla de Documentos activos coincide con los documentos de `docs/` y sus carpetas espejo de `.sdf/docs/`? ¿quedan `<placeholders>`?
4. **Wiki:** documentos de `docs/` sin página en `entregables-metas/`; fecha de última actualización y última sincronización de correo/calendario en `INDEX.md`.
5. **Memoria:** ¿existe `.sdf/MEMORY.md`? ¿respeta el tope de 80 líneas? ¿fecha de última consolidación razonable? ¿su estado actual refleja los últimos cambios cerrados?
6. **Cola de revisión (`.sdf/REVIEW.md`, si existe):** entradas con `Estado: pendiente`, agrupadas por tipo (contradicción, entidad dudosa, relación fuera de vocabulario) y con su antigüedad. No son bloqueantes; se listan para que el usuario decida.
7. **Feedback del framework:** entradas con `Estado: pendiente` en `.sdf/FRAMEWORK-FEEDBACK.md` (si existe) — recordar al dueño que las revise con `/sdf-feedback`.
8. **Índice de fuentes (opcional):** si existe `graphify-out/graph.json`, informa su fecha y si quedó más viejo que las fuentes recientes (sugerir regenerarlo desde la máquina del usuario); si no existe, NO es un problema — es un acelerador opcional.
9. **Sub-proyectos anidados (informativo):** subárboles con `.sdf/` propio (o `AGENTS.md` en su raíz, v4 o anterior) — ¿están registrados como fuente especial en `.sdf/project.md`? No auditar su interior (cada uno se audita con su propio /sdf-status).
9.1. **Sub-arneses de desarrollo (informativo, `sdf-dev`):** subcarpetas de primer nivel con `.sdf-dev.json` — lee SOLO ese archivo (nunca el código, specs o tareas del sub-arnés) y reporta, por cada uno: framework y versión, `estado_cli` (`disponible`/`pendiente`/`degradado` — si es `pendiente` o `degradado`, señálalo: falta completar la instalación real de la herramienta), herramientas de IA proyectadas, y si tiene página en `wiki/entregables-metas/` (`padre.pagina_wiki`) — si no la tiene, sugerir `/sdf-graph` para crearla.
10. **Fuentes:** rutas de Fuentes de información de `.sdf/project.md` y rutas citadas en la wiki (`Aparece en`, `Transcripción:`) que ya no existan en disco (archivos movidos/renombrados); archivos y subcarpetas presentes en el árbol pero no registrados como fuentes.

11. **Curva de consumo (`.sdf/usage.csv`, si existe) — calculada con bash/awk, NUNCA leyendo el CSV a ojo (lo mecánico primero, 0 tokens):**
    - Total de los últimos 30 días y top 5 documentos/acciones más costosos: `awk -F, -v d="$(date -d '-30 days' +%F)" '$1>=d{t[$3]+=$6} END{for(o in t) print t[o], o}' .sdf/usage.csv | sort -rn | head -5`. Desglose por agente y modelo con el mismo patrón agrupando por `$4`/`$5`.
    - **% medido vs estimado:** sumar `$6` agrupado por `$7` (fuente) y calcular qué fracción es `medido`. Menos de la mitad medido es señal de que faltan notificaciones de subagente por registrar.
    - **Mediana móvil de tokens por cambio** (ventana de 5): sumar tokens por `objeto` (`awk -F, '{s[$3]+=$6} END{for(o in s) print o, s[o]}' .sdf/usage.csv`), ordenar por fecha de cierre de cada cambio, tomar la mediana de cada ventana de 5 consecutivos y comparar la más reciente contra la anterior (sube / baja / estable). Es la señal de si el costo por documento está mejorando con el tiempo o empeorando.
    - **Arranque medido:** mediana de las últimas 10 líneas con `accion=arranque` (`awk -F, '$2=="arranque"{print $6}' .sdf/usage.csv | tail -10 | sort -n`, mediana de esa lista), comparada contra el objetivo ≤ 4.000 tokens de la sección "Módulos de reglas" del núcleo. Si no hay ninguna línea `arranque` todavía, dilo explícitamente — significa que las sesiones no lo están registrando (ver módulo `modelos-y-delegacion.md`, "Contabilidad de tokens"), no que el arranque sea gratis.
    - **Excesos de presupuesto:** para los cambios `Estado: cerrado`, comparar el campo `Presupuesto:` de su `proposal.md` contra `Tokens:` registrado. Listar los que se pasaron; si la misma causa se repite 3 veces seguidas, es un hallazgo para `.sdf/FRAMEWORK-FEEDBACK.md` (ver núcleo, "Velocidades de cierre").
    - Todo esto es **demostrable con la carpeta real del usuario**, no con una cifra teórica del plan del framework: si `usage.csv` no existe todavía o tiene pocas filas, repórtalo así — "sin datos suficientes para la curva" — en vez de rellenar con estimaciones inventadas.

Presenta el resultado como reporte breve con veredicto (sano / atención / requiere cierre) y, si hay problemas, ofrece corregirlos (`/sdf-close` para cambios abiertos, `/sdf-graph` para wiki desactualizada).
