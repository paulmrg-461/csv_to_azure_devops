---
name: sdf-sync
description: Sincroniza correos y reuniones del proyecto desde los conectores de correo y calendario
---

Ejecuta la "Sincronización con correo y calendario" del módulo `.sdf/reglas/wiki.md`:

1. Verifica conectores de correo/calendario disponibles. Si no hay, informa al usuario cómo conectarlos y termina.
2. Criterios: nombre del proyecto y alias, glosario de `.sdf/project.md`, personas/empresas con página en la wiki. Ventana: desde la "Última sincronización" de `wiki/INDEX.md` (primera vez: pregunta desde cuándo); en calendario incluye también eventos futuros.
3. Filtra lo claramente relacionado; los dudosos, listarlos al usuario para confirmar.
4. Crea/actualiza páginas con las plantillas `correo.md` y `reunion.md`: SOLO resúmenes y metadatos, NUNCA cuerpos completos. Enlaza participantes a `personas/` y temas a sus entidades.
5. Si algún hilo contiene una transcripción de reunión, procesarla según "Transcripciones de reuniones" del módulo `.sdf/reglas/wiki.md` (preservar como fuente en `transcripciones/`, destilar con `ingestor-fuentes`, enriquecer la página de la reunión). Si es un adjunto no descargable, pedir al usuario que suelte el archivo en la carpeta.
6. Actualiza la fecha de "Última sincronización" en `INDEX.md` y reporta: N hilos, N reuniones, N transcripciones, N personas nuevas.
7. Si el usuario no lo tiene, ofrece programar esta sincronización como tarea recurrente.

Al terminar: registra el consumo de esta acción en `.sdf/usage.csv` (acción `sync`; subagentes medidos por sus notificaciones, orquestador estimado — ver "Contabilidad de tokens" en el módulo `modelos-y-delegacion.md`).
