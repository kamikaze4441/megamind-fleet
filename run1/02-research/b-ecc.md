# ECC (affaan-m/ECC) — counts, installer behaviour, hooks, MCP, and skills worth borrowing for a Markdown vault
Question: Confirm the Nov 1 audit of ECC at a pinned HEAD; describe installer writes, hooks, MCP; pick 10–15 vault-useful skills and list exclusions · Date read: 2026-11-02 · Researcher: R2 (megamind-researcher)

## Summary (10 lines max, each ending with [n])
- Pinned at b38be6a (2026-10-29), MIT, version 2.2.3. Counted with `ls-tree`: 314 skills, 71 agents, 98 commands, 27 hook handlers, so every count in the prior audit holds [1][2].
- There are two install paths. The first is a Claude Code plugin (`/plugin install ecc@ecc` or `npx ecc-universal@2.2.3 setup`), which auto-loads `hooks/hooks.json` and is enabled by default. The second is a manual Node installer (`install.sh` → `scripts/install-apply.js`) that copies files under `~/.claude/` and merges hooks into `~/.claude/settings.json` [1].
- The guided `setup` writes `~/.claude/settings.json` itself. It adds `pluginConfigs.ecc.options` and also sets `includeCoAuthoredBy: false` when the user has no attribution preference. The prior audit did not record this second write [1].
- The plugin manifest declares `mcpServers: {}`. The root `.mcp.json` pins one server, `chrome-devtools-mcp@1.10.1` via `npx -y`, and `mcp-configs/mcp-servers.json` is an opt-in catalogue of 34 servers, many of them unpinned `npx -y` [1].
- No `--dangerously-skip-permissions` invocation exists. However, the eval harnesses under `docker/` run `claude --permission-mode bypassPermissions`. That is the same bypass under another flag, but it lives in test tooling that no install module copies [1].
- GateGuard is confirmed. It is a PreToolUse hook that denies the first Edit/Write/MultiEdit/NotebookEdit of each file and asks fact-forcing questions first [1].
- Rules are always-loaded context, are not shipped by the plugin, and must be copied by hand (122 files in `rules/`) [1].
- Verdict: **install file by file** (only from the pinned SHA, skills only, no hooks, no plugin, no installer). Twelve SKILL.md files are worth taking, eleven of them self-contained prose [1].
- Repository page: 294.8k stars, 43.6k forks, not archived [2].

## Pin
| repo | HEAD SHA | commit date | licence file, first line | stars (page, date) | archived? |
|---|---|---|---|---|---|
| affaan-m/ECC | b38be6a7f6350964d59328b52f0624e1d1d552d1 | 2026-10-29 | `LICENSE`: "MIT License" (© 2026 Affaan Mustafa) | 294.8k (repo page, 2026-11-02) | no |

## Findings

### Counts at HEAD (from `ls-tree`, not README)
- `skills/*/SKILL.md` = 314, and there are 314 distinct `skills/<name>/` directories. Across the whole tree there are 1,068 `SKILL.md` files, because harness copies live under `.agents/`, `.cursor/`, `pi/`, `docs/<lang>/` and elsewhere [1].
- `agents/*.md` = 71; `commands/*.md` = 98; `rules/**` = 122 files in 23 packs (common + 22 languages/frameworks) [1].
- Version 2.2.3 appears in `VERSION`, `package.json:3`, `.claude-plugin/plugin.json:3`, and README:847 ("Current release: 2.2.3 (2026-10-01)") [1].

