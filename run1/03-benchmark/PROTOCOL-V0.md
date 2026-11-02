# PROTOCOL V0 — raw-only control (grep + read of the original sources; no wiki, no index)

You answer benchmark questions about a small documentation vault. Follow this sheet exactly; it is all you need.

## Rules
1. The questions are in `/workspace/megamind-fleet/run1/03-benchmark/questions.md`. Read that file once with your normal file tool. It is the **only** file you may open directly.
2. Touch the vault **only** through the harness command `q`. Do not use cat, grep, rg, ls, find, head, a file-read tool, web search or your own memory of the documents. Anything you did not see printed by `q` is not evidence.
3. Allowed `q` subcommands in V0: `q grep`, `q read` (raw/ only), plus `q start` and `q answer`. Anything else prints `REFUSED: …` and is logged; do not retry a refused command in another form.
4. At most **8** `q` calls per question between `q start` and `q answer`. After the 8th call the harness refuses everything except `q answer`; answer with what you have.
5. Answer only from what `q` printed. If it did not show the answer, say so: answer `unknown` (e.g. `q answer Q05 "unknown" --pages "" --confidence low`). Never guess.
6. One question at a time, in the order of `questions.md`: `q start`, your calls, `q answer`, then the next question.
7. The wiki, `index.md` and the search tools do not exist for you. Sources are grouped as `raw/unraid`, `raw/ollama`, `raw/syncthing`, `raw/tailscale`, `raw/claude-code`, `raw/qmd`, `raw/manual` (a receiver owner's manual, `.txt`) and `raw/lab` (`raw/lab/LAB-STATE.md`, a fictional home lab's state file).

## Setup (once, before the first question)
```bash
eval "$(/workspace/megamind-fleet/run1/03-benchmark/bin/new-run V0 MODEL)"
```
Replace `MODEL` with `haiku` or `sonnet` (whatever the director told you). This prints and sets
`export MM_RUN=/workspace/megamind-fleet/run1/03-benchmark/results/V0-MODEL MM_VARIANT=V0 PATH=/workspace/megamind-fleet/run1/03-benchmark/bin:$PATH`.
If it says `refusing: … already has a non-empty log.jsonl`, the run was started earlier: do not delete anything; ask the director.

**If your shell does not keep variables between commands** (each tool call is a fresh shell), put the export in front of every command:
```bash
export MM_RUN=/workspace/megamind-fleet/run1/03-benchmark/results/V0-MODEL MM_VARIANT=V0 PATH=/workspace/megamind-fleet/run1/03-benchmark/bin:$PATH; q start Q01
```

## Per question
```bash
q start Q01
q grep '<distinctive term>' [raw/<group>]
q read raw/<group>/<file> <start>-<end>
q answer Q01 "<answer in one to three sentences>" --pages raw/syncthing/firewall.md --confidence high
```
- `--pages`: comma-separated list of the raw files (e.g. `raw/syncthing/firewall.md`) your answer rests on (only ones `q` actually showed you). Use `--pages ""` if none.
- `--confidence`: `high` (the text states it directly), `medium` (you combined or inferred), `low` (partial or unknown).
- Put the answer in double quotes; avoid double quotes and tabs inside it.

## Reading order for V0
1. Pick the most distinctive word or phrase in the question (a product term, flag, setting name) and run `q grep '<term>'`. If you know the product, restrict it: `q grep '<term>' raw/tailscale`.
2. Too many hits: narrow the pattern or the group, or use `--max-count 20`. No hits: try a synonym or a shorter stem.
3. Read around the best hit with a line range (about 20–60 lines), e.g. `q read raw/unraid/shares.md 150-200`. Do not read a whole large file.
4. Lab questions (hosts, services, "what needs X", "what breaks if X"): `q read raw/lab/LAB-STATE.md` (it is short) and answer from it.
5. Stop as soon as the text states the answer; answer and cite the raw file(s).

## Commands available in V0
- `q grep <pattern> [raw/<group>] [--max-count N]` — case-insensitive ripgrep over `raw/` (or one group such as `raw/syncthing`). Prints `path:line:text`, at most 60 lines (or N ≤ 60). The pattern is a regular expression; quote it.
- `q read raw/<group>/<file> [start-end]` — prints a source file with line numbers. Big files are cut at 12,000 characters; the last line tells you the next range, e.g. `[truncated] next: q read raw/claude-code/hooks.md 141-`. Prefer a range around the lines `q grep` found, e.g. `q read raw/ollama/faq.md 300-340`. PDFs are refused; read the `.txt` beside them.
