# Installing custom skills on claude.ai, in Claude Code and for Managed Agents — one folder, three targets?
Question: How are custom skills installed on claude.ai, in Claude Code and for Managed Agents (exact menu labels), and can one skill folder serve all three? · Date read: 2026-11-02 · Researcher: R1 (megamind-researcher)

## Summary (10 lines max, each line ending with [n])
- claude.ai: `Customize > Skills`, then the `"+"` button, then `"+ Create skill"`, then `"Upload a skill"`, then upload a ZIP whose top level is the skill folder. [1][3]
- Claude Code: drop the folder at `~/.claude/skills/<name>/SKILL.md` (personal) or `.claude/skills/<name>/SKILL.md` (project). Alternatively, ship it inside a plugin at `<plugin>/skills/<name>/SKILL.md`, invoked as `/plugin:skill`. [5][6][7]
- Managed Agents: upload to `POST /v1/skills` as a zip or individual files, or run `ant apply skills/<name>`. Then reference the returned `skill_*` ID in the agent's `skills[]`. Alternatively, mount a GitHub repo whose `.claude/skills/<name>/SKILL.md` is auto-discovered. [11][12][14]
- Spec frontmatter has two required fields, `name` and `description`, and four optional ones: `license`, `compatibility`, `metadata`, `allowed-tools`. [10][5]
- claude.ai uploads and the Skills API accept **only** those six fields. Any other key fails hard with "Unexpected key(s) in SKILL.md frontmatter". Claude Code accepts many more (`when_to_use`, `disable-model-invocation`, `context`, `hooks`, `paths`, …). [5]
- Limits:
  - Skills API: <30 MB uncompressed; `name` ≤64 characters, lowercase/digits/hyphens, no "anthropic"/"claude"; `description` ≤1,024 characters. [12]
  - claude.ai plugin upload: ≤5,000 files, ≤200 MB. [9]
  - claude.ai skill ZIP: the size cap is not stated. [1]
- Skills enabled on claude.ai sync one-way into Claude Code (terminal, v2.1.273+, claude.ai sign-in only) and into Cowork and cloud sessions. Plugin skills installed on the account load in chat "on the web, desktop, and mobile". [1][5][8]
- A plugin installed from the Claude Code CLI is not added to the claude.ai account. The same plugin folder can be uploaded via `Customize > Plugins` → `Add > Upload plugin`, and its skills then load in chat. [8][9]
- Plan tiers conflict across Anthropic pages:
  - The support article lists Free, Pro, Max, Ultra, Team and Enterprise. [1]
  - claude.com docs and the platform overview list Pro, Max, Ultra, Team and Enterprise. [4][10]
- Verdict: one `skills/<name>/SKILL.md` folder with spec-only frontmatter can be zipped for claude.ai, wrapped by a plugin/marketplace manifest for Claude Code, and uploaded to `/v1/skills` unchanged. GitHub auto-discovery on Managed Agents, however, requires the `.claude/skills/<name>/` path. [5][13][4]

## Findings

### claude.ai (support articles [1][2], claude.com docs [3][4])
- Upload path, as printed:
  - Prepare: "Package your skill folder as a ZIP file". Navigate to `Customize > Skills`.
  - Add: click the `"+"` button, then `"+ Create skill."`, then select `"Upload a skill."`.
  - Upload: "Upload a ZIP file containing your skill folder". The skill then appears in the list and "can be toggled on or off". [1]
- The claude.com docs name the same page `Customize > Skills` "in claude.ai and the desktop app". Its tabs are **Your skills** (grouped **Created by you**, **From your organization**, **Shared with you**, **From Anthropic & Partners**) and **Discover**. A skill is enabled with **Turn on**. [3]
- Prerequisite:
  - Individual plans: `Settings > Capabilities` → "Code execution and file creation" (called "Create and edit files" in the updated layout).
  - Team/Enterprise: `Organization settings > Plugins & skills`, "Policy" tab, with both "Code execution and file creation" and "Skills" enabled. [1]
