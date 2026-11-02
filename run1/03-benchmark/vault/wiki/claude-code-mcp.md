---
tags: [claude-code, mcp, servers, integrations]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/claude-code/mcp.md]
---
# Claude Code MCP servers

Claude Code connects to tools through the Model Context Protocol (MCP).

## Adding servers
- **Remote HTTP** (recommended): `claude mcp add --transport http <name> <url>`, e.g. `claude mcp add --transport http notion https://mcp.notion.com/mcp`; add `--header "Authorization: Bearer your-token"` for a token. In JSON, `type` accepts `streamable-http` as an alias for `http`; a JSON entry with a `url` but no `type` is a configuration error (read as stdio).
- **SSE** is deprecated: `claude mcp add --transport sse <name> <url>`.
- **Local stdio**: `claude mcp add [options] <name> -- <command> [args...]`; `--` separates Claude's options (`--transport`, `--env`, `--scope`) from the server command, e.g. `claude mcp add --transport stdio myserver -- npx server` runs `npx server`. Claude Code sets `CLAUDE_PROJECT_DIR` in the server's environment. On macOS and Linux it stops a stdio server with `SIGINT`, then `SIGTERM` 100 milliseconds later, then `SIGKILL` after a further 400 milliseconds.
- **WebSocket**: configure in `.mcp.json` or `claude mcp add-json`; no OAuth.

## Managing
`claude mcp list`, `claude mcp get notion`, `claude mcp remove notion`, and `/mcp` inside Claude Code for status. Toggle a server off in `/mcp` to disable it without removing it (recorded per project in `~/.claude.json` as `disabledMcpServers`; default-off built-ins like `computer-use` go in `enabledMcpServers`).

Time limits: per-server `timeout` in milliseconds (values below 1000 are ignored) or `MCP_TOOL_TIMEOUT` (default about 28 hours). Idle window defaults to five minutes; change with `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT` (`0` disables). A main-conversation call running past two minutes moves to a background task.

## Scopes
| Scope | Loads in | Shared | Stored in |
|---|---|---|---|
| Local (default) | current project | No | `~/.claude.json` |
| Project | current project | Yes, via version control | `.mcp.json` in project root |
| User | all your projects | No | `~/.claude.json` |
Set with `--scope`, e.g. `claude mcp add --transport http shared-server --scope project https://example.com/mcp`. Claude Code prompts for approval before using project-scoped servers from `.mcp.json`; reset with `claude mcp reset-project-choices`.

Precedence when the same server is defined twice (whole entry, no field merging): 1. Local scope, 2. Project scope, 3. User scope, 4. plugin-provided servers, 5. claude.ai connectors; a `managedMcpServers` server ranks above all. `.mcp.json` supports environment variable expansion in `command`, `args`, `env`, `url` and `headers`.

Permission rules for MCP tools are in [[claude-code-settings-permissions]].

derived_from:: [[raw/claude-code/mcp.md]]
