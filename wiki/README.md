# wiki/

Wiki de conocimiento del proyecto: páginas markdown legibles por humanos, interconectadas con enlaces clicables (markdown relativo) hacia otras páginas y hacia los archivos del proyecto, que representan las entidades y sus relaciones. La mantiene la IA automáticamente al cierre de cada cambio (ver "Wiki del proyecto" en `AGENTS.md`).

```
wiki/
├── INDEX.md             ← portada: directorio de todas las páginas por comunidad
├── personas/            ← equipo, contactos, stakeholders
├── empresas/            ← empresas, organizaciones, instituciones
├── bienes-recursos/     ← bienes, activos, sistemas, presupuestos, materiales
├── entregables-metas/   ← una página por documento de docs/, más metas e hitos
├── reuniones/           ← una página por reunión del proyecto (del calendario o mencionadas)
├── correos/             ← una página por hilo de correo relevante al proyecto
└── proyectos-relacionados/  ← carpetas hermanas y sub-proyectos SDF gobernados
```

- Las siete comunidades del diagrama son el núcleo fijo. Hay un catálogo de extensiones activables por proyecto (`lugares/`, `decisiones/`, `conceptos/`, `riesgos/`, `normas/`, `bitacora/`) — se eligen al inicializar y quedan registradas en `.sdf/project.md`; sus carpetas solo se crean al activarlas. Fuera de eso, comunidades nuevas solo con permiso del usuario.
- `correos/` y `reuniones/` se pueblan sincronizando con los conectores de correo y calendario (pedir "sincroniza la wiki"); ver protocolo en el módulo `.sdf/reglas/wiki.md`. Solo resúmenes y metadatos, nunca cuerpos completos.
- `proyectos-relacionados/` registra carpetas hermanas y sub-proyectos SDF anidados detectados por la reconciliación de fuentes — ver módulo `.sdf/reglas/anidados.md`.
- Plantillas por comunidad (en `.sdf/specs/`): `entidad.md` (personas, empresas, bienes-recursos, entregables-metas, proyectos-relacionados, y extensiones lugares/decisiones/conceptos/normas), `reunion.md`, `correo.md`, `riesgo.md` y `bitacora.md`.
- Visor de grafo interactivo (opcional): `uv tool install graphifyy` (doble "y": nombre del paquete en PyPI; el comando es `graphify`) y luego `graphify ./wiki` — los enlaces markdown se convierten en aristas y obtienes `graph.html`.

## Cómo leer la wiki (para que los enlaces a archivos abran con su aplicación)

Los enlaces son rutas relativas estándar; que un clic abra Word/Excel/Acrobat depende del visor:

- **Obsidian (recomendado):** abre como vault la **carpeta RAÍZ del proyecto**, NO la carpeta `wiki/`. Los enlaces suben niveles (`../../docs/...`), y si el vault es `wiki/`, esos destinos quedan fuera del vault y Obsidian no los abre. Con el vault en la raíz, clic en un xlsx/docx/pdf lo abre con la aplicación por defecto de Windows.
- **Typora:** funciona directo — Ctrl+clic sobre el enlace abre el archivo con su aplicación por defecto.
- Nota v5: los enlaces hacia specs (`../../.sdf/docs/<id>/spec.md`) apuntan a la carpeta oculta `.sdf/`; Obsidian ignora las carpetas ocultas y no los abre (los documentos y fuentes sí abren). Las specs se consultan desde el editor o la sesión de IA.

### Colores por comunidad en el grafo de Obsidian

El skill instala `.obsidian/graph.json` con los grupos ya coloreados por comunidad — abre la carpeta del proyecto como vault y el grafo sale pintado, sin configurar nada. Si tu vault ya existía antes del framework (y Obsidian ya había creado su propio `graph.json`), configúralos una vez a mano: vista de grafo → icono de ajustes → **Groups** → "New group", un grupo por comunidad con consultas `path:` y un color cada una:

- `path:wiki/personas` (p. ej. azul) · `path:wiki/empresas` (naranja) · `path:wiki/bienes-recursos` (verde) · `path:wiki/entregables-metas` (morado) · `path:wiki/reuniones` (amarillo) · `path:wiki/correos` (rojo) · `path:wiki/proyectos-relacionados` (gris) · y las extensiones activas (`path:wiki/conceptos`, `path:wiki/riesgos`, ...).

Se configura una sola vez por vault (queda guardado en `.obsidian/graph.json`). Bonus: en Filters usa `path:wiki` para ver solo la wiki sin el resto de la carpeta.
- **VS Code:** bueno para editar, limitado para navegar — su preview no lanza aplicaciones externas para archivos office. Úsalo para editar páginas y lee la wiki en Obsidian/Typora.