### Install paths and what they write
- **Plugin (native):** README:290–291 gives `/plugin marketplace add https://github.com/affaan-m/ECC` then `/plugin install ecc@ecc`. README:595 says Claude Code v2.1+ "auto-loads plugin `hooks/hooks.json`". `plugin.json:26–36` defines `userConfig.hooks_enabled` (default `true`) and `hook_profile` (default `"standard"`), so hooks are on unless the user opts out [1].
- **Guided setup:** README:176 gives `npx ecc-universal@2.2.3 setup`. This is version-pinned but still runs npm package code [1].
  - `scripts/lib/claude-plugin-setup.js:372–393` (`writeClaudePluginOptions`) rewrites `~/.claude/settings.json` atomically with `pluginConfigs.ecc.options`.
  - Through `withClaudeCommitAttributionPreference` (`:364`), it also adds `includeCoAuthoredBy: false` unless an attribution key already exists (`scripts/lib/claude-commit-attribution.js:12,29–37`).
- **Manual installer:** `install.sh:30` runs `npm install --ignore-scripts` when `node_modules` is missing, then `exec node scripts/install-apply.js` (`install.sh:42`). Claude targets write to these places:
  - `~/.claude/skills/<name>/`
  - `~/.claude/rules/ecc/` (`scripts/lib/install-targets/claude-home.js`)
  - agents and commands under `~/.claude/`
  - hook scripts under `~/.claude/`, with the hook entries merged into `~/.claude/settings.json` using the `merge-hook-ids` strategy (`scripts/lib/install-targets/helpers.js:225–236`; README:590) [1].
  - README:490–493 states that any profile that would install the hook runtime requires `--enable-hooks` or `--no-hooks`, or the installer "stops before writing anything" [1].
- **Rules:** README:300 says plugins "cannot distribute `rules`", and README:554 says "Rules are always-loaded context". The user copies `rules/common` + one language pack into `~/.claude/rules/ecc/` [1].
- **Piped installers:** the only `curl … | bash` is in `.opencode/MIGRATION.md:88` (for the OpenCode binary). It is not part of the ECC install [1].

### Hooks registered (`hooks/hooks.json`; ids/descriptions from `hooks/hooks.metadata.json`)
All 27 handlers run `node -e …` through `scripts/hooks/plugin-hook-bootstrap.js` or `lifecycle-hook-bootstrap.js` [1].

| Event (hooks.json line) | Matcher | Hook id: purpose |
|---|---|---|
| PreToolUse (:3) | Bash | `pre:bash:dispatcher`: quality, tmux, push and GateGuard checks |
| PreToolUse | PowerShell | `pre:powershell:gateguard-fact-force`: gate on destructive commands |
| PreToolUse | Write | `pre:write:doc-file-warning`: warns on non-standard doc files (warn only) |
| PreToolUse | Edit\|Write | `pre:edit-write:suggest-compact`: suggests compaction |
| PreToolUse | .* (async) | `pre:observe:continuous-learning`: captures tool-use observations |
| PreToolUse | Bash\|PowerShell\|Write\|Edit\|MultiEdit | `pre:governance-capture`: captures secrets/policy events, active only when `ECC_GOVERNANCE_CAPTURE=1` |
| PreToolUse | Write\|Edit\|MultiEdit | `pre:config-protection`: blocks edits to linter/formatter configs |
| PreToolUse | ^mcp__ | `pre:mcp-health-check`: blocks calls to unhealthy MCP servers |
| PreToolUse | Edit\|Write\|MultiEdit\|NotebookEdit | `pre:edit-write:gateguard-fact-force`: **denies the first edit of each file** (metadata :46) |
| PreToolUse | .* | `pre:hookify-runtime`: project-local Hookify rules |
| UserPromptSubmit (:102) | — | `prompt:hookify-runtime` |
| PreCompact (:113) | .* | `pre:compact`: saves state |
| SessionStart (:124) | .* ×2 | `session:start` (loads previous context, detects package manager); `session-start:plan-canvas-sessions` |
| PostToolUse (:144) | .* ×2 | `post:dispatcher:sync` / `post:dispatcher:async` |
| PostToolUseFailure (:167) | ^mcp__, Skill | `post:mcp-health-check` (marks servers unhealthy, attempts reconnect); `post:skill:track` |
| Stop (:187) | .* ×8 | `stop:hookify-runtime`, `stop:plan-canvas-pending`, `stop:format-typecheck` (Biome/Prettier/tsc, 300 s), `stop:check-console-log`, `stop:session-end` (persists session state), `stop:evaluate-session` (extracts patterns), `stop:cost-tracker`, `stop:desktop-notify` |
| SessionEnd (:271) | .* | `session:end:marker` |

