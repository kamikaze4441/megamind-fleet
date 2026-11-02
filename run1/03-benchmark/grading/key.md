# Answer key — golden set run 1 (auditor A1)

As sent to the director on 2026-11-02 (before the wiki existed). Paths are relative to raw/. "p." = PDF page of the manual (= printed page). Slugs for the expected pages are in `expected-pages.tsv` (wiki) and `expected-raw.tsv` (raw).

| qid | expected answer (variants) | source | expected wiki page(s) | tag | grading rule |
|---|---|---|---|---|---|
| Q01 | High-water | unraid/shares.md:291,311 | Unraid shares page | index | exact |
| Q02 | Tunable (md_write_method) (Settings → Disk Settings) | unraid/array-overview.md:164-165 | Unraid array page | deep | exact (`md_write_method` alone OK) |
| Q03 | 10% of the disk's total capacity | unraid/shares.md:172 | Unraid shares page | deep | exact; "2× largest file" (recommendation, not default) → partial |
| Q04 | about 1/8 of total RAM (ARC) | unraid/zfs-storage.md:277 | Unraid ZFS page | paraphrase | exact; "1 GB per TB" (the myth quoted) → wrong |
| Q05 | FROM | ollama/modelfile.md:100 | Ollama Modelfile page | index | exact |
| Q06 | 512; OLLAMA_MAX_QUEUE (overload → 503) | ollama/faq.md:339 (325) | Ollama FAQ/server-config page | deep | both items required; one → partial |
| Q07 | cap_perfmon (`setcap cap_perfmon+ep`) | ollama/gpu.md:166 | Ollama hardware/GPU page | deep | exact |
| Q08 | "Override Changes" | syncthing/foldertypes.md:19 | Syncthing folder-types page | index | exact; "Revert Local Changes" → wrong |
| Q09 | 30 seconds (oldest version per 30 s interval) | syncthing/versioning.md:30 | Syncthing versioning page | deep | exact |
| Q10 | 12 hours (min 1 min, max 168 h) | tailscale/tailscale-ssh.md:184,504 | Tailscale SSH page | index | exact |
| Q11 | October 20, 2022 | tailscale/magicdns.md:21 | Tailscale MagicDNS page | index | exact |
| Q12 | `--exit-node-allow-lan-access` (tailscale up/set; GUI "Allow Local Network Access") | tailscale/exit-nodes.md:62,246 | Tailscale exit-nodes page | paraphrase | exact flag; GUI setting only → partial |
| Q13 | 25,000 tokens (MAX_MCP_OUTPUT_TOKENS; warning at 10,000) | claude-code/mcp.md:1502 (444) | Claude Code MCP page | index | exact; 10,000 → wrong |
| Q14 | 1.5 seconds | claude-code/hooks.md:3582 | Claude Code hooks page | deep | exact; 600 s (general default) → wrong |
| Q15 | four hops (max depth 4) | claude-code/memory.md:106 | Claude Code memory/CLAUDE.md page | deep | exact |
| Q16 | 1,536 characters (description + when_to_use combined) | claude-code/skills.md:400 | Claude Code skills page | paraphrase | exact |
| Q17 | localhost:8181 (`qmd mcp --http`; endpoint /mcp) | qmd/README.md:141,186 | qmd page (MCP server) | index | 8181 required; host optional |
| Q18 | 15 min | manual p.227 | Denon AVR settings/ECO page | index | exact; ZONE2 "Off" → wrong |
| Q19 | 4–16 Ω | manual p.36, p.294 | Denon speaker-connection or specs page | deep | exact; "8 Ω default setting" alone → partial |
| Q20 | TUNER PRESET CH + and ZONE2 ON/OFF, held ≥3 s (with "HEOS Music" selected) | manual p.262 | Denon reset/troubleshooting page | paraphrase | both buttons required; menu path Setup→General→Reset→Network Settings (p.237) → partial; TUNER PRESET CH – + DIMMER (firmware restore, p.263) → wrong |
| Q21 | atlas, tank (tank/media + tank/appdata) | lab l.10 | plex, atlas, tank pages | dep-1hop | both required; apc-1 OK as indirect; titan named as current dependency → partial at most (planted Superseded edge on plex.md) |
| Q22 | Ollama endpoint down; new wiki pages not embedded, keyword search still works | lab l.9, l.16 | titan, ollama-endpoint, wiki-search pages | dep-1hop | both required; "wiki search down" → partial; Plex listed → partial |
| Q23 | tank (05:45 snapshot), gate (internet) | lab l.17 | rclone-backup, tank, gate pages | dep-1hop | both required; atlas accepted extra |
| Q24 | atlas (runs on), tank (vdisk on tank/domains) | lab l.6 | hermes, atlas, tank pages | dep-1hop | both required; apc-1 OK extra |
| Q25 | Sync stops: (a) Syncthing container on atlas needs tank, which exists only while atlas runs; (b) its only transport, Tailscale, runs on atlas | lab l.5, l.13, l.14 | syncthing, atlas, tank, tailscale, pebble pages | dep-2hop | a+b → correct; one → partial |
| Q26 | 1 Tailscale remote access; 2 pebble's remote access to hermes/Plex; 3 outside access to Caddy/443; 4 rclone upload to "offsite-crypt"; 5 Unraid email notifications; 6 aria network features (DHCP) | lab l.11,12,14,15,17,18,19 | gate page + each item's page | dep-2hop | ≥5 of 6 → correct; 2–4 → partial; claiming LAN hosts (static atlas/hermes/titan) lose function → partial at most |
| Q27 | hermes → atlas, tank (apc-1 optional); titan NOT needed for keyword search | lab l.4-7, l.9 | wiki-search, hermes, atlas, tank pages | dep-2hop | hermes+atlas+tank required; titan listed as required → partial |
| Q28 | tank, hermes, wiki search (+repo, 02:30 rebuild), Plex, Caddy, Syncthing, Tailscale (exit node/subnet/remote access), rclone backup; notifications accepted | lab l.5-8,10,11,13,14,17 | atlas page + dependents | dep-2hop | ≥7 of 8 and titan/Ollama, gate, aria NOT claimed → correct; 4–6 → partial |
| Q29 | hermes (cannot boot), wiki search (via hermes), Plex, Syncthing, rclone backup; Caddy backends accepted; Tailscale unaffected | lab l.6,7,10,13,17 | tank page + dependents | dep-2hop | all 5 → correct; 3–4 → partial; Tailscale claimed → partial at most |
| Q30 | wiki search service down; index goes stale (02:30 timer); wiki repo /srv/wiki unavailable (bonus); Caddy wiki route, pebble→hermes accepted | lab l.7, 8 | hermes, wiki-search pages | dep-1hop | search down + stale index required; one → partial |

## Distribution
| group | n | index | deep | paraphrase |
|---|---|---|---|---|
| unraid | 4 | 1 | 2 | 1 |
| ollama | 3 | 1 | 2 | 0 |
| syncthing | 2 | 1 | 1 | 0 |
| tailscale | 3 | 2 | 0 | 1 |
| claude-code | 4 | 1 | 2 | 1 |
| qmd | 1 | 1 | 0 | 0 |
| manual | 3 | 1 | 1 | 1 |
| total factual | 20 | 8 | 8 | 4 |
Lab: 10 — dep-1hop Q21–24, Q30; dep-2hop Q25–29.

## Slug mapping notes
All expected pages exist in vault/wiki/ (no `-` entries). For Q03, Q13 and Q14 the expected page exists but does not contain the fact (unraid-shares.md, claude-code-mcp.md, claude-code-hooks.md).
