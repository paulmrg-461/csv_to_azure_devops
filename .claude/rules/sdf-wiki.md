---
paths: wiki/**
---

# Reglas de wiki/ (carga automática al trabajar aquí)

1. Comunidades permitidas: el núcleo fijo (personas, empresas, bienes-recursos, entregables-metas, reuniones, correos) más las extensiones ACTIVAS listadas en "Comunidades de la wiki" de `.sdf/project.md` (catálogo: lugares, decisiones, conceptos, riesgos, normas, bitacora). Cualquier otra, ÚNICAMENTE con permiso explícito del usuario.
2. Modo DELTA: toca solo las páginas afectadas por el cambio actual. Nunca re-escanees todo salvo orden explícita de reconstrucción.
3. Actualiza `INDEX.md` en CADA modificación (directorio + fecha).
4. Plantillas según comunidad (en `.sdf/specs/`): `entidad.md` (personas, empresas, bienes-recursos, entregables-metas, lugares, decisiones, conceptos, normas), `reunion.md`, `correo.md`, `riesgo.md`, `bitacora.md`.
4.1. **Hechos sellados:** lo que cambia con el tiempo va en la sección "Hechos" con `desde` / `hasta` / enlace a la fuente. Un hecho NUNCA se sobrescribe: se cierra el viejo con `hasta` y se abre otro debajo. Sin fuente no hay hecho, y un `desde` desconocido se escribe `desde desconocido` — no es un intervalo abierto.
4.2. **Relaciones del vocabulario cerrado** de `.sdf/AGENTS.md` (+ las registradas en `project.md`). Si ninguna encaja, no inventes una genérica: descríbelo en "Notas e historial" y anota el término propuesto en `.sdf/REVIEW.md`.
4.3. **Alias:** antes de crear una página, busca el nombre entre los `**Alias:**` existentes (`grep -i`) y escribe allí si coincide. Ante duda de si dos páginas son la misma entidad, NO fusiones: anótalo en `.sdf/REVIEW.md`.
4.4. **Contradicción entre fuentes:** elige explícitamente sucesión, coexistencia o rechazo (ver AGENTS.md); si no puedes decidir sin el usuario, va a `.sdf/REVIEW.md` y el trabajo sigue. Las pendientes no bloquean cierres.
5. Prosa breve y legible; slugs kebab-case; reuniones y correos con prefijo de fecha `AAAA-MM-DD-`. TODOS los enlaces en markdown relativo CLICABLE: entre páginas `[Nombre](../comunidad/slug.md)`; a archivos `[<id-doc>.docx](../../docs/<id-doc>.docx)` o `[fuente](../../subcarpeta/archivo.pdf)`; a specs `[spec](../../.sdf/docs/<id-doc>/spec.md)`. Nunca rutas en texto plano ni wikilinks `[[...]]`; si encuentras wikilinks de la convención vieja, conviértelos.
6. NUNCA copies cuerpos completos de correos: solo resumen y metadatos, respetando la confidencialidad de `.sdf/project.md`.
7. Si es posible, delega la escritura al subagente `wiki-graph` (Sonnet).
8. En `decisiones/`: si la decisión nació en el cambio de un documento, la página solo resume y ENLAZA a la spec — el detalle vive allá.
