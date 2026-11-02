---
tags: [claude-code, sandbox, security, bash]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/claude-code/sandboxing.md]
---
# Claude Code sandboxed Bash tool

The Bash sandbox is an OS-enforced boundary around the shell commands Claude runs: it limits which files and network domains Bash, PowerShell and Monitor commands (and their child processes) can reach. It is **off by default**; turn it on with `/sandbox` or `sandbox.enabled` set to `true`. It runs on macOS (Seatbelt), Linux and WSL2 (needs `bubblewrap` and `socat`: `sudo apt-get install bubblewrap socat`); on native Windows commands run unsandboxed. It is built on the open source `@anthropic-ai/sandbox-runtime` package.

## Defaults
| Access | Default |
|---|---|
| Writes | working directory, per-user temp directory, added directories; protected paths stay write-denied |
| Reads | most of the machine, including `~/.ssh` and `~/.aws/credentials` |
| Network | no direct route out; a local proxy checks each host against allowed domains, which start empty |
| Environment variables | inherited from Claude Code |

## What runs outside it
Built-in file and web tools (Read, Edit, Write, WebFetch, WebSearch) follow permission rules instead — a `denyRead` entry doesn't stop the Read tool and `allowedDomains` doesn't limit WebFetch. Hooks, local MCP servers and LSP servers also run outside, as do `!` shell-mode commands you type, `excludedCommands` matches, and unsandboxed retries.

## Modes
- **Auto-allow mode**: sandboxed commands are approved with no prompt. Still enforced: `Bash` deny rules, `rm`/`rmdir` on critical paths, content-scoped ask rules like `Bash(git push *)`. A bare `Bash` ask rule is skipped for sandboxed commands (not in plan mode). Commands like `FOO=bar npm test` still prompt; allow with `Bash(FOO=bar npm *)`.
- **Regular permissions mode**: sandboxed commands go through explicit permission too; both modes enforce the same restrictions.
- Unsandboxed retry: in `bypassPermissions` it runs without a prompt; in Manual and `acceptEdits` you get a "Bash command (unsandboxed)" prompt; `dontAsk` denies it.

## Configuration (`settings.json`)
- `sandbox.filesystem.allowWrite`, e.g. `["~/.kube", "/tmp/build"]`; `denyWrite`, `denyRead`, `allowRead` — the narrower path wins when read rules overlap (`"denyRead": ["~/"]` with `"allowRead": ["."]` in project settings keeps the project readable). Arrays merge across settings scopes. Sandbox paths use `/tmp/build` absolute and `~/.kube` home-relative, unlike permission rules (`//path`).
- `sandbox.excludedCommands`, e.g. `["docker compose *"]`, runs matches with no filesystem restrictions and no network proxy.
- `network.allowedDomains` for outbound hosts.

## Protected paths
Even inside writable directories, writes are denied to `.claude` settings files, `.claude/skills`, `.claude/agents`, `.claude/commands`, `.claude/hooks`, `.mcp.json`, shell startup files such as `.bashrc` and `.zshrc`, `.gitconfig`, `hooks` and `config` inside `.git`, and most of `~/.claude` plus `~/.claude.json`. An `allowWrite` entry does not lift this; only `filesystem.disabled` does. See the **Config** tab of `/sandbox`.

Permissions and sandboxing are complementary layers: [[claude-code-settings-permissions]].

derived_from:: [[raw/claude-code/sandboxing.md]]