- ZIP format: "The ZIP should contain the skill folder as its root (not a subfolder)", i.e. `my-skill.zip/my-skill/skill.md`. Files directly in the ZIP root are "Incorrect". [2] The claude.com page agrees: "a `SKILL.md` sitting at the root of the ZIP isn't recognized as a skill". It also says the "directory name must match the `name` field". [4]
- Upload errors listed: "ZIP file exceeds size limits", "Skill folder name doesn't match the skill name", "Missing required skill.md file", "Invalid characters in skill name or description". No size number is given. [1]
- Frontmatter per the support article: `name` (64 characters maximum) and `description` (**200 characters maximum**) are required. `dependencies` is optional, e.g. "python>=3.8, pandas>=1.5.0". [2]
  - The claude.com page instead gives `name` as "Lowercase letters, numbers, and hyphens only, up to 64 characters", matching the directory, and `description` "Up to 1,024 characters". [4] The two pages disagree; see Could not verify.
- Scripts: in chat "the skill's whole folder, scripts included, is copied into the code execution sandbox". `${CLAUDE_SKILL_DIR}` is replaced in Claude Code and Cowork only, so chat needs paths that are relative to `SKILL.md`. [4]
- Plan tiers:
  - Support article: "Free, Pro, Max, Ultra, Team, and Enterprise plans", with code execution required. [1]
  - claude.com skills overview: "Pro, Max, Ultra, Team, and Enterprise plans". [3]
  - Platform overview: custom skills on "Pro, Max, Ultra, Team, and Enterprise plans". [10]
- Sharing (Team/Enterprise): the three-dot menu `(...)` → `"Share"`, or `"Publish to org"` with offer options "Available to install, Installed by default, or Required". Owners can provision org-wide. [1]
- Where claude.ai skills reach:
  - Claude Code terminal: skills "load in Claude Code in your terminal when you sign in with the same Claude account", which "needs Claude Code v2.1.273 or later". `/skills` lists them under `claude.ai sync`. The sync "is one-way" and does not happen with an API key or Bedrock. [1]
  - Microsoft 365 add-ins: skills are also available in the "Excel, PowerPoint, Word, and Outlook add-ins". [1]
  - Desktop app: the `Customize > Skills` page exists "in claude.ai and the desktop app". [3]
  - Mobile: the claude.com plugin docs say a plugin's skills are available in "Chat on the web, desktop, and mobile" [8]. "Chat" is defined to include "the mobile apps" [9]. For standalone uploaded skills, mobile is not stated on the pages read.
- Conflicting older statement: the platform overview still says claude.ai uploads go "through Settings > Features" and that "Custom Skills do not sync across surfaces" [10]. This contradicts the support article and the Claude Code docs, which describe `Customize > Skills` and one-way sync into Claude Code [1][5].

### Claude Code (skills page [5], plugins pages [6][7], plugin docs on claude.com [8][9])
- Locations (table "Choose where skills load"):
  - Personal: `~/.claude/skills/<skill-name>/SKILL.md`.
  - Project: `.claude/skills/<skill-name>/SKILL.md`.
  - Enterprise: managed-settings directory.
  - Plugin: `<plugin>/skills/<skill-name>/SKILL.md`, invoked "as `/plugin-name:skill-name`".
  - claude.ai account: synced into `~/.claude/skills/synced/`. [5]
- Personal skills do not load in Cowork or cloud sessions. Those sessions load the skills enabled for the claude.ai account. [5]
- Install is a plain folder copy: no packaging. A skill folder with `.claude-plugin/plugin.json` added also loads as a plugin named `<name>@skills-dir`. [5][7]
- Frontmatter: "All fields are optional. Only `description` is recommended". Fields:
  - `name`, `description`, `when_to_use`, `argument-hint`, `arguments`
  - `disable-model-invocation`, `user-invocable`, `allowed-tools`, `disallowed-tools`
  - `model`, `effort`, `context`, `agent`, `background`, `hooks`, `paths`, `shell`
  - `metadata`, `license`, `compatibility` [5]
- Limits: `description` + `when_to_use` are "truncated at 1,536 characters in the skill listing". "Keep `SKILL.md` under 500 lines". [5]
- Cross-surface rule (table "Using skill frontmatter outside Claude Code"):
  - "claude.ai skill uploads, the Skills API, and packaging with `package_skill.py`" accept only `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`.
  - Any other field makes "packaging or upload fail[] with a hard error".
  - Claude Code-only body features such as dynamic context injection "don't function in claude.ai chat or through the API". [5]
