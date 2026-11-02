# Wiki Log

<!-- Format follows karpathy-llm-wiki (Astro-Han, eafcc77) log entries: ## [YYYY-MM-DD] <action> | <subject>. Append-only, newest at the bottom. -->

## [2026-11-02] ingest | Unraid storage, containers, Tailscale and settings
- Disposition: New
- Raw: raw/unraid/array-overview.md; raw/unraid/cache-pools.md; raw/unraid/zfs-storage.md; raw/unraid/shares.md; raw/unraid/docker-managing-containers.md; raw/unraid/vm-setup.md; raw/unraid/tailscale.md; raw/tailscale/unraid.md; raw/unraid/customize-settings-notifications-ups.md
- Pages: unraid-array-parity, unraid-pools-zfs, unraid-shares, unraid-docker-vms, unraid-tailscale, unraid-notifications-ups

## [2026-11-02] ingest | Ollama API, Modelfile, server and GPUs
- Disposition: New; Disputed
- Raw: raw/ollama/api.md; raw/ollama/openai-compatibility.md; raw/ollama/modelfile.md; raw/ollama/faq.md; raw/ollama/gpu.md; raw/ollama/docker.md
- Pages: ollama-api, ollama-modelfile, ollama-server-gpu
- Disputed: default context window — FAQ says 4096 tokens, Modelfile table says num_ctx Default: 2048 (Status: Disputed block on ollama-server-gpu)

## [2026-11-02] ingest | Syncthing folders, versioning, ignores and firewall
- Disposition: New
- Raw: raw/syncthing/getting-started.md; raw/syncthing/foldertypes.md; raw/syncthing/versioning.md; raw/syncthing/ignoring.md; raw/syncthing/firewall.md
- Pages: syncthing-folders-versioning, syncthing-ignore-firewall

## [2026-11-02] ingest | Tailscale exit nodes, subnet routers, ACLs, SSH, MagicDNS
- Disposition: New; Update
- Raw: raw/tailscale/exit-nodes.md; raw/tailscale/subnet-routers.md; raw/tailscale/acls.md; raw/tailscale/tailscale-ssh.md; raw/tailscale/magicdns.md
- Pages: tailscale-exit-nodes-subnets, tailscale-acls-ssh, tailscale-magicdns
- Updated: unraid-tailscale (cross-links to exit nodes)

## [2026-11-02] ingest | Claude Code settings, permissions, hooks, skills, subagents, memory, MCP, sandboxing
- Disposition: New
- Raw: raw/claude-code/settings.md; raw/claude-code/permissions.md; raw/claude-code/hooks.md; raw/claude-code/skills.md; raw/claude-code/sub-agents.md; raw/claude-code/memory.md; raw/claude-code/mcp.md; raw/claude-code/sandboxing.md
- Pages: claude-code-settings-permissions, claude-code-hooks, claude-code-skills-subagents, claude-code-memory, claude-code-mcp, claude-code-sandboxing

## [2026-11-02] ingest | Denon AVR-X1700H owner's manual
- Disposition: New
- Raw: raw/manual/denon-avr-x1700h-owners-manual.txt (from raw/manual/denon-avr-x1700h-owners-manual.pdf)
- Pages: avr-setup

## [2026-11-02] ingest | QMD README
- Disposition: New
- Raw: raw/qmd/README.md
- Pages: qmd-search

## [2026-11-02] ingest | LAB-STATE (fictional lab77)
- Disposition: New
- Raw: raw/lab/LAB-STATE.md
- Pages: atlas, tank, apc-1, hermes, titan, pebble, gate, aria, plex, reverse-proxy, syncthing, tailscale, ollama-endpoint, rclone-backup, wiki-search
- Updated: qmd-search (link to hermes and wiki-search)

## [2026-11-02] lint | 0 issues found, 0 auto-fixed (bin/lint-wiki.py: 0 errors; 14 lab pages below the 150-word target)
