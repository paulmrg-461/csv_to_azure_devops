# Módulo: Wiki del proyecto (wiki/)

Cárgalo cuando la tarea toque `wiki/` directamente: crear o actualizar una página, sincronizar correo/calendario, reconciliar fuentes movidas, o cualquier paso de cierre que escriba en la wiki. El núcleo (`.sdf/AGENTS.md`) ya cubre CUÁNDO se actualiza dentro del flujo de cierre; este módulo cubre CÓMO.

`wiki/` es una wiki de conocimiento del proyecto, legible por humanos y navegable como grafo: páginas markdown interconectadas con enlaces clicables que representan las entidades del proyecto y sus relaciones. Cualquier persona puede abrirla y entender quién es quién, qué recursos hay y cómo se conecta todo.

## Comunidades

Las páginas se organizan en comunidades de dos niveles: un **núcleo fijo** siempre presente y un **catálogo de extensiones** activables por proyecto.

**Núcleo (siempre presente, una carpeta por comunidad):**

| Comunidad | Contiene |
|-----------|----------|
| `personas/` | Personas: equipo, contactos, stakeholders |
| `empresas/` | Empresas, organizaciones, instituciones |
| `bienes-recursos/` | Bienes, activos, sistemas, presupuestos, materiales |
| `entregables-metas/` | Documentos generados (uno por doc de `docs/`), metas e hitos |
| `reuniones/` | Reuniones y sesiones de trabajo del proyecto (una página por reunión, `AAAA-MM-DD-<slug>.md`) |
| `correos/` | Hilos de correo relevantes al proyecto (una página por hilo, `AAAA-MM-DD-<slug-asunto>.md`, fecha del último mensaje) |
| `proyectos-relacionados/` | Carpetas hermanas y sub-proyectos SDF anidados detectados por la reconciliación de fuentes (módulo `anidados.md`) — una página por sub-proyecto, plantilla `entidad.md` |

**Extensiones (catálogo opcional):** se eligen durante `sdf-init` — o después, cuando el usuario lo pida — según la naturaleza del proyecto. Al activar una: registrarla en `.sdf/project.md` (Convenciones, línea "Comunidades de la wiki"), crear su carpeta y su sección en `INDEX.md`. NO crear carpetas de extensiones no activadas.

| Extensión | Contiene | Plantilla |
|-----------|----------|-----------|
| `lugares/` | Sitios físicos: sedes, clínicas, obras, ciudades | `entidad.md` |
| `decisiones/` | Decisiones transversales o estratégicas. Regla anti-duplicación: si la decisión nació en el cambio de un documento, la página solo resume y ENLAZA a la spec (el detalle vive allá); el detalle completo solo va aquí cuando la decisión no pertenece a ningún documento | `entidad.md` |
| `conceptos/` | Ideas, conceptos e insights del proyecto: nociones que se citan repetidamente, hallazgos, aprendizajes y conclusiones de análisis que valga la pena capitalizar (las buenas respuestas se archivan en la wiki) | `entidad.md` |
| `riesgos/` | Registro vivo de riesgos: probabilidad, impacto, dueño, mitigación, estado | `riesgo.md` |
| `normas/` | Leyes, estándares, regulaciones y contratos marco que restringen el proyecto | `entidad.md` |
| `bitacora/` | Recapitulaciones semanales (`AAAA-Wnn.md`). Contenido DERIVADO de la wiki y los cambios cerrados: se genera bajo demanda ("recap de la semana") o como tarea programada; ante discrepancia, mandan las specs y las páginas de entidades | `bitacora.md` |

Fuera del núcleo y de las extensiones del catálogo, no crear comunidades sin permiso explícito del usuario; si el usuario acepta una totalmente nueva, registrarla en `project.md`.

## Reglas de las páginas

