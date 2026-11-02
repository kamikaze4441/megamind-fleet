---
tags: [claude-code, skills, subagents, agents]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/claude-code/skills.md, raw/claude-code/sub-agents.md]
---
# Claude Code skills and subagents

## Skills
A skill is a `SKILL.md` file with instructions; Claude uses it when relevant, or you invoke it with `/skill-name`. Unlike CLAUDE.md content, a skill's body loads only when used. **Custom commands have been merged into skills**: `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` both create `/deploy`. Skills follow the Agent Skills open standard.

Locations: Personal `~/.claude/skills/<skill-name>/SKILL.md` (all your projects); Project `.claude/skills/<skill-name>/SKILL.md` (commit for the team); Nested `<subdir>/.claude/skills/...` (load when Claude first works on files there); Enterprise (managed settings directory); Plugin (invoked as `/plugin-name:skill-name`). Project skills also load from every parent directory up to the repository root. Don't name a skill folder `synced`.

Frontmatter (all optional, `description` recommended): `name` (defaults to the directory name), `description` (with `when_to_use`, truncated at 1,536 characters), `disable-model-invocation: true` (only you can trigger it), `user-invocable: false` (only Claude), `allowed-tools` (no permission prompts during the invoking turn, e.g. `allowed-tools: Read Grep`), `disallowed-tools`, `model`, `effort`, `context: fork` (run in a forked subagent) with `agent`, `hooks`, `paths` (glob patterns limiting activation), `shell` (`bash` default or `powershell`). Unknown field names are ignored without error; frontmatter is read only when `---` is the file's first line.

## Subagents
Subagents run in their own context window with a custom system prompt, specific tool access and independent permissions, and return only a summary. Claude delegates based on each subagent's description; combined custom descriptions over 15,000 tokens trigger a startup warning.

Built-in: **Explore** (read-only; Write and Edit denied; thoroughness quick, medium or very thorough), **Plan** (research in plan mode), **General-purpose** (all tools), plus statusline-setup (Sonnet) and claude-code-guide (Haiku). Explore and Plan start without your CLAUDE.md files. Remove them with `CLAUDE_CODE_DISABLE_EXPLORE_PLAN_AGENTS=1`; block one with `permissions.deny` (e.g. `Agent(Explore)`).

Scope and priority (same name → higher wins): Managed settings 1 (highest); `--agents` CLI flag 2 (JSON, session only); `.claude/agents/` 3; `~/.claude/agents/` 4; plugin `agents/` 5 (lowest). Files are Markdown with YAML frontmatter (`name`, `description`, `tools`, `disallowedTools`, `model`, `permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills`, `memory`, `isolation`, `omitClaudeMd`) followed by the system prompt. Plugin subagents ignore `hooks`, `mcpServers` and `permissionMode`. Edits under `~/.claude/agents/` and `.claude/agents/` are picked up within a few seconds without restart.

Related: hooks in skill/subagent frontmatter [[claude-code-hooks]]; CLAUDE.md loading [[claude-code-memory]].

derived_from:: [[raw/claude-code/skills.md]]
derived_from:: [[raw/claude-code/sub-agents.md]]
