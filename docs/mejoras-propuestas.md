# Mejoras propuestas: csv_to_azure_devops

- **Fecha:** 2026-10-05
- **Rama revisada:** `main`. Los números de línea de `upload_tasks_with_ai.py` y `tasks_bugs_extractor.py` son del **árbol de trabajo**, que tiene cambios sin commitear en ambos archivos (no se tocaron); pueden no coincidir con `HEAD`.
- **Alcance:** lectura de los cinco scripts (`upload_tasks_with_ai.py`, `tasks_bugs_extractor.py`, `tasks_extractor.py`, `issues_extractor.py`, `create_user_stories.py`), `requirements.txt`, `.gitignore`, `.env.example`, la guía en `docs/` y los nombres de columnas de los archivos de datos. La carpeta `venv/` no se leyó ni se analizó; solo se contó cuántos de sus archivos están versionados (`git ls-files`).
- **Convención:** "no verificado" marca lo que depende de ejecución o de datos que no consulté. No se reproduce ningún valor de credencial. No se ejecutó ningún script (todos escriben en Azure DevOps o en archivos).

## Resumen

Utilidad Python de un solo usuario que sube Tasks a Azure DevOps desde un `tasks.csv`/`tasks.xlsx`, enriquece cada una con DeepSeek y exporta work items a Excel. Es pequeña y funciona; el riesgo no está en un fallo grave sino en que **escribe en el tracker real** y casi todo lo que la rodea (reintentos, trazabilidad, pruebas, higiene del repo) es manual.

| Categoría | Alta | Media | Baja |
|---|---|---|---|
| Seguridad | 0 | 3 | 2 |
| Correcciones | 1 | 5 | 3 |
| Refactor | 0 | 2 | 2 |
| Pruebas | 0 | 1 | 0 |
| Implementaciones futuras | 0 | 2 | 0 |

**Los tres más importantes**
1. Un fallo de red a mitad de una carga en modo LIVE aborta el lote sin guardar qué se creó, y repetir la carga duplica las tareas ya creadas (`upload_tasks_with_ai.py:392-397`, `:454-471`).
2. Tres scripts guardan el PAT escribiéndolo dentro del código (`pat = ''`), y el repo versiona su entorno virtual y estado de herramientas: un `git commit -a` descuidado publica el token.
3. Incluso en `DRY_RUN` el script envía título, módulo y descripción de cada tarea (más una descripción de la arquitectura de BnB) a DeepSeek (`upload_tasks_with_ai.py:314`, `:240`).

**Secretos expuestos:** no. El `.env` real está en `.gitignore` y nunca estuvo en el historial (`git log -- .env` vacío). Comparé sin imprimirlos los valores de `PAT` y `DEEPSEEK_API_KEY` del `.env` contra todos los archivos fuera de `venv/` y `.git/` y no aparecen en ninguno. Los `pat = ''` del código están vacíos hoy. `.env.example` solo trae marcadores. El riesgo es de proceso (hallazgos 1 y 3), no de valores filtrados.

---

## Seguridad

### 1. Tres scripts piden escribir el PAT dentro del código versionado
- **Dónde:** `create_user_stories.py:10`, `issues_extractor.py:9`, `tasks_extractor.py:9` (`pat = ''`); además `create_user_stories.py:6-7` deja comentada otra organización y proyecto.
- **Qué pasa:** estos tres scripts no leen `.env`: para usarlos hay que pegar el PAT en la variable. Los tres están versionados. Los dos scripts mantenidos (`upload_tasks_with_ai.py:14-17`, `tasks_bugs_extractor.py:11-17`) ya migraron a `.env`; la versión comprometida de `tasks_bugs_extractor.py` aún tenía `PAT = ''` con un comentario que recomendaba variables de entorno.
- **Por qué importa:** el PAT de la guía tiene permiso de lectura y **escritura** sobre work items (`docs/guia-subir-tasks-azure-devops.md`, sección 1). Pegado en un archivo rastreado, un `git commit -a` o `git add .` lo publica en el historial de Azure DevOps y queda ahí aunque se borre después.
- **Propuesta:** que los tres lean `.env` con el mismo bloque de 4 líneas que ya usa `tasks_bugs_extractor.py:10-17`; o, si `tasks_extractor.py` e `issues_extractor.py` ya no se usan, eliminarlos (ver hallazgo 16). Añadir un escaneo de secretos en pre-commit o en el pipeline del repo.
- **Esfuerzo:** S
- **Prioridad:** media
- **Riesgo de no hacerlo:** token con escritura en el historial del repositorio.
- **Contra:** `issues_extractor.py` extrae comentarios y ningún otro script lo hace; eliminarlo pierde esa función (hallazgo 16).


