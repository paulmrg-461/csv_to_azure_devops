# Módulo: Modelos y delegación

Cárgalo al invocar o simular un subagente (`wiki-graph`, `auditor`, `evaluator`, `ingestor-fuentes`), al decidir qué modelo debe correr una función del framework, o al evaluar un entregable antes de cerrarlo.

## Política de modelos (OBLIGATORIA para las funciones del framework)

Las funciones propias del framework tienen modelo asignado: **escritura de wiki (`wiki-graph`) → estándar**, **auditoría/status/lint (`auditor`) → estándar**, **evaluación de entregables (`evaluator`) → estándar, con contexto limpio**, **ingesta de fuentes crudas (`ingestor-fuentes`) → económico** (por él pasa el mayor volumen de tokens). Qué modelo concreto es "estándar" o "económico" en cada plataforma lo define la tabla `modelos` del manifiesto del arnés (`harness-manifest.json`) — nunca lo asumas ni lo inventes aquí. El contenido bruto nunca debe pasar por el contexto del agente principal si un subagente puede leerlo.

Cómo cumplirla, en orden de preferencia:

1. **Agentes nombrados:** si `wiki-graph`, `auditor`, `evaluator` e `ingestor-fuentes` (sus cuerpos viven en `assets/agentes/` y se proyectan a la carpeta de agentes de cada plataforma) aparecen como tipos de subagente invocables en la sesión, usarlos.
2. **Fallback con modelo forzado:** si los agentes nombrados NO están registrados como invocables (ocurre en algunas sesiones de Cowork), NO ejecutar la función en el agente principal: usar un subagente genérico (`general-purpose` o equivalente) FORZANDO el modelo estándar o económico según corresponda en la llamada (la evaluación además en un subagente NUEVO sin pasarle tu razonamiento, para preservar el contexto limpio) y pasándole como prompt las reglas del archivo del agente correspondiente.
3. **Último recurso — preguntar antes de continuar:** si la plataforma no permite subagentes ni fijar modelo, y el modelo de la sesión NO es el estándar del framework, preguntar al usuario antes de ejecutar funciones del framework: "El framework usa <modelo estándar> para estas funciones; tu sesión corre en <modelo>. ¿Continúo con <modelo> o prefieres cambiar la sesión?". Solo continuar con el modelo de la sesión si el usuario lo confirma (si la sesión ya corre en el estándar, continuar sin preguntar).

Al terminar cualquier función del framework, si no se pudo cumplir la política (nivel 3), decláralo en el resumen final — nunca dar a entender que corrió en el modelo previsto si no fue así.

### Dietas de contexto de los subagentes

`evaluator` y `wiki-graph` operan con **dieta de contexto obligatoria** — entradas cerradas y presupuesto de salida — escrita en el cuerpo de cada uno (`assets/agentes/evaluator.md` y `assets/agentes/wiki-graph.md`). No la repitas aquí de memoria: léela ahí antes de invocarlos. En resumen: `evaluator` no lee el proyecto completo, solo el documento, su spec y los Estándares; `wiki-graph` no relee documentos ni specs si ya le diste el destilado, y resuelve un lote completo de deltas en una sola llamada.

### Economía de sesión (ahorro de créditos sin perder calidad)

- **Modelo de sesión recomendado: el estándar del framework** (ver tabla `modelos` del manifiesto). El framework compensa con estructura (specs, checklist mecánico, evaluator) lo que un modelo mayor aporta en improvisación; un modelo superior se reserva para tareas puntuales de diseño o análisis complejo que el usuario pida explícitamente. Si la sesión corre en un modelo superior, informarlo una vez al inicio y dejar la decisión al usuario.
- **Una tarea = una sesión.** El historial de la conversación se re-cobra completo en cada turno: las sesiones largas son el mayor gasto oculto. Tras cerrar un cambio, si la conversación ya acumula varias tareas, sugerir sesión nueva — `.sdf/MEMORY.md` + `wiki/INDEX.md` reponen el contexto por ~1.000 tokens.
- **Los archivos viven en la carpeta, no en el chat.** No pedir ni fomentar que se peguen documentos en la conversación (se re-cobran cada turno); dejarlos en la carpeta y leerlos por niveles de zoom (ver núcleo).
- **Chat conciso.** Las respuestas de conversación son breves; lo extenso va a los entregables y a la wiki. Evitar `full` y sincronizaciones más frecuentes de lo necesario: el modo delta existe para no pagar reconstrucciones.

## Contabilidad de tokens (usage.csv)

Cada proyecto lleva su contador de consumo en `.sdf/usage.csv` (crearlo con encabezado al primer registro). Es un archivo DERIVADO: excluido de la reconciliación, sin spec ni página de wiki, y su pérdida no daña nada.

**Formato (una línea por acción):** `fecha,accion,objeto,agente,modelo,tokens,fuente`
- `accion`: crear-doc | actualizar-doc | adoptar | init | sync | graph | lint | consulta-mayor | **arranque**
- `objeto`: id del documento o del cambio (o `-` para acciones globales, incluida `arranque`)
- `agente`: orquestador | wiki-graph | evaluator | ingestor-fuentes | auditor
- `fuente`: `medido` (tokens reales de la notificación del subagente, o del contador de la plataforma si expone tokens de entrada de sesión) | `estimado` (bytes leídos+escritos ÷ 4) | `delta-sesion` (diferencia del contador de presupuesto de la sesión, si el entorno lo expone)

