# (g3) Verification sweep of single-source claims
Question: For draft claims A–I that rest on one source, does a second independent source confirm, contradict or refine them? · Date: 2026-11-02 · Researcher: R6 (argon-researcher)

## Summary (10 lines max)
1. A **refined**: an Anthropic maintainer confirms that request headers are a beta for a limited set of orgs (claude-ai-mcp #10, 2026-10-18). The Help Center steps for Pro/Max list "Request headers" with no beta note. Connectors added on the web reach every client, plus terminal Claude Code under a claude.ai login.
2. B **refined**: Cloudflare's Managed OAuth is documented (page updated 2026-07-01) and runs on the Zero Trust Free plan. Some setups work with claude.ai (nas-mcp-server, getsentry/plausible-mcp). Others failed: claude-ai-mcp #410 (closed "not planned", no root cause) and #315. Hard requirements: the Access app covers the bare host, MCP sits at the root `/mcp`, the claude.ai/claude.com callbacks are allowlisted, and Bot Fight Mode is skipped. A live test is still required.
3. C **confirmed** in both the 2025-06-18 and 2026-07-28 specs: no tokens in the query string, `Authorization: Bearer` header required, RFC 8707 `resource` required in authorization and token requests.
4. D **confirmed** for `claude mcp add`/`headersHelper`. **Contradicted** for the Desktop sub-question: in Desktop local/SSH sessions, neither `disableClaudeAiConnectors`, `deniedMcpServers` nor `permissions.deny` removes injected connectors (docs plus five open GitHub issues).
5. E **refined**: menu path and 24-hour link confirmed. Current exports come as several ZIP parts with a manifest (7 parts in one Oct 30 report), and memory is in its own part. The Consumer Terms clause on scripts is confirmed. One maintained parser (caitx) reads multi-part exports.
6. F **confirmed and refined**: the docs call the format internal. The line types are seen by four more sources. The cleanup sweep goes by file mtime. `getSessionMessages` returns only the chain after compaction.
7. G **confirmed**, with one refinement: a June 2026 third-party guide quoted "jitter up to 10 s", while current docs say 15% (5 s–9 min). Re-check before deploying.
8. H **confirmed** by docs plus 3+ third-party guides. For dreams, the docs show only an explicit `POST /v1/dreams`; one directory site calls dreaming "scheduled" (not verified).
9. I **confirmed and refined**: npm latest is 2.8.3 (2026-08-16), the HTTP server is unauthenticated, and `qmd bench` = precision@k/recall/MRR/F1 across 4 backends. Models total ≈2 GB. On CPU, embedding takes ≈30 min per 1.4k docs, and runs can crash mid-way yet exit 0 (#935).
10. Argon: two jobs completed. The third (G/H/I) was refused on turn 3 with Gemini HTTP 402 "prepayment credits are depleted" (spend was not at the daily cap), so G/H/I rest on my own web tools.

## Claims A–I

### A. claude.ai custom connectors: request headers beta; reach of web-added connectors — **refined**
- **Beta, limited orgs: confirmed by an independent maintainer statement.** anthropics/claude-ai-mcp issue #10 "Support custom headers for connectors" (opened 2026-01-02, still open). Maintainer localden, 2026-10-18: request headers work with "No sign-in", using `authorization`/`x-api-key`/`x-auth-token`, up to four headers, one shared credential, and the feature "is in beta for a limited set of organizations". https://github.com/anthropics/claude-ai-mcp/issues/10 [verified]
- **Refinement:** the Help Center article "Get started with custom connectors using remote MCP" ("Updated this week") lists "Under Request headers, add fixed credentials…" in both the Team/Enterprise steps and the Pro/Max steps, with no beta note. The beta note appears only in claude.com/docs. Treat the feature as unavailable unless the dialog actually shows it. https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp [verified]
- **Reach to all clients: confirmed.** The same Help Center page says Claude connects from Anthropic's cloud "across every Claude client, including claude.ai, Claude Desktop, Cowork, and the mobile apps". It adds that Desktop remote connectors are "configured and brokered through your Claude account". [verified]
- **Claude Code terminal under a claude.ai login: confirmed.**
  - code.claude.com/docs/en/mcp "Use MCP servers from claude.ai" says connectors are fetched only when the active auth is a claude.ai subscription login; an API key or `apiKeyHelper` turns them off. https://code.claude.com/docs/en/mcp.md [verified]
  - Independent: anthropics/claude-code #105840 (2026-10-29, open) reports that logging in loaded "every claude.ai connector on the account… 133 tools". https://github.com/anthropics/claude-code/issues/105840 [verified, community]
  - Independent: #58453 (2026-05-12, closed) reports that claude.ai connectors "auto-load into every Claude Code session". https://github.com/anthropics/claude-code/issues/58453 [verified, community]
- Argon agrees (job dd7a19f4) and cites the same docs plus #10. [Argon, not verified beyond the items above]

### B. Cloudflare Access Managed OAuth with claude.ai's connector OAuth client — **refined** (exists, Free plan, works for some, documented failures; live test needed)
- **Docs page:** "Managed OAuth", https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/managed-oauth/ (last updated 2026-07-01). [verified]
  - Turns Access into an OAuth 2.0 authorization server for a self-hosted app, MCP server app or MCP portal.
  - Requires "an OAuth client that supports RFC 8707".
  - DCR settings: Allow localhost/loopback clients and "Allowed redirect URIs" (https only).
  - Issues opaque tokens and forwards `Cf-Access-Jwt-Assertion` to the origin.
  - Documents DCR only. Client ID Metadata Documents (CIMD) are not mentioned, so on claude.ai use the "Register automatically" OAuth-client option.
- **Changelog (independent date):** "Managed OAuth for Cloudflare Access", 2026-03-20: opt-in for self-hosted apps, on by default for new MCP portals. https://developers.cloudflare.com/changelog/post/2026-03-20-managed-oauth/ (search result)
- **Free plan: confirmed by user reports.**
  - claude-ai-mcp #410: two reproductions name "Zero Trust Free plan" with Managed OAuth on (comments 2026-06, 2026-06-21). [verified]
  - Githubtezla/nas-mcp-server README: "Cloudflare Zero Trust (the free plan covers a personal setup)". https://github.com/Githubtezla/nas-mcp-server [verified, community]
  - The Managed OAuth page carries no plan restriction; only the MCP portal Logpush export is Enterprise-only.
- **Working with claude.ai:**
  - nas-mcp-server README: Cloudflare Tunnel + Access with managed OAuth, used as a custom connector "in Claude (web, desktop and mobile)", with redirect URIs `https://claude.ai/api/mcp/auth_callback` and `https://claude.com/api/mcp/auth_callback`. [verified, community; repo date not read]
  - getsentry/plausible-mcp README:
    - Allowlist the claude.ai callback, or DCR fails with `invalid_client_metadata: redirect_uri is not allowed by the account configuration`.
    - Loopback callbacks are allowed by default.
    - With Managed OAuth on, Cloudflare rejects a path on the app: "domain can not have a path if oauth is configured".
    - https://raw.githubusercontent.com/getsentry/plausible-mcp/main/README.md [verified, community]
  - Reddit r/ClaudeCode post by u/telsaton (2026-10-27, 8 points, 9 comments) about the NAS setup. https://www.reddit.com/r/ClaudeCode/comments/1xfupmb/ [Argon, not verified, community]
- **Failing with claude.ai:**
  - anthropics/claude-ai-mcp #410 "claude.ai web + mobile connector OAuth fails against Cloudflare Access 'Managed OAuth' MCP portal — Claude Code connects to the identical URL". Opened 2026-06-07, closed as NOT_PLANNED, no root cause given. [verified, community]
    - Comment 2026-06-21 (Zero Trust Free, self-hosted app): Cloudflare's `/authorize` returns `invalid_target … No resource parameter found` unless the RFC 8707 `resource` is sent.
    - The same comment notes the protected-resource metadata lists `cloudflared` before `oauth`, which can send the popup to the browser-login path.
    - https://github.com/anthropics/claude-ai-mcp/issues/410
  - claude-ai-mcp #315 (opened 2026-05-19, closed). https://github.com/anthropics/claude-ai-mcp/issues/315 [verified, community]
    - art804: with Managed OAuth, an MCP endpoint at path depth >1 failed and the same config at the root `/mcp` worked.
    - sredka (2026-07-31): Super Bot Fight Mode blocked Anthropic's egress range 160.79.104.0/21 after OAuth succeeded. The fix was a WAF custom rule that skips the MCP path.
  - claude-ai-mcp #572 (2026-07-07, closed 07-18 as duplicate of #476). Through a Cloudflare MCP portal, OAuth/DCR and `tools/list` succeeded, but tools were not injected into claude.ai chats; they worked through Claude Code. It recovered on 2026-07-10 with no server change. https://github.com/anthropics/claude-ai-mcp/issues/572 [verified, community]
- **MCP Inspector:** Argon reports modelcontextprotocol/inspector #1802 (2026-07-27). Its Connect button runs discovery against Inspector's own proxy; use "Quick OAuth Flow" (callback `/oauth/callback/debug`) and allow localhost clients. [Argon, not verified]

### C. MCP authorization spec: no query-string tokens, Bearer header, RFC 8707 — **confirmed**
- 2025-06-18 version: "MCP client MUST use the Authorization request header field… `Authorization: Bearer <access-token>`" and "Access tokens MUST NOT be included in the URI query string". "MCP clients MUST implement Resource Indicators… RFC 8707… The resource parameter: MUST be included in both authorization requests and token requests." https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization [verified]
- 2026-07-28 version (the target of `/specification/latest/`): the same three MUST/MUST NOT rules, word for word. https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization [verified]
- Practical tie-in: Cloudflare's endpoint enforces the `resource` requirement and fails without it (claude-ai-mcp #410 above).

### D. Claude Code `--header`/`headersHelper`; disabling Desktop-injected connectors — **confirmed** (CLI part) / **contradicted** (Desktop sub-question)
- **CLI part:** code.claude.com/docs/en/mcp documents `headers` and `headersHelper` for `http`/`sse`/`ws` servers. A `headersHelper` that is the only source of `Authorization` is re-run on retry. https://code.claude.com/docs/en/mcp.md [verified]
  - Argon cites the same page and the MCP quickstart for `--scope user` writing to the `mcpServers` key in `~/.claude.json`. It adds that the helper must print a JSON object of string headers, with a 10 s timeout. [Argon, not verified for the timeout]
  - No independent community source found for the `~/.claude.json` location (the docs are the only source).
- **Desktop sub-question:** docs, "How connectors reach Claude Code" (same page). [verified]
  - Desktop local and SSH sessions get connectors "in-process" as `type: "sdk"` servers, and "no MCP setting or managed-mcp.json reaches them".
  - `disableClaudeAiConnectors`, `ENABLE_CLAUDEAI_MCP_SERVERS` and `allowAllClaudeAiMcps` act only on connectors the CLI fetches itself.
  - Options: a user disconnects the connector at claude.ai/customize/connectors; an org sets tools to `blocked`.
  - For those tools the Desktop app applies "the session's ordinary permission rules".
- **Users report deny rules don't help (all anthropics/claude-code, all open):** [verified, community]
  - #104956 (2026-10-25): `permissions.deny` for `mcp__<uuid>__*` in settings.local.json, and "The desktop app still exposes those tools". A deny rule for a plugin server does work. https://github.com/anthropics/claude-code/issues/104956
  - #92787 (2026-09-08, marked duplicate): in Desktop, connectors mount under connection UUIDs, so `mcp__claude_ai_<name>__*` rules never match. https://github.com/anthropics/claude-code/issues/92787
  - #106481 (2026-11-01): a project's `disableClaudeAiConnectors: true` has no effect in the Desktop Code tab. https://github.com/anthropics/claude-code/issues/106481
  - #93722 (2026-09-11): `deniedMcpServers` cannot suppress connectors injected by the app.
  - #102996 (2026-10-17): the Desktop connector switch is account-wide.
- **Extra risk:** #94887 (2026-09-16, open) says that in Desktop SSH sessions, connector tools run inside the Desktop app itself. With the laptop asleep, connector calls hang even though the remote CLI is alive. https://github.com/anthropics/claude-code/issues/94887 [verified, community]

### E. claude.ai data export — **refined**
- **Menu path, delivery, 24 h: confirmed.** Help Center "Export your Claude data": "Go to Settings > Privacy. Click 'Export data'… download link via email… The download link will expire 24 hours after delivery". Not available on iOS/Android. https://support.claude.com/en/articles/9450526-export-your-claude-data [verified] (Same wording on the org-export article 13346720, search result.)
- **Multi-part ZIP in 2026: confirmed by two independent sources beyond the draft's.**
  - ModelBrain, "How to Export Claude Conversations, and What the Seven Files Hold" (Matthew Firth, 2026-10-30). https://modelbrain.net/articles/how-to-export-claude-conversations.html [verified]
    - "Our real export came as seven zip parts… listed in one manifest."
    - The conversations part held 272 conversations / 20,089 messages (88 MB zipped, 452 MB unpacked).
    - Memory sits in a separate part (`account_uuid`, `conversations_memory`, `memory_files`).
    - The links expired before every part was fetched.
  - alexgs/claude-ai-transcript-export (caitx) README, "On schema drift": "The export format is undocumented and has already changed at least once: a single zip became a directory of parts". https://github.com/alexgs/claude-ai-transcript-export [verified, community]
- **Keys:** a converter guide confirms `conversations.json` = array of conversations with an id, name, created/updated timestamps and `chat_messages` (sender human/assistant, text, created timestamp). https://ai-chat-importer.com/blog/how-to-export-claude-conversations (search result, not opened)
  - Argon adds `summary`, `account`, `parent_message_uuid`, `attachments` (with `extracted_content`) and `files`. It says `content[]` carries `thinking`/`tool_use`/`tool_result` blocks (~88–92 % of bytes). [Argon, not verified]
- **Consumer Terms (effective Oct 8, 2025): confirmed.** The terms bar access "through automated or non-human means, whether through a bot, script, or otherwise" except with an API key or explicit permission. https://www.anthropic.com/legal/consumer-terms [verified]. The export click and download stay manual.
- **Parsers handling the current format:**
  - alexgs/claude-ai-transcript-export accepts "the export directory as downloaded, one of its zips, or a bare conversations.json", has `caitx probe` for schema drift, and needs Node 22. [verified]
  - temnoon/openai_export_parser auto-detects Claude exports, but its README describes the older single-zip layout (conversations/projects/users.json). (search result)
  - osteele/claude-chat-viewer reads the ZIP directly (search result).
  - Argon also lists MarioPadilla/claude-vault (2026-10-12), olearydj/claude-json-to-markdown and others. [Argon, not verified]

### F. Claude Code transcripts — **confirmed, refined**
- **Internal format:** code.claude.com/docs/en/sessions: "The entry format is internal to Claude Code and changes between versions, so scripts that parse these files directly can break on any release." https://code.claude.com/docs/en/sessions.md [verified]
- **Line types (independent sources):**
  - anthropics/claude-code #53516 (Argon: 2026-04-26, closed not planned 2026-09-16) lists agent-name, assistant, attachment, custom-title, file-history-snapshot, last-prompt, permission-mode, queue-operation, system, user. `system` subtypes include compact_boundary, scheduled_task_fire and others. https://github.com/anthropics/claude-code/issues/53516 (search result; dates per Argon)
  - Elixir SDK `ClaudeCode.History` docs: user, assistant, system, summary, file-history-snapshot, queue-operation. https://hexdocs.pm/claude_code/ClaudeCode.History.html (search result)
  - ccassist.dev (docs read 2026-10-01): attachment, system, mode, last-prompt, queue-operation, file-history-snapshot, file-history-delta. https://ccassist.dev/blog/where-claude-code-stores-conversations/ (search result)
  - Argon adds #47089 and dxdev.com, with `ai-title` and `summary`. [Argon, not verified]
- **`cleanupPeriodDays`: confirmed.** settings-reference: default `30`, minimum `1`; a background sweep after session start deletes silently. https://code.claude.com/docs/en/settings-reference.md [verified]
  - Refinement: the sweep deletes `*.jsonl` by file `stat.mtime`. anthropics/claude-code #59248 (2026-05-14, open). [verified date/title; mtime detail per Argon]
  - #45735 (2026-04-09, fixed): `--setting-sources local` ignored the setting. [verified date/title]
- **`desktopSessionCleanupPeriodDays`: confirmed.** Without the key, Desktop/Cowork transcripts are kept "at any age". Deletion needs the transcript to be older than both this limit and `cleanupPeriodDays`. Requires v2.1.248+. [verified]
  - Argon adds that archiving a session in Desktop releases it to the normal sweep. [Argon, not verified]
- **SDK readers: confirmed, refined.** agent-sdk/sessions documents `listSessions()`/`getSessionMessages()` (TS) and `list_sessions()`/`get_session_messages()` (Python). [verified]
  - agent-sdk/session-storage: "`getSessionMessages` returns the post-compaction chain… a session whose store holds 503 raw entries may return 18 messages". The full raw history needs `store.load(key)`. https://code.claude.com/docs/en/agent-sdk/session-storage.md [verified; that page states this for the session-store variant]
  - Argon cites claude-agent-sdk-python #1411/#1439 (Oct 2026) for the same behaviour on disk. [Argon, not verified]
- **Community:** Reddit r/ClaudeAI post by u/jomi-se (2026-07-26, score 67, 71 comments) on silent 30-day deletion. https://www.reddit.com/r/ClaudeAI/comments/1v646sa/ [Argon, not verified, community]

### G. Managed Agents scheduled deployments — **confirmed** (jitter value changed since launch)
- **Docs re-read 2026-11-02:** https://platform.claude.com/docs/en/managed-agents/scheduled-deployments.md (L263–276, L664) [verified]
  - Jitter: "up to 15 percent of the interval… minimum of 5 seconds and a maximum of 9 minutes".
  - Limit: "maximum of 1,000 scheduled deployments… for each organization".
  - DST: skipped spring-forward times "are not triggered"; repeated fall-back times "fire twice".
  - Pause: "Missed triggers are not backfilled".
  - Budget: copied onto each session, so `"2000"` ≈ $20 on every run.
- **Budget units:** budgets.md L167: `amount` "is a whole number of US cents written as a string" ("125" = $1.25); decimals are rejected. https://platform.claude.com/docs/en/managed-agents/budgets.md [verified]
- **API reference (independent page):** "5-field POSIX cron… Day-of-week is 0-7… L, W, #, and ? is not supported, nor are predefined shortcuts (@daily)"; "IANA timezone identifier". It adds that each fire "is offset by a small per-schedule jitter, so a run will actually start at or shortly after its listed time". https://platform.claude.com/docs/en/api/typescript/beta/deployments (search result)
- **Third parties:**
  - getclaudeskills.com guide repeats 15 % / 5 s floor / 9 min ceiling and the DST duplicate-or-gap behaviour (search result).
  - rickhigh.substack.com: "hard ceiling of 1,000 deployments" (search result).
  - **Refinement:** developersdigest.tech (2026-06-11), reading the docs at launch, wrote "Jitter of up to 10 seconds may apply". The documented jitter has since changed, so re-check before relying on a tight time window. https://www.developersdigest.tech/blog/claude-code-routines-vs-managed-agents-schedules [verified]
- **`ant apply` format:** docs search snippet shows a deployment file with YAML frontmatter (`schedule: {type: cron, expression, timezone}`, `budget`). "In a deployment file for ant apply, the text below the frontmatter becomes that user.message." (search result of the docs page; no independent source)
- **In practice:** anthropics/claude-cookbooks #830 (2026-08-14, open): memory store not mounted in deployment-created sessions (verified by R4, see memory). No Reddit reports found in this sweep (the Argon turn for G was lost).

### H. Managed Agents pricing, memory limits, ZDR, dreams — **confirmed** (dreams trigger: docs only)
- **Pricing:** tokens + $0.08 per running session-hour.
  - claude.com product page: "Anthropic charges token rates plus $0.08 for each hour a session runs"; "not currently HIPAA eligible". https://claude.com/platform/claude-managed-agents (search result)
  - Independent guides agree: therundown.ai, imisofts (2026-10-12), truefoundry, verdent. (search results)
- **Memory limits:** docs memory.md L246/L407/L948 [verified]: 100 kB per memory, 10,000 memories per store, max 8 stores per session, versions kept 30 days (recent versions of a live memory always kept).
  - Independent: aicodex.to ("Up to 8 memory stores… Version history is retained for 30 days"), rickhigh.substack (8 stores, 100 kB), nerdleveltech (10,000 ceiling). (search results)
  - Refinement: buildfastwithai (April 2026) said there was no documented limit on file count. The 10,000 cap appeared later.
- **ZDR:** dreams.md frontmatter `zdr: eligibility: not-eligible`, "Applies to all Managed Agents sub-features". memory.md data-handling table: "Not eligible". [verified]
  - Independent: agent37.com: "not eligible for Zero Data Retention or a HIPAA BAA". (search result)
- **Dreams:**
  - Status "research-preview", request access, beta header `dreaming-2026-04-21`. The only start path documented is `POST /v1/dreams` ("Create a dream"); no automatic or scheduled trigger appears in dreams.md. [verified]
  - agent37 also calls dreams a "request-access preview". (search result)
  - Refinement: therundown.ai calls dreaming "a scheduled research-preview process". No doc support found; treat as unverified wording.

### I. qmd (tobi/qmd) — **confirmed, refined**
- **Version:** npm registry `@tobilu/qmd` dist-tag latest = 2.8.3, published 2026-08-16T22:30Z. https://registry.npmjs.org/@tobilu/qmd [verified]
- **HTTP auth:** README: "remember the endpoints are unauthenticated — put your own auth in front of a server that is reachable off-host". https://raw.githubusercontent.com/tobi/qmd/main/README.md [verified]
- **`qmd bench`:** README "Benchmarking". [verified]
  - Takes a fixture JSON of queries with `expected_files`.
  - Runs each query on `bm25`, `vector`, `hybrid`, `full` (rerank) and reports precision@k, recall, MRR and F1.
  - The example fixture lives only in a git checkout. With npm, write your own and run `qmd bench my.json -c <collection>`.
  - Gotcha: an unindexed collection "reports all zeros with no warning".
- **Model sizes:** README: `embeddinggemma-300M-Q8_0` ~300 MB, `qwen3-reranker-0.6b-q8_0` ~640 MB, `qmd-query-expansion-1.7B-q4_k_m` ~1.1 GB, so ≈2 GB downloaded on first use. [verified]
- **CPU build time and failures (tobi/qmd issues):** [verified dates/states, community]
  - #957 (2026-09-15, open): CPU-only `--no-gpu`, "Embedded 5888 chunks from 1442 documents in 30m 6s" (8 CPU cores).
  - #935 (2026-08-30, open): qmd 2.8.3 on a CPU-only laptop, ~800 Markdown files. `qmd embed` hit DisposedError mid-run, "skipped hundreds of chunks, and returned 0". Workaround: embed one collection at a time and treat "Embedding error"/"Session expired"/"skipping" in the output as failure.
  - #450 (2026-03-21, closed not planned): 8-core EPYC VPS, no GPU, crash after ~5 min.
  - #642: corpora of 28K+ docs take hours on Apple Silicon (search result).

## Could not verify
- Argon's G/H/I job (db5ef981): turns 1–2 finished, but their text is saved only on the Argon server and could not be fetched after turn 3 failed (HTTP 402). G/H/I therefore have no Argon/Reddit pass. No Reddit threads on scheduled deployments, dreams or qmd CPU timing were checked.
- Reddit scores and dates from Argon (r/ClaudeCode 1xfupmb; r/ClaudeAI 1v646sa; r/ClaudeCode 1vwekeo, 2026-08-23, 8 points): reddit.com refused direct JSON fetches from this sandbox.
- `claude mcp add --scope user` writing headers into `~/.claude.json`: no source independent of code.claude.com was found.
- That claude.ai currently sends RFC 8707 `resource` to Cloudflare's `/authorize`: only the #410 comment (June 2026) found it missing. No later confirmation either way. Only a live test settles it.
- The export's message-level keys beyond uuid/sender/text/created_at, and the share of bytes taken by `thinking`/`tool_use` blocks (Argon only).
- The `ant apply` deployment-file format has no source independent of Anthropic docs.

## Relevance (which draft claims must change, in one line each)
- h-reachability "Auth layer 1": the Access app must cover the **bare hostname** with MCP at root `/mcp`. Allowlist both `https://claude.ai/api/mcp/auth_callback` and `https://claude.com/api/mcp/auth_callback`, pick "Register automatically" (Cloudflare documents DCR, not CIMD), and add a WAF/Super-Bot-Fight-Mode skip rule for the MCP path.
- h-reachability open question "does claude.ai complete Access Managed OAuth": keep it as a mandatory live test. Cite #410 (fail, closed "not planned") alongside nas-mcp-server and plausible-mcp (work).
- h-reachability "Request headers is beta": keep. Add that the Help Center omits the beta note, and that maintainer confirmation is claude-ai-mcp #10 (2026-10-18).
- h-reachability row "Code-tab SSH sessions… §10 test": a `permissions.deny` rule will not hide Desktop-injected connector tools (#104956, #92787). Connector calls in SSH sessions run inside the Desktop app (#94887). Drop the deny-rule test and note "disconnect at claude.ai or accept".
- f-chat-history claim 2 / table row: the multi-part layout is now the current one (7 parts plus a manifest; memory is a separate part). Fetch every part within 24 h; make the multi-part path primary and the single ZIP the fallback.
- f-chat-history claim 5 / table row "Agent SDK reader": `getSessionMessages` returns only the post-compaction chain. For archiving full chats, copy or read the raw JSONL (the sweep goes by mtime), with the SDK reader as a cross-check.
- a-managed-agents / fortnightly job: re-read jitter at deploy time (15 % now, 10 s at launch); the 03:30 cron sits outside the DST window, so no change.
- qmd design (h-reachability §8 and the benchmark): the embed wrapper must check output for "Embedding error|Session expired|skipping", not just the exit code. Budget ≈2 GB of models and ~30 min per ~1.4k docs on an 8-core CPU.

## Calls and cost
- `argon_research` "verify claude.ai connectors, Cloudflare Access OAuth, MCP auth spec" (job dd7a19f4, 2 turns, A/B/C): "2 turns ≈145.5 ¢ in 10 min"; final line "≈88.0 ¢ (today UTC 1472.9 ¢ / cap 5000 ¢)".
- `argon_research` "verify Claude Code MCP headers, claude.ai export format, Claude Code transcripts" (job 004ae4a0, 3 turns, D/E/F): "3 turns ≈192.3 ¢ in 11 min"; final line "≈65.6 ¢ (today UTC 1608.1 ¢ / cap 5000 ¢)".
- `argon_research` "verify Managed Agents schedules, pricing, memory stores, and qmd" (job db5ef981, 3 turns, G/H/I): turns 1–2 done, turn 3 **refused**, "Gemini HTTP 402… Your prepayment credits are depleted". No cost line was returned. 3 `argon_result` polls after the failure returned the same error.
- `argon_result {}` listing call: no cost.

## Reddit: not reached from the sandbox; the owner's fold-in chat covers it through his Reddit connector
Every Reddit item above rests on Argon's reading and is tagged `[Argon, not verified]`. Argon is now suspended (owner, Nov 2 01:00). The owner's fold-in chat should ask, through the Reddit connector (§9 rules: ≤3 `reddit_search` calls, then `reddit_thread` on the best ids; `reddit_wiki sub=ClaudeAI page=survivalguideweekly` first):
1. r/ClaudeAI, r/ClaudeWorkflows, last 90 days: "LLM wiki" / "Karpathy wiki" / "second brain" with Claude Code — which threads report rot (duplicates, dead links after renames, stale facts) and what fixed it; scores and dates.
2. r/ClaudeAI: "everything claude code" (ECC) and "oh-my-claudecode" (OMC) — complaints about installers rewriting settings or CLAUDE.md, token cost per turn, and what people copy instead of installing.
3. r/ClaudeAI wiki `workflows/skills`: the current guidance on uploading custom skills to claude.ai (description limits, rejected frontmatter, mobile visibility) and on keeping skills in sync with Claude Code.
4. r/ClaudeAI: "Managed Agents" scheduled deployments / memory stores — real costs per run, pauses at budget, memory-store mount failures.
5. r/ClaudeAI, r/selfhosted: custom MCP connectors on claude.ai behind Cloudflare Access (Managed OAuth) — does the handshake work, and header-token ("Request headers") availability on Pro/Max.

## Sources
1. https://github.com/anthropics/claude-ai-mcp/issues/10 — read 2026-11-02
2. https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp — read 2026-11-02
3. https://claude.com/docs/connectors/custom/add-unlisted.md — read 2026-11-02
4. https://code.claude.com/docs/en/mcp.md — read 2026-11-02
5. https://github.com/anthropics/claude-code/issues/105840 ; /58453 — read 2026-11-02
6. https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/managed-oauth/ — read 2026-11-02 (updated 2026-07-01)
7. https://developers.cloudflare.com/cloudflare-one/access-controls/ai-controls/secure-mcp-servers/ (updated 2026-10-22); …/mcp-portals/ (updated 2026-10-28) — read 2026-11-02
8. https://developers.cloudflare.com/changelog/post/2026-03-20-managed-oauth/ — search result
9. https://github.com/anthropics/claude-ai-mcp/issues/410 ; /315 ; /572 — read 2026-11-02
10. https://github.com/Githubtezla/nas-mcp-server (README) — read 2026-11-02
11. https://raw.githubusercontent.com/getsentry/plausible-mcp/main/README.md — read 2026-11-02
12. https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization ; /2026-07-28/basic/authorization — read 2026-11-02
13. https://github.com/anthropics/claude-code/issues/104956 ; /106481 ; /93722 ; /94887 ; /102996 ; /92787 — read 2026-11-02
14. https://support.claude.com/en/articles/9450526-export-your-claude-data — read 2026-11-02
15. https://modelbrain.net/articles/how-to-export-claude-conversations.html (2026-10-30) — read 2026-11-02
16. https://github.com/alexgs/claude-ai-transcript-export (README) — read 2026-11-02
17. https://www.anthropic.com/legal/consumer-terms (effective Oct 8, 2025) — read 2026-11-02
18. https://code.claude.com/docs/en/sessions.md ; settings-reference.md ; claude-directory.md ; data-usage.md ; agent-sdk/sessions.md ; agent-sdk/session-storage.md ; agent-sdk/python.md — read 2026-11-02
19. https://github.com/anthropics/claude-code/issues/59248 ; /45735 ; /53516 (search result) — read 2026-11-02
20. https://hexdocs.pm/claude_code/ClaudeCode.History.html ; https://ccassist.dev/blog/where-claude-code-stores-conversations/ — search results
21. https://platform.claude.com/docs/en/managed-agents/scheduled-deployments.md ; budgets.md ; memory.md ; dreams.md — read 2026-11-02
22. https://platform.claude.com/docs/en/api/typescript/beta/deployments — search result
23. https://www.developersdigest.tech/blog/claude-code-routines-vs-managed-agents-schedules (2026-06-11) — read 2026-11-02
24. https://www.getclaudeskills.com/blog/claude-managed-agents-scheduled-deployments ; https://rickhigh.substack.com/p/loop-engineering-the-problem-and — search results
25. https://claude.com/platform/claude-managed-agents ; https://imisofts.com/blog/claude-managed-agents-pricing/ ; https://www.therundown.ai/tools/claude-managed-agents ; https://www.agent37.com/blog/claude-managed-agents-pricing ; https://www.aicodex.to/articles/claude-managed-agents-memory ; https://rickhigh.substack.com/p/claude-managed-agents-viii-your-agent ; https://nerdleveltech.com/claude-managed-agents-memory-store-tutorial ; https://www.buildfastwithai.com/blogs/claude-managed-agents-memory-2026 — search results
26. https://registry.npmjs.org/@tobilu/qmd — read 2026-11-02
27. https://raw.githubusercontent.com/tobi/qmd/main/README.md — read 2026-11-02
28. https://github.com/tobi/qmd/issues/957 ; /935 ; /450 — read 2026-11-02; /642 — search result
29. Argon jobs dd7a19f4, 004ae4a0 (Gemini with Google Search) — Reddit/HN/GitHub items marked [Argon, not verified] above
