# More repositories like ECC/OMC: eleven pinned, licensed and judged for a Markdown knowledge vault
Question: Verify at source eight named candidates plus up to three 2026 repositories of Claude Code skills/plugins for knowledge vaults, LLM wikis and Obsidian. For each: pin, licence, installer behaviour, files worth borrowing, safety verdict · Date read: 2026-11-02 · Researcher: R2 (megamind-researcher)

## Summary (10 lines max, each ending with [n])
- Repositories that can be installed file by file:
  - Astro-Han/karpathy-llm-wiki (MIT; the skill MEGAMIND already forks, plus a stdlib-only, report-only `check_evidence.py`) [7]
  - kepano/obsidian-skills (MIT; obsidian-markdown, json-canvas, obsidian-bases) [1]
  - the Apache-2.0 skills in anthropics/skills (skill-creator, mcp-builder, discernment-nudge) [2]
  - wshobson/agents `grounded-vault` (MIT; raw/wiki/archive layout with per-claim provenance and git-fingerprint drift checks) [3]
  - TrueHOOHA/LLM-Wiki (Apache-2.0; three prose skills and an OKF spec) [5]
- anthropics/skills has **no root LICENSE**. The `docx`, `pdf`, `pptx` and `xlsx` skills carry a proprietary licence that forbids copying, and `doc-coauthoring` has no licence file at all. Those skills are ideas only [2].
- charlie947/ai-second-brain contains **no export parser**. Its Step 1c is one free-form prompt that asks Claude to convert ChatGPT/Claude exports into Markdown with frontmatter `title, date, tags, category` and to run 10 sub-agents. It names no file names and no JSON keys, and it defines no dating or naming rule [6].
- vanillaflava/llm-wiki-skills (MIT) **moves** files out of `raw/` into `ingested/` as its commit step, which conflicts with a read-only `raw/`. It lends ideas only (`wiki-crystallize`, the em-dash lint, `reliability:` + `## Pending Review`) [4].
- SubFreq/agent-governance-framework (MIT, 5 stars) offers the strongest *pattern* for "owner alone merges": an append-only decision ledger enforced by a git pre-commit hook. Its `npm install` sets `core.hooksPath` [8].
- AgriciDaniel/claude-obsidian (MIT, 15.9k stars) adds 2 hooks as a plugin. Vault writes need an approved plan SHA-256, and it keeps separate source/claim ledgers. Its skills depend on a Python CLI, so it lends ideas only [9].
- nvk/llm-wiki (MIT): its Claude plugin ships commands and a skill with no hooks. The lint catalogue C1–C20 (provenance, freshness, volatility) is worth taking as ideas [10].
- ekadetov/llm-wiki (MIT) is **rejected**. Its SessionStart hook runs unpinned `npm install @tobilu/qmd @marp-team/marp-cli` automatically [11].
- claude-mem lesson: typed observations go into dated monthly log lines; the default is a hosted store [12].

## Index
| # | repo | SHA (7) | licence | verdict |
|---|---|---|---|---|
| 1 | kepano/obsidian-skills | 3ccff53 | MIT | install file-by-file (3 SKILL.md) |
| 2 | anthropics/skills | ca45fc4 | per-skill: Apache-2.0 / proprietary / none | file-by-file for Apache-2.0 skills only; proprietary and unlicensed = ideas only |
| 3 | wshobson/agents | 7e2fb55 | MIT | install file-by-file (grounded-vault et al.); reject protect-mcp hooks |
| 4 | vanillaflava/llm-wiki-skills | ff6f7be | MIT | ideas only (moves raw/) |
| 5 | TrueHOOHA/LLM-Wiki | 0455b71 | Apache-2.0 | install file-by-file (lint skill, SPEC) |
| 6 | charlie947/ai-second-brain | 6b14a52 | MIT | ideas only (no parser; curl-to-CLAUDE.md; Full Disk Access) |
| 7 | Astro-Han/karpathy-llm-wiki | eafcc77 | MIT | install file-by-file (already forked) |
| 8 | SubFreq/agent-governance-framework | 95232cc | MIT | ideas only (git-hook enforcement, npm prepare) |
| 9 | AgriciDaniel/claude-obsidian (extra) | 2e54556 | MIT (+ GPL-2.0 CSS) | ideas only (plugin hooks; Python core) |
| 10 | nvk/llm-wiki (extra) | d60674f | MIT | ideas only (large protocol; lint catalogue) |
| 11 | ekadetov/llm-wiki (extra) | 5e49545 | MIT | reject (auto `npm install` in SessionStart hook) |

---

