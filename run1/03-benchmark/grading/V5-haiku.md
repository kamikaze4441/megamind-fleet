# Grading — V5-haiku (auditor A1, run 1)

Source: `results/V5-haiku/answers.tsv` (30 rows). Key: `grading/key.md`. Expected pages: `expected-pages.tsv`. Same rules and interpretations as the Haiku V0–V7 files.

| qid | verdict | score | pages cited | expected pages hit? | note |
|---|---|---|---|---|---|
| Q01 | correct | 1 | unraid-shares.md | yes (1/1) | matches key |
| Q02 | correct | 1 | unraid-array-parity.md | yes (1/1) | matches key |
| Q03 | unknown | 0 | — | — (none cited) | honest unknown: fact absent from wiki (checked vault/wiki/) (answered 'not in vault') |
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
| Q14 | wrong | 0 | claude-code-hooks.md | yes (1/1) | wrong: answered 600 s (general command-hook default); key rule '600 s → wrong'. Wiki lacks the 1.5 s fact. |
| Q15 | correct | 1 | claude-code-memory.md | yes (1/1) | matches key |
| Q16 | correct | 1 | claude-code-skills-subagents.md | yes (1/1) | matches key |
| Q17 | correct | 1 | qmd-search.md | yes (1/1) | matches key |
| Q18 | correct | 1 | avr-setup.md | yes (1/1) | matches key |
| Q19 | correct | 1 | avr-setup.md | yes (1/1) | matches key |
| Q20 | correct | 1 | avr-setup.md | yes (1/1) | matches key |
| Q21 | correct | 1 | plex.md | yes (1/3) | atlas + tank; titan not named |
| Q22 | correct | 1 | titan.md, ollama-endpoint.md, wiki-search.md | yes (3/3) | matches key |
| Q23 | correct | 1 | rclone-backup.md | yes (1/3) | matches key |
| Q24 | correct | 1 | hermes.md | yes (1/3) | matches key |
| Q25 | correct | 1 | atlas.md, syncthing.md, tailscale.md, pebble.md | yes (4/5) | (a) accepted: Syncthing container on atlas stops; tank not named (same interpretation as V1/V2/V4); (b) Tailscale on atlas |
| Q26 | partial | 0.5 | gate.md, aria.md, atlas.md, rclone-backup.md, reverse-proxy.md, tailscale.md, hermes.md, plex.md, syncthing.md, tank.md, pebble.md | yes (7/7) | partial: names all 6 key items, but also claims via atlas that hermes, plex, syncthing and tank stop. gate only carries atlas's email notifications (lab l.18); key rule: claiming LAN hosts/services lose function → partial at most. Over-propagation along the builder's atlas→gate notifications edge |
| Q27 | correct | 1 | wiki-search.md, hermes.md, tank.md, atlas.md, apc-1.md, ollama-endpoint.md | yes (4/4) | hermes, atlas, tank, apc-1 (optional); titan correctly excluded. Also lists 'atlas needs gate' (notifications edge), which the rule does not penalise |
| Q28 | correct | 1 | atlas.md, tank.md, hermes.md, plex.md, rclone-backup.md, reverse-proxy.md, syncthing.md, tailscale.md, wiki-search.md, pebble.md | yes (9/9) | 8/8; nothing wrongly claimed |
| Q29 | correct | 1 | tank.md, plex.md, rclone-backup.md, syncthing.md, hermes.md, wiki-search.md | yes (6/6) | 5/5 |
| Q30 | partial | 0.5 | hermes.md, wiki-search.md | yes (2/2) | partial: wiki search down, but the stale index (02:30 timer) is not mentioned; key needs both |

**Counts:** correct 25, partial 2, wrong 1, unknown 2.
**Score:** 26/30. Factual 17/20, dependency 9/10.
**Unknowns:** honest (fact absent from the wiki) 2; answer existed 0.
