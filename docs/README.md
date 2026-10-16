# docs/

Los documentos gobernados del proyecto, PLANOS: un archivo por documento (`<id>.<ext>`), sin subcarpetas. La especificación y el historial de cada documento viven en la carpeta oculta `.sdf/docs/<id>/` — el espejo de esta carpeta.

```
docs/
├── README.md
└── presupuesto-2026.xlsx        ← el documento final

.sdf/docs/
└── presupuesto-2026/
    ├── spec.md                  ← su especificación (estado actual)
    └── changes/                 ← su historial de cambios
        └── 2026-07-24-crear-presupuesto-2026/   (proposal.md + tasks.md [+ design.md])
```

Reglas para cualquier IA que trabaje aquí:

1. NO crear ni modificar documentos sin un cambio abierto (proposal con Estado: en curso) en `.sdf/docs/<id>/changes/`. Si no existe, crearlo primero con las plantillas de `.sdf/specs/`.
2. Documentos PLANOS: nada de subcarpetas por documento en `docs/`; el nombre base del archivo = el id del documento.
3. Siempre el MISMO archivo: nunca copias `_v2`, `_final` ni versionadas. El historial vive en `.sdf/docs/<id>/changes/`.
4. La spec (`.sdf/docs/<id>/spec.md`) describe el estado ACTUAL del documento: si tocas el documento, actualízala en el mismo cambio.
5. Los cambios con Estado: cerrado son historial INMUTABLE: no editarlos nunca. Correcciones = cambio nuevo. Un solo cambio en curso por documento.
6. Todo documento debe estar en la tabla de Documentos activos de `.sdf/project.md`. Documentos retirados: spec marcada `obsoleto`, no borrada.
7. Al terminar: ejecutar el cierre completo del "Flujo de trabajo obligatorio" de `.sdf/AGENTS.md` (evaluación independiente cuando aplique, wiki y MEMORY al día) en la MISMA respuesta en que se entrega.
