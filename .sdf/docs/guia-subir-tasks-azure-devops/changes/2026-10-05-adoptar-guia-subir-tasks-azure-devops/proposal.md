# Propuesta: adoptar-guia-subir-tasks-azure-devops

- **Fecha:** 2026-10-05
- **Estado:** cerrado
- **Módulos:** flujo.md, tipos-de-documento.md, wiki.md, memoria-y-aprendizaje.md
- **Presupuesto:** estándar ≤80k
- **Evaluación:** no aplica — adopción por ingeniería inversa, sin cambio de contenido del documento
- **Tokens:** ~10k (orquestador estimado; sin subagentes) — dentro del presupuesto
- **Tipo:** adoptar
- **Documento(s) afectado(s):** guia-subir-tasks-azure-devops (adopción)
- **Solicitado por:** Paul Realpe (vía team-lead)

## Qué se pide

Gobernar el documento existente `README.md` con una spec por ingeniería inversa (corolario 2 de `.sdf/AGENTS.md`), sin modificar su contenido.

## Por qué

El documento nació fuera del flujo SDF. Sin spec, cualquier edición futura carece de fuente de verdad y de historial.

## Decisiones de la conversación

- **Contenido intacto:** solo se lee y se describe; la spec se marca como ingeniería inversa.
- **Ubicación:** la guía vivía en `README.md` de la raíz; al ser la portada del repositorio se dejó allí un README mínimo que enlaza a la guía (la guía íntegra pasó a `docs/guia-subir-tasks-azure-devops.md`). Ese README de la raíz está versionado en git, así que aparecerá como modificado.
- **Formato:** Markdown, igual que el origen; no se convierte a otro formato.

## Pendientes / supuestos

- Ninguno bloqueante; las limitaciones de la lectura quedan en la sección Decisiones de la spec.

## Impacto

- Specs a crear: `.sdf/docs/guia-subir-tasks-azure-devops/spec.md`
- Archivos a generar/modificar: `docs/guia-subir-tasks-azure-devops.md` (solo ubicación, contenido sin cambios)
- Tabla de documentos activos en `.sdf/project.md`: sí
