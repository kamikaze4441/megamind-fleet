# Anthropic Managed Agents: what they offer or threaten for MEGAMIND
Question: What do Managed Agents (memory stores, dreams, scheduled deployments, skills, GitHub, orchestration, secure deployment) offer or threaten for MEGAMIND, and which query pattern does the knowledge-wiki quickstart use? · Date read: 2026-11-02 · Researcher: R1 (megamind-researcher)

**V7 recommendation: YES. Pattern = "index-first file navigation". Open a fresh session for each question, with the wiki mounted read-only. Read `_index.md` first, then follow `[[wikilinks]]` and read the topic files with the ordinary file tools (read/glob/grep). Cite the `[source | as-of]` provenance carried in each page. If the wiki has no answer, give a scripted "not in the data room" refusal that names the document needed. No embeddings, vector DB, graph DB or SQLite are used. The wiki is plain Markdown with YAML frontmatter and `[[wikilinks]]`. [9]** (In the quickstart the files sit in a Managed Agents memory store mounted as a directory. For V7 the same pattern runs on the local `wiki/` + `index.md`, so nothing is added beside the Markdown wiki.)

## Summary (10 lines max, each line ending with [n])
- A memory store is a workspace-scoped set of text documents, addressed by path and mounted into the sandbox at `/mnt/memory/<slug>/`. Each memory is capped at 100 kB, a store at 10,000 memories, and a session at 8 stores. Every write creates a version, kept 30 days. [2]
- Dreams are an async research-preview job. A dream reads one memory store plus 1–100 session transcripts and writes a *new* output store. "The input store is never modified", so a human can review the output before adopting it. [3]
- Scheduled deployments: `ant apply deployment.md`, with the API request body as YAML frontmatter and the prose as the first `user.message`. The schedule is 5-field POSIX cron plus an IANA `timezone`. Optional `budget.max_list_cost.amount` is in US cents and applies to each run. [5][13][15]
- Jitter is up to 15% of the interval between runs (minimum 5 s, maximum 9 min). Each organisation can have up to 1,000 deployments. Missed triggers are not backfilled after unpause. [5]
- Skills are uploaded as a directory with `SKILL.md` (zip or individual files) to `/v1/skills`, or auto-discovered at `.claude/skills/<name>/SKILL.md` in a mounted GitHub repo. A session can use up to 500 skills. [4]
- GitHub: the `github_repository` resource needs `url` and takes an optional `authorization_token` (the docs recommend a fine-grained PAT). PRs go through the GitHub MCP server. The docs mention no GitHub App install. [7]
- Secure deployment recommendations: `limited` networking with an explicit `allowed_hosts` list, secrets in vaults injected into request headers only, `allowed_domains` on the web tools, the smallest tool set, `read_only` memory where possible, and a budget on every session or deployment. [8]
- Managed Agents is not eligible for ZDR or HIPAA. "Transcripts persist until you delete them", and memory stores are not deleted with sessions. [1][11][12]
- Pricing is model tokens plus $0.08 per session-hour while `running`. Dreams are billed at standard token rates. The pricing page lists no separate memory-store storage price. [3][14]
- The knowledge-wiki quickstart answers from the wiki only. Query sessions are read-only, and "Analyst writes propose; the dream disposes". [9]

## Findings

### Memory stores [2] (also [11], [12])
- Definition: "a workspace-scoped collection of text documents optimized for Claude". An attached store "is mounted as a directory inside the session's sandbox". The agent reads and writes it with the normal file tools, and the agent toolset is required. [2]
- Mount path is `/mnt/memory/<slug>/`, where the slug is the display name lowercased with each non-alphanumeric run replaced by a hyphen. The exact path is returned in `mount_path`. Writes elsewhere under `/mnt/memory/` fail because the parent is mounted read-only. [2]
- Writing:
  - API: `POST /v1/memory_stores/{id}/memories` with `path` and `content`. "Create does not overwrite". Updates go to `POST /v1/memory_stores/{id}/memories/{memory_id}`.
  - Optimistic concurrency: a `precondition` of `{"type":"content_sha256", ...}`.
  - CLI: `ant beta:memory-stores:memories create --path ... --content ...`.
  - Agent: file writes under the mount path are "persisted back to the store". [2]
