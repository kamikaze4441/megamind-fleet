---
tags: [lab, host, windows, gpu]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/lab/LAB-STATE.md]
---
# titan (Windows gaming PC)

titan is the Windows gaming PC at 10.77.0.30. It uses a static address.

## Role in the lab
- Ollama runs on titan on its Intel Arc GPU through Vulkan; this is the lab's [[ollama-endpoint]] (http://10.77.0.30:11434). The endpoint needs titan to be awake.
- The [[wiki-search]] service on [[hermes]] calls that endpoint for embeddings, so when titan is off, new wiki pages are not embedded, but keyword search still works.

## Background
Ollama's Vulkan support on Windows and the variables that select Vulkan devices are described in [[ollama-server-gpu]]; the HTTP API the endpoint serves is in [[ollama-api]].

derived_from:: [[raw/lab/LAB-STATE.md]]
