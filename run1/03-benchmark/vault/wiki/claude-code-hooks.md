---
tags: [claude-code, hooks, automation]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/claude-code/hooks.md]
---
# Claude Code hooks

Hooks are user-defined shell commands, HTTP endpoints, MCP tool calls, LLM prompts, or subagents that run automatically at points in Claude Code's lifecycle. When an event fires and a matcher matches, Claude Code passes JSON context (on stdin for command hooks, as the POST body for HTTP hooks).

## Events (selection)
- Per session: `SessionStart`, `SessionEnd`. Per turn: `UserPromptSubmit`, `Stop`, `StopFailure`. Per tool call: `PreToolUse` (can block), `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`.
- Others: `Notification`, `SubagentStart`, `SubagentStop`, `PreCompact`, `PostCompact`, `ConfigChange`, `CwdChanged`, `FileChanged`, `InstructionsLoaded` (when a CLAUDE.md or `.claude/rules/*.md` file is loaded), `WorktreeCreate`, `Elicitation`.

## Configuration
Three levels: hook event → matcher group → hook handlers. Locations: `~/.claude/settings.json` (all your projects), `.claude/settings.json` (project, shareable), `.claude/settings.local.json`, managed policy settings, plugin `hooks/hooks.json`, skill frontmatter, subagent frontmatter. Hook entries merge across settings levels. `allowManagedHooksOnly` in managed settings blocks user, project, local and plugin hooks.

**Matchers**: `"*"`, `""` or omitted = all; letters/digits/`_`/`-`/spaces/`,`/`|` = exact names (`Bash`, `Edit|Write`); anything else = unanchored JavaScript regex (`mcp__memory__.*`; use `^Edit$` for a whole-string match). `PreToolUse` matches tool names; `SessionStart` matches `startup`, `resume`, `clear`, `compact`, `fork`.

**Handler types**: `command`, `http`, `mcp_tool`, `prompt`, `agent` (experimental). Matching hooks run in parallel. Common fields: `if` (one permission rule, e.g. `"Bash(git *)"`), `timeout` (defaults 600 for `command`, `http`, and `mcp_tool`; 30 for `prompt`; 60 for `agent`), `statusMessage`, `once`.

## Exit codes and output
- Exit 0: success; JSON output fields apply.
- Exit 2: blocking error on events that can block — a `PreToolUse` hook blocks the tool call, `UserPromptSubmit` rejects the prompt; stderr is the reason. JSON cannot override an exit-2 block (even `permissionDecision` `"allow"`).
- Other codes: non-blocking error; the action goes ahead.
- `PreToolUse` decision control can allow, deny, ask, or defer, e.g. `permissionDecision: "deny"` with a `permissionDecisionReason`. Plain stdout reaches Claude as context only for `UserPromptSubmit`, `UserPromptExpansion`, `SessionStart` and `PostModelSwitch`.
- Files referenced with `@` are inserted without a tool call, so `PreToolUse` does not see them.

## Operations
`"async": true` (command hooks only) runs in the background and cannot block. `/hooks` opens a read-only browser. `"disableAllHooks": true` disables hooks but cannot disable managed hooks from outside managed settings. Permission rules and modes: [[claude-code-settings-permissions]]; hooks in skills and subagents: [[claude-code-skills-subagents]].

derived_from:: [[raw/claude-code/hooks.md]]
