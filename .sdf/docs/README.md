# .sdf/docs/ — specs e historiales (espejo de docs/)

Una carpeta por documento gobernado, con el mismo id que su archivo en `docs/` (raíz del proyecto):

```
.sdf/docs/<id>/
├── spec.md      ← estado actual del documento docs/<id>.<ext>
└── changes/     ← historial de cambios
    └── AAAA-MM-DD-<id-cambio>/   (proposal.md + tasks.md [+ design.md])
```

- El documento vive plano en `docs/<id>.<ext>`; aquí vive todo lo demás (spec + historial).
- Mover o compartir un documento con su historial = copiar el archivo + su carpeta espejo de aquí.
- Los cambios cerrados no se editan: son el historial inmutable de cómo evolucionó cada documento.
