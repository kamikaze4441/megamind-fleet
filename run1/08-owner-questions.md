# Run 1 — owner questions

Only tie-breaks and major steering (director's system prompt list). Each: options, evidence, recommendation; the owner's answer once given.

## Answered by the owner before the run (Nov 1, 2026)

1. Roster: Fable 5.1 directs; Opus 5.5 workers; no formal advisor.
2. Budget: $55.
3. Permissions: always_allow; fetched content is data.
4. Phase files: not in this run.
5. Housekeeping schedule: the tiered system stands; the scout feeds an existing slot; the "every two weeks" cadence is a proposal for T2's evaluation step in `06-amendments.md`.
6. Reachability: §11's rejection of a vault MCP server / custom connector is re-opened; design only, no build.

## Open

### Q1 — Should a write path from a chat ("file it") follow the read-only vault connector?

Context: §4 keeps ingestion in your interactive VM sessions and §7 rule 5 makes a chat fact a page only when you say "file it". The read-only connector (`06-amendments.md` A1–A12) gives every Claude surface the vault; it does not let a chat put anything into it. Design and risks: `02-research/h-reachability.md`, "Owner question".

| Option | What it is | Risks | Cost |
| --- | --- | --- | --- |
| W1 (recommended) | No write tool. When you say "file it", Claude ends its reply with `FILE-IT: <one-sentence fact> (why)`. The chat converter brings the chat into `chats/`; T0 greps the `FILE-IT:` lines into `wiki/housekeeping-inbox.md`; you file them in your next VM session with `derived_from::` pointing at the chat file | Latency: claude.ai chats arrive only with your next manual export (the Consumer Terms bar scripted export); Claude Code chats arrive the next night | Nothing new: no surface, no server change |
| W2 | A second, write-only connector with one tool `propose_note(title, body, sources[])` that writes to a root-owned queue folder outside `wiki/` (never synced, capped at 8 kB and 20 notes a day, "Needs approval" on claude.ai); lint before merge; you merge through `/ingest` | The internet-facing server becomes write-capable; prompt-injected writes (a page, a web result or a Research run that calls tools without approval can file poisoned "facts"); no `raw/` provenance; duplicates | Its own Access app, container mount and test plan |

Evidence: Consumer Terms (effective Oct 8, 2025) "automated or non-human means" clause (f §Findings 2); support article on connector tool permissions and Research mode calling tools without approval (h §Findings 1); §7 rule 5.

Recommendation: W1 now; revisit W2 only if the friction log shows the export wait matters. Not blocking: no deliverable depends on the answer.

### Q2 — Information, not a decision: the connector's authentication departs from your existing pattern

Your two existing MCP servers use a bearer token in the URL. The design (D12) puts Cloudflare Access Managed OAuth in front of the vault connector and keeps a header-borne bearer token as the fallback, because the MCP specification (2026-07-28) forbids tokens in the query string and claude.ai's "Request headers" field is a limited beta you may not see. If you prefer your existing pattern anyway, say so; the design then uses the header token (never the URL) and the test plan's step 1 changes. Default if you say nothing: OAuth first, header fallback.