## 1. kepano/obsidian-skills
### Pin
| repo | HEAD SHA | commit date | licence file, first line | stars (page, date) | archived? |
|---|---|---|---|---|---|
| kepano/obsidian-skills | 3ccff5338ea700537839b21900aa5358a0402c98 | 2026-09-15 (48 days) | `LICENSE`: "MIT License" (© 2026 Steph Ango) | 50.0k (2026-11-02) [1p] | no |
### Findings
- **What it is:** 6 skills (`obsidian-markdown`, `obsidian-bases`, `json-canvas`, `obsidian-cli`, `defuddle`, `knap`) in 15 files [1].
- **Installer:** README offers three routes [1]:
  - `/plugin marketplace add kepano/obsidian-skills` then `/plugin install obsidian@obsidian-skills`
  - `npx skills add …` (unpinned)
  - copy the files manually
- `.claude-plugin/plugin.json` has no hooks and no MCP. There is no `hooks/` directory and no `.mcp.json` in the tree [1].
- Dependencies by skill [1]:
  - `defuddle` (SKILL.md:10) needs `npm install -g defuddle`.
  - `knap` (SKILL.md:10) needs `npm install -g knap` or `npx knap`.
  - `obsidian-cli` needs the Obsidian desktop CLI.
  - The other three are pure syntax references with outbound doc links only.
### Files worth borrowing
| path | purpose | self-contained? | adaptation needed |
|---|---|---|---|
| skills/obsidian-markdown/SKILL.md + references/{CALLOUTS,EMBEDS,PROPERTIES}.md | Wikilinks, embeds, callouts, properties syntax | yes | Add the vault's `derived_from::` / `depends_on::` inline-field convention |
| skills/json-canvas/SKILL.md + references/EXAMPLES.md | JSON Canvas 1.0 nodes and edges | yes | Optional: render `depends_on::` graphs as `.canvas` |
| skills/obsidian-bases/SKILL.md + references/FUNCTIONS_REFERENCE.md | `.base` views, filters, formulas | yes | Optional: Bases view of pages by `status`/`updated` |
### Safety verdict
**Install file by file** (the three syntax skills). Exclude `defuddle` and `knap`: they need a global npm install, and `npx knap` is unpinned (`skills/knap/SKILL.md:10`). Do not use the plugin route.

## 2. anthropics/skills
### Pin
| repo | HEAD SHA | commit date | licence file, first line | stars (page, date) | archived? |
|---|---|---|---|---|---|
| anthropics/skills | ca45fc496a3436251f191354091d557da31c15b5 | 2026-10-28 (5 days) | **no root LICENSE file**. Per-skill `LICENSE.txt`: Apache-2.0 for 14 skills; `docx`/`pdf`/`pptx`/`xlsx`: "© 2025 Anthropic, PBC. All rights reserved."; `doc-coauthoring`, `discernment-nudge`†, `academy-guide`†: see below | 186.5k (2026-11-02) [2p] | no |

