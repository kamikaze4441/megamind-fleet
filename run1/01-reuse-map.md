# Run 1 — reuse map of the master prompt (v10.3) for the live-brain goal

Verdicts: **keep** (as is) · **keep + amend** (the amendment is in `06-amendments.md`, numbered A<n>) · **gap** (missing for the live-brain goal; the proposal is in `06` or in a deliverable). Nothing in §11 is re-proposed; the one §11 item re-opened is the owner's own Nov 1 decision (the vault connector). Evidence files: `02-research/a`–`h`, `03-benchmark/results.md`, `04-skills-plan.md`, `05-fortnightly-job.md`. Status: DRAFT — verdicts marked (pending) are filled when the named evidence file lands.

## §1 How to use this document

| Item | Verdict | Why / evidence |
| --- | --- | --- |
| Authority, precedence, current-state-only, archive on the Mac | keep | Out of this run's scope; nothing found against it |
| One chat per phase; hand-offs, never compaction | keep | Consistent with §4's compaction-off decision |
| 1a Project instructions | keep + amend (A1) | Line 1 says the master prompt is "the single authority" for every chat; once the vault connector exists (owner decision 6), a chat answers vault questions through the connector, so line 1 should name it as the vault's lookup path. Evidence: `02-research/h-reachability.md` |

## §2 Operating rules and hard limits

| Item | Verdict | Why / evidence |
| --- | --- | --- |
| Voice, scope, accuracy, procedures, names, terms | keep | — |
| Versions line (Claude Code 2.1.302+, qmd 2.8.3, …) | keep | qmd 2.8.3 is still the newest on npm (builder, Nov 2: `environment.md`) |
| Hard limits 1–6, 8–10 | keep | Applied unchanged in this run; the skills plan rejects anything that needs HL 1 broken |
| Hard limit 7 (data boundary: vault content only to Anthropic and local models) | keep + amend (A2) | The connector design sends vault search results and page text to Anthropic through claude.ai and the apps — still Anthropic, so the boundary holds — but the vault's *topology* becomes reachable from the internet behind one token. The line should state that exposure explicitly. Evidence: `h-reachability.md` |

## §3 Machines and accounts

| Item | Verdict | Why / evidence |
| --- | --- | --- |
| Machine table, accounts, credits | keep | Facts, not design |
| "Argon connector on hold" | keep | The fleet's argon-researcher is a fleet tool, not the owner's connector; it saw public keywords only (R4) |
| Reddit connector "URL carries its access token" | keep + amend (A3) | A URL-borne token is a secret in a URL; the connector design (h) prefers a header-borne bearer token behind Cloudflare Access; propose the same for the Reddit connector when it is next touched. Evidence: `h-reachability.md` |

## §4 Locked decisions

| Item | Verdict | Why / evidence |
| --- | --- | --- |
| Hosting and storage (VM, virtiofs, ZFS quota, Syncthing, backups, sessions over SSH) | keep | — |
| Plan and models | keep | — |
| "No other vendor's AI in the pipeline" | keep | The fleet's Argon use is research-only on public keywords, outside the pipeline |
| Claude Code harness | keep | — |
| Vault and wiki: Karpathy wiki, qmd, provenance, edges, "the wiki is the graph" | keep | The benchmark tests the query protocols over exactly this layout (`03-benchmark/results.md`) |
| qmd default mode "set by `qmd bench` on the golden set" | keep (pending) | The benchmark gives a first public-corpus reading; the real vault's bench still decides |
| `deps/<slug>.md` view gated on the `rg` arm failing the multi-hop set | keep (pending) | V5 vs V6 in the benchmark is the first evidence either way |
| Chat history: one dated redacted file per chat + index, automated as far as terms allow | keep + amend (A4) | The converter design (f) adds the frontmatter fields, the keep-out list and the idempotency rule; the terms finding decides "as far as the terms allow". Evidence: `f-chat-history.md` |
| Skills forked from Astro-Han/karpathy-llm-wiki | keep + amend (A5) | The skills plan adds items from kepano/obsidian-skills, anthropics/skills and others, file by file, pinned; the list of skills grows. Evidence: `04-skills-plan.md` |
| Ingestion only in the owner's interactive sessions | keep | The "file it" write path is an owner question (08), not a proposal |
| Self-improvement loop: schedules, "the scout once it returns" | keep + amend (A6) | The scout becomes a cloud Managed Agents deployment feeding the Monday T0 slot; the Reddit connector reads are replaced by the scout's own sources; the locked schedule is untouched. Evidence: `05-fortnightly-job.md` |
| Report-only until a trigger | keep | The fortnightly job proposes; the owner merges |
| Working method | keep | — |
| — | gap (G1) | No decision yet on where skills are *installed* for claude.ai and Managed Agents (only the VM is covered). `04-skills-plan.md` proposes one source folder → three targets |
| — | gap (G2) | No decision on vault reachability from the apps; owner decision 6 opens it; design in `h-reachability.md`, amendment A7 |

