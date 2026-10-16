# Módulo: Sub-proyectos anidados (SDF y de desarrollo)

Cárgalo cuando detectes un subárbol con su propia instalación (SDF o de desarrollo), cuando instales cualquiera de los dos dentro de un proyecto SDF existente, o cuando el usuario pida tocar algo de un sub-proyecto desde la sesión del padre.

Hay **dos tipos** de sub-proyecto, y ambos comparten la misma regla de frontera: el padre gobierna únicamente su propia raíz, nunca el interior del hijo.

| | Sub-proyecto **SDF** | Sub-arnés de **desarrollo** (`sdf-dev`) |
|---|---|---|
| Qué es | Otra instalación completa del framework (wiki, memoria, documentos propios) | Una app de código gobernada por Spec Kit u OpenSpec — el SDF no la gobierna |
| Detección | `.sdf/` propio — o, si es v4 o anterior, `AGENTS.md` en su raíz **sin** `.sdf-dev.json` al lado | `.sdf-dev.json` en su raíz (siempre presente, cualquiera sea el framework), o directamente `.specify/`/`openspec/` como raíces reconocidas |
| Se representa en | `wiki/proyectos-relacionados/<slug>.md` | `wiki/entregables-metas/<nombre-app>.md` (sección 4.3 del plan v6 — **no** en `proyectos-relacionados/`, que es exclusiva de este primer tipo) |
| Lo único que el padre lee del hijo | `MEMORY.md` | `README.md` y `archivo_gobernanza` (de `.sdf-dev.json`) |

**Desambiguación (importante):** ambos tipos pueden tener un `AGENTS.md` en su raíz — el puente de `sdf-dev` (módulo consumido por su skill) también instala uno. La diferencia es `.sdf-dev.json`: si existe junto al `AGENTS.md`, es un sub-arnés de desarrollo, nunca una instalación SDF v4. Verifica siempre los dos antes de decidir cuál caja negra aplicar.

## Sub-proyecto SDF

1. **Detección:** un subárbol es un sub-proyecto SDF si contiene su propia carpeta `.sdf/` — o, si es una instalación v4 o anterior, un `AGENTS.md` en su raíz **y no** un `.sdf-dev.json` junto a él (ver desambiguación arriba).
2. **Caja negra hacia adentro:** el proyecto padre NO gobierna el interior del sub-proyecto — no inventaría sus archivos, no ingesta su contenido a la wiki del padre, no audita sus cambios, no ejecuta sus comandos ni edita nada adentro. La reconciliación de fuentes (módulo `wiki.md`) excluye el subárbol completo.
3. **Representación en el padre:** el sub-proyecto se registra UNA sola vez en Fuentes de información de `project.md` del padre: `Sub-proyecto SDF: [<nombre>](<ruta>/.sdf/project.md) · [memoria](<ruta>/.sdf/MEMORY.md)` (en instalaciones v4 o anteriores esos archivos están en `<ruta>/` directamente), y con una página propia en `wiki/proyectos-relacionados/<slug>.md` (plantilla `entidad.md`) que enlaza a esos mismos archivos — la línea de `project.md` es el registro operativo, la página es su representación en la wiki. Cuando el padre necesite contexto del sub-proyecto, la lectura recomendada es su `MEMORY.md` (≤80 líneas) — el resumen oficial —, nunca recorrer su árbol.
4. **Hacia afuera:** al trabajar EN el sub-proyecto (sesión abierta en esa subcarpeta), manda su propio SDF y el padre es invisible; el sub-proyecto no lee ni escribe fuera de su raíz.
5. **Trabajo cruzado:** si en una sesión del padre el usuario pide tocar documentos del sub-proyecto, lo correcto es sugerir abrir sesión en esa subcarpeta; si el usuario insiste, aplicar las reglas del `.sdf/AGENTS.md` DEL SUB-PROYECTO (incluido su cierre completo) y no registrar nada en la wiki del padre.
6. **Instalación anidada:** instalar el SDF en una subcarpeta de un proyecto SDF es válido y no rompe nada; después de instalarlo, correr `sdf-graph` en el padre para que la reconciliación detecte el sub-proyecto nuevo, lo registre como fuente especial y ejecute el traspaso (punto 7).
7. **Traspaso — cuando el sub-proyecto nace en territorio que el padre ya había ingestado:** el conocimiento ya destilado en la wiki del padre NO se borra: es historial válido y sigue siendo útil. El traspaso, que ejecuta el `sdf-graph` del padre al detectar el sub-proyecto, hace tres cosas:
   - **Fuentes:** las entradas de Fuentes de información del padre que apunten a archivos DENTRO del subárbol se retiran de la lista (anotando "cedida al sub-proyecto <nombre>") y quedan cubiertas por la línea única del sub-proyecto. El padre deja de reconciliarlas.
   - **Páginas:** las páginas de la wiki del padre que citaban archivos del subárbol conservan su contenido y sus enlaces (siguen resolviendo mientras el hijo no reorganice por dentro), pero se les anota en "Notas e historial" que ese tema fue cedido al sub-proyecto — la verdad VIVA de ahí en adelante está en la wiki del hijo; el padre no re-ingiere ese interior nunca más.
   - **Memoria:** actualizar `MEMORY.md` del padre si el estado actual lo amerita (ej. "el frente X ahora es el sub-proyecto <nombre>").
   Desde el traspaso, cuando el padre necesite refrescarse sobre ese tema, lee el `MEMORY.md` del hijo — nunca su árbol. El hijo, por su parte, arranca de cero con su propio `sdf-init` (no hereda automáticamente páginas del padre; si el usuario quiere trasplantar alguna, la copia él o lo pide explícitamente).

