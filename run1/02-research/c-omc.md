# oh-my-claudecode (Yeachan-Heo/oh-my-claudecode): bypass flags, settings/CLAUDE.md writes, hooks, MCP, and transferable orchestration patterns
Question: Confirm the prior OMC audit at a pinned HEAD with path:line evidence, and extract the orchestration ideas and self-contained files a Haiku-default vault can reuse · Date read: 2026-11-02 · Researcher: R2 (megamind-researcher)

## Summary (10 lines max, each ending with [n])
- Pinned at 14cd0fe (2026-11-02). Licence is MIT, version 5.7.30. The repo has 48 skills, 19 agents and 21 commands. About 5,711 of its 7,807 files are compiled `dist/` output, and the hooks import that `dist/` code [1][2].
- `--dangerously-skip-permissions` is hard-coded in several places [1]:
  - every Claude tmux worker launched by `omc team`
  - `project-session-manager`
  - `--madmax` and `--yolo`
  - `autoresearch-guided`
- `omc setup` (the installer) writes two global files [1]:
  - `~/.claude/settings.json`: a `statusLine` pointing at an OMC HUD script
  - `~/.claude/CLAUDE.md`: overwritten by default, with a backup taken first
- The installed `CLAUDE.md` tells Claude "Direct writes OK for: `~/.claude/**`" (docs/CLAUDE.md:25) [1].
- The plugin auto-loads 30 hooks across 11 events and one MCP server, named `t`, which runs `bridge/mcp-server.cjs` and exposes state, notepad, memory, wiki, LSP and AST tools [1].
- One of those hooks is a `PermissionRequest` handler that auto-allows a narrow set of read-only Bash commands. The prior audit did not mention it [1].
- Patterns that transfer well as prose:
  - the routing table (haiku explore/writer, sonnet executor/verifier, opus planner/critic)
  - a bounded verify→fix loop (`max_fix_loops: 3`)
  - a PRD step that runs only when acceptance criteria are missing
  - Ralph's "story passes only after reviewer verification" rule
  - the autoresearch evaluator contract (`pass` boolean plus `score`, an append-only decision log, and a max-runtime stop) [1]
- Self-contained files worth copying: `skills/verify`, `research`, `remember`, `minimal-prose-discipline`, `agent-doc-discipline` (minus `.omc` refs), `diagram`, and `agents/critic.md`, `writer.md`, `document-specialist.md` [1].
- Verdict: **reject as a plugin or installer; install file by file for prose skills/agents only** [1].
- Stars: 38.4k on the repository page; not archived [2].

## Pin
| repo | HEAD SHA | commit date | licence file, first line | stars (page, date) | archived? |
|---|---|---|---|---|---|
| Yeachan-Heo/oh-my-claudecode | 14cd0fe92fbe376fab6c89b333b7896811986d2d | 2026-11-02 | `LICENSE`: "MIT License" (© 2025 Yeachan Heo) | 38.4k (repo page, 2026-11-02) | no |

## Findings

### Install surfaces
- **Plugin path:** README:61 and :67 give `/plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode`, then `/plugin install oh-my-claudecode`. Line 68 of `.claude-plugin/plugin.json` declares `"mcpServers": "./.mcp.json"`. Claude Code also auto-loads `hooks/hooks.json` from the plugin [1].
- **npm path:** README:73 gives `npm i -g oh-my-claude-sisyphus@latest`. It is unpinned and pulls the native `better-sqlite3` dependency (README:76–81) [1].
- **Setup:** README:83–91 gives `/omc-setup` or `omc setup`. The installer at `src/installer/index.ts` writes into `~/.claude/`, in these places [1]:
  - `agents/`, `commands/`, `skills/`, `hooks/` and `hud/` (constants at :40–47)
  - `settings.json` (`SETTINGS_FILE`, :46)
  - `.omc-version.json` (:47)
  - `~/.claude/CLAUDE.md`