- Plugin packaging:
  - Layout: `my-plugin/.claude-plugin/plugin.json` (`name` required) plus `skills/<name>/SKILL.md`. Only `plugin.json` goes inside `.claude-plugin/`. [6]
  - Test: `claude --plugin-dir ./my-first-plugin` (directory or `.zip`), `--plugin-url`, or `claude plugin init`. Validate with `claude plugin validate`. [6]
  - The manifest `skills` key adds scan directories. "A plugin with `SKILL.md` at its root, no `skills/`, and no `skills` key loads as a single skill". [6][7]
- Marketplace:
  - `.claude-plugin/marketplace.json` with `name`, `owner` and `plugins[]`; each entry has `name` and `source`. [7]
  - Install from a shell: `claude plugin marketplace add ./my-marketplace`, then `claude plugin install my-first-plugin@my-marketplace`.
  - In session: `/plugin` → **Discover** tab → choose a scope such as **Install for you (user scope)**. [7][6b]
- Plugin to claude.ai:
  - "The same plugin format also installs on claude.ai and in Cowork, where a different set of components loads". [6b]
  - claude.ai path: `Customize > Plugins` → **Add > Upload plugin** (".zip or .plugin file"), or **Add > Add marketplace** (a GitHub repo; private repos need the Claude GitHub App). [8]
  - Skills from an uploaded plugin load in chat, Cowork and Claude Code. Agents and hooks are "Ignored" in chat. [9]
  - A plugin installed on the account "also appears in Claude Code as a synced plugin" (`<name>@synced`). One installed "from the command line stays on that machine and isn't added to your account". [8][9][6c]

### Managed Agents (managed-agents/skills [11], Skills API guide [12], Create Skill reference [12b], ant apply [14])
- Upload: "a directory containing a `SKILL.md` file plus any supporting files, uploaded to your workspace as a zip archive or as individual files". It returns a `skill_*` ID. CLI: `ant apply skills/pr-summary`, which records the ID in `claude-lock.json`. [11][14]
- API requirements:
  - "Must include a `SKILL.md` file at the upload root (or at the top of a single enclosing folder)".
  - "Total upload size must be under 30 MB (uncompressed)".
  - `name` ≤64 characters, lowercase letters/numbers/hyphens, "no reserved words (`anthropic`, `claude`)"; `description` ≤1,024 characters, no XML tags.
  - Optional `display_name` ≤255 characters. [12][12b]
- Attach: agent `skills[]` entries `{type: anthropic|custom, skill_id, version}`, with `version` defaulting to `latest`. Up to 500 skills per session. [11] The Messages API allows a maximum of 20 skills per request. [12]
- Versions: custom versions are `skver_...`, and `"latest"` resolves to the newest. [12]
- GitHub discovery:
  - Exactly `.claude/skills/<skill-name>/SKILL.md` at the repo root, scanned at session start.
  - `skills/code-review/SKILL.md` ("a `skills` directory outside `.claude`") is explicitly not discovered.
  - "Repository skills use the same `SKILL.md` format as the custom skills you upload". [11]
- `ant apply` can also reference a skill by GitHub URL (`https://github.com/<owner>/<repo>/tree/<branch>/<dir>`) and uploads that directory pinned to a commit. [14]
- Runtime differences: API skills run with "No network access" and "No runtime package installation" (Messages API container) [12][10]. Managed Agents sandboxes follow the environment's networking settings (see a-managed-agents.md).
- Sharing scope: API custom skills are "Workspace-wide" [10].
- Data handling: skills are "not covered by ZDR"; "retained according to Anthropic's standard data retention policy". [10][12]

### Agent Skills spec (agentskills.io [13]; platform overview and best practices [10][10b])
- Required fields:
  - `name`: 1–64 characters, `a-z`, `0-9` and `-`; must not start or end with a hyphen and no `--`; "Must match the parent directory name".
  - `description`: 1–1,024 characters. [13]
- Optional fields:
  - `license`
  - `compatibility` (≤500 characters)
  - `metadata` (string→string map)
  - `allowed-tools` (space-separated string, "Experimental") [13]
- Body: no format restriction. "Keep your main `SKILL.md` under 500 lines". File references "one level deep". [13][10b]
- Platform additions: `name` "Cannot contain reserved words: `anthropic`, `claude`" and no XML tags. Descriptions should be written in third person. Use forward slashes in paths. Gerund naming is suggested. [10][10b]
- Level-1 metadata costs about 100 tokens per skill; the body loads when the skill is triggered. [10]