### 2. Los datos del backlog salen a un tercero, también en `DRY_RUN`
- **Dónde:** `upload_tasks_with_ai.py:32` (URL de `api.deepseek.com`), `:188-220` (prompt con título, módulo, descripción y un resumen de la arquitectura de BnB: módulos, tecnologías, nombres de servicios), `:240` (POST), `:314` (la llamada ocurre antes de la comprobación de `DRY_RUN` en `:375`).
- **Qué pasa:** cada fila del archivo de entrada se envía a DeepSeek para generar contenido. `DRY_RUN` (por defecto `true`) evita escribir en Azure DevOps pero no evita este envío; de hecho existe precisamente para revisar el contenido de la IA.
- **Por qué importa:** el backlog describe el producto y su arquitectura. Si la organización tiene una política sobre proveedores de IA externos o sobre dónde se procesan datos del producto, el script la incumple sin avisar. **No verificado:** si esa política existe.
- **Propuesta:** confirmar la política. Si hay restricción: usar un proveedor autorizado (la configuración ya admite cambiar URL y modelo si se parametriza `deepseek_api_url`, hoy fija en `:32`), o dejar la IA apagada por defecto (sin `DEEPSEEK_API_KEY` ya se desactiva, `:178-186`) y activarla con una variable explícita. Imprimir al inicio, junto a la línea de modo (`:81`), si se enviarán datos a un tercero.
- **Esfuerzo:** S
- **Prioridad:** media
- **Riesgo de no hacerlo:** envío de información de producto a un tercero sin decisión consciente.
- **Contra:** otro proveedor puede costar más o generar peor contenido para tareas técnicas en español; hay que probar la calidad (hoy hay un modo para eso, el `DRY_RUN`).


### 3. El repo versiona un entorno virtual, estado de herramientas de IA y archivos del sistema
- **Dónde:** `.gitignore:1` (solo contiene `.env`); `git ls-files` lista 4 720 archivos bajo `venv/`, además de `.omc/` (estado de sesión y `agent-replay-*.jsonl`, con cambios sin commitear), `.marscode/deviceInfo.json` y `.DS_Store`.
- **Qué pasa:** nada de eso debería estar en un repositorio. No leí `venv/`. Del resto, `.omc/state/agent-replay-*.jsonl` es un registro de sesión de una herramienta de IA y puede contener texto de conversaciones (no verificado: no lo abrí); `.marscode/deviceInfo.json` contiene un identificador de dispositivo.
- **Por qué importa:** inflan el repo, ensucian cada `git status` (hoy hay cuatro archivos de estado local modificados) y es donde un secreto pegado en una conversación terminaría en el historial.
- **Propuesta:** ampliar `.gitignore` (`venv/`, `.venv/`, `.omc/`, `.marscode/`, `.DS_Store`, `__pycache__/`, `*.xlsx` de salida) y sacarlos del índice con `git rm -r --cached` en un commit propio.
- **Esfuerzo:** S
- **Prioridad:** media
- **Riesgo de no hacerlo:** el próximo `git add .` sube más estado local; contexto de sesión de IA versionado.
- **Contra:** quitar del índice no borra el historial; reescribirlo (`git filter-repo`) cambia todos los hashes y solo se justifica si en esos archivos hay un secreto real, que no verifiqué. Recomiendo no reescribir.


