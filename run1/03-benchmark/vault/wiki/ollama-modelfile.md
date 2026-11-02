---
tags: [ollama, modelfile, parameters]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/ollama/modelfile.md]
---
# Ollama Modelfile

A Modelfile is the blueprint to create and share customized models. Format: `INSTRUCTION arguments`, `#` for comments; the **`Modelfile` is not case sensitive** and instructions can be in any order.

## Instructions
| Instruction | Purpose |
|---|---|
| `FROM` (required) | base model: `FROM llama3.2`, a Safetensors directory, or a GGUF file `FROM ./ollama-model.gguf` (split GGUF: `FROM ./model-*.gguf`) |
| `PARAMETER` | `PARAMETER <parameter> <parametervalue>` |
| `TEMPLATE` | full prompt template in Go template syntax; variables `{{ .System }}`, `{{ .Prompt }}`, `{{ .Response }}` |
| `SYSTEM` | system message |
| `LICENSE` | legal license text |
| `MESSAGE` | message history; roles system, user, assistant |
| `REQUIRES` | minimum Ollama version (e.g. 0.14.0) |
| `CAPABILITY` | adds a capability, e.g. `CAPABILITY decision` |

## Common parameters (defaults from the reference table)
- `num_ctx`: context window size (Default: 2048); example num\_ctx 4096.
- `repeat_last_n` (Default: 64, 0 = disabled, -1 = num\_ctx); `repeat_penalty` (Default: 1.0, disabled).
- `temperature` (Default: 0.8); `seed` (Default: 0); `num_predict` (Default: -1, infinite generation).
- `top_k` (Default: 40); `top_p` (Default: 0.9).
- `stop`: stop sequences; several `stop` parameters may be set.
- `draft_num_predict`: speculative draft tokens; separate draft models default to 4; 0 disables.

## Workflow
1. Save a file named `Modelfile`, e.g. `FROM llama3.2`, `PARAMETER temperature 1`, `PARAMETER num_ctx 4096`, `SYSTEM You are Mario from super mario bros, acting as an assistant.`
2. `ollama create choose-a-model-name -f <location of the file e.g. ./Modelfile>`
3. `ollama run choose-a-model-name`

View an existing model's Modelfile with `ollama show --modelfile llama3.2`. Setting `num_ctx` this way is also how to change context size for OpenAI-compatible clients ([[ollama-api]]).

derived_from:: [[raw/ollama/modelfile.md]]
