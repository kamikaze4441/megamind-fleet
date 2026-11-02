# MEGAMIND run 1 — goal, success criteria, plan

Director: Fable 5.1. Date: 2026-11-02. Budget: $55 (hard cap). Design authority: `MEGAMIND-v10.3-master-prompt-REDACTED.md` (§2, §4, §5a, §6, §7, §11 bind this run) plus the owner's Nov 1 decisions in the brief.

## Goal statement

MEGAMIND is the owner's live brain: a Karpathy-style LLM wiki (`raw/` → `wiki/` with provenance and `depends_on::` edges, `index.md`, `log.md`, qmd search) on a Debian VM on his Unraid server, read by Claude Code so that any question — about his server, network, home theatre, manuals, poster workflow, gaming PC or a past Claude conversation — is answered from the vault, not from memory of past chats. It stays live through a tiered housekeeping system (T0 daily, Tracks A/B Saturday, T1 Sunday, T2 when the gaming PC's GPU is on) that lints, proposes and ratchets improvements through the AutoResearch oracle; the owner alone merges. Community repositories (ECC, OMC and the like) are mined for sub-features file by file, pinned and licensed, never installed as plugins. Skills must be packaged once and installable on claude.ai, in Claude Code and for Managed Agents. New since Nov 1: the owner wants read access to the vault from every Claude surface (claude.ai web/desktop/mobile, Claude Code anywhere), so a read-only vault connector is now a design task.

## What it must do

1. Answer from the vault first (`index.md`, qmd, then pages; edges + `rg` backlinks for dependency questions), raw sources second, and say what it cannot see.
2. Keep every page honest: `derived_from::` lines, `## Superseded` footers, lint, fidelity checks against `raw/`.
3. Ingest chat history as one dated, redacted Markdown file per chat plus an index, in its own folder, no edges.
4. Improve itself only through the ratchet: one file per experiment, scored by the root-owned oracle, merged by the owner (automatic merges only after the ~50-case trigger).
5. Run its cloud scouting in the Monday slot that T0 already reserves; propose, never apply.
6. Be reachable read-only from claude.ai, the apps and Claude Code anywhere (design in this run; nothing built).

## What it must never do (§2 hard limits, applied to this run)

- Never `--dangerously-skip-permissions`; never a Docker socket in the VM; a job never loosens its own permissions (HL 1–3).
- No Fable in unattended profiles; unattended runs never spend usage credits (HL 4–5).
- No secret in a reply or a file; tokens handled as HL 6 says (HL 6).
- Vault content goes only to Anthropic models and the owner's local models; other vendors (Argon/Gemini) see public keywords only (HL 7). In this run: no placeholder, path or master-prompt text in any web search, fetch or Argon prompt.
- `raw/` is read-only for Claude (HL 8); borrowed code only from a pinned commit with a permissive LICENSE, notice kept (HL 9); the owner's employment is never mentioned (HL 10).
- Nothing in §11 is re-proposed (the Nov 1 re-opening of the vault connector is the one owner-made exception). Findings against locked decisions go to `06-amendments.md`, flagged, never applied.
- Nothing in this session touches the owner's machines, accounts or money.

## Success criteria (measurable)

| Criterion | Measure |
| --- | --- |
| Every deliverable in the brief exists and the auditor has signed off 02(b)–(d) and 04 | Files present; auditor verdict recorded in `07-decisions.md` |
| Reuse map covers §2–§12 | One verdict per section, each with evidence or "gap" |
| Benchmark answers the design question | V0–V5 run on Haiku 5.5 (V6/V7 and Sonnet re-runs if budget allows); per variant: correctness, expected-page recall, median wall time, median characters read; `qmd bench` on V2–V4; `results.md` names a winner and caveats |
| Skills plan is safe | Every item: licence, SHA, installer behaviour, settings rewritten, hooks added, bypass-permissions use (rejected if yes), install path ×3 |
| Fortnightly job respects §4 | Scout deployment in the Monday T0 slot, America/Vancouver cron, per-run budget, proposes only; T2 cadence raised as a proposal in `06` |
| Reachability design is complete | Both options compared; risks (topology behind one token, connectors in auto-mode sessions, token handling), costs, needs, tests; amendments to §4/§5/§11 drafted; the "file it" write-path question in `08` |
| Every claim sourced | URL + read date, or "not verified"; every repository pinned (SHA, date, licence line) |
| Budget | Session finishes the must-haves under $55; `09-cost.md` lists thread names |