### 4. El PAT tiene más permisos de los que necesitan los extractores, y no hay política de caducidad
- **Dónde:** `docs/guia-subir-tasks-azure-devops.md` (sección 1: "Work Items (Read & Write)"); los cuatro extractores solo leen.
- **Qué pasa:** la guía pide un único PAT de lectura y escritura, y los scripts de solo lectura usan el mismo `.env` y la misma variable `PAT`.
- **Por qué importa:** un extractor no necesita poder crear ni modificar nada; si el `.env` se filtra o un script se equivoca, el daño es el de un token de escritura.
- **Propuesta:** dos PAT: uno de solo lectura para los extractores y otro de escritura solo para `upload_tasks_with_ai.py` y `create_user_stories.py`, con caducidad corta (30-90 días en Azure DevOps) y su fecha de renovación en la guía. Dos variables: `PAT_READ` y `PAT_WRITE`.
- **Esfuerzo:** S
- **Prioridad:** baja
- **Riesgo de no hacerlo:** radio de daño mayor del necesario si el `.env` se filtra.
- **Contra:** dos tokens que gestionar y renovar para una utilidad de un solo usuario; si se mantiene un token único, que al menos tenga caducidad corta.


### 5. Los archivos de entrada y salida con correos y trabajo del equipo están versionados
- **Dónde:** `tasks.csv`, `tasks.xlsx`, `user_stories.csv`, `created_tasks.xlsx` (todos rastreados; el último con cambios sin commitear), `docs/guia-subir-tasks-azure-devops.md` (sección 5, correos corporativos y roles de tres personas).
- **Qué pasa:** la columna `AssignedTo` lleva correos corporativos y las tareas describen el trabajo planificado. `azure_devops_work_items.xlsx` (salida del extractor, sin rastrear hoy) contiene títulos, estados y nombres de todo el proyecto.
- **Por qué importa:** si el repositorio se comparte o se clona fuera del equipo, esos datos van con él. No leí el contenido de las hojas más allá de los nombres de columnas.
- **Propuesta:** tratar los archivos de datos como locales: ignorarlos en git y dejar un `tasks.example.csv` con una fila de ejemplo y correos ficticios.
- **Esfuerzo:** S
- **Prioridad:** baja
- **Riesgo de no hacerlo:** datos de personas y de planificación circulando con el código.
- **Contra:** perder el historial de qué se subió y cuándo; si ese registro importa, mejor guardarlo en un lugar pensado para ello (hallazgo 6).

---

## Correcciones

### 6. Un fallo de red en LIVE pierde el registro de lo creado, y repetir la carga duplica
- **Dónde:** `upload_tasks_with_ai.py:392-397` y `:437-442` (`requests.post`/`patch` sin `try`), `:454-464` (bucle), `:467-471` (la exportación a `created_tasks.xlsx` ocurre solo al final).
- **Qué pasa:** una `ConnectionError` o un corte en la tarea N lanza una excepción que termina el script antes de escribir `created_tasks.xlsx`: las N-1 tareas ya creadas en Azure DevOps quedan sin registro local. Al repetir la ejecución con el mismo archivo no hay forma de saltarlas: el script no busca duplicados (por título, sprint o historia) y crea todas otra vez. Además `created_tasks.xlsx` se reescribe entero en cada ejecución (`:471`), borrando el de la anterior.
- **Por qué importa:** work items duplicados en el tracker real (borrarlos es manual y deja ruido en las métricas del sprint) y llamadas a la IA ya pagadas, repetidas.
- **Propuesta:** (a) `try/except requests.RequestException` alrededor de cada tarea para registrar el fallo y seguir; (b) escribir cada fila creada en el archivo de salida en cuanto se crea (apéndice) en vez de al final; (c) antes de crear, consultar con WIQL si ya existe una tarea con ese título en esa iteración y saltarla.
- **Esfuerzo:** M
- **Prioridad:** alta
- **Riesgo de no hacerlo:** duplicados en producción al primer corte de red en una carga grande.
- **Contra:** el chequeo (c) por título es heurístico: dos tareas legítimas con el mismo título en el mismo sprint se tomarían por duplicado; alternativa: guardar una clave estable (por ejemplo un hash de título+historia) en un campo o etiqueta de la tarea.


