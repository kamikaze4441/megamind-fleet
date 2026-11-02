# PROTOCOL V7 — index-first file navigation (index → wikilinks → grep/ls; no search engine, no deps tools)

You answer benchmark questions about a small documentation vault. Follow this sheet exactly; it is all you need.

## Rules
1. The questions are in `/workspace/megamind-fleet/run1/03-benchmark/questions.md`. Read that file once with your normal file tool. Apart from this sheet, it is the **only** file you may open directly.
2. Touch the vault **only** through the harness command `q`. Do not use cat, grep, rg, ls, find, head, a file-read tool, web search or your own memory of the documents. Anything you did not see printed by `q` is not evidence.
3. Allowed `q` subcommands in V7: `q index`, `q read` (wiki pages), `q grep` (wiki/ only), `q ls` (wiki/ only), plus `q start` and `q answer`. Anything else prints `REFUSED: …` and is logged; do not retry a refused command in another form.
4. At most **8** `q` calls per question between `q start` and `q answer`. After the 8th call the harness refuses everything except `q answer`; answer with what you have.
5. Answer only from what `q` printed. If it did not show the answer, say so: answer exactly `unknown — not in the wiki`, then one short sentence naming the kind of source that would be needed, e.g. `q answer Q05 "unknown — not in the wiki. Would need: the product's official configuration reference." --pages "" --confidence low`. Never guess.
6. One question at a time, in the order of `questions.md`: `q start`, your calls, `q answer`, then the next question.
7. Wiki conventions: each page lists its sources in `derived_from::` lines. Lab pages (the fictional home lab "lab77") carry `depends_on:: [[page]] (reason)` lines: *this subject fails or degrades without that page's subject*. **Everything below a `## Superseded` heading is history, not current state — ignore it.**
8. "What does X need?" = X's own `depends_on::` lines. "What needs X?" / "What breaks if X stops?" = the pages whose `depends_on::` names X; include the second hop (things that need those) when the question asks what breaks, and say which are direct.

## Setup (once, before the first question)
```bash
eval "$(/workspace/megamind-fleet/run1/03-benchmark/bin/new-run V7 MODEL)"
```
Replace `MODEL` with `haiku` or `sonnet` (whatever the director told you). This prints and sets
`export MM_RUN=/workspace/megamind-fleet/run1/03-benchmark/results/V7-MODEL MM_VARIANT=V7 PATH=/workspace/megamind-fleet/run1/03-benchmark/bin:$PATH`.
If it says `refusing: … already has a non-empty log.jsonl`, the run was started earlier: do not delete anything; ask the director.

**If your shell does not keep variables between commands** (each tool call is a fresh shell), put the export in front of every command:
```bash
export MM_RUN=/workspace/megamind-fleet/run1/03-benchmark/results/V7-MODEL MM_VARIANT=V7 PATH=/workspace/megamind-fleet/run1/03-benchmark/bin:$PATH; q start Q01
```

## Per question
```bash
q start Q01
q index
q read wiki/<slug>.md      # then follow [[links]]
q grep '<exact term>' wiki
q answer Q01 "<answer in one to three sentences>" --pages unraid-shares.md --confidence high
```
- `--pages`: comma-separated list of the wiki pages (e.g. `atlas.md`) your answer rests on (only ones `q` actually showed you). Use `--pages ""` if none.
- `--confidence`: `high` (the text states it directly), `medium` (you combined or inferred), `low` (partial or unknown).
- Put the answer in double quotes; avoid double quotes and tabs inside it.

## Reading order for V7
1. `q index` (always first). It is the map: one line per page, grouped by topic.
2. `q read` the page whose summary fits best. Follow `[[wikilinks]]` on it with `q read <slug>` when the answer points elsewhere.
3. For an exact term, flag, number or name, use `q grep '<term>' wiki` to find the page and line; then read that page (a line range is fine).
4. `q ls` (or `q ls 'wiki/<prefix>*'`) when you need the list of page names.
5. Lab dependency questions: read the lab page (its `depends_on::` lines above `## Superseded`); for "what needs X" run `q grep 'depends_on:: \[\[X\]\]' wiki` and drop any hit that sits below a `## Superseded` heading in its file (check by reading that file).
6. Stop as soon as a page states the answer. If the index, the pages you read and a grep all come back without it, give the scripted refusal (rule 5).

## Commands available in V7
- `q index` — prints `index.md`: every wiki page with a one-line summary, grouped by category.
- `q read wiki/<slug>.md [start-end]` — prints a wiki page with line numbers (`q read atlas` and `q read [[atlas]]` also work). Optional line range, e.g. `q read wiki/atlas.md 10-30`.
- `q grep <pattern> [wiki] [--max-count N]` — case-insensitive ripgrep over `wiki/`. Prints `path:line:text`, at most 60 lines (or N ≤ 60). The pattern is a regular expression; quote it.
- `q ls [wiki | glob]` — lists wiki file names, e.g. `q ls wiki` or `q ls 'wiki/claude-code-*'` (at most 200 lines).
