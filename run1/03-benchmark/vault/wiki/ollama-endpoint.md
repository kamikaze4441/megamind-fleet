---
tags: [lab, service, ollama, llm]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/lab/LAB-STATE.md]
---
# Ollama endpoint on titan

The lab's Ollama endpoint is http://10.77.0.30:11434 on [[titan]]. Ollama runs on titan on its Intel Arc GPU through Vulkan, so the Ollama endpoint needs titan to be awake.

## Who uses it
The [[wiki-search]] service on [[hermes]] calls this endpoint for embeddings. When titan is off, new wiki pages are not embedded but keyword search still works.

## Background
Port 11434 is Ollama's default (see [[ollama-server-gpu]] for `OLLAMA_HOST` and Vulkan device selection, and [[ollama-api]] for the endpoints).

depends_on:: [[titan]] (Ollama runs on titan's Intel Arc GPU; the endpoint needs titan awake)
derived_from:: [[raw/lab/LAB-STATE.md]]