† `discernment-nudge` and `academy-guide` do have `LICENSE.txt` (Apache-2.0). `doc-coauthoring` has none [2].
### Findings
- **What it is:** 18 skill folders, the Agent Skills spec and a template. README:20 states that docx/pdf/pptx/xlsx are "source-available, not open source" [2].
- **Proprietary licence:** `skills/pdf/LICENSE.txt` says users may not "Reproduce or copy these materials" or "Create derivative works" [2].
- **Installer:** `/plugin marketplace add anthropics/skills`, then `/plugin install document-skills@anthropic-agent-skills` or `example-skills@…` (README:34–48). `.claude-plugin/marketplace.json` lists skills only. There is no hooks file and no `.mcp.json`, and `git grep` finds no `dangerously-skip-permissions` [2].
- **Scripts:** `skills/skill-creator/scripts/run_eval.py:70–76` and `improve_description.py:26` shell out to `claude -p` with no bypass flags [2].
### Files worth borrowing
| path | purpose | self-contained? | adaptation needed |
|---|---|---|---|
| skills/skill-creator/SKILL.md (+ agents/grader.md, analyzer.md, comparator.md; LICENSE.txt Apache-2.0) | Create skills and evaluate them against test prompts | SKILL.md: yes. Scripts: no (`claude -p`) | Use the prose and agents to package MEGAMIND skills once; keep the Apache NOTICE |
| skills/mcp-builder/SKILL.md + reference/*.md (Apache-2.0) | MCP server design and evaluation guidance | SKILL.md: yes; `scripts/*.py` need pip deps | Directly relevant to the read-only vault connector design |
| skills/discernment-nudge/SKILL.md (Apache-2.0) | Append 2–3 check-your-reliance questions after substantive answers | yes | Optional for vault query answers |
| skills/doc-coauthoring/SKILL.md | Three-stage doc co-authoring workflow | yes | **Ideas only**: no licence file |
| skills/pdf/SKILL.md | PDF handling | — | **Do not copy**: proprietary |
### Safety verdict
**File by file for the Apache-2.0 skills only**, keeping each `LICENSE.txt`. **Ideas only** for `doc-coauthoring` (no licence). **Exclude** `docx`/`pdf`/`pptx`/`xlsx` (`skills/pdf/LICENSE.txt`: copying prohibited). PDF handling for MEGAMIND therefore needs another permissively licensed source.

## 3. wshobson/agents
### Pin
| repo | HEAD SHA | commit date | licence file, first line | stars (page, date) | archived? |
|---|---|---|---|---|---|
| wshobson/agents | 7e2fb559cf4b824b27f1fec49fe88f7511066d26 | 2026-10-30 (3 days) | `LICENSE`: "MIT License" (© 2024 Seth Hobson) | 41.9k (2026-11-02) [3p] | no |
### Findings
- **Size:** 92 plugin directories, 202 agents, 185 SKILL.md and 105 commands at HEAD (from `ls-tree`). README says "94 plugins, including 92 local plugins and 2 external entries" [3][3p].
- **Installer:** `/plugin marketplace add wshobson/agents`, then `/plugin install <plugin>@claude-code-workflows` (README:46–47). README also offers skills-only routes via `gh skill install` or `npx skills add` [3p].
- **Hooks:** only `plugins/protect-mcp/hooks/hooks.json` and `plugins/review-agent-governance/hooks/hooks.json` contain hooks. Both register PreToolUse `.*` → `evaluate.sh` and PostToolUse `.*` → `sign.sh` [3]:
  - The scripts run `npx protect-mcp@0.31.1` and `npx protect-mcp@0.7.4`. These are pinned, without `-y` (`evaluate.sh:33`, `sign.sh:18`).
  - With no policy file, every tool call is allowed (`evaluate.sh:9–12`).
- No `dangerously-skip-permissions` or `bypassPermissions` anywhere; the only `mcpServers` hit is in a README [3].
- **grounded-vault:** `plugins/documentation-standards/skills/grounded-vault/SKILL.md` (104 lines) [3]:
  - Uses a `raw/` (immutable) / `wiki/` / `archive/` layout.
  - Every page carries a header block with `Raw:`, `Fingerprint: git:<sha>`, `Monitored:` and `Status: Current|Outdated|Disputed`.
  - Grounding rule: every number, date and quote must appear verbatim in the linked raw file.
  - Drift check: `git diff --stat <fp>..HEAD -- <monitored>`.
  - Superseded pages move to `archive/` "never deleted".
  - The plugin.json author is Niksa Barlovic, licence MIT. `references/details.md` embeds a stdlib-only `check_vault.py` and credits `PALAN-K/llm-wiki-loop` (MIT) as the reference implementation.
### Files worth borrowing
| path | purpose | self-contained? | adaptation needed |
|---|---|---|---|
| plugins/documentation-standards/skills/grounded-vault/SKILL.md | Per-claim provenance, git-fingerprint drift detection, archive-never-delete | yes (git only) | Map `Raw:` → `derived_from::`, `Monitored:` → `depends_on::`, `archive/` → `## Superseded`; keep MIT notice (© Seth Hobson; plugin author Niksa Barlovic) |
| plugins/documentation-standards/skills/grounded-vault/references/details.md | `check_vault.py` (stdlib + `git`), index/log templates, edge cases | script is inline Markdown; would need extracting and review | Owner reviews before any run; overlaps Astro-Han `check_evidence.py` |
| plugins/documentation-generation/skills/changelog-automation/SKILL.md | Keep a Changelog / release notes | yes | Use for `log.md` / release-note hygiene |
| plugins/documentation-generation/skills/architecture-decision-records/SKILL.md (+ references) | ADR templates | yes | Alternative to the ECC ADR skill; pick one |
| plugins/avoid-ai-writing/skills/avoid-ai-writing/SKILL.md (+ references) | Prose de-slop pattern catalogue | yes | Optional page-quality lint |
### Safety verdict
**Install file by file** (the SKILL.md files above). **Reject** `plugins/protect-mcp` and `plugins/review-agent-governance` as installs: they add PreToolUse/PostToolUse hooks that run `npx` on every tool call (`plugins/protect-mcp/hooks/hooks.json`, `evaluate.sh:33`). Do not use the marketplace.

## 4. vanillaflava/llm-wiki-skills
### Pin
| repo | HEAD SHA | commit date | licence file, first line | stars (page, date) | archived? |
|---|---|---|---|---|---|
| vanillaflava/llm-wiki-skills | ff6f7be1a0e397192a1ac4a0d06d298062e9b208 | 2026-07-11 (114 days) | `LICENSE`: "MIT License" (© 2026 Axel Tölke) | 70 (2026-11-02) [4p] | no |
### Findings
- **What it is:** 6 prose skills (`wiki-config`, `wiki-ingest`, `wiki-query`, `wiki-lint`, `wiki-integrate`, `wiki-crystallize`). Each also ships as a `.skill` zip at the repo root for Claude Desktop upload. README says they have "no code, no scripts, no remote connections" [4][4p].
- **Installer:** `npx skills add vanillaflava/llm-wiki-skills --all`, which installs to `~/.agents/skills/` with symlinks and "always fetches the latest version from master" (unpinned); or a manual folder copy [4p]. No hooks, no MCP.
- **Conflict with `raw/`:** `wiki-ingest/SKILL.md:10` says "The move of each file into `ingested/` is the atomic commit" [4].
- `wiki-lint` writes a dated report to `archive/` and checks em-dashes in titles and filenames (`wiki-lint/SKILL.md:50,92–94`) [4].
- Frontmatter gains `source:` and `reliability: high|medium|low`, plus a `## Pending Review` section for single low-confidence sources [4p].
### Files worth borrowing
| path | purpose | self-contained? | adaptation needed |
|---|---|---|---|
| wiki-crystallize/SKILL.md | Distil a long chat/session into a wiki page; update domain homes | yes | Ideas for the "file it" write path; must not touch `raw/` |
| wiki-lint/SKILL.md §6b | Em-dash in titles breaks wikilinks | yes | Add as one T0 lint rule |
| wiki-config/assets/wiki-schema.md | Mandatory/conditional frontmatter enums | yes | Compare with the MEGAMIND page schema |
### Safety verdict
**Ideas only.** The ingest step moves files out of `raw/` (`wiki-ingest/SKILL.md:10,53`), which breaks the read-only `raw/` limit (HL 8). The install path is unpinned `npx skills add` from master. The licence (MIT) would allow copying the prose rules if adapted.

## 5. TrueHOOHA/LLM-Wiki
### Pin
| repo | HEAD SHA | commit date | licence file, first line | stars (page, date) | archived? |
|---|---|---|---|---|---|
| TrueHOOHA/LLM-Wiki | 0455b71e04bafa7a419b308fca254a56d599a585 | 2026-07-16 (109 days) | `LICENSE`: "Apache License Version 2.0, January 2004" | 22 (2026-11-02) [5p] | no |
### Findings
- **What it is:** a template vault [5]:
  - `AGENTS.md` schema and `SPEC.md` (Open Knowledge Format v0.1 draft)
  - 3 skills in `.agents/skills/` (ingest 55 lines, query 43, lint 128)
  - `wiki/{entities,concepts,sources,syntheses,templates}`
  - README states "there are no helper scripts to run" [5p]
- **Installer:** none; you clone the template. No hooks, no MCP, no scripts [5].
- `raw/sources/2026-05-15--karpathy-llm-wiki-gist.md` is a copy of a third-party gist inside an Apache-2.0 repo. Its own licence is not stated [5].
- **Lint checks** (`llm-wiki-lint/SKILL.md:29–88`): OKF conformance, producer conventions (numbered `# Citations`), link health (wikilinks internal, Markdown links external), reserved files, contradictions, stale claims, orphans, missing pages, data gaps [5].
### Files worth borrowing
| path | purpose | self-contained? | adaptation needed |
|---|---|---|---|
| .agents/skills/llm-wiki-lint/SKILL.md | 9-class lint with severity output and "Done Gate" | yes | Replace OKF checks with MEGAMIND frontmatter; keep the Apache-2.0 notice |
| .agents/skills/llm-wiki-ingest/SKILL.md | "Required Step Order (exact)" plus Done Gate | yes | Pattern for strict step ordering |
| SPEC.md | OKF v0.1 bundle/frontmatter/citations spec | yes | Reference only; Astro-Han deliberately defers OKF |
### Safety verdict
**Install file by file** (prose skills under Apache-2.0, notice kept). Nothing executes, and there are no installer writes. Do not copy `raw/sources/*gist*` (third-party content, licence unknown).

## 6. charlie947/ai-second-brain
### Pin
| repo | HEAD SHA | commit date | licence file, first line | stars (page, date) | archived? |
|---|---|---|---|---|---|
| charlie947/ai-second-brain | 6b14a5282f3fe1cbb6beb45b7a9444adcc0f84ab | 2026-10-24 (9 days) | `LICENSE`: "MIT License" (© 2026 Charlie Hills) | 198 (2026-11-02) [6p] | no |
### Findings
- **What it is:** one 217-line `SKILL.md` that walks a non-technical user through three steps: AI Brain from exports, a Karpathy wiki, and a "Living Wiki" with connectors, iMessage Channels and slash commands. `ai-second-brain.skill` is a zip of that same `SKILL.md` [6].
- **Installer:** `git clone … ~/.claude/skills/ai-second-brain` and later `git pull`, both unpinned (README "Install") [6p]. No hooks, no MCP config, no settings writes.
- The skill tells Claude to run or set up several things on the user's machine [6]:
  - `curl -L https://gist.githubusercontent.com/karpathy/…/raw -o ~/Desktop/Brain/CLAUDE.md` (SKILL.md:101). The gist is unpinned and becomes the instruction file; it is not piped to a shell.
  - "Install the NotebookLM skill" from an unnamed source (:151).
  - `claude --channels plugin:imessage@claude-plugins-official` (:167).
  - macOS **Full Disk Access** for Terminal (:172–173).
- **How it parses ChatGPT and Claude exports** (for R3, the chat-history converter):
  - **Export requests** are user-side instructions only. ChatGPT: Settings → Data Controls → "Export data" (SKILL.md:46). Claude: Settings → Privacy → "Export Data" (:49). The user unzips both folders into `~/Desktop/Brain` (:55–61) [6].
  - **There is no parser.** Step 1c (:83) is a single natural-language prompt to Claude Code, which asks it to convert all ChatGPT and Claude conversations into individual Markdown files with frontmatter "(title, date, tags, category)", then run "10 sub-agents" to tag people, places, themes and projects and add wikilinks. Line :86 adds that this "will run for several minutes and spawn 10 sub-agents in parallel" [6].
  - **File names read:** none specified. `conversations.json`, `users.json` and `projects` do not appear in the repo (`git grep` on SKILL.md finds no `.json` file names) [6].
  - **JSON keys read:** none specified. `mapping`, `create_time`, `chat_messages`, `created_at`, `uuid` and `sender` do not appear [6].
  - **Dating and naming of output files:** not specified. The only requirement is a `date` frontmatter field; file naming, timezone, redaction and one-file-per-chat rules are left to the model [6].
  - **Implication:** nothing here can be reused as a deterministic converter. R3 must take export formats from another source.
### Files worth borrowing
| path | purpose | self-contained? | adaptation needed |
|---|---|---|---|
| SKILL.md:41–51 (prose only) | User-facing steps to request both exports | yes | Ideas only: wording for an owner runbook |
| SKILL.md:205–217 ("Things that commonly go wrong") | Pitfalls (spaces in folder names, wrong cwd) | yes | Ideas only |
### Safety verdict
**Ideas only.** There is no reusable parser. The skill fetches an unpinned remote file into `CLAUDE.md` (SKILL.md:101) and instructs installing an unnamed skill (:151). It pushes macOS Full Disk Access (:172) and an always-listening iMessage channel (:167), and it wires Gmail/Granola connectors. Every one of these conflicts with the vault's least-privilege posture. MIT would allow copying, but nothing is worth copying.

## 7. Astro-Han/karpathy-llm-wiki (the skill MEGAMIND forks)
### Pin
| repo | HEAD SHA | commit date | licence file, first line | stars (page, date) | archived? |
|---|---|---|---|---|---|
| Astro-Han/karpathy-llm-wiki | eafcc77001e496cc43499e4923b663aec722c813 | 2026-07-24 (101 days); subject "fix: align log inventory and examples" | `LICENSE`: "MIT License" (© 2026 Yuhan Lei) | 2.6k (2026-11-02) [7p] | no |
### Findings
- **What it is:** one `SKILL.md` (233 lines) with Ingest (Fetch → Triage → Compile → Cascade → Post-Ingest), Query, Lint (safe fixes / mechanical reports / judgment reports), 4 reference templates, examples, `scripts/check_evidence.py` and a test file [7].
- **Grounding invariant** (`SKILL.md:39–44`): numbers, dates and quotes exist verbatim in the `raw/` files named in the article's Raw field. Compile establishes it, lint verifies it [7].
- **`scripts/check_evidence.py`** (431 lines; imports only `re`, `sys`, `dataclasses`, `pathlib`) is "Report-only; never modifies files" and runs three sweeps: Fidelity, Evidence errors, Inventory (orphan raw files) [7].
- **Installer:** README gives `npx add-skill Astro-Han/karpathy-llm-wiki`, which is unpinned. Alternatively copy `SKILL.md`, `references/` and `scripts/`. No hooks, no MCP [7p].
- The README "Design Boundaries" section explicitly excludes several things [7p]:
  - automatic hooks and scheduled runs
  - vector/graph search
  - numeric confidence
  - per-article review dates
  - source-hash tracking
  - OKF
### Files worth borrowing
| path | purpose | self-contained? | adaptation needed |
|---|---|---|---|
| SKILL.md | Ingest/query/lint protocol (already forked by MEGAMIND) | yes | Re-pin the fork to eafcc77 and diff against the current fork |
| scripts/check_evidence.py | Fidelity check of wiki literals against linked `raw/` | yes (stdlib, read-only) | Owner reviews, then T0 runs it as report-only; field name `Raw` → `derived_from::` |
| references/{article,raw,index,archive}-template.md | Page templates | yes | Add `depends_on::` |
### Safety verdict
**Install file by file** (MIT, notice kept). The script is stdlib-only and report-only (`scripts/check_evidence.py:4`). Avoid `npx add-skill` (unpinned).

## 8. SubFreq/agent-governance-framework
### Pin
| repo | HEAD SHA | commit date | licence file, first line | stars (page, date) | archived? |
|---|---|---|---|---|---|
| SubFreq/agent-governance-framework | 95232cc52fdd20376130672189ed1dff0bc46485 | 2026-08-01 (93 days); 1 commit total [8p] | `LICENSE`: "MIT License" (© 2026 SubFreq) | 5 (2026-11-02) [8p] | no |
### Findings
- **What it is:** governed agent workflow with seats (Owner / Orchestrator / Implementor / Reviewer), six skills in `.claude/skills/` and `docs/DECISION_LEDGER.md`. Entries are `RUL-<n>`, append-only, and reversal is a *new* entry [8][8p].
- **Enforcement:** `.githooks/pre-commit` → `node scripts/slice-check.mjs precommit` blocks edits to settled ledger content (byte-level append-only) and changes under closed slices [8p].
- **Installer:** copy the skeleton. `package.json` has `"prepare": "git config core.hooksPath .githooks"`, so `npm install` silently switches the repo's git hooks path; it depends on `js-yaml ^4.1.0`. These are git hooks, not Claude Code hooks. No MCP, no settings writes, no bypass flags [8].
- `review-slice/SKILL.md:17` launches a cross-ecosystem reviewer "non-interactively via the Codex CLI". That would send vault content to another vendor [8].
### Files worth borrowing
| path | purpose | self-contained? | adaptation needed |
|---|---|---|---|
| docs/DECISION_LEDGER.md (format) + README "The decision ledger" | Append-only rulings; cite, never re-ask; reversal = new entry | yes | Ideas for `07-decisions.md` and vault `log.md` |
| .claude/skills/post-mortem/SKILL.md (49 lines) | Telemetry-grounded retrospective that lands changes as diffs | yes | Ideas for the ratchet's experiment review |
### Safety verdict
**Ideas only.** `npm install` rewrites git config through `prepare` (`package.json` scripts), and enforcement depends on running repo JS (`scripts/slice-check.mjs`). The reviewer seat uses a non-Anthropic CLI, which conflicts with HL 7 for vault content. Only 1 commit and 5 stars, so it is unproven.

## 9. AgriciDaniel/claude-obsidian (extra, found by search)
### Pin
| repo | HEAD SHA | commit date | licence file, first line | stars (page, date) | archived? |
|---|---|---|---|---|---|
| AgriciDaniel/claude-obsidian | 2e545563172f97f02ecaaaab376ceea1246a0583 | 2026-10-22 (11 days) | `LICENSE`: "MIT License" (© 2026 AgriciDaniel); `ATTRIBUTION.md:15–22`: two CSS snippets are GPL-2.0 | 15.9k (2026-11-02) [9p] | no |
### Findings
- **What it is:** plugin v3.0.1 with 15 skills, 3 read-only agents and a Python core (`scripts/claude-obsidian.py`, `claude_obsidian/`). It keeps separate ledgers: `.raw/.manifest.json`, `wiki/meta/ledgers/source-ledger.json` (SHA-256, authority, review state) and `claim-ledger.json` (`skills/wiki/references/provenance.md`) [9].
- **Installer:** `claude plugin marketplace add AgriciDaniel/claude-obsidian` + `claude plugin install …` (README:74–75) [9]. `hooks/hooks.json` registers 2 hooks:
  - SessionStart (`startup|resume|clear|compact|fork`) → `python3 scripts/claude-obsidian.py hook session-start`. It is silent unless `CLAUDE_OBSIDIAN_SESSION_CONTEXT=1`.
  - Stop → `… hook stop`.
  - `hooks/README.md` says hooks "never write knowledge … commit Git, run remote calls".
  - No MCP in `plugin.json`; no bypass flags.
- **Transaction contract:** reads targets and records their SHA-256, workers only draft, the orchestrator applies one plan, and applies need an approved plan hash (`skills/wiki/references/operation-transactions.md`; README:265) [9][9p].
- Skills reference the Python core: 13 of 15 SKILL.md mention `claude-obsidian.py`/`CLAUDE_PLUGIN_ROOT`, and `wiki-retrieve` calls `scripts/bm25-index.py`, `retrieve.py` and `rerank.py` [9].
### Files worth borrowing
| path | purpose | self-contained? | adaptation needed |
|---|---|---|---|
| skills/wiki/references/provenance.md | Source authority enum, `independence_key`, separate source vs claim ledgers | yes (prose; CLI snippet at top) | Ideas for `derived_from::` authority levels |
| skills/wiki/references/operation-transactions.md | Read-hash → one plan → approved apply → recover | prose, but tied to CLI | Ideas: "propose, owner merges" could carry a plan hash |
| skills/think/SKILL.md | Read-only structured review loop | yes | Optional |
### Safety verdict
**Ideas only.** The plugin auto-adds 2 hooks (`hooks/hooks.json`), and the skills need its Python runtime (`skills/wiki-retrieve/SKILL.md:16–19`). The licence is mixed: MIT, plus GPL-2.0 CSS listed in `ATTRIBUTION.md:19–22`.

## 10. nvk/llm-wiki (extra, found by search)
### Pin
| repo | HEAD SHA | commit date | licence file, first line | stars (page, date) | archived? |
|---|---|---|---|---|---|
| nvk/llm-wiki | d60674ff785e5c6d35322657d7839a7c0bdd3ca7 | 2026-10-25 (8 days) | `LICENSE`: "MIT License" (© 2026 nvk) | 1.4k (2026-11-02) [10p] | no |
### Findings
- **What it is:** a multi-runtime wiki protocol. `claude-plugin/` holds 28 commands, the `wiki-manager` skill with 24 reference files, and `bin/llm-wiki` (Python helper). Its Claude plugin.json declares no hooks or MCP, and `claude-plugin/` has no `hooks/` directory. Hooks ship only in the Codex plugin (`plugins/llm-wiki/hooks/`) [10].
- **Installer:** `claude plugin marketplace add nvk/llm-wiki` + `claude plugin install wiki@llm-wiki` (README:65–71). The README also shows `curl -sL …raw…/AGENTS.md > ~/your-project/AGENTS.md`: an unpinned overwrite, not piped to a shell [10][10p].
- **Lint catalogue** (`claude-plugin/skills/wiki-manager/references/linting.md`):
  - C4b Source Provenance (:120–137): dangling `sources:`, orphan raw files, retracted markers
  - C14 Freshness (:343–357): a 0–100 score scaled by `volatility`, with **no auto-fix** because "automated recompilation risks the 'confident wrong answer' problem"
  - C15 Missing Volatility (:359) [10]
- README says research modes run 5/8/10 parallel web agents, with options like `--min-time 2h` [10p].
### Files worth borrowing
| path | purpose | self-contained? | adaptation needed |
|---|---|---|---|
| claude-plugin/skills/wiki-manager/references/linting.md (C4b, C14, C15 sections) | Provenance and freshness lint rules with severity | prose (one CLI mention) | Ideas: add `volatility` + `verified` fields; no auto-fix for staleness |
| claude-plugin/skills/wiki-manager/references/query-lite.md | Compact read-only query protocol | yes | Ideas for a Haiku query profile |
### Safety verdict
**Ideas only.** The protocol is large and coupled to its helper CLI and hub layout. It is fine as reading material; nothing needs installing. The README's unpinned `curl … > AGENTS.md` overwrite pattern is not to be copied.

## 11. ekadetov/llm-wiki (extra, found by search)
### Pin
| repo | HEAD SHA | commit date | licence file, first line | stars (page, date) | archived? |
|---|---|---|---|---|---|
| ekadetov/llm-wiki | 5e49545a3339369cb879f1f1255c1f10e2c0ebcb | 2026-04-06 (210 days) | `LICENSE`: "MIT License" (© 2026 ekadetov) | 109 (2026-11-02) [11p] | no |
### Findings
- **What it is:** a 13-file plugin: `/llm-wiki:wiki` command, one skill with 2 references, `scripts/lint-wiki.py` (stdlib: dead links, orphans, missing source refs) and qmd integration [11].
- `hooks/hooks.json` registers SessionStart → `bash ${CLAUDE_PLUGIN_ROOT}/scripts/install-deps.sh` (timeout 120). The script runs `npm install @tobilu/qmd @marp-team/marp-cli` with **no versions** into `CLAUDE_PLUGIN_DATA` (`scripts/install-deps.sh`, the "Install packages" line) [11].
- README says it auto-commits wiki changes with git and hard-codes `~/ObsidianVault/03-Resources/` [11p].
### Files worth borrowing
| path | purpose | self-contained? | adaptation needed |
|---|---|---|---|
| scripts/lint-wiki.py | Minimal deterministic lint | yes (stdlib) | Ideas only (Astro-Han's script is stronger) |
### Safety verdict
**Reject.** A hook added on install runs unpinned `npm install` at every new session until the sentinel exists (`hooks/hooks.json`; `scripts/install-deps.sh`). That is the "unpinned package execution added automatically" case. The repo is also stale (210 days).

## claude-mem (lesson only, as instructed)
Pinned at 1466db2 (2026-11-01); the README states Apache-2.0 [12]. Lesson: typed observations (`decision`, `bugfix`, `security_alert`, `sensitive`) are appended as dated `- YYYY-MM-DD [awareness] …` lines into monthly `memory/log/YYYY-MM.md` files. Caveat: the default install uses its hosted memory ("CMEM Pro"), so data leaves the machine unless `--provider` is set [12].

## Prior-audit claims checked
| claim | confirmed/corrected | evidence |
|---|---|---|
| (brief) karpathy-llm-wiki holds the ingest/query/lint skills MEGAMIND forks | confirmed | `SKILL.md` sections Ingest (:45), Query (:132), Lint (:164) at eafcc77 |
| (brief) charlie947 parses ChatGPT and Claude exports | **corrected**: it has no parser; one free-form prompt delegates conversion to Claude | `SKILL.md:83,86`; no JSON file names or keys in the repo |
No other prior-audit claims were given for these repositories.

## Could not verify
- Whether Claude Code adds a plugin's `bin/` directory to PATH (relevant to nvk's `claude-plugin/bin/llm-wiki`). That is Claude Code behaviour, not something in the repo.
- The licence of the Karpathy gist copy in `TrueHOOHA/LLM-Wiki/raw/sources/` and of the gist that charlie947 downloads.
- Contents of npm packages referenced (`protect-mcp@0.31.1`, `@tobilu/qmd`, `defuddle`, `knap`, `skills`/`add-skill` CLIs). I read only the git trees at the SHAs.
- The ChatGPT/Claude export schemas themselves. charlie947 does not document them, so R3 needs another source.
- `PALAN-K/llm-wiki-loop` (credited by grounded-vault). Not cloned; it is outside scope.

## Relevance to MEGAMIND
- **Skills plan (04):**
  - Strongest file-by-file adds for "every page honest": `grounded-vault/SKILL.md` (wshobson, MIT), `Astro-Han scripts/check_evidence.py` (MIT, stdlib, report-only), and TrueHOOHA's `llm-wiki-lint/SKILL.md` (Apache-2.0).
  - For Obsidian syntax: `kepano obsidian-markdown` / `json-canvas` / `obsidian-bases` (MIT).
  - For packaging skills once: `anthropics/skills skill-creator` (Apache-2.0).
- **Re-pin the fork:** MEGAMIND's karpathy-llm-wiki fork should be re-pinned to eafcc77 and diffed. Its "Design Boundaries" list (no hooks, no vector search, no numeric confidence) matches MEGAMIND's propose-only posture.
- **Vault connector design:** `anthropics/skills mcp-builder` (Apache-2.0) is the only licensed MCP-building guide found here.
- **Chat-history converter (R3):** charlie947 gives no parser, keys or naming scheme. Do not cite it as a format source.
- **PDF handling:** the only official PDF skill (`anthropics/skills/pdf`) is proprietary and may not be copied, so that is a gap for 04.
- **Lint rules for T0:** em-dash in titles (vanillaflava), C14 freshness with no auto-fix (nvk), and source authority/independence (claude-obsidian) are candidate rules.
- **Hard limits:** reject ekadetov (auto `npm install` hook). Do not install wshobson `protect-mcp` / `review-agent-governance` (tool-call hooks running `npx`). Install charlie947 nowhere (Full Disk Access, iMessage, unpinned remote `CLAUDE.md`).

## Sources
[1] https://github.com/kepano/obsidian-skills — clone at 3ccff5338ea700537839b21900aa5358a0402c98 (2026-09-15) — read 2026-11-02 · [1p] repository page — read 2026-11-02
[2] https://github.com/anthropics/skills — clone at ca45fc496a3436251f191354091d557da31c15b5 (2026-10-28) — read 2026-11-02 · [2p] repository page — read 2026-11-02
[3] https://github.com/wshobson/agents — clone at 7e2fb559cf4b824b27f1fec49fe88f7511066d26 (2026-10-30) — read 2026-11-02 · [3p] repository page — read 2026-11-02
[4] https://github.com/vanillaflava/llm-wiki-skills — clone at ff6f7be1a0e397192a1ac4a0d06d298062e9b208 (2026-07-11) — read 2026-11-02 · [4p] repository page — read 2026-11-02
[5] https://github.com/TrueHOOHA/LLM-Wiki — clone at 0455b71e04bafa7a419b308fca254a56d599a585 (2026-07-16) — read 2026-11-02 · [5p] repository page — read 2026-11-02
[6] https://github.com/charlie947/ai-second-brain — clone at 6b14a5282f3fe1cbb6beb45b7a9444adcc0f84ab (2026-10-24) — read 2026-11-02 · [6p] repository page — read 2026-11-02
[7] https://github.com/Astro-Han/karpathy-llm-wiki — clone at eafcc77001e496cc43499e4923b663aec722c813 (2026-07-24) — read 2026-11-02 · [7p] repository page — read 2026-11-02
[8] https://github.com/SubFreq/agent-governance-framework — clone at 95232cc52fdd20376130672189ed1dff0bc46485 (2026-08-01) — read 2026-11-02 · [8p] repository page — read 2026-11-02
[9] https://github.com/AgriciDaniel/claude-obsidian — clone at 2e545563172f97f02ecaaaab376ceea1246a0583 (2026-10-22) — read 2026-11-02 · [9p] repository page — read 2026-11-02
[10] https://github.com/nvk/llm-wiki — clone at d60674ff785e5c6d35322657d7839a7c0bdd3ca7 (2026-10-25) — read 2026-11-02 · [10p] repository page — read 2026-11-02
[11] https://github.com/ekadetov/llm-wiki — clone at 5e49545a3339369cb879f1f1255c1f10e2c0ebcb (2026-04-06) — read 2026-11-02 · [11p] repository page — read 2026-11-02
[12] https://github.com/thedotmack/claude-mem — clone at 1466db2d8d45911e062680fba9c3c4cda92f0a47 (2026-11-01), README.md only — read 2026-11-02
Search used to find extras: web search "Claude Code skills LLM wiki Obsidian vault github 2026" — 2026-11-02.
