<!-- source: https://docs.ollama.com/api.md | fetched: 2026-11-02 | effective-url: https://docs.ollama.com/api/introduction.md -->

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.ollama.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Introduction

Use Ollama's API to build applications with cloud or local models.

## Get started

Call cloud models with an [API key](https://ollama.com/settings/keys). No Ollama installation required. Start with the [API quickstart](https://docs.ollama.com/quickstart.md#build-an-application).

To run models on your computer, [install Ollama and run a local model](https://docs.ollama.com/quickstart.md#run-a-model-locally).

## Base URLs

| API | Direct cloud access | Local Ollama server |
| - | - | - |
| Ollama | `https://ollama.com/api` | `http://localhost:11434/api` |
| OpenAI compatibility | `https://ollama.com/v1` | `http://localhost:11434/v1` |
| Anthropic client base URL | `https://ollama.com` | `http://localhost:11434` |

The Anthropic client appends `/v1/messages` to its base URL.

Cloud requests need an API key. Local requests do not. To use cloud models through your local server, [sign in to Ollama](https://docs.ollama.com/api/authentication.md#signing-in).

Creating or deleting models requires a local Ollama server. For supported API features, see [OpenAI compatibility](https://docs.ollama.com/api/openai-compatibility.md) and [Anthropic compatibility](https://docs.ollama.com/api/anthropic-compatibility.md).

## Ollama API example

Set `OLLAMA_API_KEY` to your [API key](https://ollama.com/settings/keys), then call a cloud model:

```shell theme={"system"}
curl https://ollama.com/api/chat \
  -H "Authorization: Bearer $OLLAMA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma4:31b",
    "messages": [{"role": "user", "content": "Why is the sky blue?"}],
    "stream": false
  }'
```

Read the answer from `message.content`. For local inference, use `http://localhost:11434/api/chat` with a downloaded model and omit the authorization header.

## Libraries

Use Ollama's official libraries with either a local server or the hosted API:

* [Python](https://github.com/ollama/ollama-python)
* [JavaScript](https://github.com/ollama/ollama-js)

For direct cloud access, set the host to `https://ollama.com` and supply your API key in the `Authorization: Bearer` header.

Browse [community libraries](https://github.com/ollama/ollama?tab=readme-ov-file#libraries--sdks).

## Versioning

Ollama's API isn't strictly versioned, but the API is expected to be stable and backwards compatible. Deprecations are rare and will be announced in the [release notes](https://github.com/ollama/ollama/releases).
