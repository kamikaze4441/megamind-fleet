---
tags: [claude-code, memory, claude-md, auto-memory]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/claude-code/memory.md]
---
# Claude Code memory: CLAUDE.md and auto memory

Each session starts with a fresh context window. Two mechanisms carry knowledge across sessions, both loaded at the start of every conversation and treated as context, not enforced configuration (to block an action, use a PreToolUse hook — [[claude-code-hooks]]).

| | CLAUDE.md files | Auto memory |
|---|---|---|
| Who writes it | You | Claude |
| Scope | Project, user, or org | Per repository, shared across worktrees |
| Loaded | Every session | Every session (first 200 lines or 25KB) |

## CLAUDE.md locations (load order, broadest first)
- Managed policy: macOS `/Library/Application Support/ClaudeCode/CLAUDE.md`, Linux and WSL `/etc/claude-code/CLAUDE.md`, Windows `C:\Program Files\ClaudeCode\CLAUDE.md`.
- User: `~/.claude/CLAUDE.md`.
- Project: `./CLAUDE.md` or `./.claude/CLAUDE.md` (shared via source control).
- Local: `./CLAUDE.local.md` (add to `.gitignore`).
Files in the working directory and every directory above it load at launch and are concatenated (root first), not overridden; files in subdirectories load on demand when Claude touches files there. `/init` generates a starting CLAUDE.md. Target under 200 lines per file; a file over 4 MiB is skipped. Block-level HTML comments are stripped. `@path/to/import` imports files, relative to the importing file, maximum depth of four hops. `/doctor prompt-audit` checks instruction files for conflicts. With `--add-dir`, set `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` to load the added directory's CLAUDE.md.

## `.claude/rules/`
Markdown files in `.claude/rules/` (recursive) organise instructions by topic; rules without `paths` frontmatter load at launch with the same priority as `.claude/CLAUDE.md`, rules with `paths` load only when Claude works with matching files.

## Auto memory
Claude saves notes of four `type`s: `user`, `feedback`, `project`, `reference`; it skips what it can derive from the code or what CLAUDE.md already says. On by default in local sessions; toggle in `/memory` (saves `autoMemoryEnabled` to `~/.claude/settings.json`), per project `"autoMemoryEnabled": false`, or `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.
- Storage: `~/.claude/projects/<project>/memory/`, derived from the git repository, machine-local; override with `autoMemoryDirectory` (absolute path or `~/`).
- `MEMORY.md` is the index (one line per memory); the first 200 lines of `MEMORY.md`, or the first 25KB, whichever comes first, load at session start. Topic files such as `user_role.md` are read on demand.
- Not loaded into subagents, except a fork. Memory files are excluded from the `cleanupPeriodDays` transcript sweep.

Related: [[claude-code-skills-subagents]] (skills load only when used, unlike CLAUDE.md).

derived_from:: [[raw/claude-code/memory.md]]
