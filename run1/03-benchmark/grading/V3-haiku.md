# Grading — V3-haiku (auditor A1, run 1)

Source: `results/V3-haiku/answers.tsv` (30 rows). Key: `/tmp/a1/grading/key.md`. Expected pages: `expected-pages.tsv`.

| qid | verdict | score | pages cited | expected pages hit? | note |
|---|---|---|---|---|---|
| Q01 | correct | 1 | unraid-shares.md | yes (1/1) | matches key |
| Q02 | correct | 1 | unraid-array-parity.md | yes (1/1) | matches key |
| Q03 | unknown | 0 | — | — (none cited) | honest unknown: fact absent from wiki (checked vault/wiki/) |
| Q04 | correct | 1 | unraid-pools-zfs.md | yes (1/1) | matches key |
| Q05 | correct | 1 | ollama-modelfile.md | yes (1/1) | matches key |
| Q06 | correct | 1 | ollama-server-gpu.md | yes (1/1) | matches key |
| Q07 | correct | 1 | ollama-server-gpu.md | yes (1/1) | matches key |
| Q08 | correct | 1 | syncthing-folders-versioning.md | yes (1/1) | matches key |
| Q09 | correct | 1 | syncthing-folders-versioning.md | yes (1/1) | matches key |
| Q10 | correct | 1 | tailscale-acls-ssh.md | yes (1/1) | matches key |
| Q11 | correct | 1 | tailscale-magicdns.md | yes (1/1) | matches key |
| Q12 | correct | 1 | tailscale-exit-nodes-subnets.md | yes (1/1) | matches key |
| Q13 | unknown | 0 | — | — (none cited) | honest unknown: fact absent from wiki (checked vault/wiki/) |
| Q14 | unknown | 0 | — | — (none cited) | honest unknown: fact absent from wiki (checked vault/wiki/) |
| Q15 | correct | 1 | claude-code-memory.md | yes (1/1) | matches key |
| Q16 | correct | 1 | claude-code-skills-subagents.md | yes (1/1) | matches key |
| Q17 | correct | 1 | qmd-search.md | yes (1/1) | matches key |
| Q18 | correct | 1 | avr-setup.md | yes (1/1) | matches key |
| Q19 | correct | 1 | avr-setup.md | yes (1/1) | matches key |
| Q20 | correct | 1 | avr-setup.md | yes (1/1) | matches key |
| Q21 | correct | 1 | plex.md | yes (1/3) | titan explicitly rejected as superseded |
| Q22 | correct | 1 | titan.md, ollama-endpoint.md, wiki-search.md | yes (3/3) | matches key |
| Q23 | correct | 1 | rclone-backup.md | yes (1/3) | matches key |
| Q24 | correct | 1 | hermes.md | yes (1/3) | matches key |
| Q25 | correct | 1 | syncthing.md, pebble.md, tailscale.md | yes (3/5) | (a) Syncthing on atlas + 'syncs tank/notes'; (b) Tailscale on atlas |
| Q26 | correct | 1 | gate.md, tailscale.md, reverse-proxy.md, rclone-backup.md, aria.md, pebble.md, syncthing.md | yes (6/7) | 6/6 |
| Q27 | correct | 1 | wiki-search.md, hermes.md | yes (2/4) | matches key |
| Q28 | correct | 1 | atlas.md, tank.md, hermes.md, plex.md, reverse-proxy.md, syncthing.md, tailscale.md, rclone-backup.md, wiki-search.md | yes (9/9) | 8/8 |
| Q29 | correct | 1 | tank.md, plex.md, syncthing.md, rclone-backup.md, hermes.md, wiki-search.md, reverse-proxy.md | yes (6/6) | 5/5 + Caddy note (accepted) |
| Q30 | correct | 1 | hermes.md, wiki-search.md, pebble.md, reverse-proxy.md | yes (2/2) | matches key |

**Counts:** correct 27, partial 0, wrong 0, unknown 3.
**Score:** 27/30 — factual 17/20, dependency 10/10.
**Unknowns:** honest (fact absent from the wiki) 3; answer existed 0.