### anthropics/skills repository [15]
- Content: `skills/<name>/SKILL.md` folders, a `template/SKILL.md`, and `spec/agent-skills-spec.md`. The spec file now only points to agentskills.io/specification. [15]
- A root `.claude-plugin/marketplace.json` named `anthropic-agent-skills` declares plugins with `"source": "./"`, `"strict": false` and `"skills": ["./skills/xlsx", ...]`. The plain `skills/` tree is therefore served as a Claude Code plugin marketplace without moving the folders. [15]
- README install instructions, verbatim (L33–49):
  - "You can register this repository as a Claude Code Plugin marketplace by running the following command in Claude Code: `/plugin marketplace add anthropics/skills`".
  - Then select `Browse and install plugins` → `anthropic-agent-skills` → `document-skills` or `example-skills` → `Install now`.
  - Or `/plugin install document-skills@anthropic-agent-skills`.
  - For claude.ai the README links the support article. For the API it links the Skills API quickstart. [15]
- Example `skills/brand-guidelines/SKILL.md` (L1–5) has frontmatter `name: brand-guidelines`, a `description` and `license: Complete terms in LICENSE.txt`. That is three spec fields and nothing Claude Code-only. [15]
- Repo `skills/claude-api/SKILL.md` uses `name: claude-api`, which contains a word the platform docs call reserved for API uploads [10][12]. Whether that skill uploads through `/v1/skills` was not tested.

## Repositories pinned
| repo | HEAD SHA | commit date | licence file and its first line | what was read (paths, line ranges) |
|---|---|---|---|---|
| https://github.com/anthropics/skills | ca45fc496a3436251f191354091d557da31c15b5 | 2026-10-28 | No root LICENSE file. Per-skill `LICENSE.txt`: `skills/brand-guidelines/LICENSE.txt` first non-blank line "Apache License"; `skills/docx/LICENSE.txt` first line "© 2025 Anthropic, PBC. All rights reserved." (README L20: examples Apache 2.0; docx/pdf/pptx/xlsx "source-available, not open source") | `README.md` L1–96 (full); `.claude-plugin/marketplace.json` L1–60; `skills/brand-guidelines/SKILL.md` L1–30; `skills/claude-api/SKILL.md` L1–6; `template/SKILL.md` (full); `spec/agent-skills-spec.md` (full, 3 lines); `git ls-tree` listing |

## Could not verify
- **claude.ai skill ZIP size limit**: the support article says only "ZIP file exceeds size limits" [1]. No number appears on [1][2][3][4]. The 200 MB / 5,000-file limit applies to plugin uploads [9]. The 30 MB limit applies to the Skills API [12].
- **Description length on claude.ai**: support says 200 characters [2]; the claude.com docs and spec say 1,024 [4][13]. Which one the claude.ai uploader enforces was not tested.
- **`name` format on claude.ai**: the support example uses "Brand Guidelines" (capitals and a space) [2], while the claude.com docs require lowercase-hyphen matching the folder [4].
- **`dependencies` field**: listed as optional by support [2] but absent from the six-field allowlist that the Claude Code docs say claude.ai enforces [5]. Whether it is rejected was not verified.
- **Free plan**: whether skills are included on Free is inconsistent across pages [1] vs [3][10].
- **Mobile app with standalone uploaded skills**: stated only for plugin skills ("Chat on the web, desktop, and mobile") [8]. No page read says so for skills uploaded via `Customize > Skills`.
- **Symlink into `.claude/skills/` in a mounted GitHub repo** (for Managed Agents discovery): not documented on [11]. Claude Code personal and project locations do follow symlinked folders [5].
- **Skills API rejection of Claude Code-only fields**: stated by the Claude Code docs [5]. The Skills API guide lists only `name` and `description` rules [12]. Not tested.
- **`agents-and-tools` "Skills API" page**: no page with that name exists under agents-and-tools in llms.txt. The Skills API guide lives at `build-with-claude/skills-guide` [12], which was read (creating, versioning, limits, data retention sections). The agent-skills `quickstart` and `enterprise` pages were not read.

## Relevance to MEGAMIND
- **One source folder serves all three targets with constraints.** A repo-root `skills/<name>/SKILL.md` tree can be published as follows:
  - claude.ai: zip each folder (`zip -r <name>.zip <name>/`) [4].
  - Claude Code: add a root `.claude-plugin/marketplace.json` that uses `source: "./"`, `strict: false` and `skills: ["./skills/<name>"]`, the anthropics/skills pattern [15][7].
  - Managed Agents: `ant apply skills/<name>`, or zip to `/v1/skills` [11][14].