### 7. Ninguna llamada a Azure DevOps tiene timeout
- **Dónde:** `upload_tasks_with_ai.py:392`, `:437`; `tasks_bugs_extractor.py:51`, `:70`, `:104`; `tasks_extractor.py:32`, `:49`, `:94`; `issues_extractor.py:33`, `:55`, `:93`; `create_user_stories.py:52`. Contraste: la llamada a DeepSeek sí lo tiene (`upload_tasks_with_ai.py:240`, `timeout=60`).
- **Qué pasa:** `requests` espera sin límite por defecto. Una conexión que se queda abierta cuelga el script indefinidamente (y en una carga LIVE, a mitad del lote).
- **Propuesta:** `timeout=(5, 30)` en todas, o una `requests.Session` compartida con ese valor.
- **Esfuerzo:** S
- **Prioridad:** media
- **Riesgo de no hacerlo:** ejecuciones colgadas que obligan a matar el proceso a mitad de un lote (con el problema del hallazgo 6).


### 8. Con un PAT inválido el script revienta al intentar leer JSON de una respuesta que no lo es
- **Dónde:** `upload_tasks_with_ai.py:448` y `:451` (`response.json()` en la rama de error).
- **Qué pasa:** en las ramas de error el código asume cuerpo JSON. Azure DevOps responde a un PAT inválido o caducado con una página HTML de inicio de sesión (con estado 203, según mi conocimiento del servicio; no verificado aquí), y `.json()` lanza `JSONDecodeError`, que termina el lote. `create_user_stories.py:75-78` ya resuelve esto bien (`try: response.json() except ValueError: response.text`).
- **Propuesta:** el mismo patrón en `:448` y `:451`; tratar además cualquier estado distinto de 200 como error explícito y, ante 401/203, abortar con un mensaje claro ("PAT inválido o caducado") en lugar de seguir con la siguiente tarea.
- **Esfuerzo:** S
- **Prioridad:** media
- **Riesgo de no hacerlo:** el error útil queda enterrado en una traza; el síntoma más probable de un PAT caducado.


### 9. El contenido de la IA y del CSV se inserta como HTML sin escapar
- **Dónde:** `upload_tasks_with_ai.py:101` (`_html_list`), `:317-335` (descripción completa).
- **Qué pasa:** `module`, `description`, y los textos de la IA se interpolan tal cual en HTML. Un texto técnico como `List<String>` o `Map<K, V>` (habitual en Dart y Python con tipos) se interpreta como una etiqueta y desaparece de la vista del work item. Un `&` suelto también puede romper el marcado.
- **Por qué importa:** la tarea se crea con la descripción incompleta o deformada, justo en las partes técnicas que la IA debía aportar. No es una vulnerabilidad seria (Azure DevOps sanea el HTML), es pérdida de contenido.
- **Propuesta:** `html.escape()` sobre cada valor antes de interpolarlo (salvo las etiquetas que arma el propio script).
- **Esfuerzo:** S
- **Prioridad:** media
- **Riesgo de no hacerlo:** tareas con descripciones técnicas recortadas sin que nadie lo note.


### 10. Los extractores devuelven un archivo "completo" aunque hayan fallado lotes
- **Dónde:** `tasks_bugs_extractor.py:51-57` (`continue` tras un error de lote), `:66-76` (los padres se piden en una sola URL sin lotes; un error devuelve `{}`), `tasks_extractor.py:85-88`, `issues_extractor.py:52` (todos los IDs en una sola URL), `:93-104` (una petición por work item, errores convertidos en el texto `Error fetching comments`).
- **Qué pasa:** si un lote falla, se imprime el error y se sigue; al final se escribe el Excel y se anuncia éxito (`tasks_bugs_extractor.py:195`). Quien lo abre no sabe que le faltan filas. `fetch_parent_titles` manda todos los IDs de padres juntos; la API de work items limita la cantidad de IDs por llamada (200, por mi conocimiento del servicio; no verificado), así que con muchos padres devolvería error y todos los títulos saldrían como `N/A` (`:182`). `issues_extractor.py` no usa lotes en absoluto.
- **Propuesta:** contar lotes fallidos y terminar con código de salida distinto de cero y un mensaje con el número de filas faltantes; partir en lotes de 200 también en `fetch_parent_titles` y `issues_extractor.py`.
- **Esfuerzo:** S
- **Prioridad:** media
- **Riesgo de no hacerlo:** informes de horas y estados con datos parciales presentados como completos.