## Sub-arnés de desarrollo (`sdf-dev`)

1. **Detección:** una subcarpeta con `.sdf-dev.json` en su raíz — o, ya reconocibles por sí solas como raíces de caja negra aunque `.sdf-dev.json` faltara por algún motivo, `.specify/` (Spec Kit) u `openspec/` (OpenSpec) en su raíz.
2. **Caja negra hacia adentro:** el padre NUNCA lee el código, las specs ni las tareas del sub-arnés — a diferencia de un sub-proyecto SDF (que sí tiene documentos de oficina que en teoría podrían interesar al padre), aquí no hay ambigüedad posible: es código, gobernado por un framework distinto. Las únicas lecturas permitidas son `README.md` y el archivo de gobernanza que `.sdf-dev.json` declare (`archivo_gobernanza`: la constitución de Spec Kit o el equivalente de OpenSpec). La reconciliación de fuentes (módulo `wiki.md`) excluye el subárbol completo, igual que a un SDF anidado.
3. **Representación en el padre:** se registra UNA sola vez en Fuentes de información de `project.md` del padre (`Sub-proyecto de desarrollo: [<nombre-app>](<nombre-app>/) · <framework>`, lo hace el propio `sdf-dev` al crearlo) y con una página propia en `wiki/entregables-metas/<nombre-app>.md` (plantilla `entidad.md`; la crea/actualiza `sdf-graph`, ver su cuerpo) — **no** en `proyectos-relacionados/`, reservada al tipo anterior.
4. **Documentos de oficina sobre la app SÍ se gobiernan en el padre:** manual de usuario, actas, presentaciones sobre esta aplicación van en `docs/` del padre con el flujo normal (mismo reparto que ya declara el `AGENTS.md` de la propia subcarpeta) — la caja negra es sobre el código, no sobre lo que se escribe acerca de él.
5. **Hacia afuera:** al trabajar EN el sub-arnés (sesión abierta en esa subcarpeta), manda su propio `AGENTS.md`/framework; el SDF del padre es invisible y no se aplica.
6. **Sin traspaso:** a diferencia de un SDF anidado, un sub-arnés de desarrollo no "hereda" ni cede conocimiento de la wiki del padre — nace vacío de contexto documental (es código) y el padre no re-ingiere nada de su interior en ningún momento, ni antes ni después de crearlo.