- **Frontmatter must stay inside the six spec fields** (`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`), or claude.ai and API uploads fail [5].
  - `name` = folder name, lowercase-hyphen, ≤64 characters, without "claude" or "anthropic" [12][13].
  - `description` ≤1,024 characters per spec; ≤200 if the support article's limit applies [2].
  - No `!`-injection and no reliance on `${CLAUDE_SKILL_DIR}`; use relative paths [4][5].
  - Bundle under 30 MB [12].
- **Forced variants:**
  - Managed Agents GitHub auto-discovery needs `.claude/skills/<name>/`, not `skills/<name>/` [11]. Use upload instead, or keep (or copy) the tree under `.claude/skills/`. That path also makes them Claude Code project skills [5].
  - Any Claude Code-only frontmatter (`disable-model-invocation`, `hooks`, `context: fork`, `paths`, …) would need a Claude Code-only copy [5].
- **Install paths the owner would use (labels as printed):**
  - claude.ai: `Customize > Skills` → `"+"` → `"+ Create skill"` → `"Upload a skill"` [1].
  - claude.ai plugin route: `Customize > Plugins` → `Add > Upload plugin` [8].
  - Claude Code: `/plugin marketplace add <repo>` → `/plugin install <plugin>@<marketplace>` [7][15], or copy into `~/.claude/skills/` [5].
  - Managed Agents: `ant apply skills/<name>` + `skills: [../skills/<name>]` in the agent file [14].
- **Sync shortcut:** installing the skill or plugin once on the claude.ai account syncs it one-way into Claude Code terminal sessions signed in with that account [1][5][8]. It does not reach the Managed Agents workspace, which needs its own upload [10][11].

## Sources
[1] https://support.claude.com/en/articles/12512180-using-skills-in-claude (redirected to …-use-skills-in-claude) — read 2026-11-02
[2] https://support.claude.com/en/articles/12512198-how-to-create-custom-skills — read 2026-11-02
[3] https://claude.com/docs/skills/overview.md — read 2026-11-02
[4] https://claude.com/docs/skills/how-to.md — read 2026-11-02
[5] https://code.claude.com/docs/en/skills.md — read 2026-11-02 (Getting started, Choose where skills load, Skills synced from claude.ai, Configure skills/frontmatter reference, Add supporting files, Control who invokes, Pre-approve tools, Share skills, Troubleshooting)
[6] https://code.claude.com/docs/en/plugins/create.md — read 2026-11-02 (Create your first plugin, Plugin layout, Develop without a marketplace)
[6b] https://code.claude.com/docs/en/plugins/overview.md — read 2026-11-02
[6c] https://code.claude.com/docs/en/plugins/install.md — read 2026-11-02 (Install a plugin, Plugins from your claude.ai account)
[7] https://code.claude.com/docs/en/plugins/create-marketplace.md — read 2026-11-02 (Create a marketplace, Add plugin entries); also https://code.claude.com/docs/en/plugins/components.md (Skills section) and https://code.claude.com/docs/en/plugins/manifest-reference.md (`skills` key rows, grep) — read 2026-11-02
[8] https://claude.com/docs/plugins/overview.md — read 2026-11-02
[9] https://claude.com/docs/plugins/platform-support.md — read 2026-11-02
[10] https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md — read 2026-11-02
[10b] https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md — read 2026-11-02 (Skill structure, naming, descriptions, progressive disclosure; checklist lines grepped)
[11] https://platform.claude.com/docs/en/managed-agents/skills.md — read 2026-11-02
[12] https://platform.claude.com/docs/en/build-with-claude/skills-guide.md — read 2026-11-02 (Creating a Skill + Requirements, Versioning, How Skills are loaded, Limits and constraints, Data retention)
[12b] https://platform.claude.com/docs/en/api/skills/create.md — read 2026-11-02
[13] https://agentskills.io/specification.md — read 2026-11-02
[14] https://platform.claude.com/docs/en/cli-sdks-libraries/cli/apply.md — read 2026-11-02
[15] https://github.com/anthropics/skills — cloned at ca45fc496a3436251f191354091d557da31c15b5 (2026-10-28) — read 2026-11-02
