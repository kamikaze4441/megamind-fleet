# PROTOCOL V6 — V5 + `q depsview` (generated two-hop dependency view)

You answer benchmark questions about a small documentation vault. Follow this sheet exactly; it is all you need.

## Rules
1. The questions are in `/workspace/megamind-fleet/run1/03-benchmark/questions.md`. Read that file once with your normal file tool. It is the **only** file you may open directly.
2. Touch the vault **only** through the harness command `q`. Do not use cat, grep, rg, ls, find, head, a file-read tool, web search or your own memory of the documents. Anything you did not see printed by `q` is not evidence.
3. Allowed `q` subcommands in V6: `q index`, `q query`, `q read` (wiki pages), `q deps`, `q depsview`, plus `q start` and `q answer`. Anything else prints `REFUSED: …` and is logged; do not retry a refused command in another form.
4. At most **8** `q` calls per question between `q start` and `q answer`. After the 8th call the harness refuses everything except `q answer`; answer with what you have.
5. Answer only from what `q` printed. If it did not show the answer, say so: answer `unknown` (e.g. `q answer Q05 "unknown" --pages "" --confidence low`). Never guess.
6. One question at a time, in the order of `questions.md`: `q start`, your calls, `q answer`, then the next question.
7. Wiki conventions: each page lists its sources in `derived_from::` lines. Lab pages (the fictional home lab "lab77") carry `depends_on:: [[page]] (reason)` lines: *this subject fails or degrades without that page's subject*. **Everything below a `## Superseded` heading is history, not current state — ignore it.**
8. "What does X need?" = X's own `depends_on::` lines. "What needs X?" / "What breaks if X stops?" = the pages whose `depends_on::` names X; include the second hop (things that need those) when the question asks what breaks, and say which are direct.

## Setup (once, before the first question)
```bash
eval "$(/workspace/megamind-fleet/run1/03-benchmark/bin/new-run V6 MODEL)"
```
Replace `MODEL` with `haiku` or `sonnet` (whatever the director told you). This prints and sets
`export MM_RUN=/workspace/megamind-fleet/run1/03-benchmark/results/V6-MODEL MM_VARIANT=V6 PATH=/workspace/megamind-fleet/run1/03-benchmark/bin:$PATH`.
If it says `refusing: … already has a non-empty log.jsonl`, the run was started earlier: do not delete anything; ask the director.

**If your shell does not keep variables between commands** (each tool call is a fresh shell), put the export in front of every command:
```bash
export MM_RUN=/workspace/megamind-fleet/run1/03-benchmark/results/V6-MODEL MM_VARIANT=V6 PATH=/workspace/megamind-fleet/run1/03-benchmark/bin:$PATH; q start Q01
```

## Per question
```bash
q start Q01
q depsview <slug>        # dependency questions
q query <question>       # all other questions
q read wiki/<slug>.md
q answer Q01 "<answer in one to three sentences>" --pages hermes.md --confidence high
```
- `--pages`: comma-separated list of the wiki pages (e.g. `atlas.md`) your answer rests on (only ones `q` actually showed you). Use `--pages ""` if none.
- `--confidence`: `high` (the text states it directly), `medium` (you combined or inferred), `low` (partial or unknown).
- Put the answer in double quotes; avoid double quotes and tabs inside it.

## Reading order for V6
**Dependency questions** (what does X need, what needs X, what breaks/degrades if X stops — X is a lab host, device, pool or service):
1. `q depsview <slug of X>` (lab page name in lower case, e.g. `atlas`, `rclone-backup`; if unsure, `q index` first). It already shows two hops in both directions.
2. Use `q deps <slug>` or `q read wiki/<slug>.md` only if the view leaves something unclear.
3. Answer from the edge reasons; cite the lab pages whose edges you used (the page names in the view, as `<slug>.md`).

**All other questions:** as V4 —
1. `q query <the question in plain words, including its key terms>`.
2. `q read` the top 1–2 results.
3. Nothing useful: rephrase once, then `q index` and read the best page from its summaries.
4. Stop as soon as a page states the answer; answer and cite the page(s).

## Commands available in V6
- `q depsview <slug>` — the generated dependency view for a lab page: **Needs** (direct and second hop) and **Needed by** (direct and second hop), each edge with its reason.
- `q deps <slug>` — for a lab page (e.g. `q deps atlas`): its own `depends_on::` lines (**what it needs**) and the pages whose `depends_on::` names it (**what needs it**, one hop). Only current edges are shown.
- `q query <question in plain words>` — hybrid search (keywords + vectors, no reranking) over the wiki pages; prints the top 5 as `wiki/<slug>.md:<line> score <s> <title>` plus a short snippet. Takes several seconds.
- `q read wiki/<slug>.md [start-end]` — prints a wiki page with line numbers (`q read atlas` and `q read [[atlas]]` also work). Optional line range, e.g. `q read wiki/atlas.md 10-30`.
- `q index` — prints `index.md`: every wiki page with a one-line summary, grouped by category.
