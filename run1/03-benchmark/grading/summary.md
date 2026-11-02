# Summary across all nine runs (auditor A1, run 1)

Rules: `key.md`. Scoring: correct = 1, partial = 0.5, wrong = 0, unknown = 0. "Honest" unknown means the fact is absent from what the variant may read: the wiki for V1–V7, the raw corpus for V0. "Missed" means the answer was there.

| run | correct | partial | wrong | unknown (honest / missed) | score /30 | factual /20 | dependency /10 |
|---|---|---|---|---|---|---|---|
| V0-haiku (raw only) | 28 | 0 | 0 | 2 (0 / 2) | 28 | 18 | 10 |
| V1-haiku | 27 | 0 | 1 | 2 (2 / 0) | 27 | 17 | 10 |
| V2-haiku | 27 | 0 | 1 | 2 (2 / 0) | 27 | 17 | 10 |
| V3-haiku | 27 | 0 | 0 | 3 (3 / 0) | 27 | 17 | 10 |
| V4-haiku | 27 | 0 | 0 | 3 (3 / 0) | 27 | 17 | 10 |
| V5-haiku | 25 | 2 | 1 | 2 (2 / 0) | 26 | 17 | 9 |
| V6-haiku | 25 | 2 | 1 | 2 (2 / 0) | 26 | 17 | 9 |
| V7-haiku | 27 | 0 | 0 | 3 (3 / 0) | 27 | 17 | 10 |
| V7-sonnet | 27 | 0 | 0 | 3 (3 / 0) | 27 | 17 | 10 |

## Wiki gaps
- I read every page in vault/wiki/ and also grepped for "25,000", "MAX_MCP", "1.5", "SessionEnd" and "10%".
- Three answers are missing from the wiki:
  - Q03: `unraid-shares.md` has no default Minimum Free Space.
  - Q13: `claude-code-mcp.md` has no output-token limit.
  - Q14: `claude-code-hooks.md` gives only the general 600/30/60 s defaults.
- No wiki-reading run can score above 27/30.
- V0 reads raw/, where all 30 answers exist. Its two misses (Q18, Q20) are retrieval failures in the 338 kB manual text.

## Where grading needed interpretation
1. **Q14, answers that give "600 s":** graded wrong per the key ("600 s → wrong").
   - V1, V2 and V5 inferred 600 s. V6 said the page has no SessionEnd value and offered 600 s as "the closest stated value". It never said "unknown", so it is graded like V1/V2/V5.
   - V3, V4, V7-haiku and V7-sonnet said "unknown" and are graded as honest unknowns. This is the only factual difference between the wiki runs.
2. **Q25, reason (a):** accepted when the answer says the Syncthing container on atlas stops, even without naming tank (V1, V2, V4, V5).
3. **Q26, gate down — V5 and V6 graded partial.** Both name all six key items, but both also claim that hermes, Plex, Syncthing and tank stop "via atlas". The key rule says claiming LAN hosts or services lose function is partial at most.
   - Likely cause: the builder's edge `atlas depends_on:: [[gate]]` (email notifications only). A deps traversal that ignores the edge's reason spreads it to everything on atlas.
   - V0–V4, V7-haiku and V7-sonnet did not over-propagate.
4. **Q27, V6 graded partial.** It says keyword search works without the Ollama endpoint, yet lists ollama-endpoint as a direct need and titan as an indirect need of keyword queries. Key rule: titan listed as required → partial.
5. **Q30, V5 graded partial.** It has the search service down but not the stale index (02:30 timer); the key requires both.
6. **Spurious gate dependency, not penalised (rules don't cover it):**
   - V6 Q21 and Q24 add "gate (email notifications) through atlas" to the needs of Plex and hermes.
   - V5 Q27 and V7-sonnet Q27 also list "atlas needs gate".
   - All come from the same notifications edge.
7. **Answers graded correct with a note:**
   - V0 Q22: the closing sentence the querier flagged as unsupported contradicts nothing, so no deduction.
   - V0 Q26: counted 5 of 6 (pebble's remote access not named separately), which still meets the rule.
   - V7-sonnet Q01: correct, though it notes the wiki says only "recommended" (not "default"). That observation is accurate: `raw/unraid/shares.md:311` says default, the wiki page does not.
8. **Citation slips (V7-sonnet, the querier's own admission; scores unaffected):**
   - Q22 cites titan.md and plex.md, which it saw only as grep hits.
   - Q26 cites gate.md, rclone-backup.md, tailscale.md, syncthing.md and pebble.md, also grep-only (log: it opened atlas.md, reverse-proxy.md and aria.md).
   - Page recall from cited pages is therefore inflated for those two questions.
