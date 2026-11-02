#!/usr/bin/env python3
# Writes $B/PROTOCOL-V0.md … PROTOCOL-V7.md from one template so the shared rules stay identical across variants (measures nothing).
B = "/workspace/megamind-fleet/run1/03-benchmark"

COMMON_HEAD = """# PROTOCOL {v} — {title}

You answer benchmark questions about a small documentation vault. Follow this sheet exactly; it is all you need.

## Rules
1. The questions are in `{B}/questions.md`. Read that file once with your normal file tool. It is the **only** file you may open directly.
2. Touch the vault **only** through the harness command `q`. Do not use cat, grep, rg, ls, find, head, a file-read tool, web search or your own memory of the documents. Anything you did not see printed by `q` is not evidence.
3. Allowed `q` subcommands in {v}: {allowed}, plus `q start` and `q answer`. Anything else prints `REFUSED: …` and is logged; do not retry a refused command in another form.
4. At most **8** `q` calls per question between `q start` and `q answer`. After the 8th call the harness refuses everything except `q answer`; answer with what you have.
5. Answer only from what `q` printed. If it did not show the answer, say so: {unknown_rule}
6. One question at a time, in the order of `questions.md`: `q start`, your calls, `q answer`, then the next question.
{extra_rules}
## Setup (once, before the first question)
```bash
eval "$({B}/bin/new-run {v} MODEL)"
```
Replace `MODEL` with `haiku` or `sonnet` (whatever the director told you). This prints and sets
`export MM_RUN={B}/results/{v}-MODEL MM_VARIANT={v} PATH={B}/bin:$PATH`.
If it says `refusing: … already has a non-empty log.jsonl`, the run was started earlier: do not delete anything; ask the director.

**If your shell does not keep variables between commands** (each tool call is a fresh shell), put the export in front of every command:
```bash
export MM_RUN={B}/results/{v}-MODEL MM_VARIANT={v} PATH={B}/bin:$PATH; q start Q01
```

## Per question
```bash
q start Q01
{steps_short}
q answer Q01 "<answer in one to three sentences>" --pages {pages_example} --confidence high
```
- `--pages`: comma-separated list of the {page_kind} your answer rests on (only ones `q` actually showed you). Use `--pages ""` if none.
- `--confidence`: `high` (the text states it directly), `medium` (you combined or inferred), `low` (partial or unknown).
- Put the answer in double quotes; avoid double quotes and tabs inside it.

## Reading order for {v}
{order}

## Commands available in {v}
{commands}
"""

CMD = {
    "index": "- `q index` — prints `index.md`: every wiki page with a one-line summary, grouped by category.",
    "read_wiki": "- `q read wiki/<slug>.md [start-end]` — prints a wiki page with line numbers (`q read atlas` and `q read [[atlas]]` also work). Optional line range, e.g. `q read wiki/atlas.md 10-30`.",
    "read_raw": "- `q read raw/<group>/<file> [start-end]` — prints a source file with line numbers. Big files are cut at 12,000 characters; the last line tells you the next range, e.g. `[truncated] next: q read raw/claude-code/hooks.md 141-`. Prefer a range around the lines `q grep` found, e.g. `q read raw/ollama/faq.md 300-340`. PDFs are refused; read the `.txt` beside them.",
    "grep_raw": "- `q grep <pattern> [raw/<group>] [--max-count N]` — case-insensitive ripgrep over `raw/` (or one group such as `raw/syncthing`). Prints `path:line:text`, at most 60 lines (or N ≤ 60). The pattern is a regular expression; quote it.",
    "grep_wiki": "- `q grep <pattern> [wiki] [--max-count N]` — case-insensitive ripgrep over `wiki/`. Prints `path:line:text`, at most 60 lines (or N ≤ 60). The pattern is a regular expression; quote it.",
    "ls": "- `q ls [wiki | glob]` — lists wiki file names, e.g. `q ls wiki` or `q ls 'wiki/claude-code-*'` (at most 200 lines).",
    "search": "- `q search <words>` — BM25 keyword search over the wiki pages; prints the top 5 as `wiki/<slug>.md:<line> score <s> <title>` plus a short snippet.",
    "vsearch": "- `q vsearch <question in plain words>` — semantic (vector) search over the wiki pages; prints up to 5 results as `wiki/<slug>.md:<line> score <s> <title>` plus a short snippet. Takes several seconds.",
    "query": "- `q query <question in plain words>` — hybrid search (keywords + vectors, no reranking) over the wiki pages; prints the top 5 as `wiki/<slug>.md:<line> score <s> <title>` plus a short snippet. Takes several seconds.",
    "deps": "- `q deps <slug>` — for a lab page (e.g. `q deps atlas`): its own `depends_on::` lines (**what it needs**) and the pages whose `depends_on::` names it (**what needs it**, one hop). Only current edges are shown.",
    "depsview": "- `q depsview <slug>` — the generated dependency view for a lab page: **Needs** (direct and second hop) and **Needed by** (direct and second hop), each edge with its reason.",
}