- Una página `.md` por entidad, en su comunidad, con slug en kebab-case: `wiki/personas/ana-lopez.md`.
- Plantillas (en `.sdf/specs/`): `entidad.md` para personas, empresas, bienes-recursos, entregables-metas, proyectos-relacionados y extensiones lugares/decisiones/conceptos/normas; `reunion.md`, `correo.md`, `riesgo.md` y `bitacora.md` para sus comunidades. Prosa breve y legible, NO volcados de datos.
- **Alias:** toda página que tenga otros nombres, siglas o grafías los lista en su línea `**Alias:**` de la cabecera. Es lo que hace mecánica la identificación de entidades: antes de crear una página nueva, buscar el nombre entre los alias de las existentes (`grep -i`) y escribir allí si coincide, en vez de duplicar.
- **Hechos:** lo que cambia con el tiempo NO va en la prosa del resumen sino en la sección "Hechos" de la página, sellado con vigencia y fuente (ver "Hechos, vigencia y contradicciones").
- **Todos los enlaces son markdown relativos y CLICABLES** (relativos a la ubicación de la página, que vive en `wiki/<comunidad>/`):
  - Entre páginas de la wiki, con relación tipada: `trabaja en [Acme](../empresas/acme.md)`, `responsable de [Plan piloto](../entregables-metas/plan-piloto.md)`.
  - Hacia documentos y fuentes del proyecto: `[plan-piloto.docx](../../docs/plan-piloto.docx)`, `[contrato marco](../../contratos/2026/msa-acme.pdf)`, `[transcripción](../../transcripciones/2026-07-20-kickoff.txt)`.
  - Hacia specs e historiales: `[spec](../../.sdf/docs/plan-piloto/spec.md)`. Nota: los visores que ignoran carpetas ocultas (Obsidian) no abren estos enlaces a `.sdf/`; los documentos y fuentes sí abren siempre. Costo aceptado de mantener la raíz limpia — la spec se abre desde el editor o desde la sesión de IA.
  - NUNCA rutas en texto plano ni wikilinks `[[...]]`. Las wikis creadas con la convención anterior (wikilinks) se convierten a enlaces markdown en la siguiente pasada de `sdf-graph` o `sdf-lint`.
- Cada documento de `docs/` tiene su página en `entregables-metas/` que enlaza (clicable) al archivo y a su spec, y resume qué es y a quién involucra.
- `INDEX.md` es la portada: directorio de todas las páginas por comunidad, cada entrada como enlace clicable (`[Acme](empresas/acme.md)`) con una línea de resumen. Mantenerlo SIEMPRE al día.

## Hechos, vigencia y contradicciones

La wiki no solo dice qué son las entidades: dice **desde cuándo** y **por qué lo creemos**. Los datos que cambian con el tiempo (cargos, tarifas, estados, cifras, vigencias) van en la sección "Hechos" de la página, un hecho por línea, con su intervalo y su fuente:

```
- <hecho> · desde AAAA-MM · hasta vigente · [fuente](../../<ruta>)
```

Reglas, en orden de importancia:

1. **Un hecho con vigencia NUNCA se sobrescribe.** Cuando cambia, se CIERRA el viejo (poniéndole la fecha en `hasta`) y se abre otro debajo; la línea vieja se queda en la página con su intervalo y su fuente. Reescribir el valor en su sitio destruye justamente lo que hace auditable a la wiki.
2. **Precisión honesta.** La fecha va a la precisión que se sepa: `2026`, `2026-08` o `2026-08-14`. Nunca inventar el día para que la línea quede pareja.
3. **Un inicio desconocido no es un intervalo abierto.** Si no consta desde cuándo, se escribe `desde desconocido`; poner la fecha en que lo leímos afirma algo que la fuente no dice. Igual con el cierre: `hasta vigente` solo si consta que sigue vigente; si simplemente no se sabe, `hasta desconocido`.
4. **Sin fuente no hay hecho.** Todo hecho lleva enlace a lo que lo sostiene (documento, archivo fuente, página de reunión o de correo). Lo que no se puede sustentar va a "Notas e historial" como observación, no a "Hechos".

