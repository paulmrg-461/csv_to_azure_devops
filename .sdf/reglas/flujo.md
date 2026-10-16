# Módulo: Flujo de trabajo obligatorio

Cárgalo siempre que vayas a crear, actualizar, retirar o renombrar un documento, o a cerrar cualquier cambio — incluida la inicialización de un proyecto nuevo. Tareas de solo lectura (un reporte de status, un lint, una pregunta puntual sobre la wiki) no lo necesitan.

## 0. Inicio de un proyecto nuevo

Si `.sdf/project.md` todavía es plantilla (`<placeholders>`), diligenciarlo ANTES de crear cualquier documento con una **entrevista guiada** — nunca solo con supuestos propios:

1. Deducir de la conversación y la carpeta todo lo posible (nombre, contenido existente, idioma).
2. Preguntar lo que falte en tandas cortas (2-4 por turno), priorizando: propósito y alcance → audiencias → estándares (tono, marca, confidencialidad) → fuentes y glosario. Opciones concretas, no preguntas abiertas en cadena.
3. Secciones opcionales (glosario, fuentes) pueden quedar vacías y completarse sobre la marcha.
4. Resumen y OK del usuario antes de dar `project.md` por terminado.

No avanzar con entregables sin el contexto base. Si el usuario pide algo urgente sin responder preguntas: diligenciar lo mínimo (propósito, idioma, propietario), marcar el resto pendiente.

## 0.1 Proyecto con contenido preexistente

Inventariar con el usuario los archivos previos al framework y clasificar cada uno:

- **Fuente de información:** insumos y referencia. Se quedan donde están, se listan en **Fuentes de información** de `.sdf/project.md`. Sin spec.
- **Entregable a adoptar:** documentos que el usuario seguirá editando con IA. Leer el archivo, crear spec por ingeniería inversa en `.sdf/docs/<id>/spec.md` (estructura y contenido actuales; Decisiones anota que nació fuera del flujo), mover a `docs/<id>.<ext>`, agregar a **Documentos activos**. Cada adopción es un cambio (`adoptar-<id>`) que se cierra como cualquier otro.

Duda → fuente (se adopta después). No adoptar en masa sin confirmación.

Terminado el inventario, **construir la wiki inicial**: `ingestor-fuentes` destila por lotes, `wiki-graph` escribe las páginas (módulo `modelos-y-delegacion.md`). Ofrecer sincronizar correo/calendario. Única lectura masiva: desde entonces, todo se contextualiza por la wiki en modo delta.

## 1. Antes de trabajar

- **Migración pendiente:** si existe `.sdf-migracion/` en la raíz, SDF Manager dejó pasos que exigen criterio (un `.md` por paso). Completarlos ANTES de cualquier otro trabajo (verbo `migrate`, o leer su cuerpo como guion). No es error: la carpeta funciona con normalidad mientras tanto.
- Aplicado ya el arranque fijo del núcleo (MEMORY → project.md → núcleo → módulo), **contextualizarse en niveles de zoom, del más barato al más caro, bajando solo hasta donde la tarea lo exija:**
  1. `wiki/INDEX.md` — el mapa.
  2. SOLO 3-6 páginas de wiki relevantes (localizar con grep, no hojeando comunidades).
  3. La spec del documento afectado.
  4. Archivos fuente/documentos completos ÚNICAMENTE si la wiki no alcanza (acelerador opcional de graphify: módulo `wiki.md`). Registrar la carencia — crear en el cierre lo que faltó en la wiki.
- Revisar **Documentos activos**, la spec si el documento existe, y `.sdf/docs/<id>/changes/` por si hay un cambio Estado: en curso.

## 2. Crear un documento nuevo

1. `.sdf/docs/<id>/changes/AAAA-MM-DD-<id-cambio>/proposal.md` (plantilla `proposal.md`; Estado: en curso): qué pide el usuario, por qué, decisiones, requisitos, **Módulos:** cargados, **Presupuesto:** esperado (ver Velocidades).
2. `tasks.md` con los pasos; si es complejo (estructura no obvia, muchas fuentes, cálculos), agregar `design.md`.
3. Generar `docs/<id>.<ext>` (plano).
4. `.sdf/docs/<id>/spec.md` reflejando el estado final (plantilla `spec-documento.md`; Estructura y contenido → módulo `tipos-de-documento.md`).
5. Actualizar **Documentos activos** en `.sdf/project.md`.
6. **Tanda paralela de cierre** (MISMO TURNO): `wiki-graph` (delta, sin releer documentos) + `evaluator` (velocidad estándar; módulo `modelos-y-delegacion.md`). NO PASA → corregir y reevaluar (máx. 2 ciclos, luego escalar); si la corrección tocó la wiki, `wiki-graph` retoca solo esa página.
7. Verificación en dos capas: `bash .sdf/specs/checklist.sh <id>` + los 3 puntos de juicio (ver Checklist).
8. **Estado: cerrado** + registrar consumo (`.sdf/usage.csv` + campo `Tokens:`, comparado contra el `Presupuesto:`).

