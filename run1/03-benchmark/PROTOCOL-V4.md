# PROTOCOL V4 — index + hybrid search (no rerank) + read

You answer benchmark questions about a small documentation vault. Follow this sheet exactly; it is all you need.

## Rules
1. The questions are in `/workspace/megamind-fleet/run1/03-benchmark/questions.md`. Read that file once with your normal file tool. It is the **only** file you may open directly.
2. Touch the vault **only** through the harness command `q`. Do not use cat, grep, rg, ls, find, head, a file-read tool, web search or your own memory of the documents. Anything you did not see printed by `q` is not evidence.
3. Allowed `q` subcommands in V4: `q index`, `q query`, `q read` (wiki pages), plus `q start` and `q answer`. Anything else prints `REFUSED: …` and is logged; do not retry a refused command in another form.
4. At most **8** `q` calls per question between `q start` and `q answer`. After the 8th call the harness refuses everything except `q answer`; answer with what you have.
5. Answer only from what `q` printed. If it did not show the answer, say so: answer `unknown` (e.g. `q answer Q05 "unknown" --pages "" --confidence low`). Never guess.
6. One question at a time, in the order of `questions.md`: `q start`, your calls, `q answer`, then the next question.
7. Wiki conventions: each page lists its sources in `derived_from::` lines. Lab pages (the fictional home lab "lab77") carry `depends_on:: [[page]] (reason)` lines: *this subject fails or degrades without that page's subject*. **Everything below a `## Superseded` heading is history, not current state — ignore it.**
8. "What does X need?" = X's own `depends_on::` lines. "What needs X?" / "What breaks if X stops?" = the pages whose `depends_on::` names X; include the second hop (things that need those) when the question asks what breaks, and say which are direct.

## Setup (once, before the first question)
```bash
eval "$(/workspace/megamind-fleet/run1/03-benchmark/bin/new-run V4 MODEL)"
```
Replace `MODEL` with `haiku` or `sonnet` (whatever the director told you). This prints and sets
`export MM_RUN=/workspace/megamind-fleet/run1/03-benchmark/results/V4-MODEL MM_VARIANT=V4 PATH=/workspace/megamind-fleet/run1/03-benchmark/bin:$PATH`.
If it says `refusing: … already has a non-empty log.jsonl`, the run was started earlier: do not delete anything; ask the director.

**If your shell does not keep variables between commands** (each tool call is a fresh shell), put the export in front of every command:
```bash
export MM_RUN=/workspace/megamind-fleet/run1/03-benchmark/results/V4-MODEL MM_VARIANT=V4 PATH=/workspace/megamind-fleet/run1/03-benchmark/bin:$PATH; q start Q01
```

## Per question
```bash
q start Q01
q query <the question in plain words>
q read wiki/<slug>.md
q answer Q01 "<answer in one to three sentences>" --pages unraid-shares.md --confidence high
```
- `--pages`: comma-separated list of the wiki pages (e.g. `atlas.md`) your answer rests on (only ones `q` actually showed you). Use `--pages ""` if none.
- `--confidence`: `high` (the text states it directly), `medium` (you combined or inferred), `low` (partial or unknown).
- Put the answer in double quotes; avoid double quotes and tabs inside it.

## Reading order for V4
1. `q query <the question in plain words, including its key terms>`.
2. `q read` the top 1–2 results.
3. Nothing useful: rephrase once with different key terms, then `q index` and read the best page from its summaries.
4. For lab dependency questions, read the lab page itself (its `depends_on::` lines and text above `## Superseded`); for "what needs X" you must find the pages that name X — use the index summaries and `[[links]]`.
5. Stop as soon as a page states the answer; answer and cite the page(s).

## Commands available in V4
- `q query <question in plain words>` — hybrid search (keywords + vectors, no reranking) over the wiki pages; prints the top 5 as `wiki/<slug>.md:<line> score <s> <title>` plus a short snippet. Takes several seconds.
- `q read wiki/<slug>.md [start-end]` — prints a wiki page with line numbers (`q read atlas` and `q read [[atlas]]` also work). Optional line range, e.g. `q read wiki/atlas.md 10-30`.
- `q index` — prints `index.md`: every wiki page with a one-line summary, grouped by category.
