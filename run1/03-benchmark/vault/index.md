# Index

Every wiki page, one line each, grouped by category. Paths are relative to the vault root (`wiki/<slug>.md`). Lab pages describe the fictional home lab "lab77"; their `depends_on::` lines say what each subject needs.

## Lab — hosts
- [[atlas]] `wiki/atlas.md` — Unraid server at 10.77.0.10; hosts tank, hermes, Plex, Caddy, Syncthing, Tailscale exit node, nightly backup; powered via apc-1.
- [[hermes]] `wiki/hermes.md` — Debian VM on atlas (10.77.0.20); wiki repo /srv/wiki and the wiki search service; index timer at 02:30.
- [[titan]] `wiki/titan.md` — Windows gaming PC (10.77.0.30); runs Ollama on an Intel Arc GPU via Vulkan.

## Lab — devices and network
- [[apc-1]] `wiki/apc-1.md` — UPS powering atlas; clean shutdown after 5 minutes on battery; battery replacement pending.
- [[gate]] `wiki/gate.md` — UniFi gateway at 10.77.0.1; the lab's only route to the internet; DHCP only for aria.
- [[pebble]] `wiki/pebble.md` — MacBook; remote access only through Tailscale via atlas; receives the Syncthing notes folder.
- [[aria]] `wiki/aria.md` — living-room Denon AVR-X1700H at 10.77.0.40; network address from gate.

## Lab — storage
- [[tank]] `wiki/tank.md` — ZFS pool inside atlas with shares appdata, media, domains, notes.

## Lab — services
- [[plex]] `wiki/plex.md` — Plex Docker container on atlas; library and appdata on tank.
- [[reverse-proxy]] `wiki/reverse-proxy.md` — Caddy container on atlas fronting Plex and wiki search on port 443; outside access via gate.
- [[syncthing]] `wiki/syncthing.md` — Syncthing container on atlas syncing tank/notes to pebble over Tailscale only.
- [[tailscale]] `wiki/tailscale.md` — Tailscale Unraid plugin on atlas; only exit node; subnet route 10.77.0.0/24.
- [[ollama-endpoint]] `wiki/ollama-endpoint.md` — Ollama endpoint on titan (port 11434) used for wiki embeddings.
- [[rclone-backup]] `wiki/rclone-backup.md` — nightly rclone job on atlas at 06:00 reading the 05:45 tank snapshot.
- [[wiki-search]] `wiki/wiki-search.md` — qmd wiki search service on hermes; embeddings from titan's Ollama.

## Unraid
- [[unraid-array-parity]] `wiki/unraid-array-parity.md` — array, parity rules, start/stop, write modes (md_write_method), read speeds.
- [[unraid-pools-zfs]] `wiki/unraid-pools-zfs.md` — cache pools, pool modes, minimum free space, ZFS pools, RAIDZ expansion, ARC RAM.
- [[unraid-shares]] `wiki/unraid-shares.md` — user vs disk shares, /mnt paths, primary/secondary storage, allocation methods, default shares.
- [[unraid-docker-vms]] `wiki/unraid-docker-vms.md` — container network/volume/port settings, autostart order and wait, VM Manager, snapshots.
- [[unraid-tailscale]] `wiki/unraid-tailscale.md` — Tailscale plugin install, exit node/subnet routes on Unraid, Tailscale in containers, userspace networking.
- [[unraid-notifications-ups]] `wiki/unraid-notifications-ups.md` — UPS settings, notification settings, SMTP, notification agents, scheduler, power mode.

## Ollama
- [[ollama-api]] `wiki/ollama-api.md` — base URLs, cloud vs local, OpenAI-compatible endpoints and limits, /v1/responses, context size.
- [[ollama-modelfile]] `wiki/ollama-modelfile.md` — Modelfile instructions, parameters and defaults, ollama create/show.
- [[ollama-server-gpu]] `wiki/ollama-server-gpu.md` — server environment variables, keep-alive, concurrency, Nvidia/Metal/Vulkan GPUs, Docker commands.

## Syncthing
- [[syncthing-folders-versioning]] `wiki/syncthing-folders-versioning.md` — getting started, device IDs, folder types, file versioning strategies.
- [[syncthing-ignore-firewall]] `wiki/syncthing-ignore-firewall.md` — .stignore patterns, ports 22000/21027, port forwarding, remote GUI.

## Tailscale
- [[tailscale-exit-nodes-subnets]] `wiki/tailscale-exit-nodes-subnets.md` — exit nodes (advertise, approve, grant, use) and subnet routers (IP forwarding, routes, SNAT).
- [[tailscale-acls-ssh]] `wiki/tailscale-acls-ssh.md` — ACL semantics and plan availability; Tailscale SSH setup and ssh rule fields.
- [[tailscale-magicdns]] `wiki/tailscale-magicdns.md` — MagicDNS names, FQDNs, defaults, disabling per device.

## Claude Code
- [[claude-code-settings-permissions]] `wiki/claude-code-settings-permissions.md` — settings files, precedence, permission rules and modes.
- [[claude-code-hooks]] `wiki/claude-code-hooks.md` — hook events, configuration, matchers, handler types, exit codes.
- [[claude-code-skills-subagents]] `wiki/claude-code-skills-subagents.md` — skills (locations, frontmatter) and subagents (built-ins, scopes, fields).
- [[claude-code-memory]] `wiki/claude-code-memory.md` — CLAUDE.md locations and loading, rules, auto memory.
- [[claude-code-mcp]] `wiki/claude-code-mcp.md` — adding/managing MCP servers, timeouts, scopes and precedence.
- [[claude-code-sandboxing]] `wiki/claude-code-sandboxing.md` — sandboxed Bash defaults, modes, filesystem/network settings, protected paths.

## Home theater
- [[avr-setup]] `wiki/avr-setup.md` — Denon AVR-X1700H: ARC/eARC and 8K, speakers, network, Auto Standby, protection circuit, resets.

## Tooling
- [[qmd-search]] `wiki/qmd-search.md` — QMD local search: commands, hybrid pipeline, models, qmd bench.
- `deps/<slug>.md` — generated dependency views for lab pages (Needs / Needed by), rebuilt from the `depends_on::` lines; not hand-written.
- `raw/` — the original sources each page cites in its `derived_from::` lines; read-only.