- Reading:
  - Agent: file tools on the mount.
  - API list: `GET .../memories` with `path_prefix` (must end in `/`) and `depth` (0 or 1).
  - API read: `GET .../memories/{memory_id}` returns the full content.
  - The Claude Console also exposes stores. [2]
- Limits:
  - "Individual memories within the store are capped at 100 kB (~25k tokens). A store holds a maximum of 10,000 memories." [2]
  - Up to **8 memory stores** per session.
  - `instructions` on the attachment are capped at 4,096 characters.
  - Stores can be attached only at session creation. [2]
  - At 10,000 memories, new writes fail; existing memories stay readable and editable. [2]
- Access is `read_write` by default; `read_only` is "enforced at the filesystem level". The docs warn that prompt injection can write content that later sessions "read ... as trusted memory". [2]
- Versioning and audit:
  - Every change creates an immutable `memver_...`.
  - "Versions are retained for 30 days after they are written", but the recent versions of a live memory are always kept.
  - There is no restore endpoint: you re-write old content.
  - `redact` scrubs a historical version.
  - Archiving a store is one-way and read-only. `DELETE /v1/memory_stores/{id}` permanently deletes the store with all memories and versions. [2]
- Beta header: memory store calls use `agent-memory-2026-07-22`. Sending it together with `managed-agents-2026-04-01` returns 400. Session calls keep `managed-agents-2026-04-01`. [2]
- Self-hosted sandboxes: the store is downloaded and synced by your worker rather than live-mounted (sync interval 15 s by default). On Claude Platform on AWS and Google Cloud, self-hosted sessions can't attach memory stores. [2][12]
- Can an agent read a Markdown vault mirrored into a store?
  - The docs' own examples use `.md` paths (`/formatting_standards.md`, `/preferences/formatting.md`), and the store is presented as a directory read with file tools. [2]
  - The quickstart stores a Markdown wiki with YAML frontmatter and `[[wikilinks]]` in a memory store and reads it with file tools. It seeds raw documents one `memories.create` call per file, chunking at 85,000 characters (cell 39). [9]
  - Constraints for a mirror: each file ≤100 kB, ≤10,000 files per store, text only ("text documents"). [2]
  - The docs show no bulk import or sync endpoint, only per-memory create/update. [2]
- Data handling (where it lives, retention, who reads it):
  - Memory stores are workspace-scoped [2]. The docs state "whoever can start sessions in a workspace can reference its vaults" [8]. No equivalent sentence for memory stores was found.
  - Under "What reaches Anthropic", the cloud column lists conversation history, tool results, sandbox files and state, skills and memory stores. Even with a self-hosted sandbox, "skills, and memory stores" still reach Anthropic. [12]
  - Retention: "Files you uploaded, memory stores, and vaults: Not deleted with the session. Delete them separately." Session history is "Kept until you delete the session". [11]
  - Managed Agents is "not currently eligible for Zero Data Retention or HIPAA". [1][11]
  - Org-wide rule: flagged sessions "may retain inputs and outputs for up to 2 years". [16]

### Dreams [3]
- Status: research preview behind a request-access form. Headers are `managed-agents-2026-04-01` plus `dreaming-2026-04-21`. Supported on select Claude API models only. [3][1]
- What a dream is: an "asynchronous job" whose inputs are one pre-existing **memory store** and **1 to 100 sessions** (past transcripts). It produces "another **output memory store**, separate from the input". [3]
- What it writes:
  - Duplicates merged, stale or contradicted entries replaced with the latest value, and "new insights surfaced". [3]
  - The quickstart's dream also built an index (`_index.md`) and an `escalations.md`, as instructed by steering. [9]
- When dreams run: only when you call `POST /v1/dreams` (`ant beta:dreams create`). Run time is "minutes to a few hours". The docs show no automatic or scheduled dreaming. [3]
- Steering: optional `instructions` ("a synthesis pass ... not an editor"). Line-targeted directives "generally produce no change". [3]
- Inputs untouched: "The dream itself never deletes or modifies its inputs." You choose whether to attach the output store or delete/archive it. [3]
- Lifecycle: `pending`, `running`, `completed`, `failed`, `canceled`. Partial output persists on failure or cancel. Cancel and archive endpoints exist. List returns up to 100 per page. [3]
- Error types include `timeout`, `input_memory_store_too_large`, `memory_store_org_limit_exceeded`, and others. The size limit for `input_memory_store_too_large` is not stated. [3]
- Billing: "standard API token rates for the model you select". Default rate limits apply during the preview. [3]
- Conflict with "owner merges": a dream never writes to its input, and adoption is a separate step (attaching the new store). The docs therefore describe a review gate, but nothing enforces it: the caller decides whether to attach the output. [3] The memory page also recommends dreaming as a way to prune a full store into a new output store. [2]