### 11. La guía no coincide con el script (la deriva ya está en la spec)
- **Dónde:** `docs/guia-subir-tasks-azure-devops.md` (secciones 3, 5 y 6) frente a `upload_tasks_with_ai.py:40` y `:47`.
- **Qué pasa:** la guía dice que el script lee `tasks.xlsx`; el valor por defecto es `tasks.csv` (`:47`). No menciona `DRY_RUN`, que vale `true` por defecto (`:40`): quien sigue la guía al pie de la letra ejecuta el script y no se crea nada, con una sola línea en consola que lo indica. Tampoco lista `python-dotenv` entre las dependencias (sí está en `requirements.txt`). Está registrado en `.sdf/docs/guia-subir-tasks-azure-devops/spec.md`.
- **Propuesta:** actualizar la guía como un cambio SDF propio (`actualizar-guia-subir-tasks-azure-devops`). El comportamiento del modo prueba es bueno y debe quedar documentado, no cambiado.
- **Esfuerzo:** S
- **Prioridad:** media
- **Riesgo de no hacerlo:** primer uso fallido o, al revés, quien descubre `DRY_RUN=false` sin entender el modo.


### 12. `UserStoryID` leído como número decimal no se enlaza y el aviso engaña
- **Dónde:** `upload_tasks_with_ai.py:420-423`.
- **Qué pasa:** `str(user_story_id).strip().isdigit()` es falso para `"2035.0"`. Si la columna se lee como decimal (cualquier celda vacía en la columna lo provoca en pandas), la tarea se crea pero no se enlaza, y el mensaje dice que el ID es "un placeholder US-EPICx". No verificado con los archivos reales.
- **Propuesta:** normalizar con `int(float(valor))` dentro de un `try`, y decir en el mensaje el valor leído.
- **Esfuerzo:** S
- **Prioridad:** baja
- **Riesgo de no hacerlo:** tareas huérfanas con una explicación equivocada.


### 13. Valores por defecto de producción en un extractor, y cambio de organización editando código
- **Dónde:** `tasks_bugs_extractor.py:13-14` (`or 'BlacknBlue'`, `or 'Black and Blue'`); `create_user_stories.py:6-9` (otra organización comentada junto a la activa).
- **Qué pasa:** si falta `ORGANIZATION` o `PROJECT`, el extractor apunta en silencio a la organización real, mientras que `upload_tasks_with_ai.py:23-24` falla con un error. En `create_user_stories.py` se cambia de organización comentando y descomentando líneas.
- **Por qué importa:** el script que **crea** work items es el más delicado y es el que más depende de editar código para apuntar al sitio correcto.
- **Propuesta:** el mismo comportamiento en todos: sin `ORGANIZATION`/`PROJECT` en el entorno, error. Mostrar organización y proyecto de destino en la primera línea de cada ejecución.
- **Esfuerzo:** S
- **Prioridad:** baja
- **Riesgo de no hacerlo:** una carga en el proyecto equivocado.


### 14. El prompt de la IA describe `Auth` de forma incorrecta
- **Dónde:** `upload_tasks_with_ai.py:196` ("utiliza OAuth 2.0 para permitir el inicio de sesión con email y password").
- **Qué pasa:** el servicio `bnb-auth` autentica con usuario y contraseña (bcrypt) y emite JWT HS256 propios (ver `../bnb-auth/app/domain/use_cases/authenticate_user.py` y `../bnb-auth/app/domain/services/jwt_service.py`); no usa OAuth 2.0 ni email. El resto de las descripciones del prompt (`:190-200`) no las contrasté con el código.
- **Por qué importa:** las tareas de módulo `Auth Backend` salen con descripciones y criterios de aceptación que asumen un flujo OAuth que no existe.
- **Propuesta:** corregir la línea 196 y revisar el resto del contexto contra el estado real; a largo plazo, leer ese contexto de un archivo `contexto-proyecto.md` en lugar de tenerlo dentro del código.
- **Esfuerzo:** S
- **Prioridad:** baja
- **Riesgo de no hacerlo:** contenido generado que desvía a quien implementa.

---

## Refactor

