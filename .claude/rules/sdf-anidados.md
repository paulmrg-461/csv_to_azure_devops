---
paths: */.sdf/**,*/AGENTS.md,*/.sdf-dev.json,*/.specify/**,*/openspec/**
---

# Reglas de sub-proyectos anidados (carga automática al trabajar aquí)

Se activa al tocar el `.sdf/` de una subcarpeta, o su `AGENTS.md` si es v4 o anterior: sub-proyecto SDF anidado. Detalle completo (traspaso, representación en el padre): módulo `.sdf/reglas/anidados.md`.

1. **Caja negra hacia adentro.** El padre no gobierna este interior: no lo inventaría, no lo ingesta a su wiki, no audita ni ejecuta nada aquí por iniciativa propia.
2. **Trabajo cruzado.** Si desde el padre te piden tocar algo aquí, sugiere abrir sesión en esta subcarpeta; si insisten, aplica el `.sdf/AGENTS.md` DE ESTE sub-proyecto (cierre incluido) — nunca el del padre — sin registrar nada en su wiki.
3. **Hacia afuera.** Este sub-proyecto no lee ni escribe fuera de su propia raíz.
4. **Instalación nueva aquí:** sugiere correr `sdf-graph` en el padre para que registre el sub-proyecto y ejecute el traspaso de lo ya ingestado.
