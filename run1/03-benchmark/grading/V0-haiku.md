# Grading — V0-haiku (auditor A1, run 1)

Source: `results/V0-haiku/answers.tsv` (30 rows). Key: `/tmp/a1/grading/key.md`. Expected pages: `expected-pages.tsv` (V0 reads raw only, so hits are judged against `expected-raw.tsv`).

| qid | verdict | score | pages cited | expected pages hit? | note |
|---|---|---|---|---|---|
| Q01 | correct | 1 | raw/unraid/shares.md | yes (1/1) | matches key |
| Q02 | correct | 1 | raw/unraid/array-overview.md | yes (1/1) | matches key |
| Q03 | correct | 1 | raw/unraid/shares.md | yes (1/1) | 10% of disk capacity (raw shares.md:172); wiki lacks it but V0 reads raw |
| Q04 | correct | 1 | raw/unraid/zfs-storage.md | yes (1/1) | matches key |
| Q05 | correct | 1 | raw/ollama/modelfile.md | yes (1/1) | matches key |
| Q06 | correct | 1 | raw/ollama/faq.md | yes (1/1) | matches key |
| Q07 | correct | 1 | raw/ollama/gpu.md | yes (1/1) | matches key |
| Q08 | correct | 1 | raw/syncthing/foldertypes.md | yes (1/1) | matches key |
| Q09 | correct | 1 | raw/syncthing/versioning.md | yes (1/1) | matches key |
| Q10 | correct | 1 | raw/tailscale/tailscale-ssh.md | yes (1/1) | matches key |
| Q11 | correct | 1 | raw/tailscale/magicdns.md | yes (1/1) | matches key |
| Q12 | correct | 1 | raw/tailscale/exit-nodes.md | yes (1/1) | matches key |
| Q13 | correct | 1 | raw/claude-code/mcp.md | yes (1/1) | 25,000 tokens (raw mcp.md:1502) |
| Q14 | correct | 1 | raw/claude-code/hooks.md | yes (1/1) | 1.5 s (raw hooks.md:3582) |
| Q15 | correct | 1 | raw/claude-code/memory.md | yes (1/1) | matches key |
| Q16 | correct | 1 | raw/claude-code/skills.md | yes (1/1) | matches key |
| Q17 | correct | 1 | raw/qmd/README.md | yes (1/1) | matches key |
| Q18 | unknown | 0 | — | — (none cited) | answer existed: raw manual p.227 '15 min (Default)'; querier did not find it |
| Q19 | correct | 1 | raw/manual/denon-avr-x1700h-owners-manual.txt | yes (1/1) | matches key |
| Q20 | unknown | 0 | — | — (none cited) | answer existed: raw manual p.262 (TUNER PRESET CH + and ZONE2 ON/OFF); querier did not find it |
| Q21 | correct | 1 | raw/lab/LAB-STATE.md | yes (1/1) | matches key |
| Q22 | correct | 1 | raw/lab/LAB-STATE.md | yes (1/1) | both items present (endpoint down; new pages not embedded, keyword search works); no Plex. Closing sentence 'Titan is the only lab host listed as taking down the Ollama endpoint' is not in the note (querier itself flagged it as unsupported); it contradicts nothing, so no deduction — graded as written |
| Q23 | correct | 1 | raw/lab/LAB-STATE.md | yes (1/1) | matches key |
| Q24 | correct | 1 | raw/lab/LAB-STATE.md | yes (1/1) | matches key |
| Q25 | correct | 1 | raw/lab/LAB-STATE.md | yes (1/1) | (a) Syncthing on atlas + tank; (b) Tailscale on atlas — both |
| Q26 | correct | 1 | raw/lab/LAB-STATE.md | yes (1/1) | 5 of 6: Tailscale remote access, Caddy 443 outside access, rclone, notifications, aria; pebble's remote access not named separately (counted under Tailscale only) → ≥5 rule |
| Q27 | correct | 1 | raw/lab/LAB-STATE.md | yes (1/1) | hermes, atlas, tank, apc-1 (optional); titan correctly excluded |
| Q28 | correct | 1 | raw/lab/LAB-STATE.md | yes (1/1) | 8/8 + notifications (accepted); no titan/gate/aria |
| Q29 | correct | 1 | raw/lab/LAB-STATE.md | yes (1/1) | 5/5 + Caddy (accepted); Tailscale not claimed |
| Q30 | correct | 1 | raw/lab/LAB-STATE.md | yes (1/1) | matches key |

**Counts:** correct 28, partial 0, wrong 0, unknown 2.
**Score:** 28/30 — factual 18/20, dependency 10/10.
**Unknowns:** honest (fact absent from the raw corpus) 0; answer existed 2.
