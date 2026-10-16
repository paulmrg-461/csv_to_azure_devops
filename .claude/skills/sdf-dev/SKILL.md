---
name: sdf-dev
description: Abre o retoma el sub-arnes de desarrollo de esta carpeta: especificacion, tareas y agentes de codigo
---

Abre o retoma un **sub-arnés de desarrollo**: una subcarpeta de aplicación gobernada por Spec Kit u OpenSpec, no por el SDF (regla de frontera del módulo `.sdf/reglas/anidados.md`). Dispara con `/sdf-dev <nombre>` o con una petición de oficina sin el verbo explícito ("haz una aplicación/script/dashboard que...").

## 1. Detectar si ya existe

Busca `.sdf-dev.json` en las subcarpetas de primer nivel. Si `<nombre>` (o el que el usuario describió) ya tiene una, **retómalo**: lee su `AGENTS.md` y sigue trabajando ahí con el framework que declara — no repitas la entrevista ni reinstales nada. Si no existe, sigue al paso 2.

## 2. Una sola tanda, tres preguntas

Nunca preguntes una por una. El usuario de oficina no sabe qué es OpenSpec ni Spec Kit — la pregunta de framework siempre va con la recomendación, nunca desnuda:

1. **Nombre de la subcarpeta**: kebab-case, en la raíz del proyecto, junto a las fuentes — **nunca dentro de `docs/`** (`docs/` es solo para documentos de oficina planos). Propón uno a partir de la petición si el usuario no dio uno.
2. **Framework**, con esta tabla:

   | | OpenSpec | Spec Kit |
   |---|---|---|
   | Recomendado cuando | La app es pequeña o mediana, evoluciona por cambios frecuentes, o ya existe código (brownfield). **Opción por defecto.** | Se pide gobernanza explícita (constitución, fases con puertas, checklists) o el proyecto nace de cero con varios desarrolladores. |
   | Flujo | proponer → aplicar → verificar → archivar, por capacidad | constitución → especificar → clarificar → planear → checklist → tareas → analizar → implementar → converger |
   | Necesita CLI en ejecución | Sí (`openspec status/validate/archive`) | No — Markdown + scripts autocontenidos; la CLI es solo para instalar/actualizar |

   Si el usuario no tiene preferencia, recomienda OpenSpec y explica el porqué en una frase.
3. **Herramientas de IA** con las que se va a trabajar esta subcarpeta (Claude Code, Codex, Antigravity, Gemini CLI — pueden ser varias).

## 3. Materializar: CLI real primero, snapshot después

Con red y el binario (`npx`/`uvx`) o gestor (`npm`/`uv`) disponible, corre la CLI real **dentro de la subcarpeta**, nunca en la raíz:

- **OpenSpec:** `openspec init --tools <herramientas> --profile core --language "Español"`.
- **Spec Kit:** `specify init --here --force --non-interactive --integration <clave> --script sh`, seguido de `specify integration install <otras herramientas>` para las que falten.

Si no hay red o falta el binario/gestor, materializa desde el snapshot vendorizado (`recursos_dev` en `harness-manifest.json`, resuelto en `assets/dev/speckit-1.0.5/` o `assets/dev/openspec-1.12.0/`) y dilo explícitamente: **OpenSpec queda degradado** (su `.tgz` no trae las diez dependencias que necesita en tiempo de ejecución — solo fija la versión, no materializa un proyecto funcional sin `npm install`); **Spec Kit queda completo** (sus plantillas y scripts no dependen de red ni de la CLI). Nunca prometas que un snapshot degradado "ya quedó instalado" — repórtalo como pendiente.

Con Spec Kit sin CLI: copia `templates/` y `scripts/{bash,powershell}/` del snapshot a `.specify/` de la subcarpeta (mismo layout que produce `specify init`).

Con OpenSpec sin CLI: copia el `.tgz` vendorizado a la subcarpeta y deja anotado en `.sdf-dev.json` (`estado_cli: "pendiente"`) que falta `npm install` con red antes de poder usar sus comandos.