WIKI_RULES = """7. Wiki conventions: each page lists its sources in `derived_from::` lines. Lab pages (the fictional home lab "lab77") carry `depends_on:: [[page]] (reason)` lines: *this subject fails or degrades without that page's subject*. **Everything below a `## Superseded` heading is history, not current state — ignore it.**
8. "What does X need?" = X's own `depends_on::` lines. "What needs X?" / "What breaks if X stops?" = the pages whose `depends_on::` names X; include the second hop (things that need those) when the question asks what breaks, and say which are direct.
"""
DEP_HINT_WIKI = "For lab dependency questions, read the lab page itself (its `depends_on::` lines and text above `## Superseded`); for \"what needs X\" you must find the pages that name X — use the index summaries and `[[links]]`."

UNKNOWN = 'answer `unknown` (e.g. `q answer Q05 "unknown" --pages "" --confidence low`). Never guess.'
UNKNOWN_V7 = ('answer exactly `unknown — not in the wiki`, then one short sentence naming the kind of source that would be needed, e.g. '
              '`q answer Q05 "unknown — not in the wiki. Would need: the product\'s official configuration reference." --pages "" --confidence low`. Never guess.')

V = {
 "V0": dict(title="raw-only control (grep + read of the original sources; no wiki, no index)",
    allowed="`q grep`, `q read` (raw/ only)", cmds=["grep_raw", "read_raw"], page_kind="raw files (e.g. `raw/syncthing/firewall.md`)",
    pages_example="raw/syncthing/firewall.md", extra_rules="7. The wiki, `index.md` and the search tools do not exist for you. Sources are grouped as `raw/unraid`, `raw/ollama`, `raw/syncthing`, `raw/tailscale`, `raw/claude-code`, `raw/qmd`, `raw/manual` (a receiver owner's manual, `.txt`) and `raw/lab` (`raw/lab/LAB-STATE.md`, a fictional home lab's state file).\n",
    steps="q grep '<distinctive term>' [raw/<group>]\nq read raw/<group>/<file> <start>-<end>",
    order="""1. Pick the most distinctive word or phrase in the question (a product term, flag, setting name) and run `q grep '<term>'`. If you know the product, restrict it: `q grep '<term>' raw/tailscale`.
2. Too many hits: narrow the pattern or the group, or use `--max-count 20`. No hits: try a synonym or a shorter stem.
3. Read around the best hit with a line range (about 20–60 lines), e.g. `q read raw/unraid/shares.md 150-200`. Do not read a whole large file.
4. Lab questions (hosts, services, "what needs X", "what breaks if X"): `q read raw/lab/LAB-STATE.md` (it is short) and answer from it.
5. Stop as soon as the text states the answer; answer and cite the raw file(s)."""),
 "V1": dict(title="index + read (no search, no grep)",
    allowed="`q index`, `q read` (wiki pages)", cmds=["index", "read_wiki"], page_kind="wiki pages (e.g. `atlas.md`)",
    pages_example="unraid-shares.md", extra_rules=WIKI_RULES,
    steps="q index\nq read wiki/<slug>.md",
    order="""1. `q index` (always first).
2. From the summaries pick the one page most likely to hold the answer and `q read wiki/<slug>.md`.
3. If it is not there, follow a `[[link]]` on that page or pick the next candidate from the index (at most 4 pages in total).
4. """ + DEP_HINT_WIKI + """
5. Stop as soon as a page states the answer; answer and cite the page(s)."""),
 "V2": dict(title="index + BM25 keyword search + read",
    allowed="`q index`, `q search`, `q read` (wiki pages)", cmds=["search", "read_wiki", "index"], page_kind="wiki pages (e.g. `atlas.md`)",
    pages_example="unraid-shares.md", extra_rules=WIKI_RULES,
    steps="q search <keywords>\nq read wiki/<slug>.md",
    order="""1. `q search <2–5 distinctive keywords>` (product name + the setting/term asked about). Keywords work better than full sentences.
2. If a snippet already states the answer, you may still `q read` that page once to confirm; then answer.
3. Otherwise `q read` the top 1–2 results.
4. Nothing useful: retry `q search` with synonyms once, then `q index` and read the best page from its summaries.
5. """ + DEP_HINT_WIKI + """
6. Stop as soon as a page states the answer; answer and cite the page(s)."""),
 "V3": dict(title="index + vector search + read",
    allowed="`q index`, `q vsearch`, `q read` (wiki pages)", cmds=["vsearch", "read_wiki", "index"], page_kind="wiki pages (e.g. `atlas.md`)",
    pages_example="unraid-shares.md", extra_rules=WIKI_RULES,
    steps="q vsearch <the question in plain words>\nq read wiki/<slug>.md",
    order="""1. `q vsearch <the question, rephrased in plain words>`.
2. `q read` the top 1–2 results (snippets alone are not enough to cite).
3. Nothing useful: `q index` and read the best page from its summaries.
4. """ + DEP_HINT_WIKI + """
5. Stop as soon as a page states the answer; answer and cite the page(s)."""),
 "V4": dict(title="index + hybrid search (no rerank) + read",
    allowed="`q index`, `q query`, `q read` (wiki pages)", cmds=["query", "read_wiki", "index"], page_kind="wiki pages (e.g. `atlas.md`)",
    pages_example="unraid-shares.md", extra_rules=WIKI_RULES,
    steps="q query <the question in plain words>\nq read wiki/<slug>.md",
    order="""1. `q query <the question in plain words, including its key terms>`.
2. `q read` the top 1–2 results.
3. Nothing useful: rephrase once with different key terms, then `q index` and read the best page from its summaries.
4. """ + DEP_HINT_WIKI + """
5. Stop as soon as a page states the answer; answer and cite the page(s)."""),
 "V5": dict(title="V4 + `q deps` for dependency questions",
    allowed="`q index`, `q query`, `q read` (wiki pages), `q deps`", cmds=["deps", "query", "read_wiki", "index"], page_kind="wiki pages (e.g. `atlas.md`)",
    pages_example="hermes.md", extra_rules=WIKI_RULES,
    steps="q deps <slug>            # dependency questions\nq query <question>       # all other questions\nq read wiki/<slug>.md",
    order="""**Dependency questions** (what does X need, what needs X, what breaks/degrades if X stops — X is a lab host, device, pool or service):
1. `q deps <slug of X>` (slugs are the lab page names in lower case, e.g. `atlas`, `rclone-backup`; if unsure, `q index` first).
2. "What breaks if X": for each page under *Needed by*, run `q deps <that page>` to get the second hop (stay within 8 calls).
3. Answer from the `depends_on::` reasons; `q read` a lab page only if a reason is unclear. Cite the lab pages whose edges you used.

**All other questions:** as V4 —
1. `q query <the question in plain words, including its key terms>`.
2. `q read` the top 1–2 results.
3. Nothing useful: rephrase once, then `q index` and read the best page from its summaries.
4. Stop as soon as a page states the answer; answer and cite the page(s)."""),
 "V6": dict(title="V5 + `q depsview` (generated two-hop dependency view)",
    allowed="`q index`, `q query`, `q read` (wiki pages), `q deps`, `q depsview`", cmds=["depsview", "deps", "query", "read_wiki", "index"], page_kind="wiki pages (e.g. `atlas.md`)",
    pages_example="hermes.md", extra_rules=WIKI_RULES,
    steps="q depsview <slug>        # dependency questions\nq query <question>       # all other questions\nq read wiki/<slug>.md",
    order="""**Dependency questions** (what does X need, what needs X, what breaks/degrades if X stops — X is a lab host, device, pool or service):
1. `q depsview <slug of X>` (lab page name in lower case, e.g. `atlas`, `rclone-backup`; if unsure, `q index` first). It already shows two hops in both directions.
2. Use `q deps <slug>` or `q read wiki/<slug>.md` only if the view leaves something unclear.
3. Answer from the edge reasons; cite the lab pages whose edges you used (the page names in the view, as `<slug>.md`).

**All other questions:** as V4 —
1. `q query <the question in plain words, including its key terms>`.
2. `q read` the top 1–2 results.
3. Nothing useful: rephrase once, then `q index` and read the best page from its summaries.
4. Stop as soon as a page states the answer; answer and cite the page(s)."""),
 "V7": dict(title="index-first file navigation (index → wikilinks → grep/ls; no search engine, no deps tools)",
    allowed="`q index`, `q read` (wiki pages), `q grep` (wiki/ only), `q ls` (wiki/ only)", cmds=["index", "read_wiki", "grep_wiki", "ls"], page_kind="wiki pages (e.g. `atlas.md`)",
    pages_example="unraid-shares.md", extra_rules=WIKI_RULES,
    steps="q index\nq read wiki/<slug>.md      # then follow [[links]]\nq grep '<exact term>' wiki",
    order="""1. `q index` (always first). It is the map: one line per page, grouped by topic.
2. `q read` the page whose summary fits best. Follow `[[wikilinks]]` on it with `q read <slug>` when the answer points elsewhere.
3. For an exact term, flag, number or name, use `q grep '<term>' wiki` to find the page and line; then read that page (a line range is fine).
4. `q ls` (or `q ls 'wiki/<prefix>*'`) when you need the list of page names.
5. Lab dependency questions: read the lab page (its `depends_on::` lines above `## Superseded`); for "what needs X" run `q grep 'depends_on:: \\[\\[X\\]\\]' wiki` and drop any hit that sits below a `## Superseded` heading in its file (check by reading that file).
6. Stop as soon as a page states the answer. If the index, the pages you read and a grep all come back without it, give the scripted refusal (rule 5)."""),
}

for v, d in V.items():
    text = COMMON_HEAD.format(
        v=v, title=d["title"], B=B, allowed=d["allowed"], extra_rules=d["extra_rules"],
        unknown_rule=UNKNOWN_V7 if v == "V7" else UNKNOWN,
        steps_short=d["steps"], pages_example=d["pages_example"], page_kind=d["page_kind"],
        order=d["order"], commands="\n".join(CMD[c] for c in d["cmds"]))
    open(f"{B}/PROTOCOL-{v}.md", "w").write(text)
    print("wrote", f"{B}/PROTOCOL-{v}.md", len(text))