### Scheduled deployments [5] (field reference [13], `ant apply` [15], budgets [8])
- Definition: a scheduled deployment "allows an agent to start sessions autonomously" on a cron schedule, through the Deployments API (`POST /v1/deployments`). [5]
- Requirements: agent and environment configuration, plus at least one initial event (`user.message` or `user.define_outcome`). In an `ant apply` deployment file, "the text below the frontmatter becomes that `user.message`". [5]
- Optional resources: files, GitHub, memory stores and vaults. On self-hosted environments only `memory_store` is allowed; `file` and `github_repository` need cloud. [5]
- Skills and MCP servers are **agent** fields, not deployment fields. The deployment body has no `skills` or `mcp_servers` key; they come with the pinned agent. [13][4][7]
- Exact body fields (Create Deployment reference):
  - `agent` (string, or `{type: agent, id, version}`)
  - `environment_id`
  - `initial_events[]`
  - `name`
  - `budget` (`{type: "limit", max_list_cost: {amount, currency}}`)
  - `description`
  - `metadata`
  - `resources[]`: `github_repository` (`url`, `authorization_token`, `checkout`, `mount_path`), `file` (`file_id`, `mount_path`), or `memory_store` (`memory_store_id`, `access`, `instructions`)
  - `schedule` (`type: cron`, `expression`, `timezone`)
  - `vault_ids` (max 50) [13]
- Cron:
  - "Standard POSIX cron (`minute hour day-of-month month day-of-week`)", at minute granularity. [5]
  - Day-of-week 0–7 (0 and 7 = Sunday). Seconds and year fields, `L W # ?`, and `@daily`-style shortcuts are not supported. The expression is at most 256 characters. [13]
- Time zone:
  - "IANA timezone identifier", validated against the IANA database. Both `expression` and `timezone` are required when `schedule` is set. [5][13]
  - DST uses literal wall-clock matching. A nonexistent spring-forward time is "not triggered"; a repeated fall-back time "fire[s] twice". The docs advise scheduling outside 1–3 AM local time, or using UTC. [5]
- Jitter: "up to 15 percent of the interval between runs, with a minimum of 5 seconds and a maximum of 9 minutes". [5]
- Budget per run:
  - The cap is copied onto each session, so it "bounds every run separately rather than acting as a cumulative ceiling". It can be removed with `"budget": null`. [5]
  - `amount` is "a whole number of US cents written as a string" ("125" = $1.25). [8]
  - The reference words it as minor units ("2500" is $25.00), and USD is the only currency. [13]
  - At the cap the session pauses with `budget_reached`. In-flight requests can complete, "so spend can pass the cap". [5][8]
- Runs and lifecycle:
  - Each attempt is a `deployment_run` with `trigger_context` and either a `session_id` or an `error`. [5]
  - Pause stops scheduled triggers but still allows manual runs. "Missed triggers are not backfilled" after unpause. Archive is terminal. `POST /v1/deployments/{id}/run` triggers a manual run. [5]
  - Rate-limited session creation becomes a failed run, with no retry. An archived agent auto-archives the deployment; other unrecoverable errors auto-pause it. Webhooks exist for deployment and run events. [5]
- A deployment "pins an agent version", so after an agent update you must point each deployment at the new version. [8]
- Cap: 1,000 scheduled deployments per organisation. [5]
- Docs' example manifest, verbatim [5]:

```markdown
---
name: Weekly compliance scan
agent: agent_011CYm1BLqPXpQRk5khsSXrs
environment_id: env_01595EKxaaTTGwwY3kyXdtbs
schedule:
  type: cron
  expression: "0 20 * * 5"
  timezone: America/New_York
budget:
  type: limit
  max_list_cost:
    amount: "2000"
    currency: USD
---

Run the weekly compliance scan.
```

- The `ant apply` docs' example: a deployment that references agent, environment and memory store by relative path, verbatim [15]:

```markdown
---
name: Nightly review
agent: ../agents/reviewer.md # the API's agent field: sent as {type: agent, id, version}
environment_id: ../environments/cloud.yaml # sent as the environment's ID
resources:
  - path: ../memory_stores/review-notes.yaml
    access: read_write
schedule:
  type: cron
  expression: "0 3 * * *"
  timezone: America/Los_Angeles
---

Review any open pull requests. Start with the oldest.
```

- `ant apply` behaviour [15]:
  - Needs CLI ≥1.30.0.
  - Infers the kind from the directory: `agents/`, `environments/`, `memory_stores/`, `deployments/`, `vaults/`; a skill is a directory with `SKILL.md`.
  - Writes `claude-lock.json`, which must be committed.
  - Supports `--dry-run`, `--yes` (required without a TTY), `--prune` and `--upgrade`.
  - Refuses credentials for another org or workspace.
  - Recommends Workload Identity Federation in CI.

### Skills on Managed Agents [4] (see e-skills-install.md for the full install comparison)
- A custom skill is "a directory containing a `SKILL.md` file plus any supporting files, uploaded to your workspace as a zip archive or as individual files". It goes to `POST /v1/skills` (`-F "files[]=@example_skill.zip"`) or `ant apply skills/<name>`, which returns a `skill_*` ID. [4]
- Optional `display_name` is up to 255 characters; otherwise the name is derived from `name` in `SKILL.md`. [4]
- Attaching: the agent's `skills[]` entries take `type` (`anthropic` | `custom`), `skill_id` (short name such as `xlsx`, or `skill_*`) and optional `version` (default `latest`). [4]
- Up to 500 skills per session, deduplicated across agents. More skills mean a slower sandbox start. [4]
- Repo skills: mounting a `github_repository` scans exactly `.claude/skills/<skill-name>/SKILL.md` at the repo root, once at session start. This needs the `read` tool and cloud sandboxes only. The platform loads them "without a review step". [4]

### GitHub integration [7]
- What it does: mounts a repo into the sandbox (cached for faster future sessions). An agent that declares the GitHub MCP server (`https://api.githubcopilot.com/mcp/`, `type: url`) plus an `mcp_toolset` can "create branches, commit changes, and push them". [7]
- `github_repository` fields:
  - `type` and `url` are required. The URL must be HTTPS `https://github.com/<owner>/<repo>` with no `.git`; SSH is rejected.
  - Optional: `authorization_token`, `mount_path` (default `/workspace/<repo-name>`) and `checkout` (branch or commit). [7]
- Tokens:
  - Without a token, a private repo fails to clone, and a public one clones but "`git push` fails".
  - The token "is not echoed in API responses" and can be rotated on a running session.
  - Scopes table: clone private or create PRs = `repo`; read or create issues = `repo` (private) or `public_repo`.
  - The docs advise "fine-grained personal access tokens with minimum required permissions". [7]
- App install: the page describes a personal-access-token flow only. No GitHub App installation is mentioned. [7]
- With `limited` networking, the MCP host must be in `allowed_hosts`, or `allow_mcp_servers: true` must be set. [7]
- Mounting a repo also loads its `.claude/skills`. [7]

### Secure deployment [8]
- Network:
  - Use `networking.type: limited` with only the needed `allowed_hosts`; omitting `networking` "might get `unrestricted`". [8]
  - `allow_package_managers` opens all of github.com, gitlab.com and bitbucket.org; the docs recommend `false`. [8]
  - "Network access is granted by host, not by operation", so uploads such as `git push` are possible to any allowed host. [8]
  - Attached files, memory stores and GitHub repos stay available whatever `allowed_hosts` says. [8]
- Secrets:
  - "Store every secret in a vault". Set `injection_location` to `{"header": true, "body": false}` and limit the credential's `networking` to exact hosts. Sandbox code sees a placeholder. [8]
  - "Do not give the agent a Claude API key". Keep keys out of system prompts and agent definitions. Separate workspaces by trust level, and prefer Workload Identity Federation. [8]
  - For a mounted repo's GitHub token, "Grant write access only if the agent must push". [8]