**Cómo se captura:**
1. **Subagentes (exacto):** toda invocación devuelve una notificación con sus tokens totales — registrar UNA línea por subagente invocado, con su modelo. Esto cubre con precisión la mayor parte del trabajo del framework.
2. **Orquestador (aproximado):** al cerrar la acción, registrar su consumo como `delta-sesion` si el contador está disponible, o como `estimado` (suma de bytes de archivos leídos y escritos ÷ 4). NUNCA presentar lo estimado como exacto.
3. **Arranque (una vez por sesión, no por acción):** justo después de aplicar el orden de arranque fijo del núcleo (MEMORY → project.md → núcleo → módulo(s) cargados), registrar una línea `accion=arranque, objeto=-, agente=orquestador, fuente=estimado` con la suma de bytes de esos archivos ÷ 4 (o `medido` si la plataforma expone tokens de contexto de entrada reales). Es lo que permite medir de verdad el objetivo de arranque del núcleo (≤ 4.000 tokens) en vez de estimarlo una sola vez a mano.
4. **Cuándo:** en el cierre de cada cambio (junto con marcar Estado: cerrado) y al terminar acciones sueltas (init, sync, graph, lint). Además, estampar el resumen en el proposal (campo `Tokens:`).

**Límite honesto:** desde dentro de una sesión no es observable la separación entrada/salida/caché ni el costo facturado; este contador da orden de magnitud consistente por documento, acción, agente y modelo — suficiente para comparar, detectar despilfarros y validar ahorros. La contabilidad exacta por tipo de token pertenece a la consola de facturación o al SDF Manager.

**En otras herramientas (Gemini CLI, Codex, etc.):** esta sección es autocontenida; aplicar el equivalente disponible (delegar a su modelo económico si existe, o informar al usuario con qué modelo corren estas funciones).

## Guía de delegación a subagentes

Los subagentes existen para dos cosas: paralelizar y proteger la ventana de contexto del orquestador (cada subagente explora en su propia ventana y devuelve solo lo destilado). Reglas:

1. **Toda tarea delegada lleva contrato:** objetivo concreto, formato de salida esperado, fuentes/herramientas a usar, límites explícitos (qué NO hacer, qué ya está cubierto por otro subagente) y presupuesto de esfuerzo. Las tareas vagas producen subagentes duplicando trabajo o dejando huecos.
2. **Escalado de esfuerzo:** consulta simple sobre la wiki = sin subagentes (MEMORY + INDEX + grep bastan). Documento típico = `ingestor-fuentes` (si hay fuentes por leer) + `wiki-graph` + `evaluator`. Trabajo masivo (init, reconstrucción, decenas de fuentes) = varios `ingestor-fuentes` en paralelo con partición EXPLÍCITA de archivos (cada lote asignado por nombre, sin solapes). No sobre-invertir: más subagentes que trabajo real es desperdicio.
3. **Patrón de artefactos:** los subagentes ESCRIBEN su salida en archivos (páginas de la wiki, destilados, reportes) y devuelven al orquestador solo referencias ligeras + un resumen de máximo 5 líneas. El contenido completo nunca viaja por la conversación: se pierde fidelidad y se quema contexto.
4. **Sin relecturas redundantes:** el orquestador entrega en el contrato el destilado que ya tiene fresco; los subagentes de escritura (`wiki-graph`) NO releen documentos ni specs salvo que les falte un dato puntual.
5. **Cierre por lotes:** si varios documentos cierran en la misma sesión, UNA sola llamada a `wiki-graph` con todos los deltas y los `evaluator` de cada documento lanzados en paralelo — nunca un ciclo completo por documento.
6. **Un intercambio, no un diálogo:** diseñar la tarea para que el subagente resuelva en una sola pasada. Si necesitó aclaraciones, el contrato estaba mal escrito — corregirlo la próxima vez (y si es un defecto del framework, registrarlo en `.sdf/FRAMEWORK-FEEDBACK.md`).

## Evaluación independiente del entregable

Los agentes se sesgan al evaluar su propio trabajo. Por eso los documentos NUEVOS y los cambios MAYORES no se cierran sin el veredicto del subagente `evaluator`, que opera con contexto limpio: recibe SOLO el documento terminado, su `spec.md` y los estándares de `project.md` — nunca el razonamiento de quien lo creó (dieta completa en `assets/agentes/evaluator.md`). Evalúa estado final, no proceso, en una sola pasada con rúbrica (exactitud factual, cumplimiento de spec, completitud, estándares; 0.0-1.0 por criterio) y veredicto PASA / NO PASA con correcciones accionables. Si NO PASA: el orquestador corrige y reevalúa, máximo 2 ciclos; si persiste, escalar al usuario con el reporte del evaluator. Cambios menores (retoques de forma) pueden cerrarse sin evaluación, anotándolo en el proposal.