## 3. Actualizar un documento existente

Mismo procedimiento que la sección 2 (proposal con Módulos/Presupuesto, spec actualizada, verificación en dos capas, cierre con consumo registrado), con estas diferencias:

- El documento se actualiza/regenera EN EL MISMO archivo — nunca una copia versionada.
- `evaluator` corre SOLO si el cambio es mayor (rehace secciones, cambia cifras o estructura); retoques menores = velocidad exprés, sin evaluator.

## 4. Un cambio que afecta varios documentos

Replicar la carpeta del cambio (mismo `AAAA-MM-DD-<id-cambio>`) bajo `.sdf/docs/<doc>/changes/` de CADA documento afectado: `proposal.md` único (lista todos los documentos), `tasks.md` de cada copia solo con las tareas de ese documento. Actualizar todas las specs y cerrar todas las copias.

## 5. Retirar o renombrar un documento

- **Retirar:** cambio (`retirar-<id>`), spec a estado `obsoleto` (no se borra: es historial), archivo eliminado/movido según el usuario, quitar de **Documentos activos**.
- **Renombrar:** cambio, renombrar `docs/<id>.<ext>` y su carpeta espejo `.sdf/docs/<id>/`, actualizar spec y tabla.

## 6. Registrar el razonamiento

Cada spec captura en **Decisiones** y **Registro de cambios** el razonamiento de la conversación: qué se decidió, por qué, qué se descartó — para que cualquier IA futura reconstruya con precisión por qué el documento es como es.

## Checklist de validación (antes de cerrar un cambio)

**El cierre no es opcional ni diferible**, pero tampoco lento: dos capas, con el rigor que amerite el cambio (ver Velocidades).

**Capa 1 — mecánica (script, ~2 s, ~0 tokens):** `bash .sdf/specs/checklist.sh <id>` desde la raíz. Verifica lo estructural: documento en `docs/`, spec y changes completos, proposal con Estado/Módulos/Presupuesto/Evaluación, tasks, página en la wiki, fila en `project.md`, `MEMORY.md` ≤80 líneas, INDEX con fecha del día, hechos sellados con fuente, sin relaciones genéricas ni wikilinks viejos, si se excedió el `Presupuesto:`, y cuántas entradas hay en `.sdf/REVIEW.md` (no bloquea). Corregir toda FALLA — no gastar razonamiento LLM en lo que el script ya verificó.

**Capa 2 — juicio (solo 3 puntos):**

- [ ] La spec refleja el estado REAL del documento (en estándar/crítico lo confirma `evaluator`).
- [ ] Decisiones y aprendizajes capturados (wiki/glosario/Estándares según aplique).
- [ ] Estándares de `project.md` respetados (también cubierto por `evaluator` cuando corre).

### Velocidades de cierre

- **Exprés** (presupuesto ≤ 10 k tokens) — retoques/correcciones menores, sin cambio de cifras/estructura/decisiones: sin evaluator, auto-revisión de una línea por punto de juicio; anotar `Evaluación: no aplica — cambio menor`.
- **Estándar** (presupuesto ≤ 80 k tokens) — documento nuevo o cambio mayor: script + `wiki-graph` y `evaluator` en paralelo.
- **Crítico** (presupuesto ≤ 150 k tokens) — solo si el usuario lo pide o el documento es de alto impacto declarado: estándar + `auditor` sobre el cierre. Nunca sumar el auditor por defecto — evaluator + auditor a la vez es doble validación innecesaria.

Cierre que excede su presupuesto: el proposal lo anota y `sdf-status` lo lista; tres excesos seguidos por la misma causa van a `.sdf/FRAMEWORK-FEEDBACK.md` como hallazgo, no como fracaso silencioso.

## Mejora continua del framework

Aprendizajes del PROYECTO ya tienen canal (módulo `memoria-y-aprendizaje.md`). Esto cubre lo otro: cuando una validación revele que el problema vino de una REGLA del framework (ambigüedad, paso faltante, plantilla deficiente, delegación que falló):

1. **Registrar, no editar:** anotar en `.sdf/FRAMEWORK-FEEDBACK.md` (plantilla `feedback.md`). NUNCA editar reglas o plantillas del framework dentro del proyecto: crea copias divergentes.
2. **Aplicar centralizado:** el dueño revisa con el verbo `feedback`, aplica lo aprobado en la fuente canónica del skill, re-empaqueta y redistribuye. El framework mejora una sola vez para todos.