- Least privilege:
  - Set `default_config.enabled: false` and enable only the needed tools; all eight built-in tools are on by default. [8]
  - Permission policies: `always_allow` for read/glob/grep, `auto` for bash/write/edit/web_fetch, `always_ask` for irreversible actions. "`auto` is not a human checkpoint". [8]
  - `allowed_domains` on `web_fetch` and `web_search`; `blocked_domains` is not a security control. [8]
- Untrusted input:
  - Attach memory as `read_only` unless writes are needed.
  - A mounted repo is a trust boundary because its skills load as instructions.
  - `CLAUDE.md`/`AGENTS.md` files are loaded on `read` (with `@` imports up to five deep), and only disabling `read` turns that off.
  - Recommended designs: split reading from acting, use one narrow custom tool, or keep a person in the loop. [8]
- Stop controls:
  - Budget on each session and deployment, plus `user.interrupt`.
  - Pause or archive the deployment.
  - Archive or delete sessions; deleting removes the record, events and sandbox. [8]

### Multiagent orchestration [6]
- Configured in the agent's `multiagent` block (`type: multiagent_20261001`). It has three parts:
  - `subagents`: delegation, one level deep, at most 25 child threads, up to 20 `predefined_agents`.
  - `workflows`: a program that runs many agents in a background "workflow run".
  - `advisor`: a model consulted mid-turn by the primary thread. [6]
- Defaults: subagents and workflows are enabled and inline agents are allowed. To restrict to listed agents, set `inline_agents: {type: disabled}`. [6]
- Sharing: "All agents share the same sandbox, filesystem, and vault credentials", each in its own context-isolated thread. Predefined agents are pinned to a version at create or update. [6]
- There is no approval step before a workflow run starts ("nothing enforces this"). A session budget caps the spend of runs. [6]

### Pricing and limits [14][10a]
- Tokens are billed at model rates, and prompt-caching multipliers apply. Web search costs $10 per 1,000 searches. Session runtime is "$0.08 USD per session-hour", metered only while `running`. There is no Batch discount. [14]
- Rate limits per organisation: create endpoints 300 requests/min; read endpoints 1,200 requests/min. Org spend and tier limits also apply. [10a]
- No memory-store storage price and no deployment fee appear on the pricing page; it was searched for "memory", "dream" and "deployment". [14]

### Knowledge-wiki quickstart [9] (anthropics/claude-quickstarts, `managed-agents/knowledge-wiki/`)
- Pipeline (README L50–91):
  1. Normalise sources to `[SOURCE: …]`-stamped text.
  2. Run parallel extraction sessions writing into one memory store, the wiki, with single-writer paths.
  3. Run a resolver pass on open questions.
  4. Run one steered dream that writes a new store with an index and `escalations.md`.
  5. Query "read-only from a fresh session per question".
  6. Periodically dream over the query transcripts. [9]
- Wiki format: "every node is a markdown file with YAML frontmatter, and [[wikilinks]] in the body are the edges between nodes" (notebook cell 15, `KG_SCHEMA`, raw .ipynb L490–492).
  - Layout: `entities/<slug>.md` (frontmatter: `name`, `description`, `aliases`, `metadata.type`), plus `relations/`, `metrics/` and `open_questions/` per source document.
  - Every fact ends `[source: <doc> | as-of: <date>]` (cell 15 lines 56–118). [9]
- Query pattern (notebook cell 26, raw .ipynb L1370–1408):
  - The analyst system prompt names the read-only store as the "ONLY knowledge source", requires provenance citations, and gives a "Not in the data room" refusal (cell 26 lines 3–8).
  - `ask()` creates one session for each question. It attaches the store with `"access": "read_only"` and instructions "Start at _index.md; escalations.md ranks red flags; facts carry [source | as-of] provenance - cite it" (cell 26 lines 28–41).
  - Tools: `agent_toolset_20260401` with all tools enabled, `always_allow` (cell 26 lines 16–19). [9]
- Retrieval mechanism:
  - Plain file tools on the mounted Markdown. `utilities.py` L119–139 counts every non-write tool call as one of the "reads/searches".
  - No embeddings or search service appear anywhere in the query path. Cell 0 (L11–28) contrasts the wiki with "An index (vector, keyword, or graph DB)" and says "no embedding infrastructure to run".
  - The index `_index.md` is produced by the dream ("an index that turns exploratory reads into one lookup", README L75–77). [9]