## Run plan

Wave 1 (parallel):

| # | Worker | Task | File(s) |
| --- | --- | --- | --- |
| R1 | megamind-researcher | (a) Managed Agents: overview, memory, dreams, skills, scheduled deployments, orchestration, GitHub, secure deployment; knowledge-wiki quickstart (query pattern → V7 decision); (e) skills install paths on claude.ai / Claude Code / Managed Agents with exact labels | `02-research/a-managed-agents.md`, `02-research/e-skills-install.md` |
| R2 | megamind-researcher | (b) ECC, (c) OMC, (d) ≥5 more repositories, each pinned and licensed with a safety verdict | `02-research/b-ecc.md`, `02-research/c-omc.md`, `02-research/d-more-repos.md` |
| R3 | megamind-researcher | (f) chat-history formats and converter design; (h) reachability design (vault MCP connector vs Managed Agents memory-store mirror) | `02-research/f-chat-history.md`, `02-research/h-reachability.md` |
| R4 | argon-researcher | (g) community evidence, topics 1–4, ≤6 research-grade calls | `02-research/g-community.md` |
| B1 | megamind-builder | Benchmark step 1: environment, corpus (~40 public sources + lab note) into `raw/`, `corpus.md`; report | `03-benchmark/` |

Wave 2 (after B1 step 1):

| # | Worker | Task | File(s) |
| --- | --- | --- | --- |
| A1 | megamind-auditor | Write 20 factual + 10 dependency questions from `raw/` before the wiki exists; key stays in its reply | `03-benchmark/questions.md` (no answers) |
| B1 (cont.) | megamind-builder | Build the wiki (~30 pages, §7 layout, karpathy-llm-wiki SKILL.md by hand), qmd 2.8.3 index of `wiki/`, harness, `PROTOCOL-V0..V6.md` (V7 if R1 says so), `deps/` generator, `qmd bench` fixture | `03-benchmark/` |

Wave 3:

| # | Worker | Task | File(s) |
| --- | --- | --- | --- |
| Q-V0..V6-haiku | megamind-querier ×7 | 30 questions per variant, protocol followed exactly | `03-benchmark/results/<variant>-haiku/answers.tsv` |
| A1 (cont.) | megamind-auditor | Grade each variant; verify 02(b)–(d); sign off 04 | `03-benchmark/grading/*.md`, `03-benchmark/results.md` draft inputs |
| Q-sonnet ×2 | megamind-querier-sonnet | Re-run the two best variants | `03-benchmark/results/<variant>-sonnet/answers.tsv` |
| R2 (cont.) | megamind-researcher | Draft `04-skills-plan.md` from (b)–(d) with the packaging plan | `04-skills-plan.md` |
| R1 (cont.) | megamind-researcher | Draft `05-fortnightly-job.md` and `deployments/megamind-scout.md` validated against the docs it cites | `05-fortnightly-job.md`, `05-deployments/megamind-scout.md` |

Director throughout: `01-reuse-map.md` (from the master prompt and the research files), `06-amendments.md`, `07-decisions.md`, `08-owner-questions.md`, `03-benchmark/results.md` (final judgement), `09-cost.md` last; commits after each finished deliverable; memory summary at the end.

Budget priority if tight (brief): 00, 01, 03 (V0–V5 Haiku), 04, 06, 07, 08, 09 first; (d) extras, Sonnet re-runs, V6/V7, Argon topics 3–4 are elastic.
