# Audit report — research (b)–(d) and 04-skills-plan.md (auditor A1, run 1, 2026-11-02)

## Method
- I cloned all 14 repositories named in the Pin tables (13 repositories, plus claude-mem from d's "lesson only" section). Each was a blobless clone: `GIT_LFS_SKIP_SMUDGE=1 git clone -q --depth 1 --filter=blob:none --no-checkout` into `/tmp/a1/pins/<owner>__<repo>`.
- I read files only with `git show HEAD:<path>`, `git ls-tree` and `sed -n`. Nothing was checked out, installed or executed.
- Line numbers below are the line numbers in those `git show` outputs.
- I did not check star counts or archived status, because the repository web pages were not fetched.

## Pins: HEAD SHA and licence first line (all repositories in the Pin tables)
| repo | audited SHA | HEAD today (commit date) | result | licence file, first line(s) as read |
|---|---|---|---|---|
| affaan-m/ECC | b38be6a7f635… | same (2026-10-29) | holds | `LICENSE` L1 "MIT License", L3 "Copyright (c) 2026 Affaan Mustafa" |
| Yeachan-Heo/oh-my-claudecode | 14cd0fe92fbe… | same (2026-11-02) | holds | L1 "MIT License", L3 "Copyright (c) 2025 Yeachan Heo" |
| kepano/obsidian-skills | 3ccff5338ea7… | same (2026-09-15) | holds | L1 "MIT License", L3 "Copyright (c) 2026 Steph Ango (@kepano)" |
| anthropics/skills | ca45fc496a34… | same (2026-10-28) | holds | no root LICENSE (root: `.claude-plugin`, `README.md`, `THIRD_PARTY_NOTICES.md`, `skills`, `spec`, `template`). Per-skill `LICENSE.txt`: 14 Apache, `docx`/`pdf`/`pptx`/`xlsx` "© 2025 Anthropic, PBC. All rights reserved.", `doc-coauthoring` has none |
| wshobson/agents | 7e2fb559cf4b… | same (2026-10-30) | holds | L1 "MIT License", L3 "Copyright (c) 2024 Seth Hobson" |
| vanillaflava/llm-wiki-skills | ff6f7be1a0e3… | same (2026-07-11) | holds | L1 "MIT License", L3 "Copyright (c) 2026 Axel Tölke" |
| TrueHOOHA/LLM-Wiki | 0455b71e04ba… | same (2026-07-16) | holds | L1 "Apache License", L2 "Version 2.0, January 2004" (indented) |
| charlie947/ai-second-brain | 6b14a5282f3f… | same (2026-10-24) | holds | L1 "MIT License", L3 "Copyright (c) 2026 Charlie Hills" |
| Astro-Han/karpathy-llm-wiki | eafcc77001e4… | same (2026-07-24) | holds | L1 "MIT License", L3 "Copyright (c) 2026 Yuhan Lei" |
| SubFreq/agent-governance-framework | 95232cc52fdd… | same (2026-08-01) | holds | L1 "MIT License", L3 "Copyright (c) 2026 SubFreq" |
| AgriciDaniel/claude-obsidian | 2e545563172f… | same (2026-10-22) | holds | L1 "MIT License", L3 "Copyright (c) 2026 AgriciDaniel (AI Marketing Hub)" |
| nvk/llm-wiki | d60674ff785e… | same (2026-10-25) | holds | L1 "MIT License", L3 "Copyright (c) 2026 nvk" |
| ekadetov/llm-wiki | 5e49545a3339… | same (2026-04-06) | holds | L1 "MIT License", L3 "Copyright (c) 2026 ekadetov" |
| thedotmack/claude-mem | 1466db2d8d45… | **newer HEAD** 99985e9b0303… (2026-11-02); audited SHA reachable (`git cat-file -t` → `commit` after `git fetch --depth 1 origin 1466db2…`) | holds | `LICENSE` exists at 1466db2; first non-blank line "Apache License". d only cites the README, which is consistent with this |

---

## b-ecc.md — verdict: **verified**
| claim | evidence I saw | result |
|---|---|---|
| 314 skills, 71 agents, 98 commands, 122 rules files, 1,068 SKILL.md repo-wide, 333 files under `docker/` | `ls-tree` counts: 314 / 71 / 98 / 122 / 1068 / 333 | holds |
| 27 hook handlers: Pre 10, Prompt 1, PreCompact 1, SessionStart 2, Post 2, PostFailure 2, Stop 8, SessionEnd 1; event lines :3/:102/:113/:124/:144/:167/:187/:271 | parsed `hooks/hooks.json`: identical counts and matchers; `grep -n` gives the same line numbers | holds |
| `plugin.json` hooks are on by default (`:26–36`); `mcpServers: {}` (`:39`); version `:3` | L25 `"userConfig"`, L30 `"default": true` (hooks_enabled), L36 `"default": "standard"`, L39 `"mcpServers": {}`, L3 `"version": "2.2.3"` | holds |
| setup rewrites `~/.claude/settings.json` (`claude-plugin-setup.js:372–393`, `:364`) and adds `includeCoAuthoredBy: false` (`claude-commit-attribution.js:12,29–37`) | L372 `function writeClaudePluginOptions`, L393 `writeFileAtomic(settingsPath, …)`, L364 `withClaudeCommitAttributionPreference`; attribution L12 `COAUTHOR_SETTING_KEY = 'includeCoAuthoredBy'`, L35 `[COAUTHOR_SETTING_KEY]: false` | holds |
| manual installer merges hooks into settings (`helpers.js:225–236`, strategy `merge-hook-ids`) | `planClaudeHooksOperations` … `kind: 'update-claude-settings', strategy: 'merge-hook-ids'` in that range | holds |
| `install.sh:30` runs npm install, `:42` execs node | L30 `npm install --ignore-scripts --no-audit --no-fund …`, L42 `exec node "$NODE_SCRIPT" "$@"` | holds |
| README:490–493 (`--enable-hooks`/`--no-hooks` or "stops before writing anything"), :300, :554, :595, :605, :609, :847 | all lines read; quoted text present | holds |
| GateGuard denies the first edit (`hooks.metadata.json:46`; `gateguard-fact-force.js:1–20`) | L46 `"id": "pre:edit-write:gateguard-fact-force"`, description "deny the first Edit/Write/MultiEdit/NotebookEdit of each file"; the script header says "PreToolUse Hook: GateGuard Fact-Forcing Gate" | holds |
| no `--dangerously-skip-permissions` invocation, but `bypassPermissions` at `docker/gateguard-effectiveness/lib.js:183`; `rules/common/hooks.md:14` prohibits the flag | lib.js L183 `'--permission-mode', 'bypassPermissions',`; hooks.md L14 "- Never use dangerously-skip-permissions flag" | holds (I did not run a repo-wide grep for the flag) |
| `.mcp.json` = `chrome-devtools-mcp@1.10.1` via `npx -y`; catalogue of 34 | `.mcp.json` content as stated; `mcp-configs/mcp-servers.json` has 34 entries | holds |
| `context-and-decisions` ships its own MIT LICENSE (© 2026 Matt Pocock) and `references/source.md` | folder contains `LICENSE`, `SKILL.md`, `references/source.md`, `templates/context.example.md`; LICENSE L3 "Copyright (c) 2026 Matt Pocock" | holds |
Corrections: none.

## c-omc.md — verdict: **verified**
| claim | evidence I saw | result |
|---|---|---|
| v5.7.30; 48 skills, 19 agents, 21 commands; 7,807 files, 5,711 under `dist/` | `package.json` L3 `"version": "5.7.30"`; 48 × `skills/*/SKILL.md` (the 49th entry is `skills/AGENTS.md`); 19 / 21; `ls-tree` 7807 / 5711 | holds |
| `--dangerously-skip-permissions` at `src/team/model-contract.ts:211` and `:309` | L211 `const args = ['--dangerously-skip-permissions'];` (claude contract); L309 the same (agy) | holds |
| `src/cli/launch.ts:51`, `:791–821` map `--madmax`/`--yolo` to the flag | L51 `const CLAUDE_BYPASS_FLAG = '--dangerously-skip-permissions';`; the comment "Maps --madmax/--yolo to --dangerously-skip-permissions" and `normalizeClaudeLaunchArgs` are in that range | holds |
| `src/cli/autoresearch-guided.ts:27,413` | L27 the same constant; L413 `buildTmuxShellCommandWithEnv('claude', [CLAUDE_BYPASS_FLAG], …)` | holds |
| PSM `lib/tmux.sh:84–87`, `SKILL.md:260–262` | tmux.sh L87 `tmux send-keys … "claude --dangerously-skip-permissions" Enter`; SKILL.md L262 the same | holds |
| installer writes `settings.json` (`index.ts:46`, statusLine `:835–844`) | L46 `SETTINGS_FILE = join(CLAUDE_CONFIG_DIR, 'settings.json')`; L838 `settings.statusLine = { type: 'command', … }` | holds |
| global CLAUDE.md overwrite (`index.ts:2721–2735`; `omc-setup/SKILL.md:65`) | `executeClaudeMdTransaction({ mode: 'global-overwrite', root: CLAUDE_CONFIG_DIR, … })`; opt-out `claudeMdEnabled=false`; SKILL.md L65 "Default: explicitly overwrites ~/.claude/CLAUDE.md …" | holds |
| installed `docs/CLAUDE.md:25` grants writes to `~/.claude/**` | L25 "Direct writes OK for: `~/.claude/**`, `.omc/**`, `.claude/**`, `CLAUDE.md`, `AGENTS.md`." | holds |
| 30 hooks over 11 events; `PermissionRequest` at `hooks.json:95` auto-allows read-only Bash | parsed counts: UPS 2, SessionStart 7, Pre 2, PermissionRequest 1, Post 4, PostFailure 1, SubagentStart 1, SubagentStop 2, PreCompact 3, Stop 5, SessionEnd 2 = 30 / 11; L95 `"PermissionRequest"`; `permission-handler/index.ts` returns `behavior: 'allow', reason: 'Safe read-only command'` (L558–572) | holds |
| MCP server `t` (`plugin.json:68` → `.mcp.json`) | L68 `"mcpServers": "./.mcp.json"`; `.mcp.json` `"t": {"command": "node", "args": ["${CLAUDE_PLUGIN_ROOT}/bridge/mcp-server.cjs"]}` | holds |
| team pipeline `:99`, verify ≥ sonnet `:117`, bounded fix `:151`; `state_write` at `:257`; `wiki` skill calls `wiki_ingest` | all lines read and as stated | holds |
| `skills/verify` 37 lines, `research` 39, `agents/critic.md` 279 with `model: opus`, `disallowedTools: Write, Edit`; no `.omc` references | `wc -l` 37 / 39 / 279; frontmatter as stated; `grep -c '\.omc'` = 0 in all three | holds |
Corrections: none.

## d-more-repos.md — verdict: **verified with corrections**
| claim | evidence I saw | result |
|---|---|---|
| kepano: 15 files, no hooks, no `.mcp.json`; `defuddle`/`knap` SKILL.md:10 need global npm | `ls-tree` 15 files, no hooks or MCP file; plugin.json has no hooks/mcpServers; L10 "`npm install -g defuddle`" and "`npm install -g knap` … use `npx knap`" | holds |
| anthropics/skills has no root LICENSE; `pdf/LICENSE.txt` forbids copying | root listing has no LICENSE; pdf LICENSE.txt L1 "© 2025 Anthropic, PBC. All rights reserved.", L18 "Reproduce or copy these materials", L20 "Create derivative works" | holds |
| anthropics/skills "18 skill folders" (§2 Findings) | `ls-tree skills/` lists **19** folders: 14 Apache, 4 proprietary, 1 without a licence (`doc-coauthoring`) | **does not hold** |
| `skill-creator` scripts call `claude -p` (`run_eval.py:70–76`, `improve_description.py:26`) | run_eval L70–76 `cmd = ["claude", "-p", query, …]`; improve_description L26 `["claude", "-p", "--output-format", "text"]`; no bypass flag | holds |
| wshobson: hooks only in `protect-mcp` and `review-agent-governance`; `npx protect-mcp@0.31.1` at `evaluate.sh:33`, `@0.7.4` at `sign.sh:18`; no policy → allow-all (`evaluate.sh:9–12`) | only these two `hooks.json` files in the tree; both are PreToolUse `.*` → evaluate.sh and PostToolUse `.*` → sign.sh; lines as cited (the review-agent-governance copy has its npx line at L38) | holds |
| wshobson counts: 92 plugins, 202 agents, 185 SKILL.md, 105 commands | `ls-tree`: 92 / 202 / 185 / 105 | holds |
| grounded-vault (104 lines): `archive/` "moved, never deleted"; header `Raw/Fingerprint/Monitored/Status`; "Commit gate" uses a pre-commit hook; plugin author Niksa Barlovic, MIT | `wc -l` 104; L31, L44–53, L91–97 as quoted; plugin.json author "Niksa Barlovic", `"license": "MIT"` | holds |
| vanillaflava `wiki-ingest/SKILL.md:10` moves files out of `raw/` | L10 "The move of each file into `ingested/` is the atomic commit"; L53 "moving files to ingested/" | holds |
| TrueHOOHA lint skill: "9-class lint with severity output and 'Done Gate'" (§5 table) | `llm-wiki-lint/SKILL.md` (128 lines) has Checks 1–9 (L29–88), Output Contract L107, Guardrails L113, **Verification Checklist** L120, and no "Done Gate". "Done Gate" is in `llm-wiki-ingest/SKILL.md:41` | **does not hold** (the Done Gate is attributed to the wrong file) |
| TrueHOOHA licence "Apache License Version 2.0, January 2004" | L1 "Apache License", L2 "Version 2.0, January 2004" (two lines) | holds (two lines merged into one) |
| charlie947: 217-line SKILL.md; curl into CLAUDE.md `:101`; NotebookLM `:151`; iMessage `:167`; Full Disk Access `:172–173`; no parser (`:83,86`) | `wc -l` 217; each line as quoted; `grep` for `conversations.json`/`create_time`/`chat_messages` = 0 | holds |
| Astro-Han: SKILL.md 233 lines, Ingest :45, Query :132, Lint :164; `check_evidence.py` 431 lines, "Report-only" L4, stdlib imports | `wc -l` 233 and 431; headings at 45/132/164; L4 "Report-only; never modifies files."; imports `re`, `sys`, `dataclasses`, `pathlib` only | holds |
| SubFreq: `prepare` sets `core.hooksPath`; review seat via Codex CLI (`review-slice/SKILL.md:17`) | package.json `"prepare": "git config core.hooksPath .githooks"`, `js-yaml ^4.1.0`; L17 "non-interactively via the Codex CLI" | holds ("1 commit total" could not be checked with a depth-1 clone) |
| claude-obsidian: 2 hooks (SessionStart matcher `startup|resume|clear|compact|fork`, Stop) running python3; GPL-2.0 CSS (`ATTRIBUTION.md:15–22`); `wiki-retrieve/SKILL.md:16–19` calls bm25/retrieve/rerank scripts | hooks.json as stated; ATTRIBUTION L19 "**License:** GPL-2.0" with the two `.css` files; L16–19 as stated | holds |
| nvk: Claude plugin has no hooks/MCP; hooks only in the Codex plugin; 28 commands; "24 reference files" | only `plugins/llm-wiki/hooks/*` (Codex) and no hooks in `claude-plugin/`; 28 command files; **23** files under `claude-plugin/skills/wiki-manager/references/` | 24 → **does not hold** (23); the rest holds |
| ekadetov: SessionStart hook → `install-deps.sh` (timeout 120) runs unpinned `npm install @tobilu/qmd @marp-team/marp-cli` | hooks.json as stated; install-deps.sh L44 `if npm install @tobilu/qmd @marp-team/marp-cli …` with no versions (`deps-version.txt` "1.0.0" is a sentinel, not a package version) | holds |

Corrections for d-more-repos.md:
1. §2 Findings. Wrong: "**What it is:** 18 skill folders, the Agent Skills spec and a template." Right: "**What it is:** 19 skill folders (14 Apache-2.0, 4 proprietary, 1 with no licence file), the Agent Skills spec and a template."
2. §5 Files table, row `.agents/skills/llm-wiki-lint/SKILL.md`. Wrong: "9-class lint with severity output and "Done Gate"". Right: "9-class lint with severity output and a Verification Checklist (L120–128); the "Done Gate" is in `.agents/skills/llm-wiki-ingest/SKILL.md:41`".
3. §10 Findings. Wrong: "the `wiki-manager` skill with 24 reference files". Right: "the `wiki-manager` skill with 23 reference files".

---

## 04-skills-plan.md — verdict: **verified with corrections**
| check | evidence I saw | result |
|---|---|---|
| Every adopted item (2.1–2.18) has all seven fields: what it does, licence, SHA, safety verdict, what to adapt, install path, notes | a script scanned every block 2.1–2.18 for the seven bold field labels; none is missing | holds |
| Each safety verdict covers installer, settings, hooks, MCP and bypass | a keyword scan of each safety-verdict text shows that only 2.1 names all five. 2.2/2.3 inherit it ("as 2.1"), which I accept. The other 15 blocks (2.4–2.18) omit two to five of the checks: 2.4, 2.8, 2.11 omit settings and bypass; 2.5 omits installer and settings; 2.6 omits settings, hooks and MCP; 2.17 omits settings; 2.7, 2.10, 2.16, 2.18 say only "prose only" or "reference only"; 2.9 and 2.12–2.15 omit two to four | **does not hold** (field incomplete in 15 of 18 blocks; the facts behind it are clean, see the next row) |
| No adopted item needs `--dangerously-skip-permissions`, a hook install or an MCP install | adopted files read at their SHAs: karpathy SKILL.md and check_evidence.py (stdlib, no subprocess or network); grounded-vault (its pre-commit "Commit gate" L91–97 is deleted by the plan); ECC skills are prose (only `recursive-decision-ledger` has an extra `tools:` key, which the plan deletes); OMC verify/research/critic (no `.omc` refs; the LSP line L168 is removed by the plan); obsidian-markdown (prose); skill-creator (the `claude -p` scripts are not copied; `quick_validate.py`/`package_skill.py` import only `sys`/`os`/`re`/`yaml`/`fnmatch`/`zipfile`/`pathlib`); mcp-builder is reference only | holds |
| Every adopted item's licence permits copying | MIT: Astro-Han, wshobson, ECC (+ Matt Pocock MIT in `context-and-decisions/LICENSE`), kepano, OMC. Apache-2.0: `skill-creator/LICENSE.txt`, `mcp-builder/LICENSE.txt`, TrueHOOHA `LICENSE`. No proprietary or unlicensed file is adopted (`pdf`, `doc-coauthoring` are excluded) | holds |
| §2.8 licence quote: `LICENSE` L1 "Apache License, Version 2.0" | L1 "Apache License", L2 "Version 2.0, January 2004"; L97 "(b) You must cause any modified files to carry prominent notices"; L189 "Copyright [yyyy] [name of copyright owner]" | L97/L189 hold; the **L1 quote does not hold** |
| §2.3/§2.8 "Done Gate" taken from `llm-wiki-lint/SKILL.md` (L27–88, L107–128) | the lint file has no "Done Gate"; it is at `llm-wiki-ingest/SKILL.md:41` (same repo and SHA, Apache-2.0) | **does not hold** (provenance) |
| §2.1–2.4 karpathy line refs (Init L28–37, Fetch L49–62, Post-Ingest L102, Research L122–128, Query L132–160 with L144 read-only and L156 index update, Lint L164–225, L195 command; `METADATA_RE` L48) | headings and lines match exactly | holds |
| §2.4 "a `git grep` for `write`/`open(` found none" | no `open(`; "write" occurs once, in the docstring at L25 ("locate-before-write"), not as a call | holds in substance (wording nit) |
| §2.6/2.7/2.10/2.15/2.11 description lengths 478/472/432/370/479 and `tools:` key | measured 478/475/432/373/479 (±3 from quoting and whitespace); `recursive-decision-ledger` keys `name, description, license, metadata, tools`; `living-docs-governance` `metadata: origin: ECC` | holds |
| §2.9 obsidian-markdown 196 lines, description 262 characters, L47 `` `!` to embed `` | `wc -l` 196; 262 characters; L47 "Prefix any wikilink with `!` to embed its content inline:" | holds |
| §2.14 critic L168 is the LSP line | L168 "Use LSP tools (lsp_hover, …) when available" | holds |
| §2.17 skill-creator: 485-line SKILL.md; `ALLOWED_PROPERTIES` L42; name rules L65–71; description ≤1,024 L83; package arcname L96; exclusions L19–24 | all match. Note: `package_skill.py` L17 imports `from scripts.quick_validate import validate_skill`, so the build script must keep that package path or adjust the import | holds |
| Packaging frontmatter rules (§3.1, §3.6) vs e-skills-install.md | e L8–9: the six spec fields; other keys fail hard on claude.ai and the API. e L11/L87: `name` ≤64, lowercase/digits/hyphens, no "anthropic"/"claude", description ≤1,024, no XML. e L102–107: name matches the parent directory, no leading/trailing/double hyphen, compatibility ≤500, metadata string→string. e L63: SKILL.md <500 lines. e L34: the support article says description ≤200. 04 §3.1/§3.6 reproduce all of these. (e L34 also lists an optional `dependencies` field from the support article; 04 excludes it, which is the conservative choice.) | holds, except for an internal inconsistency: §3.6 says "`description` is 1–200 characters", while §3.8 says "the validation checklist tests ≤1,024 as the hard limit and warns above 200" |
| Rejected table (§2.20) reasons match b–d | each row is consistent with b/c/d and with my checks: ECC plugin hooks (`plugin.json` L26–30), setup and settings lines, docker L183, rules README L554; OMC hooks L95, MCP L68, statusLine/CLAUDE.md lines, bypass lines; team L257 `state_write` and wiki `wiki_ingest(`; wshobson evaluate.sh L33; ekadetov install-deps.sh; claude-obsidian hooks and ATTRIBUTION; SubFreq `prepare` and L17; vanillaflava L10/L53; charlie L101/L172; anthropics pdf LICENSE; doc-coauthoring has no licence; knap L10. The count of 17 rows matches Summary item 5 | holds |
| Summary 1: 18 items = 15 adapted + 2 as is + 1 reference | §1 table: adapted #1–8, 11–17 (15); as is #9, #10; reference #18 | holds |

Corrections for 04-skills-plan.md:
1. §2.8 **Licence**. Wrong: "`LICENSE` L1 "Apache License, Version 2.0"." Right: "`LICENSE` L1 "Apache License", L2 "Version 2.0, January 2004"."
2. §2.8 and §2.3 (Done Gate provenance). Wrong (§2.8): "Keep "Done Gate" wording as the lint skill's exit criterion." and the notice line "Sections 'Severity' and 'Done Gate' adapted from TrueHOOHA/LLM-Wiki@0455b71 (Apache-2.0), modified". Right: "Keep the Verification Checklist (`llm-wiki-lint/SKILL.md` L120–128) as the lint skill's exit criterion; the "Done Gate" pattern comes from `llm-wiki-ingest/SKILL.md` L41 (same SHA, Apache-2.0)". Then do one of two things: add that file to the `files_taken` entry for #8, or drop the Done Gate wording. Set the notice line to name the sections actually taken. §2.3 "Add from TrueHOOHA: severity labels and the Done Gate (see 2.8)" must follow whichever choice is made.
3. §2.4–2.18 **Safety verdict**. Add one line per block that states all five checks explicitly, e.g. "installer: none used (file copy); settings.json: no write; hooks: none; MCP: none; bypass flags: none (`git grep` at SHA)". Name the exceptions that the plan already handles: grounded-vault's pre-commit "Commit gate" (deleted), skill-creator's `claude -p` scripts (not copied), and `recursive-decision-ledger`'s `tools:` key (deleted). My evidence (table above) supports "none" for every adopted file.
4. §3.6, third checkbox. Wrong: "`description` is 1–200 characters (the stricter claude.ai figure [e2])". Right, to match §3.8: "`description` is 1–1,024 characters (hard fail above 1,024 [e13]); warn above 200 (the claude.ai Help Center figure [e2])". Alternatively, change §3.8 to say 200 is the hard limit. The two sections must not disagree.
5. Nit, §2.4. Wrong: "a `git grep` for `write`/`open(` found none." Right: "no `open(` and no write calls; "write" appears only in the docstring at L25."

## Sign-off
04-skills-plan.md: NOT SIGNED OFF: (1) the Done Gate is attributed to `llm-wiki-lint` but comes from `llm-wiki-ingest/SKILL.md:41` (provenance and notice text, §2.3/§2.8); (2) the §2.8 licence first-line quote is wrong; (3) the safety-verdict field lacks the explicit installer/settings/hooks/MCP/bypass checks in 15 of 18 blocks; (4) §3.6 (≤200) and §3.8 (≤1,024 hard, warn above 200) contradict each other. No safety or licence blocker was found: once corrections 1–4 are applied as quoted above, I will re-check and sign off.