- Write discipline:
  - Query sessions never write. "Analyst writes propose; the dream disposes".
  - Optional "tiny side store for *miss logging only*" (cell 25 line 7).
  - Raw documents are deliberately not given as fallback (cell 25 line 5). [9]
- Export: cell 23–24 lists all memories and writes them to local `.md` files ("a local export is one loop away"). [9]
- Costs stated: `mini` tier about $35 and about 1 h; wiki queries about $0.16 versus $0.62 raw at full scale (cell 2, README L134–147). These are the authors' directional figures. [9]
- Setup risk notes:
  - The README's quick path is `claude "walk me through setting up..."`. The directory's `CLAUDE.md` tells Claude to follow `skill.md` step by step.
  - The manual path is `pip install -r requirements.txt` followed by `python3` fetch scripts.
  - There is no piped shell installer, no settings.json rewrite and no hooks. Nothing from the clone was executed. [9]

## Repositories pinned
| repo | HEAD SHA | commit date | licence file and its first line | what was read (paths, line ranges) |
|---|---|---|---|---|
| https://github.com/anthropics/claude-quickstarts | 1a18c340ca42b9137d991637afe867bdcf70a9ce | 2026-10-29 | `LICENSE`: "MIT License" | `managed-agents/knowledge-wiki/README.md` (L1–147, full); `CLAUDE.md` (L1–15, full); `skill.md` (L1–113, full; a setup guide for Claude Code, not an Agent Skill with frontmatter); `utilities.py` (L59, L83–183); `distill_documents_into_knowledge_wiki.ipynb`: all 45 cells' source, key cells 0, 15, 21, 25, 26, 39 (raw L490–492, L1355–1408) |

README install instructions (verbatim, from L117–128):
```bash
pip install -r requirements.txt

export EDGAR_USER_AGENT="your-name your-email"   # SEC asks for a contact

python3 build_manifest.py
python3 fetch_data_room.py --tier=mini   # 26 documents, ~0.5 MB text
python3 fetch_real_deck.py               # 6 slides of a real board deck (~1 MB)
python3 make_analyst_docx.py

jupyter lab distill_documents_into_knowledge_wiki.ipynb
```

## Could not verify
- **Memory-store residency/region and access roles**: no page states the region where memory store content is stored or which Console/workspace roles can read a store. Pages checked: memory [2], choosing-an-environment [12], monitoring [11], api-and-data-retention [16]. Only "workspace-scoped" [2] and "reaches Anthropic" [12] are stated.
- **Retention of memory content after `DELETE`**: the page says delete is "permanent". Backup or retention windows after deletion are not stated [2].
- **Dedicated Managed Agents pricing page**: none exists in the managed-agents nav (llms.txt). Pricing is a section of `about-claude/pricing` [14]. No storage price for memory stores or deployments is listed.
- **Dream input size limit**: `input_memory_store_too_large` is named, but the threshold is not given [3].
- **Dreams on a schedule**: no docs page shows dreams triggered by a deployment or cron. Dreams are created by explicit API call only [3][5].
- **GitHub App installation**: not mentioned on the GitHub page [7]. Only the PAT flow is documented.
- **Skill size limits for `/v1/skills`**: not on the managed-agents skills page [4]; see e-skills-install.md.
- The quickstart's saved outputs record counts of reads/searches but not tool names. Whether the analyst used `grep` or only `read`/`glob` in the committed run is not verifiable from the saved outputs [9].

## Relevance to MEGAMIND
- **Memory stores.**
  - Offers: a hosted, versioned (30-day) Markdown directory that a Managed Agent reads with file tools, and that the Console and API expose for review and export [2][9]. It could hold a read-only mirror of `wiki/` for cloud-side jobs. Attaching it `read_only` matches "owner merges" at the filesystem level [2].
  - Threatens:
    - Mirroring vault text puts it on Anthropic infrastructure. That destination is allowed, but the content is not ZDR-eligible and persists until explicitly deleted [1][11]. Flagged content may be kept up to 2 years [16].
    - Limits that a mirror must respect: 100 kB per file, 10,000 files per store, text only, and no bulk sync endpoint [2].
    - A `read_write` attachment would let a cloud agent change memory outside the owner's merge, and prompt-injected writes become "trusted memory" [2].
