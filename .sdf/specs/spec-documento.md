# Spec: <título del documento>

- **Id:** <id-documento>
- **Archivo:** `docs/<id-documento>.<ext>`
- **Formato:** Word | Excel | PowerPoint | PDF
- **Estado:** vigente | borrador | obsoleto
- **Creado:** AAAA-MM-DD
- **Última actualización:** AAAA-MM-DD

## Propósito

Qué problema resuelve este documento y para qué se usa.

## Audiencia

A quién va dirigido y qué necesita entender o decidir al leerlo.

## Requisitos

Lo que el documento DEBE cumplir. Redactar como requisitos verificables (que alguien pueda comprobar abriendo el documento).

- El documento DEBE ...
- El documento DEBE ...
- El documento NO DEBE ...

## Estructura y contenido

Descripción del contenido ACTUAL del documento, en la unidad natural del formato
(ver "Guía por tipo de documento" en `AGENTS.md`):

- Word → sección por sección
- Excel → hoja por hoja (columnas, fórmulas, gráficos)
- PowerPoint → slide por slide (título, mensaje clave, visual)
- PDF → según su formato de origen

1. **<Sección/Hoja/Slide 1>:** ...
2. **<Sección/Hoja/Slide 2>:** ...

## Formato y estilo

Particularidades visuales o de formato de ESTE documento que se aparten o precisen los estándares de `project.md` (plantilla usada, paleta, orientación, tamaños). Eliminar si aplica solo el estándar general.

## Fuentes de datos

De dónde salen las cifras, textos o referencias (archivos fuente, URLs, conversaciones, criterio del usuario). Indicar fecha de corte de los datos si aplica.

## Decisiones

Razonamiento capturado de las conversaciones con el usuario. Formato: decisión, por qué, alternativas descartadas.

- **AAAA-MM-DD — <decisión>:** por qué se tomó; qué se descartó.

## Registro de cambios

| Fecha | Cambio (carpeta en changes/) | Resumen |
|-------|------------------------------|---------|
| AAAA-MM-DD | AAAA-MM-DD-crear-<id-documento> | Creación inicial |
