---
tags: [ollama, api, openai-compatibility]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/ollama/api.md, raw/ollama/openai-compatibility.md]
---
# Ollama API and OpenAI compatibility

## Base URLs
| API | Direct cloud access | Local Ollama server |
|---|---|---|
| Ollama | `https://ollama.com/api` | `http://localhost:11434/api` |
| OpenAI compatibility | `https://ollama.com/v1` | `http://localhost:11434/v1` |
| Anthropic client base URL | `https://ollama.com` | `http://localhost:11434` |

The Anthropic client appends `/v1/messages` to its base URL. Cloud requests need an API key (set `OLLAMA_API_KEY`, sent as `Authorization: Bearer`); local requests do not. Creating or deleting models requires a local Ollama server. For local chat use `http://localhost:11434/api/chat` and read the answer from `message.content`. The API isn't strictly versioned but is expected to be stable and backwards compatible.

## OpenAI-compatible endpoints
Ollama supports a subset of the OpenAI API. With the OpenAI client on a local server use `base_url='http://localhost:11434/v1/'`; an `api_key` value is required but ignored.
- `/v1/chat/completions`: chat, streaming, JSON mode, reproducible outputs, vision (base64 images only, not image URLs), tools, reasoning control; **no** logprobs, `tool_choice`, `logit_bias`, `user` or `n`. `reasoning_effort` / `reasoning.effort` control thinking; use `/api/show` to discover supported values.
- `/v1/completions`: `prompt` currently only accepts a string; `suffix` supported.
- `/v1/models` and `/v1/models/{model}`: `created` is when the model was last modified; `owned_by` defaults to `"library"`.
- `/v1/embeddings`, `/v1/audio/speech`, `/v1/audio/transcriptions`, `/v1/audio/translations`.
- `POST /v1/responses`: added in Ollama v0.13.3; only the non-stateful flavor (no `previous_response_id` or `conversation`).

## Models and context size
Download a model before local use: `ollama pull llama3.2`. Tools that expect default OpenAI names can use a copy: `ollama cp llama3.2 gpt-3.5-turbo`. The OpenAI API has no way to set the context size; create a `Modelfile` with `PARAMETER num_ctx <context size>` and build it with `ollama create mymodel` (see [[ollama-modelfile]]).

derived_from:: [[raw/ollama/api.md]]
derived_from:: [[raw/ollama/openai-compatibility.md]]