**Cuando dos fuentes se contradicen** hay exactamente tres salidas, y hay que elegir una explícitamente — nunca dejar que gane la que llegó de último:

| Salida | Cuándo aplica | Qué se hace |
|--------|---------------|-------------|
| **Sucesión** | El mundo cambió: el hecho nuevo reemplaza al viejo a partir de una fecha | Cerrar el viejo con `hasta`, abrir el nuevo con `desde`. Es el caso común. |
| **Coexistencia** | Ambos son ciertos en ámbitos distintos (dos contratos, dos filiales, dos productos) | Conservar los dos, precisando en cada línea el ámbito que los distingue. |
| **Rechazo** | Una de las fuentes es menos confiable y no hay razón para creerle | No escribir el hecho nuevo; anotar en "Notas e historial" que se descartó y por qué. |

Precedencia de fuentes cuando toca decidir: **documento firmado o publicado > documento de trabajo > correo > transcripción de reunión > lo que alguien recuerda**. Orienta, no decide sola: una transcripción reciente puede vencer a un contrato viejo si describe un cambio posterior.

**Si no se puede elegir sin el usuario, NO se adivina.** La entrada va a `.sdf/REVIEW.md` (plantilla `review.md`, se crea al primer hallazgo) con las dos versiones, sus fuentes y las opciones, y el trabajo continúa. También van ahí: entidades que podrían ser la misma pero sin certeza (antes de fusionar dos páginas), relaciones que no encajan en el vocabulario, fuentes de identidad o ruta ambigua, y comunidades nuevas que parecerían necesarias.

Las entradas pendientes se reportan al usuario en el cierre y en `sdf-status`, y **no bloquean un cierre**: la cola existe para que el trabajo siga sin inventar, no para frenarlo. Cuando el usuario decide, el conocimiento va a la página y la entrada pasa a "Resueltas".

## Vocabulario de relaciones

Las aristas de la wiki solo sirven si significan algo. Las relaciones se toman de este vocabulario cerrado:

| Grupo | Relaciones |
|-------|-----------|
| Personas y organizaciones | `trabaja en` · `dirige` · `pertenece a` · `contrata a` · `provee a` |
| Responsabilidad y participación | `responsable de` · `participa en` · `convocada por` · `involucra a` |
| Objetos y dependencias | `usa` · `depende de` · `sucede a` |
| Contexto y restricción | `regulado por` · `ubicado en` · `afecta a` |
| Temas tratados | `se trató` · `se discute` · `decide sobre` |

- **Ninguna relación es mejor que una vaga.** Si nada encaja, NO escribir `relacionado con` ni `asociado a`: describir el vínculo en prosa en "Notas e historial" y anotar el término propuesto en `.sdf/REVIEW.md`. Una relación genérica es una afirmación falsa disfrazada de dato; la ausencia solo es un hueco.
- **El proyecto puede ampliarlo.** Cuando el usuario aprueba un término propuesto, se registra en la línea "Relaciones de la wiki" de `.sdf/project.md` y desde ahí vale igual que las del núcleo. El vocabulario crece por confirmación, no por improvisación.
- Se escribe en palabras, delante del enlace: `- responsable de: [Plan piloto](../entregables-metas/plan-piloto.md) — desde el arranque.`

## Cuándo y cómo se actualiza (modo delta — nunca re-escanear todo)

1. **Al cerrar un cambio** (paso obligatorio del cierre): crear/actualizar la página del entregable en `entregables-metas/` y las páginas de las entidades que el documento menciona (solo las nuevas o las que cambiaron). Actualizar `INDEX.md`.
2. **Al registrar una fuente nueva** en `.sdf/project.md`: extraer sus entidades relevantes y crear/actualizar sus páginas.
3. **Sincronización con correo y calendario** — cuando el usuario lo pida ("sincroniza la wiki", "trae los correos/reuniones del proyecto") o como parte de una reconstrucción completa. Ver protocolo abajo.
4. **Reconstrucción completa** solo si el usuario la pide (ej. "reconstruye la wiki"): re-escanear fuentes, `docs/` y specs, sincronizar correo/calendario, y regenerar `wiki/` entero.

