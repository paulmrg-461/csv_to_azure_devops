# Groq

- **Comunidad:** empresas
- **Alias:** Groq API, GroqCloud
- **Actualizado:** 2026-10-16

## Resumen

Proveedor de IA alternativo con contrato OpenAI-compatible que el script usa para enriquecer cada Task cuando `AI_PROVIDER=groq`. Es el proveedor activo en el `.env` local del proyecto.

## Hechos

- Endpoint `https://api.groq.com/openai/v1/chat/completions` · desde 2026-10-16 · hasta desconocido · [script](../../upload_tasks_with_ai.py)
- Clave en `GROQ_API_KEY` · desde 2026-10-16 · hasta desconocido · [.env.example](../../.env.example)
- Modelo válido en la cuenta del proyecto: `openai/gpt-oss-120b` · desde 2026-10-16 · hasta desconocido · [script](../../upload_tasks_with_ai.py)

## Relaciones

- provee a: [upload_tasks_with_ai.py](../bienes-recursos/upload-tasks-with-ai.md) — texto de descripción, actividades y criterios

## Aparece en

- [guía](../../docs/guia-subir-tasks-azure-devops.md)

## Notas e historial

- 2026-10-16 — `llama-3.3-70b-versatile` devuelve 404 `model_not_found` en esta cuenta; se usa `openai/gpt-oss-120b`. El valor de la clave no se lee ni se reproduce.
