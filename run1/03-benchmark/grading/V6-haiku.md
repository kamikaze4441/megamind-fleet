# Grading — V6-haiku (auditor A1, run 1)

Source: `results/V6-haiku/answers.tsv` (30 rows). Key: `grading/key.md`. Expected pages: `expected-pages.tsv`. Same rules and interpretations as the Haiku V0–V7 files.

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
| Q14 | wrong | 0 | claude-code-hooks.md | yes (1/1) | wrong (interpretation): says the page has no SessionEnd-specific value, then offers 600 s as 'the closest stated value' instead of answering unknown; key rule '600 s → wrong'. Treated like V1/V2/V5, not like V3/V4/V7, which said only 'unknown' |
| Q15 | correct | 1 | claude-code-memory.md | yes (1/1) | matches key |
| Q16 | correct | 1 | claude-code-skills-subagents.md | yes (1/1) | matches key |
| Q17 | correct | 1 | qmd-search.md | yes (1/1) | matches key |
| Q18 | correct | 1 | avr-setup.md | yes (1/1) | matches key |
| Q19 | correct | 1 | avr-setup.md | yes (1/1) | matches key |
| Q20 | correct | 1 | avr-setup.md | yes (1/1) | matches key |
| Q21 | correct | 1 | plex.md, atlas.md, tank.md | yes (3/3) | atlas + tank required, both present; apc-1 accepted; 'gate for email notifications' through atlas is spurious for Plex, but the rule does not penalise it; titan not named |
| Q22 | correct | 1 | titan.md, ollama-endpoint.md, wiki-search.md | yes (3/3) | matches key |
| Q23 | correct | 1 | rclone-backup.md, atlas.md, tank.md | yes (2/3) | tank + gate (+atlas, apc-1) |
| Q24 | correct | 1 | hermes.md, atlas.md, tank.md | yes (3/3) | atlas + tank; apc-1 accepted; gate (notifications) spurious, not penalised |
| Q25 | correct | 1 | atlas.md, syncthing.md, tailscale.md, pebble.md, tank.md | yes (5/5) | (a) atlas + tank; (b) Tailscale on atlas: both |
| Q26 | partial | 0.5 | gate.md, aria.md, atlas.md, rclone-backup.md, reverse-proxy.md, tailscale.md, hermes.md, plex.md, syncthing.md, tank.md, pebble.md | yes (7/7) | partial: names all 6 key items, but also claims via atlas that hermes, plex, syncthing and tank stop. gate only carries atlas's email notifications (lab l.18); key rule: claiming LAN hosts/services lose function → partial at most. Over-propagation along the builder's atlas→gate notifications edge |
| Q27 | partial | 0.5 | wiki-search.md, hermes.md, ollama-endpoint.md, atlas.md, tank.md, titan.md | yes (4/4) | partial: says keyword search still works without the Ollama endpoint, yet lists ollama-endpoint as a direct need and titan as an indirect need of keyword queries. Key rule: titan listed as required → partial |
| Q28 | correct | 1 | atlas.md, tank.md, hermes.md, plex.md, rclone-backup.md, reverse-proxy.md, syncthing.md, tailscale.md, wiki-search.md, pebble.md | yes (9/9) | 8/8 |
| Q29 | correct | 1 | tank.md, hermes.md, plex.md, rclone-backup.md, syncthing.md, wiki-search.md | yes (6/6) | 5/5 |
| Q30 | correct | 1 | hermes.md, wiki-search.md | yes (2/2) | wiki search down + 'index timer … lost, new pages are not indexed' (accepted as stale index) |

**Counts:** correct 25, partial 2, wrong 1, unknown 2.
**Score:** 26/30. Factual 17/20, dependency 9/10.
**Unknowns:** honest (fact absent from the wiki) 2; answer existed 0.