- **Dreams.**
  - Offers: consolidation that writes a new store and leaves the input untouched, with a reviewable output [3]. This maps to "propose, owner merges" if the output is exported and diffed against the vault (quickstart cells 23–24) [9].
  - Threatens:
    - A dream does reorganise the whole store (merges, replaces "stale or contradicted entries"), so adoption is wholesale unless diffed [3].
    - A dream sees only the store and transcripts, never raw sources [9].
    - Research preview, gated access, token-billed, and run time of minutes to hours [3].
    - Not schedulable through the documented deployment API [3][5].
- **Scheduled deployments.**
  - Offers: a cloud cron for "scout" or housekeeping jobs. It has a Markdown manifest (`ant apply`, frontmatter = request body, prose = prompt), IANA time zone, a per-run `budget` in cents, pause/run/archive, run history, and webhooks [5][13][15].
  - Threatens / changes:
    - Runs happen on Anthropic, not the home VM. A deployment can mount memory stores, files and GitHub repos, but cannot reach the home VM unless a host is opened [5][8][12].
    - DST double or skipped fires [5]; jitter up to 9 min [5].
    - Each run is capped separately, with no cumulative ceiling [5].
    - The agent version is pinned, so it must be re-pointed after updates [8].
- **Skills.**
  - Offers: the same `SKILL.md` folder is uploaded by `ant apply skills/<name>` or by zip to `/v1/skills` [4][15]. Alternatively, repo-hosted `.claude/skills/<name>/SKILL.md` is auto-discovered when the repo is mounted [4].
  - Threatens: repo skills load "without a review step", so the skills directory is part of the trust boundary [4][8].
- **GitHub.**
  - Offers: mount a repo (e.g. a vault mirror or a proposals repo) and open PRs through the GitHub MCP server. This fits "agent proposes a PR, owner merges" [7].
  - Threatens:
    - Needs a PAT held per session. A token with write scope lets sandbox code push to the mounted repo for the whole session [8].
    - Private vault content in a GitHub repo is a second destination beyond Anthropic.
    - With `allow_package_managers`, all of github.com becomes reachable [8].
- **Orchestration.**
  - Offers: lead/fetcher/writer split, inside one session or across sessions, for "read untrusted web, then act" scouting [6][8].
  - Threatens:
    - Agents in one session share sandbox, files and vault credentials, so the split separates tools only [6][8].
    - Workflow runs start without approval and multiply token spend, so a session budget is required [6].

## Sources
[1] https://platform.claude.com/docs/en/managed-agents/overview.md — read 2026-11-02
[2] https://platform.claude.com/docs/en/managed-agents/memory.md — read 2026-11-02
[3] https://platform.claude.com/docs/en/managed-agents/dreams.md — read 2026-11-02
[4] https://platform.claude.com/docs/en/managed-agents/skills.md — read 2026-11-02
[5] https://platform.claude.com/docs/en/managed-agents/scheduled-deployments.md — read 2026-11-02
[6] https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration.md — read 2026-11-02 (sections: Hand work, Predefined/inline, Delegate, Dynamic workflows; advisor section skimmed)
[7] https://platform.claude.com/docs/en/managed-agents/github.md — read 2026-11-02
[8] https://platform.claude.com/docs/en/managed-agents/secure-deployment.md — read 2026-11-02
[9] https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents/knowledge-wiki — cloned at 1a18c340ca42b9137d991637afe867bdcf70a9ce (2026-10-29), MIT — read 2026-11-02
[10a] https://platform.claude.com/docs/en/managed-agents/reference.md (Rate limits section) — read 2026-11-02
[11] https://platform.claude.com/docs/en/managed-agents/secure-deployment-monitoring.md — read 2026-11-02 (retention section)
[12] https://platform.claude.com/docs/en/managed-agents/choosing-an-environment.md — read 2026-11-02 (comparison table, differences)
[13] https://platform.claude.com/docs/en/api/beta/deployments/create.md — read 2026-11-02 (body parameters)
[14] https://platform.claude.com/docs/en/about-claude/pricing.md — read 2026-11-02 (Claude Managed Agents pricing section)
[15] https://platform.claude.com/docs/en/cli-sdks-libraries/cli/apply.md — read 2026-11-02
[16] https://platform.claude.com/docs/en/manage-claude/api-and-data-retention.md — read 2026-11-02 (ZDR scope, Managed Agents row, retention regardless of arrangement)
