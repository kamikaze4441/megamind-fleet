---
tags: [claude-code, settings, permissions, precedence]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/claude-code/settings.md, raw/claude-code/permissions.md]
---
# Claude Code settings files and permission rules

## Settings files and scope
| Scope | File | Who it affects |
|---|---|---|
| User | `~/.claude/settings.json` | you, every project on this machine |
| Shared project | `.claude/settings.json` | everyone in the folder; commit it for teammates |
| Project local | `.claude/settings.local.json` | you, this project only; kept out of git |
| Managed | `managed-settings.json` and other managed sources | everyone the organization deploys it to |
Claude Code also writes `~/.claude.json` for itself (account, MCP server configs, per-project trust). Settings files are strict JSON: a `//` comment or a trailing comma is a Settings Error. Most edits (including `permissions` and `hooks`) reload without restart; `model` and `effortLevel` are read once at session start. Run `/status` and read the `Setting sources` line to confirm what loaded; `claude doctor` lists rejected entries. One session only: `claude --settings '{"model": "claude-opus-5-5"}'`.

## Precedence (highest first)
1. Managed settings — nothing in your files or `--settings` overrides a managed key.
2. Command line (`--settings <file-or-json>`).
3. Project local (`.claude/settings.local.json`).
4. Shared project (`.claude/settings.json`).
5. User (`~/.claude/settings.json`).
Environment variables are not a level: `ANTHROPIC_MODEL` applies over `model` from any file, `ANTHROPIC_DEFAULT_MODEL` only when no file sets `model`. List keys such as `permissions.allow` merge across files instead of overriding.

## Permission rules
Manage with `/permissions`. **Allow**, **Ask**, **Deny**; evaluated deny, then ask, then allow — the first match wins and specificity doesn't change the order, so `Bash(aws *)` deny beats a `Bash(aws s3 ls)` allow. Rules are enforced by Claude Code, not by the model; `CLAUDE.md` cannot grant access. "Yes, and don't ask again" saves an `allow` rule to `.claude/settings.local.json` at the git repository root.
- Syntax `Tool` or `Tool(specifier)`: `Bash(npm run build)`, `Read(./.env)`, `WebFetch(domain:example.com)`; `Bash(*)` equals `Bash`. Put `*` after the subcommand: `Bash(git log *)`.
- Compound commands split on `&&`, `||`, `;`, `|`, `|&`, `&` and newlines; every subcommand must be allowed.
- MCP: `mcp__puppeteer__*` or `mcp__puppeteer__puppeteer_navigate`. Subagents: `Agent(Explore)` in `deny`.
- Parameter rules for deny/ask: `Agent(model:opus)`, `Bash(run_in_background:true)`.

## Permission modes (`defaultMode`)
`default` (Manual), `acceptEdits`, `plan`, `auto` (classifier), `dontAsk`, `bypassPermissions` (only in isolated environments). Block modes with `permissions.disableBypassPermissionsMode` or `permissions.disableAutoMode` set to `"disable"`.

Permissions and sandboxing are complementary; with `autoAllowBashIfSandboxed` at its default `true`, sandboxed Bash runs without a bare `Bash` ask prompt (see [[claude-code-sandboxing]]). Hooks can also decide permissions ([[claude-code-hooks]]).

derived_from:: [[raw/claude-code/settings.md]]
derived_from:: [[raw/claude-code/permissions.md]]