## 4. Proyecciones por herramienta de IA elegida

Reusa el generador de la 6.0 (`sdf/tools/generar-proyecciones.sh`/`.ps1`), sin lógica nueva por plataforma — el framework elegido decide el destino de sus propios comandos:

- **Spec Kit:** `.claude/skills/speckit-*` (Claude Code), `.agents/skills/speckit-*` (Codex, Antigravity), `.gemini/commands/speckit.*.toml` (Gemini CLI).
- **OpenSpec:** `.claude/skills/openspec-*` + `.claude/commands/opsx/` (Claude Code), `.agents/skills/openspec-*` (Codex, Antigravity).

## 5. Instalar el puente

Copia `assets/dev/puente/{AGENTS.md,CLAUDE.md,GEMINI.md,.sdf-dev.json}` a la raíz de la subcarpeta, resolviendo sus marcadores `{...}`:

- `{nombre-app}` → el nombre elegido en el paso 2.
- `{framework}` / `{version}` → el framework elegido y su versión de `versiones_minimas`.
- `{prefijo_comandos}` → `/speckit-*` o `/opsx:*` según el framework.
- `{archivo_gobernanza}` → `.specify/memory/constitution.md` (Spec Kit) o el `config.yaml`/equivalente que OpenSpec haya creado.
- En `.sdf-dev.json`: `herramientas` (lista del paso 2), `creado` (fecha real), `estado_cli` (paso 3), `padre.raiz` (ruta relativa real desde la subcarpeta hasta la raíz del proyecto) y `padre.pagina_wiki` (`entregables-metas/<nombre-app>.md` — sección 4.3 del plan v6: los sub-arneses de desarrollo se representan en `entregables-metas/`, no en `proyectos-relacionados/`, que hoy es exclusiva de sub-proyectos SDF anidados, módulo `anidados.md`).

No ofrezcas crear los cuatro agentes (`assets/dev/agentes/{implementador,revisor,probador,investigador}.md`) sin preguntar primero cuáles quiere el usuario. El que elija se proyecta a la subcarpeta con el envoltorio y modelo de cada herramienta ya elegida en el paso 2 (tabla `modelos.por_plataforma` del manifiesto, mismos envoltorios que usan los roles del propio SDF — `frontmatter-yaml` en Claude Code/Antigravity, `toml` en Codex, `frontmatter-yaml` en Gemini CLI — pero resueltos por ti, no por el generador mecánico, porque el destino es esta subcarpeta):

| Agente | Clase de modelo | Destino por herramienta |
|---|---|---|
| `implementador` | estándar | `.claude/agents/implementador.md`, `.codex/agents/implementador.toml`, `.agents/agents/implementador.md`, `.gemini/agents/implementador.md` |
| `revisor` | estándar | igual patrón que arriba |
| `probador` | económico | igual patrón que arriba |
| `investigador` | económico | igual patrón que arriba |

Sin prefijo `sdf-` en el nombre (a diferencia de los agentes del SDF del padre): estos son del sub-arnés, no compiten con nada del árbol compartido del padre.

## 6. Registrar en el padre y cerrar

1. Registra la subcarpeta en **Fuentes de información** de `.sdf/project.md`: `Sub-proyecto de desarrollo: [<nombre-app>](<nombre-app>/) · <framework>` — y recuérdale al usuario correr `/sdf-graph` para que cree su página en `wiki/proyectos-relacionados/` y la excluya de la reconciliación (igual que un SDF anidado).
2. Muestra un resumen: framework elegido y por qué, estado de la CLI (real o pendiente), herramientas de IA proyectadas, agentes creados, y el recordatorio de `/sdf-graph`.
3. Registra el consumo de esta acción en `.sdf/usage.csv` (acción `dev`; ver "Contabilidad de tokens" en `modelos-y-delegacion.md`).
