# 04 — Skills and plugins plan
Drafted by R2 (megamind-researcher), 2026-11-02, for auditor sign-off. Inputs: `02-research/b-ecc.md`, `c-omc.md`, `d-more-repos.md` (R2) and `e-skills-install.md` [e] (R1). Every upstream file was read at a pinned clone. Nothing in this plan has been installed or run.

## Summary (10 lines)
1. This plan covers 18 items: 15 adopted adapted, 2 adopted as is (obsidian-markdown, loop-design-check) and 1 reference only (mcp-builder). They come from 7 upstream repositories, each pinned to a full SHA under a licence that permits copying (MIT or Apache-2.0) (§1).
2. Core of the plan: the three karpathy-llm-wiki operations (`ingest`, `query`, `lint`), re-pinned to Astro-Han eafcc77, plus that repo's `check_evidence.py`. The script is modified only to read `derived_from::` instead of `> Raw:` (§2.1–2.4).
3. The adapted items share three rules that come from the vault, not upstream:
   - Claude never writes to `raw/`.
   - `index.md` is never written by a skill.
   - Provenance and edges use only `derived_from::` and `depends_on:: [[page]] (reason)`.
4. The PDF gap is covered without the proprietary anthropics/skills `pdf` skill. A root-owned script runs Debian `pdftotext` (poppler-utils, GPL-2 or GPL-3, used as an installed tool, not copied) and writes into `raw/` (§2.19).
5. 17 items are rejected for install. Each has a cited reason: a permission bypass, a settings or CLAUDE.md rewrite, auto-added hooks or MCP servers, unpinned package installs, or a licence that forbids copying (§2.20).
6. Packaging uses one source tree in this repository: `skills/<name>/SKILL.md`. Frontmatter is limited to the six spec fields, and `name` equals the folder name [e5][e13]. Licence notices go in `NOTICES.md` and upstream pins in `skills/pins.json` (§3).
7. One build script produces three outputs:
   - (a) one zip per skill for claude.ai `Customize > Skills` [e1][e2];
   - (b) a Claude Code plugin from a root `.claude-plugin/marketplace.json` using `"source": "./"`, `"strict": false` and a `skills` list, the anthropics/skills pattern [e15][P3];
   - (c) `ant apply skills/<name>` uploads for Managed Agents [e11][e14].
8. Recommendation: use `ant apply` uploads for Managed Agents, and **do not** keep a `.claude/skills/` mirror. The fleet repo is mounted by the scout, and a root `.claude/skills/` would be auto-loaded with no review step (05 §3a; [e11]).
9. No item needs a per-target variant if two conditions hold: frontmatter stays inside the six fields, and descriptions stay ≤200 characters. 200 is claude.ai's stricter stated limit [e2]; the spec allows 1,024 [e13]. The remaining differences are runtime ones: no vault on claude.ai, no network in the API container, plugin namespacing in Claude Code (§3.5).
10. The fortnightly scout may refresh SKILL.md and `references/` from an upstream pin by PR. It never touches `scripts/`; script changes become proposals for the owner. The owner merges and the owner installs (§3.7).

---

## 1. Adopted items

Verdicts: **as is** means copied unchanged except frontmatter checks. **adapted** means a MEGAMIND-owned derivative, with the changes recorded in `skills/pins.json`. **reference** means read for design; not packaged.

