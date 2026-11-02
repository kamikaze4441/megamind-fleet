# (g2) Community evidence — skills, repositories, Managed Agents
Question: What do 2026 community reports say about the skill repositories the skills plan borrows from, about borrowing single SKILL.md files, about plugin install/namespacing and claude.ai skill upload limits, and about running Claude Managed Agents scheduled jobs (a weekly/fortnightly "scout" that opens PRs)? · Date: 2026-11-02 · Researcher: R5 (argon-researcher)

Tags: [community] = forum/Reddit/HN/GitHub-issue/blog material. [verified] = I opened the page myself (web_fetch, or curl of the github.com HTML / raw file) and the claim matches. [Argon, not verified] = Argon reported it and I did not open the source. Reddit is blocked by this sandbox's egress policy and web_fetch refuses Reddit URLs that are not "shown", so **no Reddit claim below is verified**. Argon became unavailable partway through (Gemini HTTP 402, "prepayment credits are depleted"). Topics 2 and 3 therefore rest on my own GitHub and web research; see "Calls and cost".

## Summary (10 lines max)
1. The borrowed repos are alive but uneven. kepano/obsidian-skills and wshobson/agents both ship fixes that installed plugins never receive, because the version is not bumped (kepano #146 open, wshobson #786). Vendor by pinned SHA instead of relying on plugin auto-update. [verified]
2. The claude.ai uploader enforces **1,024** characters for the description. The only upload error text people have reported is "field 'description' in SKILL.md must be at most 1024 characters". The 200-character figure comes from the help-center doc, and nobody has reported an error that cites it. Keep ≤200 anyway, because it is documented and costs nothing. [verified]
3. claude.ai and Cowork reject `<`/`>` in a `description`. On the git-sync path such skills are **silently dropped** while the sync reports success, and `claude plugin validate` still passes (CC #82749, #63081). [verified]
4. Frontmatter keys outside the six spec fields cause a hard upload error. Community repos solve this with a packaging step that strips Claude Code-only keys from the upload bundle (anthropics/skills #37, rfsbraz #25). [verified]
5. Cherry-picking is mainstream advice, and the reason is the standing token cost: about 27k tokens for a full ECC install. For updates, `gh skill` (GitHub CLI ≥2.90, preview) pins a tag or SHA and writes repo/ref/tree-SHA provenance into the frontmatter. [verified]
6. In Managed Agents, the git proxy rejects pushes with HTTP 503 unless the branch is exactly `claude/<session-id>` (CC #66571). Users open the PR through the GitHub MCP server. [verified]
7. The memory store did not mount in scheduled-deployment sessions (cookbooks #830, still open). Anthropic's own daily-brief quickstart nonetheless relies on /mnt/memory in a scheduled deployment, so test the mount on day one. [verified]
8. The official daily-brief quickstart **disables web_search/web_fetch**, because they run outside the sandbox allowlist. Its budget_reached state pauses the run instead of failing it, which looks like silence. A scout that needs web_fetch must take on that exfiltration route consciously. [verified]
9. MCP calls under `always_allow` are still sometimes denied ("Permission to use … has been denied"; anthropic-sdk-typescript #1099, open since Jun 2026). An unattended scout needs a "PR not opened" alarm. [verified]
10. Real cost reports: the daily-brief quickstart measured about $1.00 per busy run (Sonnet 5), about $1.50 (Opus 5), and $0.15–0.30 when every source is unreadable. Runtime at $0.08/h is negligible for short runs. Nobody has published a weekly web scout that opens PRs. [verified / thin]

## Topic 1 — the repositories: quality, breakage, what people keep

**kepano/obsidian-skills**
- #146 "Auto-update in Claude Code delivers no new content without a version bump". plugin.json and marketplace.json are stuck at 1.0.1 although new skills have landed. Opened 2026-09-16, OPEN. https://github.com/kepano/obsidian-skills/issues/146 [community][verified]
- #149, Obsidian 1.14.4: obsidian-markdown/obsidian-bases have a "Mermaid trust gate, silent tag truncation, and two silent sort failures". The reporter checked rendered output in a real 120-note vault. Opened 2026-10-18, OPEN. https://github.com/kepano/obsidian-skills/issues/149 [community][verified]
- #128: obsidian-cli "Common patterns" leaves out rename/move/delete. Agents then fall back to `mv`, which breaks wikilinks, or to `eval`. Opened 2026-08-01, OPEN. https://github.com/kepano/obsidian-skills/issues/128 [community][verified]
- #144: a frontmatter alias does not resolve a bare `[[Alias]]` wikilink (obsidian-markdown, obsidian-cli). #112: request to prefix skill names (`obs-`) for multi-pack setups, 2026-07-14, OPEN. Titles and dates read from the issue list/page. https://github.com/kepano/obsidian-skills/issues [community][verified]
- Reddit r/ObsidianMD 1q8gn9c, "Kepano released obsidian-skills repo – what custom skills are you building?", 471 upvotes, 2026-01-09. https://www.reddit.com/r/ObsidianMD/comments/1q8gn9c/ [community][Argon, not verified]
- Blog "agents&me" (2026-07-06, per Argon) recommends keeping **obsidian-markdown** and **defuddle** and skipping obsidian-cli, bases and json-canvas unless an Obsidian desktop instance is being driven. [community][Argon, not verified; no URL given]

**anthropics/skills**
- #2104: the repo copies of docx/pptx/xlsx lag the claude.ai-synced copies by about three months. The synced copies changed from 2026-09-30 to 10-27; the repo copies last changed 2026-07-17. Opened 2026-11-01, OPEN. https://github.com/anthropics/skills/issues/2104 [community][verified]
- #2090: skill-creator/SKILL.md is 503 lines, over Anthropic's own 500-line guide, and the document-skill descriptions are not written in third person. Opened 2026-11-02, OPEN. https://github.com/anthropics/skills/issues/2090 [community][verified]
- #919: with both document-skills and example-skills enabled (the default after installing the marketplace), the same 17 skills load twice under two prefixes. Opened 2026-04-15, OPEN. https://github.com/anthropics/skills/issues/919 [community][verified]
- #763: skill-creator puts its eval workspace next to the skill in .claude/skills/, and Claude reads it mid-session, burning tokens. Opened 2026-03-25, OPEN. https://github.com/anthropics/skills/issues/763 [community][verified]
- #1668, mcp-builder: requirements allow `mcp>=2`, and in 2.x connections.py fails at import (`streamablehttp_client` was renamed). Opened 2026-08-29, OPEN. https://github.com/anthropics/skills/issues/1668 [community][verified]
- #1153: `references/` relative paths do not resolve from the skill directory, either in Claude Code `Read` (resolved against cwd) or in claude.ai `view`. Opened 2026-08-25, with the repro dated 2026-05-17; OPEN. https://github.com/anthropics/skills/issues/1153 [community][verified]
- #249: skill-creator says "Do not include any other fields in YAML frontmatter", which contradicts the spec's optional fields. Opened 2026-01-18, OPEN. https://github.com/anthropics/skills/issues/249 [community][verified]
- r/ClaudeCode: "Anthropic updated the skill-creator skill…", 48 upvotes, 2026-03-03. Another post says skill-creator "killed rolling context in 2 minutes" (2026-10-08). [community][Argon, not verified]

**wshobson/agents**
- #786: fixes since 2026-05-22 never reach installed plugins because the versions are not bumped (Claude Code 2.1.308). Opened 2026-10-30, CLOSED. https://github.com/wshobson/agents/issues/786 [community][verified]
- #787: sast-configuration references run-sast.sh and semgrep-rules.md, which do not exist (follow-up to #514). Opened 2026-10-25, CLOSED. #701: the protect-mcp and review-agent-governance hooks pass `$TOOL_NAME`/`$TOOL_INPUT`, which Claude Code does not set. 2026-09-13, CLOSED. https://github.com/wshobson/agents/issues/787 , /701 [community][verified]
- #777: architecture-decision-records `adr generate toc > docs/adr/README.md` overwrites the curated index. Title from the issue list. https://github.com/wshobson/agents/issues [community][verified]
- A DEV Community review (2026-10-15) keeps individual skills (postgresql-table-design, sql-optimization-patterns) but warns that the architecture skills push solo projects into over-engineering. An r/ClaudeWorkflows audit (2026-07-29) reports "92.5% missing tools, perfect duplicates" across public agent collections, including this one. [community][Argon, not verified]

**LLM-wiki repositories**
- AgriciDaniel/claude-obsidian:
  - #165, "marketplace add … doesnt work" ("Marketplace sync failed"), Windows desktop app, 2026-08-13, OPEN.
  - #162, v2.1.0 hooks.json command+args split → the hook payload is executed as Python (`NameError: name 'false'`), 2026-08-09, CLOSED.
  - #183, lint walks into .claude/ worktrees and produces thousands of false findings, 2026-08-31, CLOSED.
  - #192: the source/claim ledgers have a hard 16 MB read cap.
  - #196/#168: SessionStart/Stop hooks hit the 5 s timeout on Windows.
  - https://github.com/AgriciDaniel/claude-obsidian/issues [community][verified]
- nvk/llm-wiki:
  - #138, session hooks rebuild global indexes on every event and blow the 5 s deadline, 2026-10-31, OPEN.
  - #119, the same additionalContext is re-injected on every prompt, which breaks prefix caching, 2026-10-22, CLOSED.
  - #104, the `references/` git symlink 404s on raw.githubusercontent.com, 2026-10-22, CLOSED.
  - #91, lint never validates footnotes or wikilinks.
  - https://github.com/nvk/llm-wiki/issues [community][verified]
- Astro-Han/karpathy-llm-wiki:
  - #10: `check_evidence.py` normalises the article side and not the raw side, so verbatim quotes that contain Markdown are flagged as suspect. 2026-09-20, OPEN.
  - #7: a user adds a `Fingerprint: git:<hash>` + `Monitored:` header and runs `git diff` at session start ("0.01s, 0 tokens") to catch drift. 2026-08-21, OPEN.
  - https://github.com/Astro-Han/karpathy-llm-wiki/issues/10 , /7 [community][verified]
  - Per Argon, the README's "Design Boundaries" section drops persisted line-number citations, numeric confidence and source-hash tracking after three months of logs. [Argon, not verified]
- vanillaflava/llm-wiki-skills:
  - A single issue, #1, "Linking and Source Attribution" (2026-04-16, CLOSED): too much reliance on `changes` in frontmatter. Thin. [community][verified]
  - README (per Argon): claude.ai web/mobile "cannot reach files on your disk … not recommended for primary use". [Argon, not verified]
- TrueHOOHA/LLM-Wiki: the issue list is empty. Nothing found in the community: **thin**, because the repo has 22 stars and no visible discussion. [verified empty list]

**Other 2026 repositories the community recommends** (stars read from the github.com page, 2026-11-02 [verified]; "what people say" from Argon unless marked)
1. Ar9av/obsidian-wiki, https://github.com/Ar9av/obsidian-wiki , **3,654★**, MIT. A Claude Code plugin with wiki-setup/ingest/query/lint skills. It marks claims with `^[inferred]`/`^[ambiguous]` and lints undated claims. It appears in the Starmorph "How to Build Karpathy's LLM Wiki" guide (2026-04-09). [community][stars verified; rest Argon, not verified]
2. lucasastorian/llmwiki, https://github.com/lucasastorian/llmwiki , **1,741★**, Apache-2.0. MCP into claude.ai/Code with a deterministic lint ("citation resolution, dangling links, orphan and stale pages"). Cited in the Astro-Han README. [community][stars verified; rest Argon, not verified]
3. ussumant/llm-wiki-compiler, https://github.com/ussumant/llm-wiki-compiler , **329★**, MIT. Reddit r/ClaudeCode 1scidpz, 106 upvotes, 2026-04-05: "reduced my context tokens by 84%". [community][stars verified; Reddit Argon, not verified]
4. alirezarezvani/claude-skills, https://github.com/alirezarezvani/claude-skills , **29,143★**, MIT. Argon's figures of "5,200+/12k" were wrong. It has an `engineering/llm-wiki` skill with stdlib Python lint/BM25 scripts. [stars verified; skill contents Argon, not verified]
5. pricklywiggles/niamos, https://github.com/pricklywiggles/niamos , **194★**. PARA plus wiki skills (place-wiki, audit). r/ObsidianMD 1u9oxug, 304 upvotes, 2026-06-19. [community][stars verified; Reddit Argon, not verified]
- Index of the field: gavischneider/awesome-llm-wiki, **256★** [verified stars].

## Topic 2 — the practice of copying single SKILL.md files

- dev.to/aidiveyt, "Everything Claude Code costs 27,000 tokens before you type. I kept five pieces." 286 skill descriptions ≈21k tokens and 68 agents ≈5k tokens, i.e. 14% of a 200k window. "Copying five directories out is the intended use, not a workaround." https://dev.to/aidiveyt/everything-claude-code-costs-27000-tokens-before-you-type-i-kept-five-pieces-52bb [community][verified via search snippet]
- dev.to/harivenkatakrishnakotha: installing ECC globally came to about 103k tokens of files. The author kept only skills used in "80%+ of your projects" globally and went from 20 global skills to 6. https://dev.to/harivenkatakrishnakotha/how-i-cut-claude-codes-token-overhead-by-44-and-stopped-hitting-usage-limits-mid-session-3fkf [community][verified via search snippet]
- Why plugins are avoided in favour of single skills:
  - CC #98220: `skillOverrides` cannot disable an individual plugin skill. The only option is to disable the whole plugin. 2026-09-29, OPEN. https://github.com/anthropics/claude-code/issues/98220
  - #89724: skillOverrides silently no-ops for plugin-namespaced keys. 2026-08-26, CLOSED.
  - #64606: the description budget (`skillListingBudgetFraction` 0.01, ~8k chars) silently truncates or drops skills. 2026-06-02, CLOSED.
  - [community][verified]
- What breaks on copy or upload:
  - Unexpected frontmatter keys. anthropics/skills #37 quotes the claude.ai error "unexpected key in SKILL.md frontmatter: properties must be in ('name', 'description', 'license', 'allowed-tools', 'metadata')" (2025-10-19, OPEN).
  - The current docs' form is "Unexpected key(s) in SKILL.md frontmatter: argument-hint. Allowed properties are: allowed-tools, compatibility, description, license, metadata, name". https://code.claude.com/docs/en/skills
  - Both sources: [verified]
- rfsbraz/genealogy-agent-skills #25 (2026-10-21, CLOSED): quick_validate failed 23 of 26 skills on `disable-model-invocation`. The fix keeps the key in source and strips it in the upload bundles. The issue also notes that once the key is gone every skill can auto-trigger on claude.ai, so descriptions must also say when **not** to use the skill. https://github.com/rfsbraz/genealogy-agent-skills/issues/25 [community][verified]
- anthropics/skills #394 (2026-08-14, OPEN): asks the validator to warn rather than error on Claude Code extension fields. #1957 (2026-10-03, OPEN): skill-creator's own `description: [TODO: …]` template parses as a YAML list and fails its own validator. https://github.com/anthropics/skills/issues/394 , /1957 [community][verified]
- Relative `references/` and symlinked reference folders break when copied or loaded remotely (anthropics/skills #1153; nvk/llm-wiki #104, above). Copying "the whole skill directory, not only SKILL.md" is standard advice. https://aiagentskills.net/blog/how-to-install-claude-skills [community][verified]
- Keeping copies updated:
  - GitHub's `gh skill` (changelog 2026-04-16, preview) has `--pin` for a tag or SHA. Pinned skills are skipped by updates. Provenance (repository, ref, tree SHA) is written into the SKILL.md frontmatter, and `gh skill update` compares tree SHAs "to detect real content changes, not just version bumps".
  - Its install docs warn that skills "may contain prompt injections, hidden instructions, or malicious scripts".
  - Sources: https://github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/ , https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills [verified via search snippets]
- Divergence risk when copying: "the two copies then diverge and nothing tells you". A stale copy in ~/.claude/skills beats the project copy "and nothing says so". https://www.matthewswong.com/en/blog/claude-code-plugin-vs-skill-bundling/ [community][verified via search snippet]
- A vendoring example: deonmenezes/mobile-app-skill copies 48 of 50 skills "unmodified under their own licences", pinned to the commits in CREDITS.md. https://github.com/deonmenezes/mobile-app-skill [community][verified via search snippet]
- Reddit r/aiagents 1sdvq9t (639 pts, 2026-04-06) gives cherry-pick advice for ECC. That rests on an earlier Argon job (0acdde65, run by R4), not this one. [Argon, not verified]
- Thin: the Argon job dedicated to this topic failed (RESOURCE_EXHAUSTED). No Reddit thread was reached for scripts that need a runtime once copied, or for diff scripts against upstream.

## Topic 3 — plugin install/settings, namespacing, claude.ai upload limits

- **Description limit actually enforced on upload: 1,024.**
  - mrKanoh/wcag-accessibility-audit-skill #4 (2026-08-14): "field 'description' in SKILL.md must be at most 1024 characters" when importing into Claude.
  - a-digital-arts-institute/adai-v1 #95 (2026-10-28): "Customize → Skills → Upload rejects it with: field 'description' in SKILL.md must be at most 1024 characters".
  - https://github.com/mrKanoh/wcag-accessibility-audit-skill/issues/4 , https://github.com/a-digital-arts-institute/adai-v1/issues/95 [community][verified via search snippet; dates verified]
- **200 characters is the documented limit.** The support article says "(200 characters maximum)" for the description and 64 for the name; I curl'd the page. https://support.claude.com/en/articles/12512198-how-to-create-custom-skills [verified]
  - Several PRs shorten descriptions to ≤200 "to fit claude.ai's documented 200-character limit" (BoniniTech/career-assessment #20; AlveeeRahman/skill-vision #4: "would still have been rejected on upload at 461 chars"; motkep173 PR #13). None quotes an actual 200-character error message. [community][verified via search snippet]
- Angle brackets:
  - CC #63081 (2026-05-28): a Cowork plugin upload fails with a generic "Plugin validation failed" when any SKILL.md `description` contains `<…>`. Closed as a duplicate.
  - CC #82749 (2026-07-31): git-sync to claude.ai **silently omits** those skills and reports success, while `claude plugin validate` passes.
  - CC #56376 (2026-05-05): the upload UI swallows the server's `validation_errors[]`.
  - https://github.com/anthropics/claude-code/issues/82749 [community][verified]
- Name rules: anthropics/skills #241 (2026-01-15, OPEN) shows the upload error "Skill name … can only contain lowercase letters, numbers, and hyphens", and complains that the official examples break it. https://github.com/anthropics/skills/issues/241 [community][verified]
- Batch upload: CC #82044 (2026-07-28). When re-uploading several zipped skills that already exist, only one gets the replace prompt and the rest are rejected. https://github.com/anthropics/claude-code/issues/82044 [community][verified]
- Account skills have no read-back and no compare-and-swap, so concurrent sessions overwrite each other's edits (CC #89828, 2026-08-26). https://github.com/anthropics/claude-code/issues/89828 [community][verified]
- Namespacing:
  - Docs: a plugin skill is `/plugin:name`, and the bare `/name` also works "unless another command already uses that name". https://code.claude.com/docs/en/skills [verified]
  - Community: CC #92738 (2026-09-07, OPEN), a bare-name invocation shows a false "isn't a recognized command" warning. #91417 (2026-09-02, CLOSED), mid-input completion never matches `plugin:skill`. #74363 (2026-07-05, CLOSED), the VS Code extension can't submit `/plugin:skill`. #95519 (2026-09-19, OPEN), an *uninstalled* catalog plugin claims `/rc` and shadows a local skill. #100175 (2026-10-07, OPEN), a personal skill is listed twice, once unscoped and once as self-namespaced. [community][verified]
- Marketplace/settings:
  - CC #95100 (2026-09-17, OPEN): on the web, the marketplace name is the bare repo name, so two `*/skills` repos collide (`marketplace_name_taken`).
  - #96319 (2026-09-23, CLOSED): the claude.ai web/desktop loaders ignored the marketplace `skills` array, so every plugin got every repo skill.
  - #105549 (2026-10-28, OPEN): a plugin enabled only through a project's `enabledPlugins` doesn't load headless.
  - #97264 (2026-09-25, OPEN): with CLAUDE_CONFIG_DIR set, starting in $HOME records a project-scope install of every user plugin.
  - #98894 (2026-10-02) and #95157 (2026-09-17): claude.ai account plugins can't be removed. They re-enable server-side and sync back into Claude Code.
  - All at https://github.com/anthropics/claude-code/issues/<n> [community][verified]
  - I found no community complaint specifically about `claude plugin marketplace add` writing extraKnownMarketplaces into ~/.claude/settings.json. **Thin.** The docs fact (user settings) is in R2's notes.
- ZIP size: there is no community report of a claude.ai skill ZIP size limit. The support page names "ZIP too large" without a number. The Skills API states <30 MB (R1's e-skills-install.md). **Thin.**
- Mobile:
  - One user says "I can trigger tomorrow and deadline skills from the Claude app on my Android" (dev.to/mxomasuku). This is a single anecdote, and the post does not say whether those were uploaded custom skills. https://dev.to/mxomasuku/can-claude-skills-save-us-from-the-smartphone-4828 [community][verified via search snippet]
  - The help-center "Use skills in Claude" page does not mention mobile. **Thin.**

## Topic 4 — Claude Managed Agents in practice

- **Git push policy.** CC #66571 (opened 2026-06-09, closed by the stale bot): "The sandbox git push proxy … returns HTTP 503 on every push attempt". A user later found that pushes work only to a branch named exactly `claude/<session-id>`, and that a push to main gets a 503 that "is actually the policy, so retrying won't help". The PR then goes through the GitHub MCP server. A second user: "using MCP as a fallback". https://github.com/anthropics/claude-code/issues/66571 [community][verified]
- **Memory mount in deployments.** anthropics/claude-cookbooks #830 (2026-08-14, OPEN): /mnt/memory was absent in 3/3 deployment-created sessions. `mount_path` is returned even when the mount failed (PR #843 rewords the notebook). The memory_* tools work as a fallback. https://github.com/anthropics/claude-cookbooks/issues/830 [community][verified]
  - Contrast: Anthropic's daily-brief quickstart (claude-quickstarts @1a18c34) mounts two stores in a cron deployment (`"32 7 * * 1-5"`, America/New_York) and reads /mnt/memory/preferences every run. [verified]
- **Reference scheduled-job design (daily-brief):**
  - The budget is `amount: "500"` (cents as a string, $5/run). "A run that reaches it pauses rather than fails, which from the channel looks like silence."
  - web_search and web_fetch are disabled because they "run on Anthropic's servers, outside the" sandbox allowlist.
  - The GitHub MCP toolset is `always_allow`, with a read-only token.
  - Measured cost: about $1.00/run on Sonnet 5 and $1.50 on Opus 5 for a busy day; $0.15–0.30 when every source is unreadable.
  - https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents/daily-brief (README.md, agent.md, deployment.md, read raw) [verified]
- **MCP permission flakiness.** anthropic-sdk-typescript #1099 (2026-06-23, OPEN): MCP calls are "randomly denied with 'Permission to use [tool] has been denied' despite … always_allow", correlating with `agent.custom_tool_use` classification. A second org reproduced it. https://github.com/anthropics/anthropic-sdk-typescript/issues/1099 [community][verified]
- anthropic-sdk-python #1687 (2026-06-19, CLOSED as fixed): configuring web_search/web_fetch in the agent toolset alongside an mcp_toolset misrouted MCP calls so they never executed. The maintainer says it "no longer reproduces". This is the exact combination the scout uses. https://github.com/anthropics/anthropic-sdk-python/issues/1687 [community][verified]
- Other failure modes:
  - #1383 (2026-04-14, CLOSED): Managed Agents MCP was SSE-only, which broke Streamable-HTTP servers.
  - #1405 (CLOSED): a 406 on the GET probe lost tool results.
  - #1562 (CLOSED): `vault_ids` were not inherited by subagents.
  - #2026 (2026-10-18, OPEN): self-hosted sessions_token expires after about 60 minutes.
  - TS #1066 (CLOSED): `skills.versions.create` stripped filenames ("SKILL.md file must be exactly in the top-level folder").
  - https://github.com/anthropics/anthropic-sdk-python/issues/<n> [community][verified]
- "Silent failure" guidance: "If an MCP server is down or its token has expired, the run still starts without that server's tools … A reader cannot tell that apart from a quiet day." AI Catchup, scheduled-agent best practices (curl'd). https://aicatchup.com/practices/scheduled-claude-agent-automations [community][verified]
- PRs through GitHub MCP in practice: Port.io's Managed Agents template enables only `create_pull_request` (`default_config.enabled:false`, `always_allow`) and does clone/commit/push through the `github_repository` resource. https://docs.port.io/workflows/build-workflows/nodes/action-nodes/integration-actions/ai/claude-managed-agents/ [verified]
- Costs as described by third parties: runtime is $0.08/session-hour, counted only while running. A 24/7 agent costs about $58/month in runtime alone, and "The $0.08 meter is not what empties the account; the model is." https://www.agent37.com/blog/claude-managed-agents-pricing [verified via search snippet]
- Claude Code Routines versus deployments: routines run on the subscription, have a one-hour minimum interval, act as the user, and push only to `claude/`-prefixed branches. Deployments bill to the API, use minute-level cron, and have a dollar cap. https://www.developersdigest.tech/blog/claude-code-routines-vs-managed-agents-schedules [verified via search snippet]
- Dreams:
  - r/ClaudeAI 1t5j84j (u/ClaudeOfficial, 46 upvotes, 2026-05-06), "Harvey saw ~6x higher task completion". Commenters: "Dreaming is way to burn more of your tokens" and "you've removed that access and made us fill in a form".
  - r/AI_Agents 1tuwftb (2026-06-02): memory "maintenance is" the hard problem.
  - [community][Argon, not verified]
- Mnemoverse (2026-09-03): the memory API "has no search endpoint"; listing has only path_prefix and depth 0/1. [Argon, not verified]
- Recurring PR agents in production: a Medium post (Ali Süleyman Topuz, 2026-09-04) mentions "cron-triggered research and data-cleanup jobs" plus an overnight PR reviewer. [Argon, not verified]
  - **Nobody was found running a weekly web "scout" that opens PRs through GitHub MCP on a scheduled deployment.** Thin: only the halves exist (daily-brief, Port, #66571).

## Could not verify
- Every Reddit item. Egress to reddit.com is blocked here, and web_fetch refuses unshown Reddit URLs. Scores, dates and post ids above are Argon's.
- Argon's blog claims: agents&me on kepano (no URL), the DEV review of wshobson, the r/ClaudeWorkflows "92.5% missing tools" audit, Mnemoverse, the Topuz Medium post, the Astro-Han "Design Boundaries" wording.
- Argon's star counts for alirezarezvani/claude-skills were wrong: it said 5.2k/12k, the page shows 29,143. Its anthropics/skills issue dates were partly off; #1153 is 2026-08-25, not May 17.
- Whether the claude.ai uploader *also* rejects 201–1,024-character descriptions. No observed error supports this, and the help center says 200.
- The claude.ai skill ZIP size limit; whether uploaded skills appear in the iOS/Android apps.
- Whether cookbooks #830, the memory mount failing in deployments, is fixed. The issue is open while the official quickstart relies on the mount.
- Whether `claude/<session-id>` is still the git-proxy rule (it is a user's finding from June 2026 and not in the docs).
- Argon job 5e972d4d's turn 1 (47k chars on topic 3) finished, but its text is stored only on the Argon operator's server and could not be retrieved after the 402 refusal.

## Relevance
**Topic 1 (repos):**
- Confirm the plan's file-by-file borrowing from kepano (obsidian-markdown) and the pinned-SHA approach. Two upstreams demonstrably fail to deliver fixes through plugin auto-update (kepano #146, wshobson #786).
- Add known defects to each adapted skill's notes: kepano #128 (teach rename, not `mv`), #144 (alias wikilinks), #149 (Obsidian 1.14 Bases sort).
- Astro-Han #10 is a known bug in check_evidence.py's normalisation. Fix it before reuse, or rewrite.
- anthropics/skills skill-creator is over its own 500-line guide and has the workspace-in-.claude/skills token leak (#763). Keep it as a reference only, and do not run it inside the vault repo.
- Consider Ar9av/obsidian-wiki (^[inferred] markers, undated-claim lint) and lucasastorian/llmwiki (deterministic lint list) as idea sources.

**Topic 2 (copying):**
- Keep spec-only frontmatter in the shared skill folder. Alternatively, keep Claude Code-only keys in source and strip them in a packaging step, as rfsbraz does.
- Record provenance (upstream repo, path, SHA, licence) per borrowed skill. `gh skill`'s `metadata.github-*` frontmatter is a ready-made format that also works in the `metadata` map allowed on claude.ai.
- Do not borrow skills whose value depends on scripts needing a runtime absent on claude.ai or the API.

**Topic 3 (upload):**
- The lint for the skills folder should enforce: name `[a-z0-9-]` ≤64 and equal to the folder name; description ≤200 (the documented limit, with 1,024 as the hard limit); **no `<` or `>` in descriptions**; only the six keys.
- `claude plugin validate` does not catch angle brackets. Rely on our own check, not on validate.
- Expect `/plugin:skill` namespacing quirks. Prefer plain `.claude/skills/` for the vault's own skills.
- Treat mobile availability as unverified.

**Topic 4 (fortnightly scout):**
- Confirm vault-held GitHub MCP for PRs. If the job also pushes with git through a mounted repo, the branch must be `claude/<session-id>`. Alternatively, do everything through MCP (create_branch, push_files, create_pull_request).
- Add a first-step memory-mount check with a memory_* tool fallback (#830).
- Add an explicit "PR not opened / source unreadable" final line so that silence is impossible. Budget pauses look like silence, MCP can be denied despite always_allow, and expired tokens drop tools silently.
- Re-decide web_fetch. Anthropic's own reference job disables it as an exfiltration route. If the scout needs it, document the risk and restrict MCP tools to an allow-list (`default_config.enabled:false`).
- Expected cost of about $1 per run on Sonnet matches the existing ~$1.50 estimate.

## Calls and cost
- `argon_research`, "community reports on Claude skills repos for LLM wikis and Obsidian" (job ef931138, 3 turns): saved, 24,394 chars, "3 turns ≈197.3 ¢ in 12 min". Last turn line: "≈69.7 ¢ (today UTC 1542.6 ¢ / cap 5000 ¢)".
- `argon_research`, "copying individual SKILL.md files from big Claude Code skill repos" (job 4e215e8c, 3 turns planned): **failed RESOURCE_EXHAUSTED in turn 1**. No answer and no cost line returned.
- `argon_research`, "Claude plugin install settings, namespacing and claude.ai skill upload limits" (job 5e972d4d, 2 turns): turn 1 done (47,031 chars, not retrievable). **Turn 2 refused: "Gemini HTTP 402 … Your prepayment credits are depleted"**. No cost line returned.
- `argon_research`, "Claude Managed Agents in practice 2026" (job d0520f84, 2 turns): saved, 28,800 chars, "2 turns ≈193.8 ¢ in 12 min". Last turn line: "≈104.6 ¢ (today UTC 1712.7 ¢ / cap 5000 ¢)".
- `ask_argon` ping (thinking low, no search) to check availability: **refused, "Gemini: prepaid balance is empty, top up in AI Studio → Billing" (HTTP 402)**. No cost.
- Refusal type: prepaid-credit exhaustion at Google (HTTP 402), **not** the server's daily cap. The daily total was 1712.7 ¢ of 5000 ¢ at the last report. After the refusal I made no further Argon calls and fell back to web_search and curl of GitHub.

## Sources
- GitHub issues (opened via curl of github.com HTML):
  - kepano/obsidian-skills #112 #128 #144 #146 #149
  - anthropics/skills #37 #241 #249 #394 #763 #919 #1153 #1622 #1668 #1957 #2048 #2090 #2104
  - wshobson/agents #701 #777 #786 #787
  - AgriciDaniel/claude-obsidian #162 #165 #183 #192 #196
  - nvk/llm-wiki #91 #104 #119 #138
  - Astro-Han/karpathy-llm-wiki #7 #10
  - vanillaflava/llm-wiki-skills #1
  - anthropics/claude-code #44780 #56376 #63081 #64606 #66571 #74363 #82044 #82749 #89724 #89828 #91417 #92738 #95100 #95157 #95519 #96319 #97264 #98220 #98894 #100175 #105549
  - anthropics/claude-cookbooks #539 #830
  - anthropics/anthropic-sdk-python #1383 #1405 #1562 #1687 #2026
  - anthropics/anthropic-sdk-typescript #1066 #1099
  - rfsbraz/genealogy-agent-skills #25
  - mrKanoh/wcag-accessibility-audit-skill #4
  - a-digital-arts-institute/adai-v1 #95
- Repo pages (stars): Ar9av/obsidian-wiki, lucasastorian/llmwiki, ussumant/llm-wiki-compiler, alirezarezvani/claude-skills, pricklywiggles/niamos, gavischneider/awesome-llm-wiki.
- Raw files: anthropics/claude-quickstarts @1a18c340 managed-agents/daily-brief/{README.md, agents/daily-brief/agent.md, deployment.md}.
- Docs and support: https://support.claude.com/en/articles/12512198-how-to-create-custom-skills (curl), https://support.claude.com/en/articles/12512180-use-skills-in-claude , https://code.claude.com/docs/en/skills
- GitHub `gh skill`: https://github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/ , https://cli.github.com/manual/gh_skill_install
- Blogs: dev.to aidiveyt (ECC 27k tokens), dev.to harivenkatakrishnakotha, dev.to mxomasuku, matthewswong.com, aiagentskills.net, https://aicatchup.com/practices/scheduled-claude-agent-automations (curl), docs.port.io Claude Managed Agents node (curl), agent37.com pricing, developersdigest.tech routines vs schedules, BoniniTech PR #20, AlveeeRahman PR #4, motkep173 PR #13
- Argon-only (not opened):
  - Reddit r/ObsidianMD 1q8gn9c, 1u9oxug
  - Reddit r/ClaudeCode 1scidpz
  - Reddit r/LLMDevs 1situqz
  - Reddit r/ClaudeAI 1t5j84j
  - Reddit r/AI_Agents 1tuwftb
  - blog.starmorph.com Karpathy LLM wiki guide
  - mnemoverse.com memory API note
  - topuzas.medium.com
  - growthexe.substack.com "1,116 Claude Code skills"
