# (f) Chat history into the vault: claude.ai exports and Claude Code transcripts, and a converter spec
Question: how do claude.ai exports and Claude Code transcripts look, what do the terms allow to be automated, and how should a redacting, idempotent converter turn them into one dated Markdown file per chat plus an index? · Date read: 2026-11-02 · Researcher: R3 (megamind-researcher)

## Summary (10 lines max, each ending with [n])
1. You start a claude.ai export at Settings > Privacy > "Export data" on the web app or Claude Desktop (the mobile apps can't do it). A download link arrives by e-mail, only works while you are signed in, and expires after 24 hours [1].
2. The Help Center doesn't document the file layout. Pinned parsers read `conversations.json` (a list of conversations, each with `uuid`, `name`, `created_at`, `updated_at`, `account`, `chat_messages`) [11][12]. A community report from Oct 27, 2026 describes a newer export split into several zip parts [17].
3. Scripting the export itself is not allowed. The Consumer Terms forbid using the Services "through automated or non-human means, whether through a bot, script, or otherwise" except through an API key or with explicit permission, and I found no such permission for exports [2]. So the owner clicks "Export data" and downloads the file by hand; everything after that can be automated.
4. Claude Code stores transcripts at `~/.claude/projects/<project>/<session-id>.jsonl`. The docs say the format "is internal to Claude Code and changes between versions" and point scripts to `/export` and the script interfaces instead [4].
5. The Agent SDK documents `list_sessions()` and `get_session_messages()` for listing sessions on disk and reading their messages. They are the documented way to read transcripts [8][9].
6. Transcripts are deleted after `cleanupPeriodDays` (default 30, minimum 1, and `0` fails validation). Transcripts of sessions started or last continued in Claude Desktop are kept at any age unless `desktopSessionCleanupPeriodDays` is set [5][6].
7. Transcripts are plaintext. A credential a tool prints is written into the `.jsonl` [5], so redaction must run before anything reaches the vault.
8. The JSONL line types seen by a maintained parser are `user`, `assistant`, `summary`, `ai-title`, `system`, `queue-operation` and `attachment`. `file-history-snapshot`, `last-prompt`, `permission-mode`, `mode`, `custom-title`, `agent-name`, `agent-color` and `frame-link` are skipped. `tool_use`, `tool_result` and `thinking` are content blocks inside messages, not line types [13].
9. The graph-memory-starter's `turns()` keeps only main-thread user and assistant text, in order. It drops sub-agent (sidechain) lines, tool-result carriers, meta and compaction-summary lines, and harness-injected user events [16].
10. The converter spec below is a root-owned script run by T0's nightly job. It redacts in memory before any write, keys idempotency on chat id, adds no edges and escapes edge syntax found in chat text, and is tested only on synthetic fixtures [4][5][16].

## Findings

### 1. claude.ai data export
- **Who can export:** individual users on Free, Pro, Max and Ultra. On Team/Enterprise an Owner must turn on "Allow members to export their own data", and Primary Owners export the whole organization from Organization settings > Data and privacy instead [1].
- **Exact labels:** "Settings > Privacy" on the web app or Claude Desktop, then click "Export data". Exports can't be started from Claude for iOS or Android [1].
- **Delivery:** "There may be a small delay while the export is generated". The link goes to the account's e-mail address, needs you to be signed in, and expires 24 hours after delivery; a new export can be requested any time [1].
- **Time to deliver:** the official page says only "small delay" [1]. A community skill says it arrives "in about 5 minutes" [inferred from charlie947/ai-second-brain@6b14a52, SKILL.md L48–L49] [15].
- **Contents (official):** "conversation data and the user data for your account". On Team/Enterprise the export does not include the contents of uploaded files [1].
- **File names and layout (not documented officially):**
  - `simonw/claude-to-sqlite` opens a ZIP, requires a member named `conversations.json`, and fails otherwise [inferred from simonw/claude-to-sqlite@c64aac7, `claude_to_sqlite/cli.py` `parse_file`] [11]. Its README warns the file "may be missing the `.zip` extension" [11].
  - A community source names `conversations.json`, `users.json` and `projects.json` in the ZIP [community, evenfall.ai guide, updated Aug 4, 2026] [18].
  - A maintainer who received an export on 2026-10-27 reports a different layout. A manifest JSON lists six zip parts (`light_metadata`, `projects`, `memories`, `frames`, `claude_code_cloud`, `conversations`), `conversations-000.zip` holds `conversations.json`, and `projects-000.zip` holds one JSON per project [community, GitHub issue MHammett/content-intelligence#422, comment Oct 27, 2026] [17]. **The converter must accept both layouts.**
- **`conversations.json` structure (inferred):**
  - Top level: a JSON list of conversations [11][12].
  - Per conversation: `uuid`, `name`, `created_at`, `updated_at`, `account{uuid}`, `chat_messages[]` [inferred from jmorenobl/claude-conversation-extractor@919192c, `models.py` L53–L61] [12]. The Oct 2026 report adds `summary` [17].
  - Per message: `uuid`, `text`, `content[]`, `sender` ("human" or "assistant"), `created_at`, `updated_at`, `attachments[]`, `files[]` [12, `models.py` L40–L50]. The Oct 2026 report adds `parent_message_uuid` [17].
  - Content block: `type`, `text`, `start_timestamp`, `stop_timestamp`, `citations` [12, `models.py` L30–L37]. Tool-use blocks carry `name` and `input` [17].
  - Attachment/file object: `file_name`, `file_size`, `file_type`, `extracted_content` [12, `models.py` L21–L27].
- **Trap in the `text` field:** the flat `text` field substitutes a placeholder ("This block is not supported on your current device yet") wherever a message held a thinking block, tool call or tool result. The `content` array holds the real prose [community, evenfall.ai, Aug 4, 2026] [18]. **The converter reads `content` first and falls back to `text`.**
- **Project linkage:** "Conversations carry no project id"; project instructions and knowledge files are in the separate projects part [community, #422] [17]. Not verified officially.
- **Older artifact markup:** an Oct 2024 parser pulls artifacts out of `<antArtifact …>` tags inside assistant `text` [11, `cli.py` `extract_artifacts`]. Old exports may contain them.

### 2. Terms on automating the export
- The Consumer Terms (effective Oct 8, 2025, as shown on the page) say users may not access or use the Services "through automated or non-human means, whether through a bot, script, or otherwise", except via an Anthropic API Key "or where we otherwise explicitly permit it" [2].
- The same list bars crawling, scraping or otherwise harvesting data from the Services "other than as permitted under these Terms" [2].
- The Usage Policy (effective date shown: Nov 12, 2026) bars bypassing product restrictions and automating account creation. It has no clause specific to exports [3].
- **Verdict:** a script that clicks "Export data", fetches the e-mailed link or calls claude.ai's internal endpoints is automated access, and I found no explicit permission for it. Scripted export is **not permitted (verified from the text of the terms; no permission found)**. Converting a downloaded file on the VM does not touch the Services, and Claude Code transcripts are local files [2][4].
- Browser userscripts that read claude.ai's internal API exist [community]. They are the kind of automated access the terms bar and are out of scope.

### 3. Claude Code transcripts
- **Location:** JSONL at `~/.claude/projects/<project>/<session-id>.jsonl`, where `<project>` is the working-directory path with non-alphanumeric characters replaced by `-`. Names over 200 characters are truncated and a hash is appended [4].
- **What each line is:** a message, a tool use or result, a record of a request sent to the model, or a metadata entry. The format "is internal to Claude Code and changes between versions, so scripts that parse these files directly can break on any release" [4].
- **What a transcript holds:** messages, tool calls, tool results, and also the system prompt, tool definitions and request parameters [5].
- **Related files:**
  - Set-aside copies named `<session>.orphaned-<timestamp>-<suffix>.jsonl` and `<session>.jsonl.superseded-<timestamp>` don't appear in the picker [5].
  - `projects/<project>/<session>/subagents/` holds subagent transcripts in the same format, and `projects/<project>/<session>/tool-results/` holds large tool outputs that were spilled to separate files [5].
  - `sessions/` holds one small file per running session [5].
- **Retention:**
  - Transcripts are deleted after `cleanupPeriodDays` (default `30`, minimum `1`; `0` fails validation, and docs suggest `3650` for long retention). The sweep runs after a session starts and deletes without a message [6].
  - Desktop and Cowork transcripts are kept at any age unless `desktopSessionCleanupPeriodDays` is set (v2.1.248 or later). Managed settings that set `cleanupPeriodDays` override this [5].
- **Plaintext:** transcripts "are not encrypted at rest", and a credential a tool prints "is written to `projects/<project>/<session>.jsonl`" [5].
- **Resume:** `claude --resume <transcript-path>` resumes from a `.jsonl` at an absolute path [4]. `/export` writes a rendered plain-text transcript [4].
- **Documented script interfaces:**
  - `claude -p --output-format json|stream-json`; `claude -p --resume <id>`; the `transcript_path` field in hook and status-line input; the Agent SDK [4].
  - A `SessionEnd` hook "can archive the transcript when a session ends" [4]. SessionEnd hooks share a 1.5-second budget, raised to at most 60 s [7].
  - The transcript "is written asynchronously and may lag" [7].
- **Documented readers:**
  - Python `list_sessions(directory, limit, offset, include_worktrees)` returns `session_id`, `summary`, `last_modified`, `file_size`, `custom_title`, `first_prompt`, `git_branch`, `cwd`, `tag` and `created_at` [9].
  - `get_session_messages(session_id, directory, limit, offset)` returns `type` ("user"/"assistant"), `uuid`, `session_id`, `message` (raw content), `parent_tool_use_id` and `parent_agent_id` [9].
  - TypeScript has `listSessions()` and `getSessionMessages()` [8].
- **Line types (undocumented; inferred from daaain/claude-code-log@9834d25):**
  - Registry `ENTRY_CREATORS` = `user`, `assistant`, `summary`, `ai-title`, `system`, `queue-operation`, `attachment` (`factories/transcript_factory.py` L213–L221). Unknown types that carry `uuid` and `sessionId` pass through (L243–L253) [13].
  - Silently skipped types: `file-history-snapshot`, `last-prompt`, `permission-mode`, `mode`, `custom-title`, `agent-name`, `agent-color`, `frame-link` (`converter.py` L117–L134) [13].
  - Common fields: `parentUuid`, `isSidechain`, `userType`, `cwd`, `sessionId`, `version`, `uuid`, `timestamp`, `isMeta`, `agentId`, `gitBranch`. A `user` line may carry `toolUseResult`. `summary` lines have `summary` and `leafUuid`. `ai-title` lines have `aiTitle` (`models.py` L230–L311) [13].
  - Content blocks: user = `text`, `tool_result`, `image`; assistant = `text`, `tool_use`, `thinking` (`transcript_factory.py` L53–L54) [13].
- **A weaker parser:** ZeroSumQuant/claude-conversation-extractor@a12b72e treats `tool_use`, `tool_result` and `system` as top-level line types (`src/extract_claude_logs.py` L84–L150) [14]. That disagrees with [13]. **Plain statement: the line format is undocumented, and parsers disagree.**

### 4. The `turns()` filter idea (graph-memory-starter)
- Public description from the file's docstring: the code does the filtering, keeping "your words and the replies"; tool calls, results, file dumps, thinking and anything unrecognised are dropped [16, `digest/session_end.py` L1–L13].
- `turns(transcript)` in plain words: read the JSONL line by line, then skip a line when any of these holds:
  - it is malformed;
  - it is a sub-agent's own talk (`isSidechain`);
  - its type is not `user` or `assistant`;
  - it is a tool-result carrier (`toolUseResult`);
  - it is meta or a compaction summary;
  - its role is not user/assistant.
  - Of the remaining lines, keep only `text` blocks. From user text, strip `<system-reminder>` blocks and drop it if it starts with a harness-injected marker such as `<command-name>`, `<bash-stdout>`, `<task-notification>` or "[Request interrupted". Drop empty bodies.
  - The result is an ordered list of (You | Claude, text) pairs [16, L29–L113].
- **Licence:** MIT, so the idea can be borrowed. Copying the code would need the notice kept (HL 9).

## Design

### D1. Where it runs and who writes
| Item | Spec |
| --- | --- |
| Program | `/opt/megamind/bin/chat-convert` plus `/opt/megamind/chat-convert/{patterns.toml,tests/}`. Root-owned and outside every Claude-writable path (HL 3) |
| Trigger | T0's nightly run (05:30). It is never started by Claude and never by a hook in a Claude session |
| Runs as | root (or a dedicated system user) so it can read `/home/claude/.claude/projects/` and write the chat folder. Claude gets Read only: Edit/Write deny on `<chats>/**` and sandbox `denyWrite` (the folder name is set by R16; written `chats/` below) |
| Output owner | `chats/` is root-owned 0755 and files are 0644, so Claude can read but not write them (protection rests on the OS, §4). The exception to 99:100/2775 has to be settled with Syncthing write-back (see Could not verify) |
| Inputs | (a) the newest claude.ai export file that the owner drops by hand into the export inbox (D5); (b) `/home/claude/.claude/projects/*/*.jsonl` on the VM, skipping `*.orphaned-*`, `*.superseded-*` and `*/subagents/*` [5]; (c) <bench> transcripts are excluded (public-input bench, §3) |
| Live-session guard | Skip a transcript whose session has a file in `~/.claude/sessions/` (a running session [5]) or that changed in the last 60 minutes |
| Retention | Keep `cleanupPeriodDays` at 30. The nightly run converts well inside that window, so raw transcripts with plaintext secrets age out [5][6]. Set `desktopSessionCleanupPeriodDays: 30` so Code-tab transcripts don't live forever [6] |

### D2. Reading
| Source | Primary reader | Fallback |
| --- | --- | --- |
| claude.ai | Streaming JSON parse of `conversations.json`, found either at the ZIP root [11] or inside `conversations-*.zip` named by a manifest [17]. The file may lack a `.zip` extension [11] | None. An unknown layout stops the run (fail closed) and writes one line to `wiki/lint-inbox.md` |
| Claude Code | Agent SDK `list_sessions()` and `get_session_messages()` (documented [9]). Then apply `turns()` rules to each returned `message` | A raw JSONL reader guarded by a schema check: known types per [13], unknown types skipped and counted. If more than 5 % of lines are unknown, the run stops (fail closed) |

### D3. Output file
- **Name:** `chats/YYYY-MM-DD-<slug>.md`.
  - The date is `created` in America/Vancouver (the VM's zone, §3).
  - The slug comes from the title: ASCII-folded, lowercase, `[a-z0-9-]`, at most 60 characters. On a collision, append `-<first 8 of chat_id>`.
  - The name is fixed the first time a chat is seen. A later title change rewrites the frontmatter, not the file name.
- **Frontmatter:**
```yaml
---
source: claude.ai            # or claude-code
chat_id: <uuid or session-id>
created: 2026-10-25T09:38:55-07:00
updated: 2026-10-25T10:40:03-07:00
title: <redacted title>
message_count: <turns kept>
redacted: true
converter: chat-convert <version>
---
```
- **Title:**
  - claude.ai: `name`, or "Untitled" plus the first 8 characters of the id when empty [12].
  - Claude Code: `custom_title`, else `summary`, from `list_sessions()` [9]. The fallback is the first user prompt, cut to 80 characters.
- **Body:**
  - `# <title>`, then one `## You · HH:MM` or `## Claude · HH:MM` heading per kept turn, in source order.
  - Headings inside a turn are demoted two levels (capped at H6). Code fences are kept as written.
- **Kept per turn:** text blocks (claude.ai from `content[]` first, `text` only as fallback [18]; Claude Code per `turns()` [16]).
- **Dropped or summarized:**

| Block | Rule |
| --- | --- |
| thinking | dropped |
| tool_use | one line `> tool: <name>`. The input is shown only if it is 200 characters or fewer after redaction |
| tool_result / `toolUseResult` carrier | kept in a fenced block if it is N = 500 characters or fewer after redaction, else `> [tool result, <n> chars, dropped]` |
| attachments / files | `> attachment: <file_name> (<file_size> B)` only. `extracted_content` is dropped |
| sidechain / subagent lines, meta, compaction summary, injected harness events | dropped [16] |
| images | `> [image]` |

- **Edge neutralization:** chats carry no edges (§4, §7 rule 5). The converter escapes any `depends_on::`, `supersedes::` or `derived_from::` in chat text to `depends_on\::` (and likewise), and escapes every `[[` to `\[\[`. Markdown still renders the text as written, but neither `rg` for the field names, nor a backlink search for `[[page`, nor lint can match a chat line as an edge or a link. A body line that equals `## Superseded` is demoted to `#### Superseded (quoted)`.
- **Ending:** the last turn, then exactly one provenance block. Nothing else follows: no edges, no tags, no generated links.

### D4. Index
- **File:** `chats/index.md`, generated in full each run. It is never edited by hand and lives in the chat folder, not in the vault's `index.md`.
- **Content:** one table, newest first: `| date | title | file | source | summary |`.
- **How the summary is made:** the default is deterministic and costs zero quota.
  - claude.ai: the export's `summary` field if non-empty [17], else the first user turn.
  - Claude Code: the SDK `summary` [9], else the first user turn.
  - The summary is redacted and cut to 120 characters.
  - An option, as a proposal only: a B580 one-line summary. §7 rule 4 limits the B580 to tags and the two inbox files, so this needs the owner's amendment.
- **Vault index:** the vault `index.md` gets one Tooling line pointing at `chats/index.md`. That line is written by Claude in an interactive session (§7: `index.md` is never generated).

### D5. Provenance and the export inbox
- **The conflict:** the brief asks for `derived_from::` lines pointing at the export in `raw/`. But the export holds every chat unredacted, and §7 rule 6 says "No secrets in the vault … even in notes". An export in `raw/` puts any secret pasted into a chat into the vault, the Syncthing copy on the Mac and the off-site backup.
- **Option A, as briefed:** the owner saves the export to `raw/exports/claude-ai/YYYY-MM-DD-claude-export.zip`. Each claude.ai chat file ends with `derived_from:: raw/exports/claude-ai/YYYY-MM-DD-claude-export.zip#<chat_id> (sha256 <first 16>)`. This needs the owner to accept unredacted chats in `raw/`, which means an amendment to §7 rule 6.
- **Option B, recommended:** the owner saves the export to a root-owned inbox outside the vault (`/srv/megamind-inbox/claude-ai/`, mode 700, not synced). The converter appends to `chats/_sources.md` one line per export (date, file name, sha256, size). Each chat ends with `derived_from:: chats/_sources.md#<export-date> (chat <chat_id>, sha256 <first 16>)`. The inbox keeps the newest 3 exports. Whether it is backed up is the owner's choice.
- **Claude Code chats** end with `derived_from:: claude-code:~/.claude/projects/<project>/<session-id>.jsonl (sha256 <first 16>, read <date>; source ages out after cleanupPeriodDays)`.
- **Lint:** it must accept these two non-`raw/` provenance forms in `chats/` only. That is a lint rule change for R16.

### D6. Redaction (in memory, before any write)
- **Order:** read, filter, then redact title, every turn, every kept tool line and the summary. Then render, then the post-scan, then the atomic write: temp file in `chats/.tmp/`, `fsync`, rename. Logs record pattern names and counts only, never the matched text.
- **Pattern classes** (from `patterns.toml`; each replaced by `[REDACTED:<class>]`; no example values in the file or the tests' sources):

| Class | Rule (shape only) |
| --- | --- |
| api_key | Known vendor prefixes (Anthropic `sk-ant-`, generic `sk-`, GitHub `ghp_`/`gho_`/`github_pat_`, AWS `AKIA`, Google `AIza`, Slack `xox?-`) followed by a long token, plus long high-entropy strings next to the words key, token or secret |
| bearer | `Authorization:` header values; `Bearer <token>` anywhere |
| password | `password\|passwd\|pwd\|passphrase\|secret\|token\|api[_-]?key` followed by `:` or `=` and a value; `user:pass@` inside URLs; `?token=`/`&key=`/`access_token=` query values |
| cookie | `Cookie:` and `Set-Cookie:` header lines; `CF_Authorization` values |
| tailscale | `tskey-` followed by a token (Tailscale's key form [19]) |
| jwt / private_key | three base64url segments starting `eyJ`; `-----BEGIN … PRIVATE KEY-----` blocks |
| email | RFC-5322-ish address |
| ipv4 / ipv6 | **Optional, default ON once a connector can read `chats/`** (see h-reachability.md). §7 rule 6 allows IPs in the vault, but a remote read path changes that |
| keep_out | every line of the owner's word list, matched case-insensitively as literal strings |

- **Keep-out list outside the vault:** `/etc/megamind/keep-out.txt` on the VM, root:root 0600, read only by the converter. It is the VM twin of the Mac's `~/.config/megamind/keep-out.txt` (§2 Terms). Rules:
  - one entry per line;
  - the converter refuses to start if the file has a blank line, because a blank pattern matches everything (same rule as §2), or if the file is missing, group- or world-readable, or inside the vault;
  - the list is never echoed into logs.
- **Fail closed:** after rendering, the same patterns run on the output. Any hit means the file goes to `chats/.quarantine/` (root-only 0700, not synced), is not written to `chats/`, and gets one line in `wiki/lint-inbox.md` with the chat id and class name.

### D7. Idempotency
- **Manifest:** `chats/.state/manifest.tsv`, root-only. Columns: `source  chat_id  file  source_updated  body_sha256  converter_version  status`.
- **Per chat:**
  - New `(source, chat_id)`: create the file.
  - Known chat with a newer `source_updated` or a changed `body_sha256`: rewrite the same file.
  - Unchanged: no write.
- **Never duplicates:** the key is the id, not the file name or the title.
- **Absent chats:** a chat missing from a newer export (deleted, or a date-limited export) or a transcript that aged out is never deleted. Its status becomes `absent-since-<date>`, and only the owner deletes.
- **Tamper check:** if a file's hash differs from `body_sha256` while the source hasn't changed, someone edited it (for example Syncthing write-back from the Mac). The converter rewrites it and logs one lint line.
- **A converter version bump** re-renders everything once, in one commit.
- **Git:** a run ends with one local commit, e.g. `chats: +3 new, 2 updated (export 2026-11-01)`, and one `log.md` line: `## [YYYY-MM-DD] housekeeping | chat-convert`.

### D8. Testing (synthetic data only; no real chats exist here or are ever used as fixtures)
| Test | Fixture | Pass |
| --- | --- | --- |
| Golden render | 3 synthetic claude.ai chats: plain; tool_use/tool_result/thinking plus placeholder `text`; attachments with `extracted_content`. 1 synthetic export in each layout [11][17] | Output equals the stored golden files byte for byte |
| JSONL coverage | Synthetic `.jsonl` with each type in [13], a sidechain line, an `isMeta` line, a `toolUseResult` carrier, an injected `<command-name>` user line, an unknown type, a malformed line | Only main-thread user/assistant text appears. Counts are reported. More than 5 % unknown lines stops the run |
| Redaction | Every class built at test run time from the pattern definitions (never stored as literals), plus a random canary string in the keep-out list | Zero matches in `chats/`, logs or manifest. The canary is found only in quarantine when the post-scan is forced to fail |
| Keep-out guards | Blank line; mode 0644; file inside the vault | Converter refuses to start, exit code is non-zero |
| Idempotency | Run twice | Second run: zero writes, manifest unchanged, no commit |
| Update | Change one message and bump `updated_at` | The same file is rewritten. File count unchanged |
| Absence | Drop one chat from the export | File kept, manifest status `absent-since-…` |
| Edge neutralization | Chat text containing `depends_on:: [[x]] (y)` and `## Superseded` | `rg 'depends_on::' chats/` and `rg '\[\[x' chats/` return nothing outside the provenance block, and the vault lint sees no edge |
| Live guard | Transcript with a matching `~/.claude/sessions/` file | Skipped |
| Fail closed | Unknown export layout | No writes, one lint line |

- **Where tests run:** `/opt/megamind/chat-convert/tests/` against a temporary directory. They are part of the guard tests run before T0 enables the converter, and never run against the live vault.

## Repositories pinned
| repo | HEAD SHA | commit date | licence file, first line | what was read |
| --- | --- | --- | --- | --- |
| charlie947/ai-second-brain | 6b14a5282f3fe1cbb6beb45b7a9444adcc0f84ab | 2026-10-24 | "MIT License" | README L13–L36: install by `git clone https://github.com/charlie947/ai-second-brain.git ~/.claude/skills/ai-second-brain`; SKILL.md L41–L83. **It has no parser**: it asks Claude to "Convert all my ChatGPT and Claude conversations into individual markdown files" (L83) |
| simonw/claude-to-sqlite | c64aac7dce3c6f206e699c9c7dfe71d9f25829b7 | 2024-10-20 | "Apache License" | README install `pip install claude-to-sqlite`, schema; `claude_to_sqlite/cli.py` (`parse_file`, `extract_artifacts`) |
| jmorenobl/claude-conversation-extractor | 919192c751dbdc935364741662d381bfb7065937 | 2025-08-13 | "MIT License" | `src/claude_conversation_extractor/models.py` L5–L64 |
| daaain/claude-code-log | 9834d25c88dc4dbe8f8ade40ae4b74602ae7669d | 2026-10-09 | "MIT License" | README install `uv tool install claude-code-log` / `pip install claude-code-log`; `factories/transcript_factory.py` L53–L54, L211–L254; `models.py` L230–L311; `converter.py` L110–L135 |
| ZeroSumQuant/claude-conversation-extractor | a12b72e3be2e23d4ed1956fd67a09472b311e783 | 2025-09-15 | "MIT License" | `src/extract_claude_logs.py` L73–L150 (top-level type handling) |
| Glitch-Cat-Club/graph-memory-starter | 496a6e9d9b9578943ec5ed34c2780de5a0fa5510 | 2026-08-30 | "MIT License" | `digest/session_end.py` L1–L135 (`turns()`, `text_blocks()`, `INJECTED`) |

Nothing in these clones was executed or installed.

## Could not verify
- **Official export layout:** file names and JSON keys. The Help Center is silent [1]. Two community layouts differ [17][18]. Whether the current export is one ZIP or a manifest of parts depends on account or date and is not settled.
- **Official time to deliver:** only "small delay" [1].
- **Project linkage** inside `conversations.json`: community says there is none [17]. Not verified officially.
- **Whether the export's `claude_code_cloud` part** holds Claude Code cloud-session transcripts [17]. If it does, the converter needs a third source type.
- **Agent SDK footprint:** whether `list_sessions()`/`get_session_messages()` need the Claude Code CLI or credentials at runtime, and what installing the Python SDK on the VM adds. The docs only say they are synchronous [9].
- **Code-tab SSH transcript location:** where Desktop's Code-tab SSH sessions write transcripts on the VM (the `~/.claude/projects/` of the remote user is assumed). Not stated on the pages read.
- **Syncthing write-back:** how Syncthing treats a root-owned `chats/` inside a folder synced as 99:100 with "Ignore Permissions". Write-back from the Mac is possible. R16 has to settle it, or `chats/` moves to a send-only arrangement.
- **Whether Anthropic regards a scripted download** of the e-mailed link as permitted. The terms' text bars automated access without explicit permission [2]. No Help Center page grants it.

## Relevance to MEGAMIND
- **§4 Vault and wiki, chat-history bullet** ("automated as far as the terms allow"): export request and download stay manual (Consumer Terms [2]). Conversion, redaction, index and commit are automated in T0.
- **§7 table, chat-history row** ("T0's converter, not Claude"): confirmed. Add root ownership of `chats/` with Claude Read-only, and the manifest, `_sources.md`, quarantine and `index.md` inside it.
- **§7 rule 6 (no secrets in the vault)** versus "export in `raw/`": D5 option B keeps the unredacted export out of the vault. If the owner prefers option A, rule 6 needs a written exception. Goes to `06-amendments.md`.
- **§7 rule 7 (lint):** accept `chats/_sources.md` and `claude-code:` provenance in `chats/` only, and lint `chats/` for edge syntax (D3).
- **§5a friction log line** ("Transcripts … undocumented format"): update to "format internal and version-dependent; read through Agent SDK `list_sessions()`/`get_session_messages()`" [4][9].
- **§4 Claude Code harness / P6 settings:** add `cleanupPeriodDays: 30` and `desktopSessionCleanupPeriodDays: 30` explicitly [5][6].
- **R16 row** ("borrows the starter's `turns()` filter idea"): the idea is described in Finding 4. It is MIT, so code can be copied with the notice kept (HL 9).
- **§2 Terms, keep-out list:** a VM twin `/etc/megamind/keep-out.txt` (root 0600) is needed for the converter. The Mac copy stays the source; the owner copies it by hand.

## Sources
[1] https://support.claude.com/en/articles/9450526-export-your-claude-data — read 2026-11-02
[2] https://www.anthropic.com/legal/consumer-terms (page shows "Effective Oct 8, 2025") — read 2026-11-02
[3] https://www.anthropic.com/legal/aup (page shows "Effective Nov 12, 2026") — read 2026-11-02
[4] https://code.claude.com/docs/en/sessions.md (sections "Export and locate session data", "Where transcripts are stored") — read 2026-11-02
[5] https://code.claude.com/docs/en/claude-directory.md ("Cleaned up automatically", "Plaintext storage") — read 2026-11-02
[6] https://code.claude.com/docs/en/settings-reference.md (`cleanupPeriodDays`, `desktopSessionCleanupPeriodDays`) — read 2026-11-02
[7] https://code.claude.com/docs/en/hooks.md (`transcript_path`, SessionEnd budget) — read 2026-11-02
[8] https://code.claude.com/docs/en/agent-sdk/sessions.md — read 2026-11-02
[9] https://code.claude.com/docs/en/agent-sdk/python.md (`list_sessions`, `get_session_messages`) — read 2026-11-02
[10] https://code.claude.com/docs/llms.txt (index used to find [4]–[9]) — read 2026-11-02
[11] https://github.com/simonw/claude-to-sqlite @ c64aac7 (2024-10-20, Apache-2.0) — read 2026-11-02
[12] https://github.com/jmorenobl/claude-conversation-extractor @ 919192c (2025-08-13, MIT) — read 2026-11-02
[13] https://github.com/daaain/claude-code-log @ 9834d25 (2026-10-09, MIT) — read 2026-11-02
[14] https://github.com/ZeroSumQuant/claude-conversation-extractor @ a12b72e (2025-09-15, MIT) — read 2026-11-02
[15] https://github.com/charlie947/ai-second-brain @ 6b14a52 (2026-10-24, MIT) — read 2026-11-02
[16] https://github.com/Glitch-Cat-Club/graph-memory-starter @ 496a6e9 (2026-08-30, MIT), `digest/session_end.py` — read 2026-11-02
[17] https://github.com/MHammett/content-intelligence/issues/422 [community; issue opened Oct 27, 2026; maintainer comment Oct 27, 2026; no score shown] — read 2026-11-02
[18] https://www.evenfall.ai/guides/export-claude-conversations [community; "updated August 4, 2026"] — read 2026-11-02
[19] https://tailscale.com/kb/1085/auth-keys (key shown as `tskey-…`) — read 2026-11-02