- Other settings changes [1]:
  - The installer also syncs a "unified MCP registry" into settings (`syncUnifiedMcpRegistryTargets`, :858).
  - It removes "legacy" and "stale plugin duplicate" hook entries from `settings.json` (:734, :764).
  - The README tells users to set `env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in `~/.claude/settings.json` for Team mode (README ~:185–192 in the fetched page [2]).

### `--dangerously-skip-permissions` (grep at HEAD, excluding `dist/`)
- `src/cli/launch.ts:51` defines the `CLAUDE_BYPASS_FLAG` constant. `:791–821` (`normalizeClaudeLaunchArgs`) "Maps --madmax/--yolo to --dangerously-skip-permissions" [1].
- `src/team/model-contract.ts:211`: the Claude worker contract's `buildLaunchArgs` always starts with `['--dangerously-skip-permissions']`. It adds `--bare` when `ANTHROPIC_API_KEY` is set (:202–204). These are the `omc team N:claude` tmux workers [1].
- `src/team/model-contract.ts:309`: the antigravity (`agy`) workers get the same flag [1].
- `src/cli/autoresearch-guided.ts:27,413`: `spawnAutoresearchSetupTmux` starts `claude --dangerously-skip-permissions` in a detached tmux session [1].
- `skills/project-session-manager/SKILL.md:260–262,314,344` and `skills/project-session-manager/lib/tmux.sh:84–87`: `tmux send-keys … "claude --dangerously-skip-permissions" Enter` [1].
- `scripts/run-provider-advisor.js:82`: agy advisor args [1].
- `SECURITY.md:76` admits this "Auto-approval risk class", noting that headless CLI workers "launch with auto-approve flags" [1].
- Compiled copies of these call sites also appear in `bridge/cli.cjs`, `bridge/runtime-cli.cjs` and `bridge/team.js` (133 occurrences repo-wide, including `dist/`) [1].

### `settings.json` / `statusLine` / `CLAUDE.md`
- `src/installer/index.ts:835–844` sets `settings.statusLine = { type: 'command', command: <omc-hud> }` when none exists or when an OMC string form needs migrating. With `--force` it overwrites only an OMC-owned statusLine (:845–851) [1].
- `src/installer/index.ts:2721–2735` runs `executeClaudeMdTransaction({ mode: 'global-overwrite', root: CLAUDE_CONFIG_DIR, source: docs/CLAUDE.md })` with backups. Users opt out only via `claudeMdEnabled=false` in `.omc-config.json` [1].
- `skills/omc-setup/SKILL.md:65`: "Default: explicitly overwrites ~/.claude/CLAUDE.md so plain `claude` also uses OMC". A preserve mode writes `CLAUDE-omc.md` instead (:66) [1].
- Project-scoped plugin installs skip both the global CLAUDE.md and the settings.json writes (:2722–2726, :2752, :2785) [1].
- The installed `docs/CLAUDE.md` contains these lines [1]:
  - `:25` "Direct writes OK for: `~/.claude/**`, `.omc/**`, `.claude/**`, `CLAUDE.md`, `AGENTS.md`"
  - `:23–24` the model routing
  - `:38` "small→haiku, standard→sonnet, large/security→opus"

### Hooks (`hooks/hooks.json`, `"description": "OMC orchestration hooks with async capabilities"`)
Every handler runs `scripts/run.cjs` → `scripts/<name>.mjs`, which imports from `dist/hooks/...` [1].

| Event (line) | Matcher | Script: purpose (from script header) |
|---|---|---|
| UserPromptSubmit (:4) | * | `keyword-detector`: detects magic keywords and invokes skills; `skill-injector`: injects learned skills by trigger |
| SessionStart (:21) | * | `session-start` (restores persistent modes), `project-memory-session` (detects env, injects context), `wiki-session-start`, `stale-run-reporter` ("unattended-run watchdog"), `runs-reconciler` |
| SessionStart | `init` (:53) | `setup-init`: creates `.omc/` dirs, sets env vars; patches `hooks.json` on Windows (`src/hooks/setup/index.ts:155–198`) |
| SessionStart | `maintenance` (:63) | `setup-maintenance` |
| PreToolUse (:73) | * | `pre-tool-enforcer`: injects reminders before every tool |
| PreToolUse | Bash (:85) | `git-guardrails`: blocks `git push`, `reset --hard`, `clean -f`, `branch -D`, `checkout .` in unattended modes or when `OMC_GIT_GUARDRAILS=1` |
| **PermissionRequest (:95)** | Bash | `permission-handler`: **auto-allows** `git status`, `ls`, `gh issue/pr view/list/status` and safe repo-path `cat`/`head`/`tail`/`sed -n`/`rg` (`src/hooks/permission-handler/index.ts:33–38, 405–481, 561–571`) |
| PostToolUse (:107) | *, *, Read\|Write\|Edit\|MultiEdit ×2 | `post-tool-verifier` (verification reminders), `project-memory-posttool` (learns from tool outputs), `post-tool-rules-injector`, `post-tool-directory-context-injector` |
| PostToolUseFailure (:140) | * | `post-tool-use-failure`: records the last tool error for retry guidance |
| SubagentStart (:152) / SubagentStop (:164) | * | `subagent-tracker`; `verify-deliverables`: advisory check that a finishing subagent produced its expected files |
| PreCompact (:181) | * ×3 | `pre-compact`, `project-memory-precompact`, `wiki-pre-compact` |
| Stop (:203) | * ×5 | `context-guard-stop`, `workflow-drift-guard`, `persistent-mode` (the "continuation enforcer" that keeps ralph/autopilot going), `budget-guard`, `code-simplifier` |
| SessionEnd (:235) | * ×2 | `session-end`, `wiki-session-end` (session-log auto-capture) |

Total: **30 handlers** over 11 events: UserPromptSubmit 2, SessionStart 7, PreToolUse 2, PermissionRequest 1, PostToolUse 4, PostToolUseFailure 1, SubagentStart 1, SubagentStop 2, PreCompact 3, Stop 5, SessionEnd 2 [1].

### MCP server
- `.mcp.json` defines `"t": { "command": "node", "args": ["${CLAUDE_PLUGIN_ROOT}/bridge/mcp-server.cjs"] }` [1].
- Its source is `src/mcp/omc-tools-server.ts:10–21`. It registers LSP, AST, skills, state, notepad, memory, trace, shared-memory, wiki and (optionally) interop tools [1].
- The `wiki` skill's `wiki_ingest` / `wiki_query` / `wiki_lint` functions are MCP tools on this server, so that skill is not self-contained [1].

### Orchestration patterns (what transfers as prose)
- **Model routing:**
  - `docs/CLAUDE.md:23–24`: haiku = quick lookups, sonnet = standard, opus = architecture/deep analysis. Delegated agents run on their pinned tier, not the session model.
  - Agent frontmatter pins `explore` and `writer` to haiku; `executor`, `verifier`, `debugger`, `document-specialist` and `scientist` to sonnet; `planner`, `critic`, `analyst`, `architect`, `code-reviewer` and `security-reviewer` to opus.
  - Read-only agents carry `disallowedTools: Write, Edit` [1].
- **Team pipeline:** `skills/team/SKILL.md:99` gives `team-plan -> team-prd -> team-exec -> team-verify -> team-fix (loop)`.
  - The stage routing table (:107–111) assigns explore(haiku) + planner(opus) to plan, analyst(opus) to prd, executor(sonnet) to exec, verifier(sonnet) to verify and executor/debugger to fix.
  - The rules state that "`team-verify` always uses at least `sonnet`" (:117), that risk escalates review (:118), and that the fix loop is bounded at `max_fix_loops` default 3 before a terminal `failed` (:151, :282) [1].
- **PRD step:** `team-prd` runs only when "scope is ambiguous or acceptance criteria are missing", and exits when acceptance criteria and boundaries are explicit (:126–129) [1].
- **Ralph:** `skills/ralph/SKILL.md` describes a "PRD-driven persistence loop".
  - `prd.json` user stories must reach `passes: true` and be reviewer-verified.
  - `progress.txt` carries learnings across iterations.
  - The reviewer is chosen with `--critic=architect|critic|codex`.
  - Optional `observableChecks` (`fileContains`, `gitGrep`) verify by content and are "never PR status".
  - The loop is kept alive by the Stop hook `persistent-mode` [1].
- **Autoresearch:** `skills/autoresearch/SKILL.md`.
  - The evaluator must output JSON with a required boolean `pass` and an optional numeric `score`.
  - Each iteration runs exactly one experiment, persists `iteration-NNNN.json` and appends `decision-log.md`.
  - Runs stop at max-runtime or on cancel. Cron reruns append rather than overwrite [1].
- **Authoring vs review:** `docs/CLAUDE.md` execution protocols: "Never self-approve in the same active context." `skills/review/SKILL.md` runs two separate axes (standards vs intent) and never cross-ranks them [1].
- **Wiki lint rules** (`src/hooks/wiki/lint.ts:5–30`): orphan, stale (`staleDays`), broken-ref (`[[page]]`), low-confidence, oversized, and structural contradiction (same slug prefix with conflicting metadata). Semantic contradiction is noted as "v2" [1].
- **Deliverable check** (`scripts/verify-deliverables.mjs:3–21`): a subagent marked done with zero output files is flagged by file existence and a minimum size. It is advisory [1].

## Prior-audit claims checked
| claim | confirmed/corrected | evidence |
|---|---|---|
| MIT | confirmed | `LICENSE` line 1; `plugin.json` `"license": "MIT"` |
| v5.7.30 | confirmed | `package.json:3`; `plugin.json:3`; `docs/CLAUDE.md:2` |
| orchestration via Task tool with haiku/sonnet/opus tiers | confirmed (plus a `fable` tier) | `docs/CLAUDE.md:22–26`; agent frontmatter `model:`; `skills/team/SKILL.md:107–111` |
| team pipeline plan → prd → exec → verify → fix | confirmed | `skills/team/SKILL.md:99,122–151`; README:181 |
| `omc team` tmux workers launch `claude --dangerously-skip-permissions` | confirmed | `src/team/model-contract.ts:211` |
| `project-session-manager` launches it | confirmed | `skills/project-session-manager/lib/tmux.sh:87`; `SKILL.md:262,314,344` |
| `--madmax`/`--yolo` launch it | confirmed | `src/cli/launch.ts:51,791–821` |
| `autoresearch-guided` launches it | confirmed | `src/cli/autoresearch-guided.ts:27,413` |
| `omc setup` writes `~/.claude/settings.json` (statusLine) | confirmed | `src/installer/index.ts:46,835–844` |
| `omc setup` writes `~/.claude/CLAUDE.md` | confirmed (default overwrite with backup) | `src/installer/index.ts:2721–2735`; `skills/omc-setup/SKILL.md:65` |
| plugin auto-loads 30 hooks | confirmed | 30 handlers in `hooks/hooks.json` |
| plugin auto-loads an MCP server | confirmed | `.claude-plugin/plugin.json:68` → `.mcp.json` server `t` |
| (not in prior audit) PermissionRequest auto-allow hook | added | `hooks/hooks.json:95`; `src/hooks/permission-handler/index.ts:561–571` |
| (not in prior audit) installed CLAUDE.md grants direct writes to `~/.claude/**` | added | `docs/CLAUDE.md:25` |

## Files worth borrowing
All paths are at 14cd0fe, MIT, © 2025 Yeachan Heo; keep the notice.

| path | purpose | self-contained? | adaptation needed |
|---|---|---|---|
| skills/verify/SKILL.md (37 lines) | Evidence before "done"; report only what was verified | yes | Replace "tests/typecheck" with vault checks (lint, fidelity vs `raw/`, link check) |
| skills/research/SKILL.md (39 lines) | Question → local evidence first → official docs → cited findings + unknowns | yes | Make "local" mean `index.md`, qmd, `wiki/` |
| skills/remember/SKILL.md (41 lines) | Classify session findings by destination (durable / working / instruction / stale) | yes | Collapse the destinations to wiki page vs `log.md` vs CLAUDE.md proposal; drop the "notepad" names |
| skills/review/SKILL.md (57 lines) | Two-axis review (standards vs intent); reviewer is not the author | mostly (Quality Gates section references `omc quality-gates`) | Delete the Quality Gates section; use for the owner-merge review brief |
| skills/minimal-prose-discipline/SKILL.md (73 lines) | Terse replies; protected core (paths, numbers, negators) never rewritten | yes | None beyond dropping "yard" vocabulary |
| skills/agent-doc-discipline/SKILL.md (54 lines) | Agent-facing docs: checkable rules with a why, one meaning one home | mostly (mentions `.omc/skills/`, drydock) | Rewrite the surface list to CLAUDE.md / SKILL.md / `wiki/` conventions |
| skills/diagram/SKILL.md | Smallest visual that carries structure | yes | None |
| skills/session-flow/SKILL.md (49 lines) | Evidence-backed reorientation map of the current session | yes | Optional |
| agents/critic.md (279 lines) | Opus final-gate reviewer with "what's missing" gap analysis, `disallowedTools: Write, Edit` | yes (mentions LSP tools "when available") | Set `model:` per vault policy; use for the auditor role |
| agents/writer.md (90 lines) | Haiku technical writer | yes | Point it at page templates |
| agents/document-specialist.md (77 lines) | External docs lookup, read-only | yes | Restrict to official docs first, matching the researcher method |
| agents/verifier.md (113 lines) | Evidence-based completion checks | partly (`lsp_diagnostics_directory` ×5) | Remove the LSP lines |
| skills/team/SKILL.md :99–151 (excerpt only) | Stage table + entry/exit criteria + bounded fix loop | no (state_write MCP, Team runtime) | Ideas only: copy the table as prose into the housekeeping protocol |
| skills/ralph/SKILL.md, skills/autoresearch/SKILL.md | PRD/story loop; evaluator contract | no (`omc ralph verify`, `.omc/state`, Stop hook) | Ideas only |
| src/hooks/wiki/lint.ts :5–30 (header) | Six lint classes for a Markdown wiki | no (TypeScript runtime) | Ideas only for the T0 lint checklist |

## Safety verdict
**Reject** as a plugin, npm CLI, or `omc setup`. Reasons:
1. `--dangerously-skip-permissions` is hard-coded for team workers (`src/team/model-contract.ts:211`), for PSM (`skills/project-session-manager/lib/tmux.sh:87`), for autoresearch setup (`src/cli/autoresearch-guided.ts:413`), and behind `--madmax`/`--yolo` (`src/cli/launch.ts:791`).
2. It rewrites `~/.claude/settings.json` (`src/installer/index.ts:837–844`) and overwrites `~/.claude/CLAUDE.md` by default (`:2721–2735`; `skills/omc-setup/SKILL.md:65`). The CLAUDE.md it installs grants direct writes to `~/.claude/**` (`docs/CLAUDE.md:25`).
3. The plugin auto-adds 30 hooks, including a `PermissionRequest` auto-allow (`hooks/hooks.json:95`), and an MCP server (`plugin.json:68`).
4. The runtime is mostly prebuilt `dist/` (5,711 files), which a file-by-file audit cannot cover. The npm path is unpinned `@latest` (README:73).

**Install file by file:** the prose-only skills and agents in the table above. **Ideas only:** team, ralph, autoresearch, the wiki lint classes, and verify-deliverables.

## Could not verify
- Whether the CLI `omc setup` asks before the global CLAUDE.md overwrite. The skill flow uses AskUserQuestion for update/resume choices (`skills/omc-setup/SKILL.md:133,168`). I did not trace the CLI prompt flow, which lives in `dist/`.
- The behaviour of the compiled `bridge/*.cjs` beyond the grep hits. I did not read those bundles in full.
- The npm package contents for `oh-my-claude-sisyphus@5.7.30`.

## Relevance to MEGAMIND
- **Housekeeping and ratchet design:** the autoresearch contract (`pass` + `score`, one experiment per iteration, append-only decision log, max-runtime stop) matches "one file per experiment, scored by the oracle". Adopt it as prose; do not run the skill.
- **Haiku-default subagents:** copy the routing rule "delegated agents run on their pinned tier, not the session model", plus the floor "verify always ≥ sonnet". These are proposals for the T1/T2 tiers; whether Haiku may verify is for the director to decide.
- **The vault's own lint:** the six lint classes in `src/hooks/wiki/lint.ts` and the advisory deliverable check give T0 a checklist of orphan, stale, broken `[[ref]]`, oversized, contradiction and empty-output checks.
- **Hard limits:** OMC as a plugin breaks HL 1 (bypass flags) and the settings/CLAUDE.md rule. Record it as reject in 04.

## Sources
[1] https://github.com/yeachan-heo/oh-my-claudecode — git clone at 14cd0fe92fbe376fab6c89b333b7896811986d2d (2026-11-02); files cited by path:line — read 2026-11-02
[2] https://github.com/yeachan-heo/oh-my-claudecode (repository page: stars 38.4k, forks 3.5k, not archived; README as rendered) — read 2026-11-02