### 15. `upload_tasks_with_ai.py` hace todo al importarse y `create_task` mezcla seis responsabilidades
- **Dónde:** `upload_tasks_with_ai.py:12-28` (configuración y `raise` a nivel de módulo), `:75-83` (lectura de archivos), `:454-473` (bucle y exportación), `:294-451` (`create_task`, 157 líneas).
- **Qué pasa:** no hay `main()` ni `if __name__ == '__main__'`: importar el módulo (por ejemplo desde una prueba) lee `.env`, exige credenciales y recorre el archivo. `create_task` valida la estimación, llama a la IA, arma HTML, decide el modo de prueba, crea la tarea y la enlaza. `tasks_bugs_extractor.py:79-200` ya muestra el patrón correcto (`main()` con funciones pequeñas).
- **Por qué importa:** impide probarlo (hallazgo 19) y obliga a leer 157 líneas para cambiar una. 
- **Propuesta:** envolver en `main()`; separar `build_description(...)`, `create_work_item(...)`, `link_to_user_story(...)`. No cambiar comportamiento.
- **Esfuerzo:** M
- **Prioridad:** media
- **Riesgo de no hacerlo:** cada cambio al script es manual y sin red de seguridad.
- **Contra:** el archivo tiene cambios sin commitear: hacerlo después de que el propietario los confirme, para no mezclar.

### 16. Cuatro extractores que se solapan, con configuración repetida
- **Dónde:** `tasks_extractor.py`, `issues_extractor.py`, `tasks_bugs_extractor.py`, `create_user_stories.py` (organización y proyecto fijos en `:7-8`, `:7-8`, `:13-14`, `:8-9`).
- **Qué pasa:** `tasks_bugs_extractor.py` cubre `Task`, `Bug` e `Issue`, con lotes, títulos de padres y configuración por `.env`; supera a `tasks_extractor.py` y a la parte de issues de `issues_extractor.py`. Lo único que el nuevo no hace es traer los comentarios (`issues_extractor.py:89-104`). Los cinco scripts repiten el armado de `HTTPBasicAuth('', pat)` y las URL.
- **Propuesta:** archivar o eliminar `tasks_extractor.py` y `issues_extractor.py` (están en git) tras pasar los comentarios al extractor nuevo si hacen falta; crear un módulo `ado.py` de ~30 líneas con sesión autenticada, timeout y lotes.
- **Esfuerzo:** S (eliminar) / M (módulo común)
- **Prioridad:** media
- **Riesgo de no hacerlo:** el hallazgo 1 sigue vivo mientras existan los scripts con `pat = ''`.
- **Contra:** para una utilidad de un solo usuario, un módulo común puede ser más estructura que el problema; eliminar los dos scripts viejos ya da la mayor parte del beneficio.

### 17. La cadena de recuperación del JSON de la IA es larga para un caso que quizá ya no ocurre
- **Dónde:** `upload_tasks_with_ai.py:105-174` (limpieza de bloques de código, recorte de llaves, saneo de barras, extracción por expresiones regulares), junto a `:234` (`response_format: json_object`) y `:176` (4 reintentos).
- **Qué pasa:** hay cuatro capas de reparación de JSON. La última (`_regex_fallback_extract`) entrega contenido parcial y puede desalinear campos si el texto trae comillas internas.
- **Propuesta:** instrumentar cuántas tareas llegan a cada capa durante dos o tres cargas (un contador impreso al final) y eliminar las que no se usen.
- **Esfuerzo:** S
- **Prioridad:** baja
- **Riesgo de no hacerlo:** código difícil de razonar; sin impacto en el resultado.
- **Contra:** estas capas existen porque el modelo falló en algún momento (el comentario de `:121-122` cita rutas de Windows); sin medir, quitarlas puede reintroducir fallos.

### 18. Salidas con nombre fijo, sobrescritas en cada ejecución
- **Dónde:** `upload_tasks_with_ai.py:470` (`created_tasks.xlsx`), `tasks_bugs_extractor.py:38`, `issues_extractor.py:113`, `tasks_extractor.py:112`.
- **Qué pasa:** cada ejecución pisa la anterior. En el caso de la carga, es el único registro de qué IDs se crearon (hallazgo 6).
- **Propuesta:** nombre con marca de tiempo (`created_tasks_2026-10-05T1530.xlsx`) en una carpeta `salidas/` ignorada por git.
- **Esfuerzo:** S
- **Prioridad:** baja
- **Riesgo de no hacerlo:** pérdida de trazabilidad.

---

## Pruebas