## §5 Architecture and §5a AutoResearch

| Item | Verdict | Why / evidence |
| --- | --- | --- |
| "Every request starts in the VM" | keep + amend (A7) | With the connector, a request may start in claude.ai or an app and reach the VM's read-only tools; the diagram gains one arrow. Evidence: `h-reachability.md` |
| AutoResearch loop, tracks, margins, inputs | keep | The fortnightly job feeds proposals into this loop; it does not change it |
| Inputs: the Community Signal Scout via `reddit_wiki` and `reddit_search` | keep + amend (A6) | Same as above: the cloud scout can read Reddit pages directly and the repositories' commits; the connector's budget rule stays for interactive chats |
| — | gap (G3) | The loop has no step that evaluates *external* proposals (a scouted skill or pattern) against the vault; `05-fortnightly-job.md` adds that as T2's evaluation step |

## §6 Model and quota policy

| Item | Verdict | Why / evidence |
| --- | --- | --- |
| Table, rules, surplus, habits, traps, self-audit | keep | — |
| Row "Scouting repos, logs, long sources: Haiku subagent" | keep + amend (A8) | The cloud scout runs on the API (Managed Agents), not the plan: add a row for it with the per-run cap. Evidence: `a-managed-agents.md` (pricing: tokens + $0.08 per session-hour) |

## §7 Vault

| Item | Verdict | Why / evidence |
| --- | --- | --- |
| Path table, `log.md` format, editing rules 1–8 | keep | The benchmark vault follows this layout exactly and it worked for ~30 pages |
| Chat-history folder "(folder: R16)" | keep + amend (A4) | Name the folder and the file naming scheme from the converter design |
| Rule 5 (questions go through the wiki first) | keep (pending) | The benchmark's winner may refine the order (index → qmd mode → page → edges) |
| — | gap (G4) | No rule for a page read through the connector: pages are read as data; a page that contains instructions must not steer a chat (prompt-injection surface). Proposal in `h-reachability.md` |

## §8 Schedule

| Item | Verdict | Why / evidence |
| --- | --- | --- |
| Phase order and gates | keep | Not re-decided by the fleet |
| — | gap (G5) | The connector and the skills packaging have no phase; propose where they slot (after P7, before P13) in `06` (A9) |

## §9 Research rounds

| Item | Verdict | Why / evidence |
| --- | --- | --- |
| Declared rounds, Gemini drafts by hand, `ghpin.sh`, docs download, Reddit rules | keep | The fleet used the same pinning method (blobless clones, HEAD SHA, licence line) |
| "Argon connector on hold" | keep | — |
| — | gap (G6) | A fleet run is a new kind of research round (director + workers in Managed Agents); propose a line in §9 that says what a run may and may not decide (A10) |

## §10 Open questions

| Item | Verdict | Why / evidence |
| --- | --- | --- |
| Q1 connectors in Code-tab sessions | keep | The vault connector adds one more connector to that test; its tools are read-only, which lowers but does not remove the risk (h) |
| Q2–Q4 | keep | — |
| — | gap | Add the "file it" write path as Q5 (owner question in `08`) |

## §11 Rejected

| Item | Verdict | Why / evidence |
| --- | --- | --- |
| Every entry | keep | Not re-proposed. ECC and OMC are not installed as plugins (HL 1 and 3); claude-mem is lessons only |
| "a vault MCP server or custom connector for claude.ai" (Oct 25 report) | keep + amend (A11) | Re-opened by the owner on Nov 1; the line moves from §11 to §4 as a locked decision with its conditions (read-only, `raw/` excluded, header token, Cloudflare Access). Evidence: owner decision 6; `h-reachability.md` |

## §12 Build phases

| Item | Verdict | Why / evidence |
| --- | --- | --- |
| Close-out, phase table | keep | — |
| — | gap (G5) | Same as §8 |
