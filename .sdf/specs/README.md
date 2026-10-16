# specs/ — plantillas del framework

Esta carpeta contiene ÚNICAMENTE las plantillas. Las specs reales de cada documento viven en `.sdf/docs/<id>/spec.md`, la carpeta espejo de su documento `docs/<id>.<ext>`. No editar las plantillas al usarlas: copiarlas al destino y rellenarlas.

| Plantilla | Se copia a | Cuándo |
|-----------|-----------|--------|
| `proposal.md` | `.sdf/docs/<id>/changes/AAAA-MM-DD-<id-cambio>/proposal.md` | Siempre, al abrir un cambio |
| `tasks.md` | misma carpeta del cambio | Siempre, al abrir un cambio |
| `design.md` | misma carpeta del cambio | Solo cambios complejos (opcional) |
| `spec-documento.md` | `.sdf/docs/<id>/spec.md` | Al crear o adoptar un documento |
| `entidad.md` | `wiki/<comunidad>/<slug>.md` | Páginas de la wiki (personas, empresas, bienes-recursos, entregables-metas; extensiones lugares, decisiones, conceptos, normas) |
| `reunion.md` | `wiki/reuniones/AAAA-MM-DD-<slug>.md` | Al crear la página de una reunión |
| `correo.md` | `wiki/correos/AAAA-MM-DD-<slug-asunto>.md` | Al crear la página de un hilo de correo |
| `riesgo.md` | `wiki/riesgos/<slug>.md` | Al registrar un riesgo (extensión activa) |
| `bitacora.md` | `wiki/bitacora/AAAA-Wnn.md` | Recap semanal (extensión activa) |
| `memoria.md` | `.sdf/MEMORY.md` | La genera /sdf-init; se mantiene en modo delta al cierre |
| `feedback.md` | `.sdf/FRAMEWORK-FEEDBACK.md` | Al registrar la primera propuesta de mejora del framework |
| `review.md` | `.sdf/REVIEW.md` | Al primer hallazgo que la IA no puede resolver sola (contradicción, entidad dudosa, relación fuera de vocabulario) |
| `checklist.sh` | (no se copia: se ejecuta aquí) | Verificación mecánica del cierre: `bash .sdf/specs/checklist.sh <id-doc>` |