### 19. No hay pruebas, y la única protección contra escribir en producción (`DRY_RUN`) no está comprobada
- **Dónde:** no existe carpeta `tests/`; `requirements.txt` no incluye `pytest`.
- **Qué pasa:** ningún comportamiento se verifica automáticamente. Lo más valioso a cubrir, todo puro y sin red: que con `DRY_RUN` activo **no** se llame a `requests.post`/`patch` de Azure DevOps (`:375-389`), el reparto 70/30 de la estimación (`:309-310`), la lectura de estimaciones con coma decimal (`:299-306`), `_try_parse_json`/`_as_list`/`_html_list`, la resolución de `INPUT_FILE` con comas y comodines (`:49-58`) y el filtro de IDs enlazables (`:420`).
- **Propuesta:** `pytest` con `requests` simulado; primero el hallazgo 15 (sin `main()` el módulo no se puede importar sin efectos).
- **Esfuerzo:** M
- **Prioridad:** media
- **Riesgo de no hacerlo:** un cambio de rutina en el script puede romper el modo prueba y el siguiente "ensayo" crear tareas reales.

---

## Implementaciones futuras

### 20. Cerrar el flujo historia → tareas
- **Dónde:** `create_user_stories.py:14` (archivo fijo `./user_stories.csv`, sin modo prueba, sin `.env`) frente a `upload_tasks_with_ai.py:40-47` (modo prueba, `INPUT_FILE` con comodines); `upload_tasks_with_ai.py:420-423` (aviso de marcadores `US-EPICx` que hay que sustituir a mano antes de LIVE).
- **Qué pasa:** el flujo previsto es crear las historias (`[KeyResult]`) y luego las tareas enlazadas a su ID. El script de tareas ya se modernizó (modo prueba, varios archivos por épica); el de historias no, y los IDs devueltos (`created_user_stories.xlsx`, `create_user_stories.py:93`) hay que copiarlos a mano al archivo de tareas.
- **Propuesta:** darle a `create_user_stories.py` el mismo tratamiento (`.env`, `DRY_RUN`, apéndice a la salida) y un paso que sustituya los marcadores `US-EPICx` del archivo de tareas por los IDs creados.
- **Esfuerzo:** M
- **Prioridad:** media
- **Riesgo de no hacerlo:** un copia-pega manual de IDs en cada épica, con la posibilidad de enlazar la tarea a la historia equivocada.

### 21. Validación previa al envío
- **Dónde:** `docs/guia-subir-tasks-azure-devops.md` sección 7 (lista como causas de fallo: sprint inexistente, `AssignedTo` inválido, historia inaccesible).
- **Qué pasa:** esos tres fallos se descubren hoy tarea por tarea, después de haber gastado la llamada a la IA (`:314` precede a `:392`).
- **Propuesta:** en modo prueba, consultar a la API la existencia de cada iteración, usuario e historia distintos del archivo y listar los problemas antes de generar contenido con IA.
- **Esfuerzo:** M
- **Prioridad:** media
- **Riesgo de no hacerlo:** cargas que fallan a la mitad por datos de entrada que se podían comprobar antes.

---

## Orden sugerido

1. Hallazgo 6 (resiliencia y duplicados) y 7 (timeouts): son los dos que evitan daño en el tracker real.
2. Hallazgos 1 y 3: dejar de poder publicar el PAT por accidente y limpiar el repo; combinan con eliminar los dos extractores antiguos (16).
3. Hallazgo 2: decidir la política de datos hacia DeepSeek antes de la próxima carga grande.
4. Hallazgos 8, 9, 10, 11.
5. Pruebas (19) precedidas de la separación en funciones (15).

## Lo que no verifiqué

- Ningún script se ejecutó. Los comportamientos de Azure DevOps (respuesta 203 con PAT inválido, límite de 200 IDs) son de conocimiento del servicio, no observados aquí.
- El contenido de `venv/` (no se leyó por indicación), de `.omc/` y de los archivos de datos más allá de sus cabeceras.
- Si existe una política de la organización sobre proveedores de IA externos (hallazgo 2).
- Si `UserStoryID` se lee como decimal con los archivos reales (hallazgo 12).
- Las diferencias exactas entre `HEAD` y el árbol de trabajo en los dos archivos con cambios sin commitear.
