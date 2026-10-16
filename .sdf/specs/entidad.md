# <Nombre de la entidad>

- **Comunidad:** personas | empresas | bienes-recursos | entregables-metas | <extensión activa: lugares, decisiones, conceptos, normas>
- **Alias:** <otros nombres, siglas o grafías con que aparece esta entidad, separados por coma; eliminar la línea si no aplica>
- **Actualizado:** AAAA-MM-DD

> Para reuniones y correos usar `reunion.md` y `correo.md`; para riesgos, `riesgo.md`; para la bitácora semanal, `bitacora.md`.

## Resumen

<2-5 frases legibles: qué o quién es, y por qué importa en este proyecto. Prosa, no volcado de datos — los datos van en "Hechos".>

## Hechos

<Lo que puede cambiar con el tiempo: cargos, tarifas, estados, vigencias, cifras. Un hecho por línea, con su vigencia y su origen.
REGLA: un hecho NO se sobrescribe. Cuando cambia, se CIERRA el viejo (poniéndole `hasta`) y se abre otro debajo; la línea vieja se queda.
Fechas a la precisión que se sepa (AAAA, AAAA-MM o AAAA-MM-DD). `desde desconocido` cuando no consta — un inicio desconocido NO es un intervalo abierto.
`hasta vigente` solo si consta que sigue vigente. Ver "Hechos, vigencia y contradicciones" en `.sdf/AGENTS.md`. Eliminar la sección si la entidad no tiene hechos datables.>

- <hecho actual> · desde AAAA-MM · hasta vigente · [fuente](../../<subcarpeta>/<archivo>)
- <hecho anterior, ya cerrado> · desde AAAA-MM · hasta AAAA-MM · [fuente](../../<subcarpeta>/<archivo>)

## Relaciones

<Enlaces tipados y CLICABLES hacia otras páginas (markdown relativo desde esta página): la relación + el enlace.
La relación se toma del VOCABULARIO CERRADO de `.sdf/AGENTS.md`, más las que el proyecto haya registrado en `project.md`.
Si ninguna encaja, NO inventes una genérica ("relacionado con"): deja el vínculo descrito en "Notas e historial" y anota el término propuesto en `.sdf/REVIEW.md`.>

- <trabaja en | responsable de | depende de | regulado por | ...>: [<Nombre>](../<comunidad>/<slug>.md) — <contexto breve>

## Aparece en

<Dónde se menciona esta entidad, con enlaces clicables a los archivos (rutas relativas: los docs y fuentes están dos niveles arriba).>

- [<id-doc>.<ext>](../../docs/<id-doc>.<ext>) — <en qué contexto>
- [<archivo fuente>](../../<subcarpeta>/<archivo>) — <en qué contexto>

## Notas e historial

- AAAA-MM-DD — <hecho relevante, decisión o cambio que involucra a esta entidad>