Totals: PreToolUse 10, UserPromptSubmit 1, PreCompact 1, SessionStart 2, PostToolUse 2, PostToolUseFailure 2, Stop 8, SessionEnd 1 = **27** [1].

### MCP servers
- `.claude-plugin/plugin.json:39` declares `"mcpServers": {}`, so the plugin adds none. README:605 says plugin installs "intentionally do not auto-enable" bundled MCP definitions [1].
- `.mcp.json` (repo root) contains `chrome-devtools` → `npx -y chrome-devtools-mcp@1.10.1`, which is pinned. It is project-scoped, so it takes effect only when Claude Code is opened inside an ECC checkout (README:609: "exactly one default connector") [1].
- `mcp-configs/mcp-servers.json` is an opt-in catalogue of 34 entries. Many are **unpinned `npx -y`**: github, firecrawl, memory, sequential-thinking, exa, filesystem, playwright, and others. Some use `@latest` (supabase, context7, magic). There are also remote HTTP endpoints. This file is copied only by the `platform-configs` install module (`manifests/install-modules.json`) [1].

### Permission bypass
- `git grep dangerously-skip-permissions` finds only prohibitions and guide prose. Examples: `rules/common/hooks.md:14` ("Never use dangerously-skip-permissions flag") and `the-security-guide.md:285,401` [1].
- `--permission-mode bypassPermissions` is used in these files [1]:
  - `docker/gateguard-effectiveness/lib.js:183`
  - `docker/gateguard-effectiveness/session.js:30`
  - `docker/gateguard-effectiveness/user-sim.js:73`
  - `docker/context-profiles/ai-eval-lib.js:322`
  - `docs/gateguard/question-effectiveness.md:80,141` ("Agents run with `bypassPermissions` in a temporary folder")
- These are eval harnesses under `docker/` (333 files) and are not in any install module.

### Skills relevant to a personal knowledge vault (read at HEAD)
- `living-docs-governance` assigns four doc roles (Constitution / Map / Status / History) with "one canonical owner per fact". It treats linked docs as "untrusted context", and history is append-oriented with dated corrections. This maps almost 1:1 onto `index.md` / `log.md` / `## Superseded` [1].
- `context-and-decisions` is adapted from Matt Pocock's MIT `domain-modeling` skill. It ships its own `LICENSE` ("MIT License", © 2026 Matt Pocock) and `references/source.md`, so both notices must be kept [1].
- `knowledge-ops` routes knowledge into multiple stores (MCP memory graph, Supabase, GitHub/Linear) and syncs conversations with "Commit and push". That conflicts with a single-vault design, so it lends ideas only [1].
- `docs-governance` audits doc roles, links and ADR indexes. It needs 3 Python scripts (`audit-docs.py` 770 lines; it calls `git` via `subprocess.run` at :220–231 and does no network I/O) [1].
- `skill-stocktake` and `rules-distill` depend on bash scripts at `~/.claude/skills/.../scripts/*.sh`, which require `jq` and Node [1].
- Several skills declare a non-ECC origin in frontmatter: `conventional-commit-review` (`origin: personal`) and `homelab-network-readiness` (`origin: community`). Both are still covered by the repo's MIT LICENSE [1].