## Reconciliación de fuentes (archivos movidos, renombrados, carpetas nuevas)

Los archivos fuente viven donde el usuario quiera — raíz o subcarpetas a cualquier profundidad — y el usuario puede moverlos, renombrar carpetas o crear subcarpetas nuevas en cualquier momento. La identidad de una fuente es el ARCHIVO, no su ruta: mover un archivo no cambia su conocimiento, así que la reconciliación solo repara rutas y NUNCA re-ingesta contenido que no cambió.

Ejecutar la reconciliación en cada refresco de la wiki (delta o completo) y en `sdf-status`:

1. **Inventario actual:** listar el árbol de archivos fuente con bash (`find`/`ls -R`), excluyendo las carpetas del framework (`docs/`, `wiki/`, `.sdf/`, `.claude/`, `.obsidian/`, `graphify-out/`), los adaptadores de la raíz (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`) y cualquier subárbol que contenga su propio `.sdf/` — o un `AGENTS.md` en su raíz, si es una instalación v4 o anterior — (sub-proyecto SDF anidado: se registra como fuente especial, no se inventaría por dentro; ver módulo `anidados.md`). Esto es determinístico y no gasta tokens de lectura.
2. **Rutas registradas:** compararlo contra las rutas de Fuentes de información de `.sdf/project.md` y las rutas de los enlaces markdown a archivos en las páginas de la wiki (`Aparece en`, `Transcripción:`, relaciones), localizables con grep.
3. **Ruta rota (el archivo ya no está donde decía):** buscar el archivo por nombre en el árbol. Un solo match → es un movimiento/renombre de carpeta: actualizar la ruta en `project.md` y en todas las páginas de la wiki que la citen (mapeo viejo→nuevo delegable a `wiki-graph`; si muchas rutas rotas comparten prefijo, es una carpeta renombrada: actualizar por prefijo). Cero o varios matches → preguntar al usuario (¿se eliminó? ¿se renombró el archivo? ¿cuál es cuál?).
4. **Archivos nuevos** (incluidas subcarpetas nuevas a cualquier profundidad): listarlos al usuario y proponer cuáles registrar como fuentes e ingestar (`ingestor-fuentes`). No ingestar en masa sin confirmación.
5. **Archivo eliminado confirmado:** quitarlo de Fuentes de información; en las páginas de la wiki que lo citaban, anotar en "Notas e historial" que la fuente ya no está disponible (no borrar el conocimiento ya destilado).

Convención que hace esto barato: registrar fuentes SIEMPRE con su ruta relativa a la raíz del proyecto (ej. `contratos/2026/msa-acme.pdf`). Como `project.md` vive en `.sdf/`, sus enlaces markdown a fuentes llevan el prefijo `../`; la ruta canónica registrada es lo que sigue al `../`.

## Sincronización con correo y calendario

Si la plataforma tiene conectores de correo y/o calendario (como Claude Cowork con Gmail/Outlook/Google Calendar), poblar `correos/` y `reuniones/` así:

1. **Criterios de búsqueda:** nombre del proyecto y sus alias, términos del glosario de `.sdf/project.md`, y las personas/empresas que ya tienen página en la wiki (nombres y correos). Ventana temporal: desde la **última sincronización** registrada en `INDEX.md` (primera vez: preguntar al usuario desde cuándo buscar); en calendario incluir también eventos futuros.
2. **Filtrado:** solo hilos/eventos claramente relacionados con el proyecto. En caso de duda, listar los dudosos al usuario para que confirme, en vez de incluirlos.
3. **Contenido de las páginas:** SOLO resumen y metadatos — participantes, fecha, asunto/título, qué se trató, acuerdos y compromisos. NUNCA copiar cuerpos completos de correos. Respetar el nivel de confidencialidad de `project.md`.
4. **Enlaces:** participantes → páginas de `personas/` (crearlas si son relevantes y no existen); temas → páginas de `entregables-metas/`, `empresas/`, etc. Los compromisos detectados pueden alimentar "Notas e historial" de las entidades implicadas.
5. **Cierre de la sincronización:** actualizar la fecha de "Última sincronización" en `INDEX.md`. Si no hay conectores disponibles, informarlo al usuario y continuar sin este paso (la wiki sigue funcionando).
6. **Recurrencia:** si la plataforma permite tareas programadas (Cowork las tiene), ofrecer al usuario programar la sincronización (ej. semanal).

Nota de arquitectura: los conectores los usa el agente principal de la sesión; si la escritura de páginas se delega al subagente `wiki-graph`, el principal busca en correo/calendario y le entrega los datos ya extraídos.

## Transcripciones de reuniones

Cuando aparezca una transcripción de reunión (Teams, Zoom, Meet, Fireflies, etc.), por cualquier vía — detectada en un hilo de correo durante la sincronización, o como archivo que el usuario deja en la carpeta y pide ingestar — procesarla así:

1. **Preservar la fuente:** guardar la transcripción como archivo fuente en `transcripciones/` (crearla si no existe) con nombre `AAAA-MM-DD-<slug-reunion>.<ext>`, y registrarla en Fuentes de información de `.sdf/project.md`. Es capa inmutable: no se edita. Si venía como adjunto de correo que el conector no puede descargar, pedir al usuario que suelte el archivo en la carpeta.
2. **Destilar:** el subagente `ingestor-fuentes` la lee completa y devuelve: temas tratados, decisiones, acuerdos y compromisos (quién, qué, para cuándo), y entidades mencionadas. El texto crudo no pasa por el contexto principal.
3. **Enriquecer la wiki:** crear o actualizar la página de la reunión en `wiki/reuniones/` con ese destilado (secciones Resumen y Acuerdos y compromisos), enlazando participantes y entregables, y con una línea "Transcripción: `transcripciones/<archivo>`". Actualizar también las páginas de las entidades con compromisos nuevos. NUNCA copiar la transcripción completa en la página.
4. **Ofrecer entregables:** si de la reunión se desprenden documentos (acta formal, plan de acción), ofrecer crearlos por el flujo normal de specs.

## Visualización opcional con graphify

La wiki es compatible con [graphify](https://github.com/Graphify-Labs/graphify): sus enlaces markdown se convierten en aristas del grafo. Quien quiera el visor interactivo puede instalar el CLI (`uv tool install graphifyy` — sí, con doble "y": así se llama el paquete en PyPI aunque el comando sea `graphify`) y correr `graphify ./wiki` — la salida (`graph.html`, `graph.json`) queda en `graphify-out/`, que es descartable y NO se gobierna con specs. Esto es opcional: la wiki funciona completa sin graphify.

**Índice de fuentes (acelerador opcional del nivel 4 de zoom — ver núcleo):** en proyectos con muchas fuentes crudas, el usuario puede correr `graphify .` desde la raíz del proyecto EN SU MÁQUINA (instalación global; la generación del índice es responsabilidad externa, NUNCA del framework ni de sus agentes) y dejar `graphify-out/graph.json` en la carpeta. Reglas de consumo:

1. El framework solo LEE el índice; jamás lo genera, repara ni exige. Sin índice, todo funciona igual.
2. Frescura antes de confiar: comparar la fecha de `graph.json` contra las fuentes más recientes (`ls -t`). Índice más viejo que las fuentes = solo orientativo; verificar en el archivo real antes de afirmar nada.
3. Uso: en el nivel 4 del zoom, consultar el JSON (grep/jq) para localizar en qué archivo/sección está lo buscado, y abrir solo ese archivo.
4. `graphify-out/` es derivado y descartable: excluido de la reconciliación de fuentes, sin spec, sin páginas en la wiki, y regenerable en cualquier momento.
