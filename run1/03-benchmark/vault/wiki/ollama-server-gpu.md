---
tags: [ollama, server, gpu, docker, environment-variables]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/ollama/faq.md, raw/ollama/gpu.md, raw/ollama/docker.md]
---
# Ollama server configuration, GPUs and Docker

## Server environment variables
The server is configured with environment variables: on Mac `launchctl setenv OLLAMA_HOST "0.0.0.0:11434"` then restart the app; on Linux `systemctl edit ollama.service` and add `Environment="OLLAMA_HOST=0.0.0.0:11434"` under `[Service]`, then `systemctl daemon-reload` and `systemctl restart ollama`; on Windows quit Ollama, edit the account's environment variables, restart from the Start menu.
- Ollama binds 127.0.0.1 port 11434 by default; change it with `OLLAMA_HOST` to expose it on the network.
- `OLLAMA_CONTEXT_LENGTH` — default context window is 4096 tokens (e.g. `OLLAMA_CONTEXT_LENGTH=8192 ollama serve`).
- `OLLAMA_MODELS` — model directory; defaults macOS `~/.ollama/models`, Linux `/usr/share/ollama/.ollama/models`, Windows `C:\Users\%username%\.ollama\models`.
- `OLLAMA_KEEP_ALIVE` — models stay in memory 5 minutes by default; the API `keep_alive` (e.g. "10m", 3600, -1, 0) overrides it; `ollama stop llama3.2` unloads now.
- `OLLAMA_MAX_LOADED_MODELS` (default 3 \* the number of GPUs or 3 for CPU), `OLLAMA_NUM_PARALLEL` (default 1), `OLLAMA_MAX_QUEUE` (default 512; overload returns a 503 error).
- `OLLAMA_FLASH_ATTENTION=1` forces Flash Attention on, `=0` disables it.

> **Status: Disputed**
> The FAQ says the default context window is 4096 tokens; the Modelfile reference table lists `num_ctx` (Default: 2048). See [[ollama-modelfile]].

`ollama ps` shows where a model is loaded: `100% GPU`, `100% CPU`, or split like `48%/52% CPU/GPU`.

## GPUs
- **Nvidia**: compute capability 5.0+ and driver 550 and newer (5.0 through 6.2 need 570 or newer). Limit GPUs with `CUDA_VISIBLE_DEVICES` (UUIDs from `nvidia-smi -L`; "-1" forces CPU). After Linux suspend/resume: `sudo rmmod nvidia_uvm && sudo modprobe nvidia_uvm`.
- **Metal** on Apple devices.
- **Vulkan** (Windows and Linux, enabled by default when the backend is installed; Windows drivers usually bundle it; Linux Intel and AMD need extra components). Select devices with `GGML_VK_VISIBLE_DEVICES` (e.g. `GGML_VK_VISIBLE_DEVICES=1` for the discrete GPU on mixed iGPU/dGPU systems); disable with `OLLAMA_VULKAN=0` or `GGML_VK_VISIBLE_DEVICES=-1`. VRAM reporting needs root or `sudo setcap cap_perfmon+ep /usr/local/bin/ollama`.

## Docker
- CPU only: `docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama`
- Nvidia: install the NVIDIA Container Toolkit, `sudo nvidia-ctk runtime configure --runtime=docker`, then add `--gpus=all`.
- AMD: image tag `ollama/ollama:rocm` with `--device /dev/kfd --device /dev/dri`.
- Vulkan is bundled in the `ollama/ollama` image.
- Run a model: `docker exec -it ollama ollama run llama3.2`

derived_from:: [[raw/ollama/faq.md]]
derived_from:: [[raw/ollama/gpu.md]]
derived_from:: [[raw/ollama/docker.md]]