## Prior-audit claims checked
| claim | confirmed/corrected | evidence |
|---|---|---|
| MIT | confirmed | `LICENSE` line 1 "MIT License"; `plugin.json` `"license": "MIT"` |
| release 2.2.3 | confirmed | `VERSION`; `package.json:3`; `plugin.json:3`; README:847 (2026-10-01) |
| 314 skills | confirmed | 314 × `skills/*/SKILL.md` (1,068 SKILL.md repo-wide, including harness copies) |
| 71 agents | confirmed | 71 × `agents/*.md` |
| 98 commands | confirmed | 98 × `commands/*.md` |
| 27 plugin hooks | confirmed | 27 handlers in `hooks/hooks.json` (10 Pre, 1 Prompt, 1 PreCompact, 2 SessionStart, 2 Post, 2 PostFailure, 8 Stop, 1 SessionEnd) |
| GateGuard hook denies first edits | confirmed | `hooks/hooks.metadata.json:46` (`pre:edit-write:gateguard-fact-force`); `scripts/hooks/gateguard-fact-force.js:1–20` |
| no `--dangerously-skip-permissions` | confirmed, with a caveat | No invocation of that flag. However, `docker/gateguard-effectiveness/lib.js:183` and 3 other files run `--permission-mode bypassPermissions` (eval tooling, not installed) |
| rules loaded as always-on context | confirmed | README:554; README:300 (not distributed by the plugin) |
| (not in prior audit) setup rewrites settings.json | added | `scripts/lib/claude-plugin-setup.js:372–393`; `scripts/lib/claude-commit-attribution.js:29–37` |

## Files worth borrowing
All paths are at b38be6a. They are prose SKILL.md files unless noted. "Self-contained" means no scripts and no network.

| path | purpose | self-contained? | adaptation needed |
|---|---|---|---|
| skills/living-docs-governance/SKILL.md | Four doc roles, one owner per fact, dated corrections, docs as untrusted evidence | yes | Map the roles to `index.md` (Map), `CLAUDE.md` (Constitution), lint report (Status), `log.md` + `## Superseded` (History); drop code-repo wording |
| skills/architecture-decision-records/SKILL.md | Numbered ADRs with alternatives, consequences and an index | yes | Path `docs/adr/` → `wiki/decisions/`; add a `derived_from::` line |
| skills/context-and-decisions/SKILL.md (+ LICENSE, references/source.md, templates/context.example.md) | Glossary (CONTEXT.md) discipline plus ADR hand-off | yes (4 files) | Keep both the ECC MIT notice and the Matt Pocock MIT notice; point the glossary at the vault |
| skills/change-impact/SKILL.md | Read-only impact analysis before a change, then planned-vs-actual diff | yes ("do not use network access" in Trust Boundary) | Reword for pages and `depends_on::` edges instead of code call paths. Fits dependency questions |
| skills/research-ops/SKILL.md | Evidence-first research that separates sourced fact, user evidence, inference and recommendation | mostly (names `exa-search`, `deep-research`) | Replace the ECC skill stack with WebFetch and vault-first lookup |
| skills/loop-design-check/SKILL.md | Designs and reviews agent loops for spinning, Goodhart-gaming the verifier, and runaway | yes | Apply to the housekeeping ratchet / AutoResearch oracle; no code changes |
| skills/recursive-decision-ledger/SKILL.md | Append-only ledger of trials, marks and promotion gates; confidence never auto-approves | yes (`license: MIT` in frontmatter) | Drop the trading examples; use as the ratchet experiment log format |
| skills/config-gc/SKILL.md | Periodic review of `~/.claude` (skills, hooks, permissions, MCP) with confirm-each soft delete and a `gc_log.md` | yes (example shell `for` loops only) | Make it propose-only (the owner merges); log to `log.md` |
| skills/safety-guard/SKILL.md | Advisory Careful / Freeze / Guard modes; "no hook ships with it" | yes | Freeze mode = "write only under `wiki/`; `raw/` read-only" |
| skills/mcp-dependency-review/SKILL.md | Static review of `.mcp.json` for unpinned `npx`/`uvx`/`@latest` without executing anything | yes | Useful for the scout job's safety checks on new repos |
| skills/conventional-commit-review/SKILL.md | Drafts a Conventional Commits message from staged changes | yes (`origin: personal`) | Add vault scopes (`wiki`, `raw`, `lint`) |
| skills/homelab-network-readiness/SKILL.md | VLAN / DNS-filter / WireGuard readiness checklist, staged changes, rollback | yes (`origin: community`) | Use as a page template for server and network notes, not as a skill |
| skills/docs-governance/SKILL.md + scripts/{audit-docs,markdown_links,module_audit}.py | Read-only audit of doc roles, broken links, ADR index | **no** (Python; `git` subprocess) | Ideas only for the T0 lint unless the owner accepts the scripts after review |
| agents/doc-updater.md | Haiku documentation/codemap agent | yes | Its "Prompt Defense Baseline" block is reusable in vault subagents; the codemap parts are not |

