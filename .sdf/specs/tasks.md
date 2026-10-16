# Tareas: <id-cambio>

## 1. Preparación

- [ ] 1.1 Leer `.sdf/project.md` y la(s) spec(s) existente(s) (si aplica)
- [ ] 1.2 Confirmar decisiones pendientes con el usuario
- [ ] 1.3 Recopilar fuentes de datos necesarias

## 2. Ejecución

- [ ] 2.1 Generar/actualizar `docs/<id>.<ext>`
- [ ] 2.2 <paso específico del contenido>
- [ ] 2.3 <paso específico del contenido>

## 3. Cierre

- [ ] 3.1 Crear/actualizar `.sdf/docs/<id>/spec.md` con la plantilla `spec-documento.md` (requisitos, estructura, decisiones, registro de cambios)
- [ ] 3.2 Actualizar tabla de documentos activos en `.sdf/project.md`
- [ ] 3.3 Tanda paralela (mismo turno): `wiki-graph` (wiki + MEMORY delta) y `evaluator` (si documento nuevo o cambio mayor) — hasta PASA (máx. 2 ciclos)
- [ ] 3.4 Capturar aprendizajes: descubrimientos → wiki/glosario; correcciones del usuario → Estándares de `project.md` o spec
- [ ] 3.5 Verificación: `bash .sdf/specs/checklist.sh <id>` (mecánica) + 3 puntos de juicio
- [ ] 3.6 Marcar `proposal.md` con Estado: cerrado y registrar consumo (`.sdf/usage.csv` + campo Tokens)