| # | MEGAMIND skill name | Source repo @ SHA(7) | Upstream path | Licence | What it does for MEGAMIND | Verdict |
|---|---|---|---|---|---|---|
| 1 | `ingest` | Astro-Han/karpathy-llm-wiki @ eafcc77 | `SKILL.md` §Ingest (L45–131), `references/article-template.md` | MIT | Compiles one `raw/` file into wiki pages with triage, cascade updates and a log entry | adapted |
| 2 | `query` | Astro-Han/karpathy-llm-wiki @ eafcc77 | `SKILL.md` §Query (L132–160) | MIT | Answers from the vault first, cites pages, writes nothing unless asked | adapted |
| 3 | `lint` | Astro-Han/karpathy-llm-wiki @ eafcc77 | `SKILL.md` §Lint (L164–225) | MIT | Index, link, provenance and judgment checks; reports only | adapted |
| 4 | `lint/scripts/check_evidence.py` | Astro-Han/karpathy-llm-wiki @ eafcc77 | `scripts/check_evidence.py` (431 lines) | MIT | Report-only check that numbers, dates and quotes in pages exist verbatim in the linked `raw/` files, plus orphan raw files | adapted (2 regexes) |
| 5 | `grounded-vault` | wshobson/agents @ 7e2fb55 | `plugins/documentation-standards/skills/grounded-vault/SKILL.md` | MIT | Grounding rule, git-fingerprint drift check for pages that describe server configs, archive-never-delete | adapted |
| 6 | `living-docs-governance` | affaan-m/ECC @ b38be6a | `skills/living-docs-governance/SKILL.md` | MIT | Four doc roles (constitution, map, status, history), one owner per fact, dated corrections | adapted |
| 7 | `change-impact` | affaan-m/ECC @ b38be6a | `skills/change-impact/SKILL.md` | MIT | Before and after a page edit, lists every page that `depends_on::` it and reconciles the plan with the diff | adapted |
| 8 | rules merged into `lint` | TrueHOOHA/LLM-Wiki @ 0455b71 | `.agents/skills/llm-wiki-lint/SKILL.md` (L27–88) | Apache-2.0 | Severity-rated lint classes (contradictions, stale claims, orphans, missing pages, data gaps) and a Verification Checklist | adapted (merged into #3) |
| 9 | `obsidian-markdown` | kepano/obsidian-skills @ 3ccff53 | `skills/obsidian-markdown/` (SKILL.md + 3 references) | MIT | Correct wikilinks, embeds, callouts and properties for pages the owner reads in Obsidian | as is |
| 10 | `loop-design-check` | affaan-m/ECC @ b38be6a | `skills/loop-design-check/SKILL.md` | MIT | Reviews housekeeping and ratchet loops for spinning, Goodhart-gaming the oracle and runaway | as is |
| 11 | `decision-ledger` | affaan-m/ECC @ b38be6a | `skills/recursive-decision-ledger/SKILL.md` | MIT | Append-only experiment ledger with marks and promotion gates; confidence never auto-approves | adapted |
| 12 | `vault-verify` | Yeachan-Heo/oh-my-claudecode @ 14cd0fe | `skills/verify/SKILL.md` | MIT | Evidence before "done": reports only what was actually checked | adapted |
| 13 | `vault-research` | Yeachan-Heo/oh-my-claudecode @ 14cd0fe | `skills/research/SKILL.md` | MIT | Question → vault first → official docs → findings with sources and unknowns (also used by the scout) | adapted |
| 14 | `critic-review` | Yeachan-Heo/oh-my-claudecode @ 14cd0fe | `agents/critic.md` | MIT | Read-only gap analysis of a plan or proposal ("what's missing"); used before owner merges | adapted (agent → skill) |
| 15 | `context-and-decisions` | affaan-m/ECC @ b38be6a | `skills/context-and-decisions/` (SKILL.md, LICENSE, references/source.md, templates/context.example.md) | MIT (ECC) + MIT (Matt Pocock) | Glossary discipline for vault terms; hands decisions to #16 | adapted |
| 16 | `decision-records` | affaan-m/ECC @ b38be6a | `skills/architecture-decision-records/SKILL.md` | MIT | Numbered decision pages with alternatives and consequences | adapted |
| 17 | `skill-creator` | anthropics/skills @ ca45fc4 | `skills/skill-creator/` (SKILL.md, agents/*.md, scripts/quick_validate.py, scripts/package_skill.py) | Apache-2.0 | Authoring and evaluating MEGAMIND skills. Its validator and packager are reused by the build script | adapted (Claude Code only) |
| 18 | `mcp-builder` | anthropics/skills @ ca45fc4 | `skills/mcp-builder/SKILL.md` + `reference/*.md` | Apache-2.0 | Design reference for the read-only vault connector (search/read tools) | reference only |

MEGAMIND's own skills (`scout-5090`, `crystallize`, `housekeeping`, `megamind-scout`) are packaged by the same pipeline. They have no upstream pin (origin `megamind` in `skills/pins.json`).

---

## 2. Item blocks

**Install paths shared by all packaged items.** Each block below states which of these targets apply.
- **claude.ai:**
  - Zip `<name>/` so the folder is the zip root [e2][e4].
  - Upload via `Customize > Skills` → `"+"` → `"+ Create skill"` → `"Upload a skill"` [e1].
  - Alternatively, upload the whole plugin zip via `Customize > Plugins` → `Add > Upload plugin` [e8][e9].
  - Account skills sync one way into Claude Code signed in with the same account (v2.1.273+), into `~/.claude/skills/synced/` [e1][e5].
- **Claude Code:**
  - Session form: `/plugin marketplace add <gh-user>/megamind-fleet#<tag>`, then `/plugin install megamind@megamind`. The session form "opens the plugin's details in the `/plugin` panel, where you install it" [P1 L97][P2 L190–201]. `#<tag>` pins a tag [P2 L196].
  - Shell form: `claude plugin marketplace add <gh-user>/megamind-fleet#<tag>` and `claude plugin install megamind@megamind` [P1 L84, L92][P2 L201].
  - Skills are invoked as `/megamind:<name>` [e5].
  - Both commands write user settings: the marketplace is "declared in user settings" [P1 L87], and a user-scope install puts `enabledPlugins` in `~/.claude/settings.json` [P2 L134]. Because settings are root-owned and owner-edited, **the owner runs them**.
- **Managed Agents:**
  - `ant apply skills/<name>` uploads the folder and records the `skill_*` ID in `claude-lock.json` [e14][e11].
  - The agent file lists `skills: [../skills/<name>]`, which is the form 05 §4 already uses for `megamind-scout`.
  - Upload limit: <30 MB uncompressed; `name` ≤64 characters, lowercase/digits/hyphens, no `anthropic`/`claude` [e12].

### 2.1 `ingest` (karpathy-llm-wiki, Ingest section)
- **What it does:** Fetch → Triage (New / Update / Disputed / No material) → Compile with source fidelity ("locate before you write") → Cascade updates → Post-Ingest log entry (`SKILL.md` L45–131).
- **Licence:** `LICENSE` L1 "MIT License", L3 "Copyright (c) 2026 Yuhan Lei". MIT requires the notice in all copies, so the notice **travels** in `NOTICES.md` and in the skill's `license:` field ("MIT; see NOTICES.md").
- **Commit SHA:** eafcc77001e496cc43499e4923b663aec722c813 (2026-07-24).
- **Safety verdict:**
  - Five checks (auditor-verified at the pinned SHA): installer: none used (file copy); `settings.json`: no write; hooks: none; MCP: none; bypass flags (`--dangerously-skip-permissions`, `bypassPermissions`): none.
  - Installer: README `npx add-skill Astro-Han/karpathy-llm-wiki` is unpinned and **not used**; we copy files. No settings rewrite, no hooks, no MCP. No `dangerously-skip-permissions` or `bypassPermissions` (d-more-repos §7).
  - The upstream frontmatter has only `name` and `description` (SKILL.md L1–4).
  - Verdict: install file by file.
- **What to adapt:**
  - **Remove Fetch (L49–62), which writes `raw/<topic>/…`.** In MEGAMIND, `raw/` is read-only for Claude. Ingest takes an existing `raw/` path, and sources are placed by the owner or by root-owned scripts (see §2.19 for PDFs).
  - **Remove Initialization (L28–37), which creates `wiki/index.md`.** Also change Post-Ingest (L102) from "Update `wiki/index.md`" to "write the proposed index line(s) into the ingest report for the owner". `index.md` is hand-maintained.
  - Replace the `> Raw:` / `> Sources:` header (`references/article-template.md` L3–5) with one `derived_from:: [[raw/<path>]]` line per source.
  - Replace "Status: Outdated" blocks (template L17–21; SKILL.md L96) with a `## Superseded` footer on the old claim's page.
  - Add the step "when a compiled page relies on another page, write `depends_on:: [[page]] (reason)`". No other field names are allowed.
  - Delete §Research (L122–128), which runs multi-source web search. Research belongs to `vault-research` and the scout.
  - Keep the "compile one source at a time" rule (L128). No subagents.
  - `name: ingest`; description ≤200 characters.
- **Install path:** Claude Code (VM vault and anywhere) and Managed Agents (if a cloud job ever ingests). On claude.ai: upload only if the owner wants the procedure available there; there is no vault on disk in chat [e4].
- **Notes:** The current fork's pin is not recorded in this run. Diff it against eafcc77 before replacing it (open question Q1).

### 2.2 `query` (karpathy-llm-wiki, Query section)
- **What it does:** "Read `wiki/index.md` … then full-text search … Never claim the wiki has no relevant content until both … come back empty". It cites pages and writes nothing unless asked (`SKILL.md` L139–144).
- **Licence:** as 2.1 (MIT, Yuhan Lei); the notice travels.
- **Commit SHA:** eafcc77001e496cc43499e4923b663aec722c813.
- **Safety verdict:** as 2.1. Read-only by design (L144). Install file by file.
  - Five checks (auditor-verified at the pinned SHA): installer: none used (file copy); `settings.json`: no write; hooks: none; MCP: none; bypass flags (`--dangerously-skip-permissions`, `bypassPermissions`): none.
- **What to adapt:**
  - Lookup order becomes `index.md` → qmd → pages. Dependency questions add `depends_on::` edges and `rg` backlinks.
  - Add "say what you could not see" (vault rule).
  - §Archiving (L146–160) writes a page and updates `wiki/index.md`. Keep page creation only on explicit owner request, and replace the index update (L156) with a proposed index line.
  - Citation format stays project-root-relative (L143).
  - For the vault connector (MCP) variant, the same text applies with "search/read tools" in place of `rg`/qmd.
- **Install path:** all three. On claude.ai and in chat, the skill pairs with the read-only vault connector, once one exists (see h-reachability.md).
- **Notes:** This is the skill most likely to be used from claude.ai. Its description must name the connector tools once those exist.

### 2.3 `lint` (karpathy-llm-wiki, Lint section, plus TrueHOOHA rules)
- **What it does:** Upstream has three tiers (SKILL.md L164–225):
  - Safe Fixes: index consistency, internal links, Raw references, See Also.
  - Mechanical Reports: the `check_evidence.py` run.
  - Judgment Reports: contradictions, outdated claims, orphans, missing pages.
- **Licence:** MIT (Yuhan Lei). The merged TrueHOOHA rules are Apache-2.0 (see 2.8). Both notices travel.
- **Commit SHA:** eafcc77001e496cc43499e4923b663aec722c813 (plus TrueHOOHA 0455b71e04bafa7a419b308fca254a56d599a585 for the merged rules).
- **Safety verdict:** as 2.1. Install file by file.
  - Five checks (auditor-verified at the pinned SHA): installer: none used (file copy); `settings.json`: no write; hooks: none; MCP: none; bypass flags (`--dangerously-skip-permissions`, `bypassPermissions`): none.
- **What to adapt:**
  - **Turn every "Safe Fix" into a report** (L168–191). Upstream adds missing index entries and rewrites paths, but in MEGAMIND lint proposes and the owner merges. It must never write `index.md`.
  - Replace "Raw references" (L182–185) with checks on `derived_from::` targets.
  - Add these `depends_on::` checks: the target exists; a `(reason)` is present; no other edge field names appear anywhere.
  - Replace "Malformed Status blocks" (L211) with "`## Superseded` footer present and dated".
  - Add from TrueHOOHA: severity labels and the Verification Checklist (see 2.8).
  - Add from vanillaflava (idea only, no text copied): em-dash in titles or filenames breaks wikilinks (d-more-repos §4).
  - Post-Lint log line (L217–223) stays.
  - Subagents: if split across topics, Haiku subagents (vault default).
- **Install path:** Claude Code (VM T0 housekeeping) and Managed Agents (only if a cloud job lints a mounted copy). Not useful on claude.ai, because the script needs the vault on disk [e4].
- **Notes:** T0 runs lint as a report. Hooks are not used: hooks are root-owned and none come from upstream.

### 2.4 `check_evidence.py` (inside `skills/lint/scripts/`)
- **What it does:** "Report-only; never modifies files" (L4). Three sweeps: Fidelity, Evidence errors, Inventory (L6–17). Imports only `re`, `sys`, `dataclasses`, `pathlib`. There is no network use, no `open(` and no write call; "write" appears only in the docstring at L25.
- **Licence:** MIT, Yuhan Lei; the notice travels. The modified file keeps a header line "Modified for MEGAMIND from Astro-Han/karpathy-llm-wiki@eafcc77".
- **Commit SHA:** eafcc77001e496cc43499e4923b663aec722c813.
- **Safety verdict:** no installer, no hooks, no MCP. Runs as `python3 <skill-dir>/scripts/check_evidence.py <root>` (SKILL.md L195). Install as a pinned, reviewed script.
  - Five checks (auditor-verified at the pinned SHA): installer: none used (file copy); `settings.json`: no write; hooks: none; MCP: none; bypass flags (`--dangerously-skip-permissions`, `bypassPermissions`): none.
- **What to adapt:**
  - `METADATA_RE` (L48) and `raw_links_of()` (L260–267) currently read `> Raw:` lines with Markdown links. They must read `derived_from::` lines with `[[raw/…]]` wikilinks or relative paths.
  - The "evidence must live in raw/" rule (L14, L304) stays.
  - The no-material log key (L324) must match the adapted log format.
  - Record the diff in `skills/pins.json` as `"modified": true` with a one-line reason. The owner reviews the script before first use.
- **Install path:** ships inside `lint`, so it reaches the same targets. On claude.ai it would only run against files uploaded into chat, so it is not useful there.
- **Notes:** The scout never refreshes this file (§3.7).

### 2.5 `grounded-vault`
- **What it does:**
  - Layers: `raw/` immutable, `wiki/` compiled, `archive/` "moved, never deleted" (L31).
  - Page header: `Raw:`, `Fingerprint: git:<sha>`, `Monitored:`, `Status:` (L44–53).
  - Grounding rule and a `git diff --stat <fp>..HEAD -- <monitored>` drift check.
  - Commit gate (L91–97).
- **Licence:** `LICENSE` L1 "MIT License", L3 "Copyright (c) 2024 Seth Hobson". The plugin manifest names author Niksa Barlovic, licence MIT (`plugins/documentation-standards/.claude-plugin/plugin.json`). The notice travels and credits both.
- **Commit SHA:** 7e2fb559cf4b824b27f1fec49fe88f7511066d26 (2026-10-30).
- **Safety verdict:** this plugin has no hooks or MCP. Only `protect-mcp` and `review-agent-governance` in that repo add hooks (d-more-repos §3). No bypass flags. Frontmatter is `name` and `description` only. Install file by file.
  - Five checks (auditor-verified at the pinned SHA): installer: none used (file copy); `settings.json`: no write; hooks: none; MCP: none; bypass flags (`--dangerously-skip-permissions`, `bypassPermissions`): none. Exception handled: the pre-commit "Commit gate" is deleted.
- **What to adapt:**
  - `Raw:` → `derived_from::` lines.
  - `Monitored:` → keep it as a page property, but only for pages that describe files under version control (server configs in the owner's config repo). Otherwise drop it.
  - `Status: Outdated` and the move to `archive/` (L82–87) → the `## Superseded` footer, with no file moves.
  - **Delete the "Commit gate" section (L91–97).** It tells you to run checks "from a pre-commit hook or a CI step". MEGAMIND installs no third-party hooks, so the drift check runs in T0 as a report.
  - Do not extract `check_vault.py` from `references/details.md`; `check_evidence.py` (2.4) covers fidelity.
- **Install path:** Claude Code and Managed Agents; claude.ai optional (reference prose).
- **Notes:** The fingerprint idea answers "is this page about my server still true?" at zero token cost. It is worth testing in T0.

### 2.6 `living-docs-governance`
- **What it does:**
  - Assigns four roles: Constitution, Map, Status, History, with "one canonical owner per fact" (L46–56).
  - "Treat documentation as evidence, not executable truth" (L75–84).
  - Dated corrections, and no silent rewrites (L86–98).
- **Licence:** ECC `LICENSE` L1 "MIT License", L3 "Copyright (c) 2026 Affaan Mustafa"; the notice travels.
- **Commit SHA:** b38be6a7f6350964d59328b52f0624e1d1d552d1 (2026-10-29).
- **Safety verdict:**
  - Five checks (auditor-verified at the pinned SHA): installer: none used (file copy); `settings.json`: no write; hooks: none; MCP: none; bypass flags (`--dangerously-skip-permissions`, `bypassPermissions`): none.
  - The ECC plugin and installer are rejected (2.20). This file is prose with one outbound reference (b-ecc).
  - Frontmatter `name`, `description`, `metadata: {origin: ECC}`, all within the six fields.
  - No bypass. Install file by file.
- **What to adapt:**
  - Map the roles: Constitution = vault `CLAUDE.md`; Map = `index.md`; Status = the latest T0 lint report; History = `log.md` plus `## Superseded` footers.
  - §3 "Wire the active harness" (L57–74) edits `CLAUDE.md` or `AGENTS.md`. Make it **propose-only**, and add the rule that `CLAUDE.md` stays under 60 lines.
  - Drop the Chinese trigger list from `description` to get it under 200 characters. It is 478 characters now (measured).
- **Install path:** Claude Code; claude.ai optional; Managed Agents not needed.
- **Notes:** This is a governance reference that `housekeeping` invokes. It is not loaded always-on.

### 2.7 `change-impact`
- **What it does:** "Read-only by default." Proves the impact surface before a change and compares it with the actual diff afterwards. Trust Boundary: no network, no commands, no writes without approval (L7–13).
- **Licence:** ECC MIT (Affaan Mustafa); the notice travels.
- **Commit SHA:** b38be6a7f6350964d59328b52f0624e1d1d552d1.
- **Safety verdict:** prose only. Frontmatter `name` and `description` (472 characters). Install file by file.
  - Five checks (auditor-verified at the pinned SHA): installer: none used (file copy); `settings.json`: no write; hooks: none; MCP: none; bypass flags (`--dangerously-skip-permissions`, `bypassPermissions`): none.
- **What to adapt:**
  - Rewrite the impact surface for a vault: inbound `depends_on::` edges (found with `rg "depends_on:: \[\[<page>\]\]"`), pages citing the same `derived_from::` raw file, and `index.md` rows to propose.
  - Remove the §"Related Skills" (L44–50) references to ECC skills that MEGAMIND does not package.
  - Shorten the description to ≤200 characters.
- **Install path:** Claude Code and Managed Agents (housekeeping jobs); claude.ai optional.
- **Notes:** This is the natural partner of `query` for dependency questions.

### 2.8 TrueHOOHA `llm-wiki-lint` rules (merged into `lint`)
- **What it does:**
  - Nine check classes: OKF conformance, producer conventions, link health, reserved files, contradictions, stale claims, orphans, missing pages, data gaps (`SKILL.md` L27–88).
  - Output contract (L107–112), guardrails (L113–119), verification checklist (L120–128).
- **Licence:** `LICENSE` L1 "Apache License", L2 "Version 2.0, January 2004". The copyright line is the unfilled template "Copyright [yyyy] [name of copyright owner]" (L189), so the credit goes to the repository owner TrueHOOHA. Apache-2.0 §4(b) (L97) requires modified files to "carry prominent notices stating that You changed the files". Therefore:
  - the full Apache-2.0 text travels in `NOTICES.md`;
  - `lint/SKILL.md` carries a line "Sections 'Severity' and 'Verification Checklist' adapted from TrueHOOHA/LLM-Wiki@0455b71 `.agents/skills/llm-wiki-lint/SKILL.md` (Apache-2.0), modified".
- **Commit SHA:** 0455b71e04bafa7a419b308fca254a56d599a585 (2026-07-16).
- **Safety verdict:** no installer, scripts, hooks or MCP. The repo is a template (d-more-repos §5). Install file by file (text merged).
  - Five checks (auditor-verified at the pinned SHA): installer: none used (file copy); `settings.json`: no write; hooks: none; MCP: none; bypass flags (`--dangerously-skip-permissions`, `bypassPermissions`): none.
- **What to adapt:**
  - Drop the OKF conformance checks (L29–40); they apply to TrueHOOHA's SPEC.md, not MEGAMIND.
  - Keep contradictions, stale claims, orphans, missing pages and data gaps (L62–88), with severities.
  - Keep the Verification Checklist (`llm-wiki-lint/SKILL.md` L120–128) as the lint skill's exit criterion. (The "Done Gate" pattern lives in `llm-wiki-ingest/SKILL.md` L41, same SHA; not taken here — audit correction.)
- **Install path:** as `lint`.
- **Notes:** Do not copy `raw/sources/*karpathy-llm-wiki-gist.md`; it is third-party text of unknown licence (d-more-repos §5).

### 2.9 `obsidian-markdown`
- **What it does:** Obsidian Flavored Markdown syntax (wikilinks, embeds, callouts, properties) with three reference files (196-line SKILL.md).
- **Licence:** `LICENSE` L1 "MIT License", L3 "Copyright (c) 2026 Steph Ango (@kepano)"; the notice travels.
- **Commit SHA:** 3ccff5338ea700537839b21900aa5358a0402c98 (2026-09-15).
- **Safety verdict:**
  - Five checks (auditor-verified at the pinned SHA): installer: none used (file copy); `settings.json`: no write; hooks: none; MCP: none; bypass flags (`--dangerously-skip-permissions`, `bypassPermissions`): none.
  - The plugin has no hooks, MCP or settings writes. `defuddle` and `knap` (global npm installs, unpinned `npx knap`) are excluded (d-more-repos §1).
  - Frontmatter `name` and `description` only. Install file by file.
- **What to adapt:** none to the text. Two packaging notes:
  - The description is 262 characters, which is over the claude.ai 200 limit if that limit is enforced [e2]. If so, shorten it and record the change in the pin entry (the only edit).
  - L47 contains "`` `!` to embed ``". A naive `` !` `` injection regex would flag it. The validator must match only `` !`<command>` `` command-injection forms (§3.6).
- **Install path:** all three (pure syntax reference).
- **Notes:** `obsidian-bases` and `json-canvas` are **not adopted**:
  - The vault does not use `.base` views.
  - `index.md` is hand-maintained.
  - A `.canvas` of `depends_on::` edges would be a generated artefact nobody asked for.
  - Both stay reference only.

### 2.10 `loop-design-check`
- **What it does:** Writes or reviews an agent loop. Machine-decidable goal (Step 1), damping against runaway (Step 4, L87–89), "Land in three stages … don't go fully automatic on day one" (Step 5, L91–95), and five failure modes for review (L97–115).
- **Licence:** ECC MIT (Affaan Mustafa); the notice travels.
- **Commit SHA:** b38be6a7f6350964d59328b52f0624e1d1d552d1.
- **Safety verdict:** prose only. Frontmatter `name`, `description`, `metadata`. Install as is.
  - Five checks (auditor-verified at the pinned SHA): installer: none used (file copy); `settings.json`: no write; hooks: none; MCP: none; bypass flags (`--dangerously-skip-permissions`, `bypassPermissions`): none.
- **What to adapt:**
  - Nothing in the text.
  - The description is 432 characters; shorten it to ≤200 if claude.ai enforces that limit.
- **Install path:** Claude Code (owner and T1 design sessions); claude.ai optional.
- **Notes:** Use when changing the AutoResearch ratchet or a housekeeping tier. It matches the rule that automatic merges come only after the ~50-case trigger.

### 2.11 `decision-ledger` (from `recursive-decision-ledger`)
- **What it does:** The ledger contract records rollout id, prior winner, fresh information, trial counts, marks, coherence and promotion gate result (L17–31). "Prefer JSONL for append-only ledgers" (L32). Recursive confidence never auto-approves destructive actions (description).
- **Licence:** ECC MIT (Affaan Mustafa). Frontmatter also says `license: MIT`. The notice travels.
- **Commit SHA:** b38be6a7f6350964d59328b52f0624e1d1d552d1.
- **Safety verdict:** prose only; no installer, hooks or MCP. **Frontmatter carries `tools: Read, Write, Edit, Bash, Grep, Glob`**, which is not one of the six fields. claude.ai and the Skills API reject it with a hard error [e5].
  - Five checks (auditor-verified at the pinned SHA): installer: none used (file copy); `settings.json`: no write; hooks: none; MCP: none; bypass flags (`--dangerously-skip-permissions`, `bypassPermissions`): none. Exception handled: the `tools:` key is deleted.
- **What to adapt:**
  - **Delete the `tools:` key.**
  - Rename to `decision-ledger`, since the upstream name references "Prime Gauss" style prompting.
  - Remove the trading and deploy examples.
  - The "promotion gate" means the oracle score plus owner merge. The ledger is one JSONL line per ratchet experiment, kept beside the experiment file.
- **Install path:** Claude Code and Managed Agents (if a cloud job runs experiments); claude.ai not needed.
- **Notes:** This pairs with the OMC autoresearch evaluator contract (`pass` boolean plus `score`, append-only decision log), which is taken as an idea only (c-omc).

### 2.12 `vault-verify` (from OMC `verify`)
- **What it does:** "Do not say a change is complete without evidence". Verification order; the output lists what was verified, what was run, what passed, and what is unverified (37 lines).
- **Licence:** OMC `LICENSE` L1 "MIT License", L3 "Copyright (c) 2025 Yeachan Heo"; the notice travels.
- **Commit SHA:** 14cd0fe92fbe376fab6c89b333b7896811986d2d (2026-11-02).
- **Safety verdict:**
  - Five checks (auditor-verified at the pinned SHA): installer: none used (file copy); `settings.json`: no write; hooks: none; MCP: none; bypass flags (`--dangerously-skip-permissions`, `bypassPermissions`): none.
  - The OMC plugin, setup and team are rejected (2.20). This file is prose.
  - Frontmatter `name` and `description`. No references to `.omc` or MCP tools (`c-omc` table: omcrefs=0).
  - Install file by file.
- **What to adapt:**
  - Replace "tests/typecheck" with vault checks: `lint` report, `check_evidence.py`, link targets, and the `index.md` row proposed.
  - Rename to `vault-verify` to avoid a collision with generic `verify` skills on a claude.ai account.
- **Install path:** all three.
- **Notes:** none.

### 2.13 `vault-research` (from OMC `research`)
- **What it does:** "Search the repo and its docs first — local evidence outranks recollection". Cite file and line; separate verified from inferred; "Do not implement as a side effect of researching" (39 lines).
- **Licence:** OMC MIT (Yeachan Heo); the notice travels.
- **Commit SHA:** 14cd0fe92fbe376fab6c89b333b7896811986d2d.
- **Safety verdict:** prose; no `.omc`/MCP references. Install file by file.
  - Five checks (auditor-verified at the pinned SHA): installer: none used (file copy); `settings.json`: no write; hooks: none; MCP: none; bypass flags (`--dangerously-skip-permissions`, `bypassPermissions`): none.
- **What to adapt:**
  - "Local" means `index.md`, qmd, then `wiki/`, then `raw/`.
  - Network use only where the environment allows it (the scout's environment; not the VM's unattended tiers).
  - The output for the scout maps to the proposals schema (05 §1).
  - Parallel lookups use Haiku subagents (vault default).
- **Install path:** all three. On Managed Agents it is attached to the scout agent next to `megamind-scout`.
- **Notes:** ECC `research-ops` (a fact/inference/recommendation split) is the same idea; it is not packaged.

### 2.14 `critic-review` (from OMC `agents/critic.md`)
- **What it does:** Final-gate review: "A false approval costs 10-100x more than a false rejection", gap analysis of what is missing, and multi-perspective checks. It is read-only (`disallowedTools: Write, Edit`) (279 lines).
- **Licence:** OMC MIT (Yeachan Heo); the notice travels.
- **Commit SHA:** 14cd0fe92fbe376fab6c89b333b7896811986d2d.
- **Safety verdict:** prose; no hooks or MCP. The upstream frontmatter has `model: opus` and `disallowedTools`, which are agent fields and not among the six skill fields [e5]. Install file by file after conversion.
  - Five checks (auditor-verified at the pinned SHA): installer: none used (file copy); `settings.json`: no write; hooks: none; MCP: none; bypass flags (`--dangerously-skip-permissions`, `bypassPermissions`): none.
- **What to adapt:**
  - **Convert the agent into a skill.** Frontmatter keeps only `name: critic-review` and `description`. Put "read-only: never edit files" in the body.
  - Remove the LSP tool lines (L168).
  - No agent file ships in the plugin. A root `agents/` directory would load as plugin subagents [P4 L297], and §3.1 bans it. If the owner wants a subagent form, they copy one by hand into `~/.claude/agents/critic-review.md` with `model: haiku` (vault default) and `disallowedTools: Write, Edit`. Agents are ignored in chat anyway [e9].
- **Install path:** skill on all three. The optional hand-copied agent file works in Claude Code only.
- **Notes:** Running the critic on Sonnet instead of Haiku for merges is an owner decision (Q3).

### 2.15 `context-and-decisions`
- **What it does:**
  - A narrowly scoped glossary (`CONTEXT.md`) for terms that need repeated explanation.
  - Refines language during the conversation.
  - Hands hard-to-reverse decisions to the ADR skill (L11–45).
- **Licence:**
  - ECC MIT (Affaan Mustafa).
  - `skills/context-and-decisions/LICENSE` L1 "MIT License", L3 "Copyright (c) 2026 Matt Pocock".
  - `references/source.md` L3 says it is adapted from Matt Pocock's `domain-modeling` skill "pinned at `c55ee46073ed923f86ce59a5eb3b6d895095d1b7`".
  - **Both notices travel.** The folder's own `LICENSE` and `references/source.md` are copied unchanged.
- **Commit SHA:** b38be6a7f6350964d59328b52f0624e1d1d552d1.
- **Safety verdict:** prose plus a template; no scripts, hooks or MCP. Frontmatter `name` and `description`. Install file by file.
  - Five checks (auditor-verified at the pinned SHA): installer: none used (file copy); `settings.json`: no write; hooks: none; MCP: none; bypass flags (`--dangerously-skip-permissions`, `bypassPermissions`): none.
- **What to adapt:**
  - `CONTEXT.md` → a single `wiki/glossary.md` page that carries `derived_from::` lines.
  - The ADR handoff points at `decision-records` (2.16).
  - Drop "Scheduling and Task Boundary" (L86–88), which refers to GitHub Issues and Linear.
  - The description is 370 characters; shorten it.
- **Install path:** Claude Code; claude.ai optional.
- **Notes:** none.

### 2.16 `decision-records` (from `architecture-decision-records`)
- **What it does:** Numbered ADRs with Context, Decision, Alternatives, Consequences, an index table, and "Decision Detection Signals" (L12–150).
- **Licence:** ECC MIT (Affaan Mustafa); the notice travels.
- **Commit SHA:** b38be6a7f6350964d59328b52f0624e1d1d552d1.
- **Safety verdict:** prose only; frontmatter `name`, `description`, `metadata`. Install file by file.
  - Five checks (auditor-verified at the pinned SHA): installer: none used (file copy); `settings.json`: no write; hooks: none; MCP: none; bypass flags (`--dangerously-skip-permissions`, `bypassPermissions`): none.
- **What to adapt:**
  - Path `docs/adr/` (L95–105) → `wiki/decisions/NNNN-slug.md`.
  - Each ADR carries `derived_from::` lines and, where a decision rests on another page, `depends_on:: [[page]] (reason)`.
  - The ADR index table (L107–116) is **proposed**, not written, under the same rule as `index.md`.
  - Rename to `decision-records`, which is shorter and not code-specific.
- **Install path:** Claude Code; claude.ai optional.
- **Notes:** The run's `07-decisions.md` already follows this shape.

### 2.17 `skill-creator`
- **What it does:** Create, edit and evaluate skills (485-line SKILL.md), with grader, analyzer and comparator agents. It includes:
  - `scripts/quick_validate.py`: `ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata', 'compatibility'}` (L42), kebab-case name check (L65–71), ≤64-character name, ≤1,024-character description (L83), and no `<`/`>` in descriptions.
  - `scripts/package_skill.py`: a zip with the skill folder as root (`arcname = file_path.relative_to(skill_path.parent)`, L96), excluding `__pycache__`, `node_modules`, `*.pyc`, `.DS_Store` and a root `evals/` (L19–24).
- **Licence:** `skills/skill-creator/LICENSE.txt` is Apache-2.0. The repo has **no root LICENSE**. Apache §4 requires the licence text to travel and modified files to carry change notices.
- **Commit SHA:** ca45fc496a3436251f191354091d557da31c15b5 (2026-10-28).
- **Safety verdict:**
  - Five checks (auditor-verified at the pinned SHA): installer: none used (file copy); `settings.json`: no write; hooks: none; MCP: none; bypass flags (`--dangerously-skip-permissions`, `bypassPermissions`): none. Exception handled: the `claude -p` scripts are not copied.
  - No installer; the marketplace lists skills only. No hooks, MCP or bypass flags (d-more-repos §2).
  - `run_eval.py` (L70–76) and `improve_description.py` (L26) shell out to `claude -p` (no bypass flag). They are **not copied**.
  - `quick_validate.py` and `package_skill.py` use only the standard library plus `yaml` (PyYAML). No network.
  - Install file by file.
- **What to adapt:**
  - Take SKILL.md, `agents/*.md`, `quick_validate.py` and `package_skill.py`. Drop `run_eval.py`, `run_loop.py`, `improve_description.py`, `aggregate_benchmark.py`, `generate_report.py` and `eval-viewer/`.
  - Subagent steps in SKILL.md default to Haiku.
  - The build script imports the two scripts unchanged (§3.4).
- **Install path:** Claude Code only (the owner's authoring machine). Not uploaded to claude.ai or Managed Agents.
- **Notes:** If evaluation with `claude -p` is wanted later, the owner runs it by hand from a reviewed checkout, never unattended.

### 2.18 `mcp-builder` (reference only)
- **What it does:** Guidance for designing MCP servers, with `reference/mcp_best_practices.md`, Python and Node server guides, and `evaluation.md`.
- **Licence:** `skills/mcp-builder/LICENSE.txt` Apache-2.0. If any text is quoted into the connector design, the Apache notice travels with it.
- **Commit SHA:** ca45fc496a3436251f191354091d557da31c15b5.
- **Safety verdict:** reference only. `scripts/connections.py`, `evaluation.py` and `requirements.txt` need pip packages and network, and are not copied.
  - Five checks (auditor-verified at the pinned SHA): installer: none used (file copy); `settings.json`: no write; hooks: none; MCP: none; bypass flags (`--dangerously-skip-permissions`, `bypassPermissions`): none.
- **What to adapt:** nothing is packaged. The connector design (h-reachability.md) cites its best-practice sections.
- **Install path:** none (not packaged).
- **Notes:** The connector is an MCP server the owner builds and runs. Installing it is an owner action under the "no third-party MCP" rule; it is not part of this plan.

### 2.19 PDF handling (gap)
- **What MEGAMIND does instead:**
  - A root-owned script converts each new PDF dropped into an intake folder with `pdftotext -layout <in.pdf> raw/<topic>/<slug>.txt`. Splitting on form feed gives one page per `\f`, which `derived_from::` can cite as `p.N`.
  - The script runs outside Claude. Claude then reads the text under `raw/` like any other source, with `ingest`.
  - The tool is Debian `poppler-utils` (trixie 25.03.0-5+deb13u4, which ships `pdftotext -- text extraction`). Its copyright file states "GPL-2 or GPL-3" [D]. It is used as an installed system program; no code is copied into the fleet repo.
- **Not copied:** anthropics/skills `skills/pdf/`. Its `LICENSE.txt` begins "© 2025 Anthropic, PBC. All rights reserved." and forbids users to "Reproduce or copy these materials" (d-more-repos §2).
- **Commit SHA / licence / safety:** not applicable; no upstream skill is used.
- **Install path:** VM only (the owner installs `poppler-utils` with apt).
- **Notes:**
  - On claude.ai, PDFs can still be uploaded to chat directly. That uses Anthropic's built-in capability and does not depend on this plan.
  - Scanned PDFs (no text layer) need OCR, which is not planned (Q5).

### 2.20 Rejected items
| Item | Reason (evidence) |
|---|---|
| ECC plugin (`/plugin install ecc@ecc`) | Auto-loads 27 hooks, enabled by default (`hooks/hooks.json`; `.claude-plugin/plugin.json` L26–30) (b-ecc) |
| ECC `npx ecc-universal setup` / `install.sh` | Rewrites `~/.claude/settings.json` (`scripts/lib/claude-plugin-setup.js` L372–393; `includeCoAuthoredBy` L29–37 of `claude-commit-attribution.js`). Manual install merges hooks into settings.json (`scripts/lib/install-targets/helpers.js` L225–236) |
| ECC `docker/` harnesses, `mcp-configs/mcp-servers.json` | `--permission-mode bypassPermissions` (`docker/gateguard-effectiveness/lib.js` L183); unpinned `npx -y` MCP catalogue |
| ECC `rules/` | Always-loaded context (README L554), against the 60-line CLAUDE.md rule |
| OMC plugin | 30 hooks including a `PermissionRequest` auto-allow (`hooks/hooks.json` L95) and an MCP server `t` (`.claude-plugin/plugin.json` L68) (c-omc) |
| OMC `omc setup` / `/omc-setup` | Sets `statusLine` in settings.json (`src/installer/index.ts` L835–844). Overwrites `~/.claude/CLAUDE.md` by default (L2721–2735; `skills/omc-setup/SKILL.md` L65) |
| OMC `omc team`, `project-session-manager`, `--madmax`/`--yolo`, autoresearch-guided | `--dangerously-skip-permissions` (`src/team/model-contract.ts` L211; `skills/project-session-manager/lib/tmux.sh` L87; `src/cli/launch.ts` L791–821; `src/cli/autoresearch-guided.ts` L413) |
| OMC `wiki`, `ralph`, `team`, `autoresearch` skills | Depend on the OMC MCP server and state tools (`skills/wiki/SKILL.md` `wiki_ingest(...)` calls; `skills/team/SKILL.md` L257 `state_write`). Ideas only |
| wshobson `protect-mcp`, `review-agent-governance` plugins | PreToolUse/PostToolUse hooks on `.*` run `npx protect-mcp@…` on every tool call (`plugins/protect-mcp/hooks/hooks.json`; `evaluate.sh` L33) |
| ekadetov/llm-wiki | SessionStart hook runs unpinned `npm install @tobilu/qmd @marp-team/marp-cli` (`hooks/hooks.json`; `scripts/install-deps.sh`) |
| AgriciDaniel/claude-obsidian plugin | Adds 2 hooks (`hooks/hooks.json`); its skills need the bundled Python core (`skills/wiki-retrieve/SKILL.md` L16–19); two GPL-2.0 CSS files (`ATTRIBUTION.md` L19–22). Ideas only |
| SubFreq/agent-governance-framework | `npm install` runs `prepare: git config core.hooksPath .githooks` (`package.json`). Its reviewer seat uses the Codex CLI, so content goes to another vendor (`.claude/skills/review-slice/SKILL.md` L17). Ideas only |
| vanillaflava `wiki-ingest` | Moves files out of `raw/` (`wiki-ingest/SKILL.md` L10, L53), against HL 8. Ideas only (`wiki-crystallize` informs MEGAMIND's own `crystallize`) |
| charlie947/ai-second-brain | No parser. Downloads an unpinned gist into CLAUDE.md (`SKILL.md` L101) and asks for Full Disk Access (L172) |
| anthropics/skills `docx`, `pdf`, `pptx`, `xlsx` | Proprietary: "© 2025 Anthropic, PBC. All rights reserved."; copying prohibited (`skills/pdf/LICENSE.txt`) |
| anthropics/skills `doc-coauthoring` | No licence file in the folder and no root LICENSE. Ideas only |
| kepano `defuddle`, `knap` | Need `npm install -g`; `npx knap` is unpinned (`skills/knap/SKILL.md` L10) |

---

## 3. Packaging plan

### 3.1 Source tree (in this repository)
```
skills/
  <name>/SKILL.md            # frontmatter: only name, description, license, compatibility, metadata, allowed-tools
  <name>/references/*.md     # optional, one level deep [e13]
  <name>/scripts/*           # only when pinned and owner-reviewed (today: lint/scripts/check_evidence.py)
  pins.json                  # upstream pins (3.3)
NOTICES.md                   # every upstream licence text and copyright line (3.2)
.claude-plugin/marketplace.json
tools/build-skills.py        # described in 3.4, not written in this run
dist/                        # build output, git-ignored
```
Rules for the tree:
- `name` equals the folder name: lowercase, digits and hyphens, ≤64 characters, no leading/trailing or doubled hyphen, no `anthropic`/`claude` [e12][e13].
- No root `.claude/skills/` directory (05 §3a).
- No root `hooks/`, `agents/`, `commands/` or `.mcp.json`. With `"source": "./"` the repository root *is* the plugin root, and those are default component locations:
  - `agents/` [P4 L297];
  - `hooks/hooks.json` "at the plugin root" [P4 L333];
  - `.mcp.json` "at the plugin root" [P4 L191].
- 05 §4 proposes `agents/megamind-scout*.md` at the repo root for `ant apply` agent files. **This conflicts.** Those files would load as Claude Code subagents of the `megamind` plugin. Move them to `deploy/agents/` (Q2).

### 3.2 `NOTICES.md`
One section per upstream, each with the licence's first line, the copyright line, the full licence text, the SHA and the files taken:
- Astro-Han/karpathy-llm-wiki (MIT, © 2026 Yuhan Lei)
- wshobson/agents (MIT, © 2024 Seth Hobson; grounded-vault plugin author Niksa Barlovic)
- affaan-m/ECC (MIT, © 2026 Affaan Mustafa)
- Matt Pocock domain-modeling via ECC (MIT, © 2026 Matt Pocock; pinned c55ee46… per `references/source.md`)
- kepano/obsidian-skills (MIT, © 2026 Steph Ango)
- Yeachan-Heo/oh-my-claudecode (MIT, © 2025 Yeachan Heo)
- anthropics/skills skill-creator (Apache-2.0, full text)
- TrueHOOHA/LLM-Wiki (Apache-2.0, full text; copyright line unfilled upstream, credited to TrueHOOHA)

Each adapted SKILL.md also sets `license: "MIT; see NOTICES.md"` or `"Apache-2.0; see NOTICES.md"`. Apache-derived files add a "modified by MEGAMIND" line, per Apache-2.0 §4(b).

### 3.3 `skills/pins.json`
Example shape (values from §2):
```json
{
  "version": 1,
  "skills": {
    "ingest": {
      "origin": "upstream",
      "repo": "https://github.com/Astro-Han/karpathy-llm-wiki",
      "sha": "eafcc77001e496cc43499e4923b663aec722c813",
      "licence": "MIT", "licence_file": "LICENSE", "copyright": "Copyright (c) 2026 Yuhan Lei",
      "pinned": "2026-11-02",
      "files_taken": [
        {"from": "SKILL.md", "lines": "45-131", "to": "skills/ingest/SKILL.md", "modified": true,
         "why": "no raw/ writes; no index.md writes; derived_from::/depends_on::/## Superseded"}
      ],
      "scripts": [],
      "targets": ["claude-code", "managed-agents"]
    },
    "crystallize": {"origin": "megamind", "targets": ["claude-code"]}
  }
}
```
Rules for the file:
- `scripts[]` lists each script with its upstream path, SHA, sha256 of the reviewed copy, and `"reviewed_by": "owner"`.
- `targets` drives the build.
- This file is separate from the scout's watch list `scout/pins.json` (megamind-scout.md, Inputs 1). See §3.7 and Q4.

### 3.4 Build script (`tools/build-skills.py`; described here, not written)
1. **Validate** every `skills/<name>/` against the §3.6 checklist. Use upstream `quick_validate.py` (ca45fc4, Apache-2.0, L42 allowed keys, L65–84 name and description rules) plus MEGAMIND's extra checks. Stop on the first failure.
2. **claude.ai zips:** for each skill whose targets include `claude-ai`, write `dist/claude-ai/<name>.zip` with `<name>/` as the zip root. Reuse `package_skill.py`'s arcname rule (L96) and exclusions (L19–24), and write `.zip` instead of `.skill` [e2][e4]. Print the sha256 of each zip.
3. **Claude Code plugin:**
   - Regenerate `.claude-plugin/marketplace.json` from `pins.json` targets:
     ```json
     {"name": "megamind", "owner": {"name": "<gh-user>"},
      "plugins": [{"name": "megamind", "source": "./", "strict": false,
                   "description": "MEGAMIND vault skills",
                   "skills": ["./skills/ingest", "./skills/query", "./skills/lint", "..."]}]}
     ```
   - There is no `.claude-plugin/plugin.json`, so "the entry is the manifest" [P3 L105, L127].
   - The entry must not carry `hooks`, `mcpServers`, `lspServers`, `channels` or `userConfig`.
   - `"megamind"` is not a reserved marketplace name [P3 L43].
   - Then run `claude plugin validate .` (the documented form is `claude plugin validate ./my-marketplace` [P1 L74]).
   - This is the anthropics/skills pattern: `"source": "./"`, `"strict": false`, `"skills": ["./skills/xlsx", …]` [e15].
4. **Managed Agents:**
   - For each skill whose targets include `managed-agents`, print (do not run) `ant apply skills/<name>`. The owner runs it with workspace credentials; `ant apply` records the version in `claude-lock.json` [e14].
   - Fallback: write `dist/api/<name>.zip` for `POST /v1/skills` (<30 MB uncompressed) [e12].
5. **Manifest:** write `dist/MANIFEST.json` with each skill's name, upstream SHA, source tree hash and output sha256. Exit non-zero on any warning.

**Recommendation for Managed Agents: upload with `ant apply`, no `.claude/skills/` mirror.** Reasons:
- **Versioning:** upload gives each skill a version, and the agent file references it by relative path; `ant apply` "pins agent and skill references to the version it just applied" (05 §4, from [e14]).
- **No unreviewed auto-load:** the scout mounts this repository. A root `.claude/skills/` would be auto-discovered at session start [e11] and loaded "without a review step" (05 §3a).
- **No drift:** a mirror duplicates the tree, and the copies can drift apart.

### 3.5 Differences that force per-target variants
| Difference | Effect | Handling |
|---|---|---|
| Frontmatter: claude.ai and the API accept only six fields; Claude Code accepts many more [e5] | Any Claude Code-only key (`disable-model-invocation`, `context`, `hooks`, …) would need a second copy | **Use none.** If `housekeeping` ever needs `disable-model-invocation`, it gets a Claude Code-only variant built from the same source (none planned) |
| `description` limit: 200 (support article) vs 1,024 (spec, claude.com) [e2][e4][e13] | Upstream descriptions measure 247–479 characters (§2) | Write all MEGAMIND descriptions ≤200; no variant |
| `${CLAUDE_SKILL_DIR}` substituted only in Claude Code and Cowork [e4] | Script paths break in chat | Relative paths only (`scripts/check_evidence.py`) |
| Plugin namespacing: plugin skills are `/megamind:<name>` [e5] | The vault's habit is `/ingest`, `/query`, `/lint` | Either accept the namespace, or let the owner copy the folders into the vault's project `.claude/skills/` (no settings write) (Q1) |
| Agents ignored in chat; plugin agents Claude Code only [e9] | `critic-review` subagent form | The skill form carries the content. No plugin agent file is shipped; an owner-copied agent works in Claude Code only |
| Runtime network: API container has none; Managed Agents follows its environment; VM tiers are local [e12] | `vault-research` web steps | The skill text says "only where the environment allows" |
| Vault on disk: claude.ai has none | `ingest` and `lint` are useless there | `targets` in `pins.json` excludes `claude-ai` for them |

**Net:** one source tree, no per-target copies of skills. Differences are handled by `targets` and by writing to the strictest limits.

### 3.6 Validation checklist (run by the build and by the owner before merging a refresh)
- [ ] Frontmatter keys ⊆ {`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`}. Fail on anything else (e.g. ECC `tools:`) [e5]; `quick_validate.py` L42–49.
- [ ] `name` equals the folder name, matches `^[a-z0-9]+(-[a-z0-9]+)*$`, ≤64 characters, contains neither `claude` nor `anthropic` [e12][e13].
- [ ] `description` is 1–1,024 characters (hard fail above 1,024 [e13]); warn above 200 (the claude.ai Help Center figure [e2]); no `<`/`>` (`quick_validate.py`; [e12] "no XML tags"). `metadata` values are strings [e13]; `compatibility` ≤500 characters [e13].
- [ ] SKILL.md under 500 lines [e5][e13]. References are one level deep [e13].
- [ ] Skill folder <30 MB uncompressed [e12]. The plugin as a whole stays ≤5,000 files and ≤200 MB for claude.ai plugin upload [e9].
- [ ] No dynamic context injection. Fail on `` !`<cmd>` `` where `!` follows whitespace or line start and the backtick span is a command; allow `` `!` `` inside inline code (obsidian-markdown L47). This feature does not work in claude.ai or the API anyway [e5].
- [ ] No `${CLAUDE_SKILL_DIR}`, no absolute paths, and no `curl`/`wget`/`npx`/`pip install` lines in SKILL.md or references.
- [ ] Every file under `scripts/` is listed in `pins.json` with a sha256 that matches, plus owner review.
- [ ] `license:` field present and a matching `NOTICES.md` section present. Apache-derived files carry a "modified" notice.
- [ ] Repository root has no `.claude/skills/`, `hooks/`, `agents/`, `commands/` or `.mcp.json`. `marketplace.json` has no `hooks`, `mcpServers`, `lspServers`, `channels` or `userConfig` [P3 L105][P4].
- [ ] The vault rules hold:
  - no instruction writes `raw/` or `index.md`;
  - edge syntax is exactly `depends_on:: [[page]] (reason)`;
  - provenance is `derived_from::`;
  - supersession uses a `## Superseded` footer;
  - subagent steps say Haiku unless the owner decided otherwise.
- [ ] `claude plugin validate .` passes [P1 L74].

### 3.7 How the scout refreshes a packaged skill
The scout runs fortnightly (05 schedules it weekly on Mondays at 03:30). Steps:
1. The scout compares each upstream's commits since the SHA in `skills/pins.json` (via its existing watch list, megamind-scout.md Inputs 1–2) and checks whether any `files_taken[].from` path changed.
2. If it did, the scout writes one proposal (05 schema). It may also put a refresh into its PR:
   - The refresh may change only `skills/<name>/SKILL.md` and `skills/<name>/references/*`, plus that skill's `sha` and `pinned` fields in `skills/pins.json`.
   - Re-apply the recorded MEGAMIND adaptations; never take the upstream file wholesale.
   - If the upstream licence file changed, write a proposal only, with no refresh.
3. **`scripts/` is never touched.** An upstream change to a pinned script (today only `check_evidence.py`) becomes a proposal with the upstream diff summary. The owner reviews and updates the script and its sha256 by hand.
4. Out of scope for the scout: `skills/megamind-scout/` and `scout/pins.json` (05 deployment rule B).
5. The PR must pass the §3.6 checklist; the build script's validate step runs in the owner's review, not in CI hooks.
6. Merging changes the packaged tree only. Re-uploading to claude.ai, `ant apply` and `claude plugin marketplace update` are separate owner actions (05 §6).

---

### 3.8 Director's additions after the community pass (R5, `02-research/g2-community-skills.md`, all [verified] GitHub issues)
- **Description limit:** the claude.ai uploader's only reported error is "must be at most 1024 characters" (mrKanoh #4, adai-v1 #95); the 200-character figure appears in the Help Center only. The plan keeps ≤200 as the safe choice; the validation checklist tests ≤1,024 as the hard limit and warns above 200.
- **Angle brackets:** claude.ai and Cowork reject `<` or `>` inside `description`; on git-sync such skills are silently dropped while the sync reports success, and `claude plugin validate` passes (claude-code #82749, #63081). The checklist adds "no `<` or `>` in description".
- **Strip step:** the common fix for non-spec frontmatter keys is a packaging step that keeps Claude Code-only keys in source and strips them from the upload bundle (anthropics/skills #37, rfsbraz #25). The build script does this; the stripped bundle's description must still say when not to use the skill.
- **Vendoring by SHA is the right call:** upstream fixes in kepano/obsidian-skills (#146, open) and wshobson/agents (#786) never reached installed plugins because versions were not bumped. `gh skill` (GitHub CLI ≥2.90, preview) pins a tag or SHA and writes repo/ref/tree-SHA provenance into the frontmatter — a candidate for `pins.json` provenance fields, not adopted yet (preview).
- **Stale cloud skills:** a scheduled cloud routine ran a stale skill for days while reporting success (R4, claude-code #93163/#84611): the scout's starting message states its `scout_skill_version` and the PR body repeats it, so a stale skill is visible.

## 4. Open questions / not verified

Director's decisions on the drafter's questions (D20–D23 in `07-decisions.md`):
- **Q1 → decided:** on the VM the owner copies the skill folders into the vault's own `.claude/skills/` (bare `/ingest`, `/query`, `/lint` keep working; no settings write; the folders are tripwire files that T1 already checks). The plugin route (`/megamind:<name>`) is for the owner's other Claude Code installs (the Mac, the bench container) and the marketplace entry exists for them. The current fork of karpathy-llm-wiki is diffed against eafcc77 before replacement (P7 step).
- **Q2 → decided:** `ant apply` project files (agents, environment, deployment) live under `deploy/` in the fleet repository, never at the root, so the plugin's `"source": "./"` cannot pick them up as subagents. `05-fortnightly-job.md` §4 is annotated accordingly.
- **Q3 → decided (director, not owner):** `critic-review` runs on Sonnet 5.5 for merge reviews, Haiku for lint-style passes — the master prompt's §6 already puts review work on Sonnet and bulk reading on Haiku; no new policy.
- **Q4 → decided:** the two pin files stay separate. `scout/pins.json` is the watch list (scout read-only). `skills/pins.json` is the packaging record; deployment rule B gets one carve-out: the scout may change only the `sha` and `pinned` fields of the one skill it refreshes, in the same PR as the refresh.
- **Q5 (owner, later):** OCR for scanned PDFs is not planned (`pdftotext` returns nothing for image-only pages); raise it when a scanned manual appears.
- **Not verified:**
  - Whether claude.ai enforces the 200- or the 1,024-character description limit [e2] vs [e4]. The plan writes ≤200 to be safe.
  - claude.ai skill ZIP size limit (not stated) [e1].
  - Whether nested `metadata:` maps (ECC `metadata: {origin: ECC}`) pass the claude.ai uploader. The spec says string→string map [e13], which this is; not tested.
  - Whether `"source": "./"` copies the whole fleet repo (research files included) into each user's plugin cache. The docs say a root plugin "gets every submodule … or none" [P3 L187]; whole-tree copying is inferred, not stated. If it does, the plugin source moves to a `plugin/` subdirectory that the build script fills.
  - Whether the VM has `poppler-utils` installed (the sandbox had `pdftotext`; the VM was not inspected).
  - `ant apply` was not run. Its pinning behaviour is taken from [e14] and 05 §4.

## Sources
- [e] `run1/02-research/e-skills-install.md` (R1, read 2026-11-02). Sub-sources as numbered there:
  - [e1] support.claude.com/en/articles/12512180
  - [e2] support.claude.com/en/articles/12512198
  - [e4] claude.com/docs/skills/how-to.md
  - [e5] code.claude.com/docs/en/skills.md
  - [e8] claude.com/docs/plugins/overview.md
  - [e9] claude.com/docs/plugins/platform-support.md
  - [e11] platform.claude.com/docs/en/managed-agents/skills.md
  - [e12] platform.claude.com/docs/en/build-with-claude/skills-guide.md
  - [e13] agentskills.io/specification.md
  - [e14] platform.claude.com/docs/en/cli-sdks-libraries/cli/apply.md
  - [e15] github.com/anthropics/skills @ ca45fc4
- [P1] https://code.claude.com/docs/en/plugins/create-marketplace.md — read 2026-11-02 (L74, L84, L87, L92, L95, L97)
- [P2] https://code.claude.com/docs/en/plugins/install.md — read 2026-11-02 (L134, L190–201, L196)
- [P3] https://code.claude.com/docs/en/plugins/marketplace-reference.md — read 2026-11-02 (L43, L105, L121–130, L187–191)
- [P4] https://code.claude.com/docs/en/plugins/components.md — read 2026-11-02 (L191, L297, L333)
- [D] https://packages.debian.org/trixie/poppler-utils and https://metadata.ftp-master.debian.org/changelogs/main/p/poppler/stable_copyright — read 2026-11-02
- 05: `run1/05-fortnightly-job.md` and `run1/05-deployments/megamind-scout.md` (R1, read 2026-11-02)
- Clone pins (all read 2026-11-02; details in b-ecc.md, c-omc.md, d-more-repos.md):
  - https://github.com/Astro-Han/karpathy-llm-wiki @ eafcc77001e496cc43499e4923b663aec722c813 (2026-07-24), MIT
  - https://github.com/wshobson/agents @ 7e2fb559cf4b824b27f1fec49fe88f7511066d26 (2026-10-30), MIT
  - https://github.com/affaan-m/ECC @ b38be6a7f6350964d59328b52f0624e1d1d552d1 (2026-10-29), MIT
  - https://github.com/TrueHOOHA/LLM-Wiki @ 0455b71e04bafa7a419b308fca254a56d599a585 (2026-07-16), Apache-2.0
  - https://github.com/kepano/obsidian-skills @ 3ccff5338ea700537839b21900aa5358a0402c98 (2026-09-15), MIT
  - https://github.com/Yeachan-Heo/oh-my-claudecode @ 14cd0fe92fbe376fab6c89b333b7896811986d2d (2026-11-02), MIT
  - https://github.com/anthropics/skills @ ca45fc496a3436251f191354091d557da31c15b5 (2026-10-28), per-skill LICENSE.txt