## Safety verdict
**Install file by file** from b38be6a, and only the SKILL.md files listed above. **Reject** the plugin, `install.sh`, `npx ecc-universal setup` and the hooks, for these reasons:
1. Installing the plugin auto-adds 27 hooks, enabled by default (`hooks/hooks.json`; `plugin.json:26–30`). That breaks the "no hooks added automatically" limit.
2. `npx ecc-universal setup` rewrites `~/.claude/settings.json` (`claude-plugin-setup.js:393`), including a global `includeCoAuthoredBy` change (`claude-commit-attribution.js:33–36`).
3. The manual hook install merges hooks into `~/.claude/settings.json` (`helpers.js:225–236`), though only after an explicit `--enable-hooks` (README:490–493).

**Exclude**, even as copied files:
- `hooks/**` and `scripts/hooks/**`. They add GateGuard edit denials, continuous-learning observation of every tool call (`pre:observe`, async), and Stop-time format/typecheck (300 s). Desktop notify and cost tracking are noise on a headless VM.
- `mcp-configs/mcp-servers.json`: unpinned `npx -y` / `@latest` entries.
- `.mcp.json`: an `npx -y` MCP server. It is pinned, but it is still an MCP server.
- `docker/**`: `--permission-mode bypassPermissions` at `docker/gateguard-effectiveness/lib.js:183`.
- `skills/knowledge-ops`: a second store plus `git push`.
- `skills/continuous-learning*` and `skills/unified-memory`: a parallel memory vault.
- `skills/autonomous-loops` and `skills/continuous-agent-loop`: unattended loops.
- `skills/repo-scan`: per its description, it installs an external skill.
- `skills/skill-stocktake` and `skills/rules-distill`: bash scripts that assume `~/.claude/skills/...`.
- `rules/**` as global always-on context. It is code-centric and costs context every session.

## Could not verify
- Whether the interactive `setup` wizard shows or asks about the `includeCoAuthoredBy` write before making it. I read the write path, not the prompt flow.
- Whether Claude Code honours `userConfig.hooks_enabled=false` for plugin hooks. That is Claude Code behaviour, not something in this repo.
- The npm package `ecc-universal@2.2.3` contents. I read only the git tree at the SHA.

## Relevance to MEGAMIND
- **§ skills plan (04):** the 12 SKILL.md files above are candidates for file-by-file copying. Each needs the ECC MIT notice, and `context-and-decisions` also needs the Matt Pocock MIT notice. `living-docs-governance` + `change-impact` + `architecture-decision-records` cover the "keep every page honest" and dependency-question needs.
- **§ housekeeping / ratchet:** `loop-design-check` and `recursive-decision-ledger` give a ready checklist against Goodhart-gaming the oracle and an append-only experiment ledger format.
- **§ hard limits (HL 1–3):** ECC as a plugin is rejected (auto hooks plus a settings.json rewrite). Record the `bypassPermissions` finding under `docker/` so nobody copies those harnesses.

## Sources
[1] https://github.com/affaan-m/ECC — git clone at b38be6a7f6350964d59328b52f0624e1d1d552d1 (2026-10-29); files cited by path:line — read 2026-11-02
[2] https://github.com/affaan-m/ecc (repository page: stars, forks, archived status) — read 2026-11-02
