# Benchmark 03 — retrieval protocols over a Karpathy-style LLM wiki (run 1)

`$B` = `/workspace/megamind-fleet/run1/03-benchmark`. CPU is shared and unknown; timings are indicative only.

## Layout
| path | what |
|---|---|
| `environment.md` | sandbox facts, tool versions, qmd models and index timings, failures |
| `corpus.md` | every source: URL, licence/terms, fetch date, raw path, bytes, wiki pages it fed |
| `raw/` | frozen corpus (36 sources, 37 files); `raw.sha256` holds the checksums |
| `vault/` | the vault the queriers use: `raw` (symlink to `../raw`), `wiki/` (37 pages), `index.md`, `log.md`, `deps/` (generated) |
| `vault-notes.md` | builder notes: ingest procedure, Superseded fixtures (which page), edge list, gaps |
| `PROTOCOL-V0.md` … `PROTOCOL-V7.md` | self-contained instruction sheets for queriers, one per variant |
| `questions.md` | the auditor's questions (the answer key is held by the auditor, not here) |
| `bin/q` | query harness — the only interface a querier has to the vault |
| `bin/new-run` | creates `results/<variant>-<model>/` (empty `log.jsonl`, `answers.tsv` header) and clears qmd's query cache |
| `bin/metrics.py` | per-question metrics → `<run>/metrics.tsv` |
| `bin/build-deps.py` | regenerates `vault/deps/` from `depends_on::` lines |
| `bin/lint-wiki.py` | wiki fidelity/structure lint |
| `bin/make-bench-fixture.py` | TSV → `qmd bench` fixture JSON |
| `harness/` | corpus fetcher, corpus.md and protocol generators, `selftest.sh`, logs (`logs/qmd-embed.log`) |
| `results/` | one directory per run; `_selftest-V*` are the builder's trial runs, `_selftest-transcript.txt` their full transcript |

## Variants (allowed-set table; the same table is `VARIANTS` in `bin/q`)
| variant | subcommands besides `start`/`answer` | `q read` may open | `q grep` / `q ls` scope |
|---|---|---|---|
| V0 raw-only control | `grep`, `read` | `raw/` | grep: `raw/` |
| V1 index + read | `index`, `read` | `wiki/`, `index.md` | — |
| V2 + BM25 | `index`, `search`, `read` | `wiki/`, `index.md` | — |
| V3 + vector | `index`, `vsearch`, `read` | `wiki/`, `index.md` | — |
| V4 + hybrid | `index`, `query`, `read` | `wiki/`, `index.md` | — |
| V5 = V4 + deps | `index`, `query`, `read`, `deps` | `wiki/`, `index.md` | — |
| V6 = V5 + depsview | `index`, `query`, `read`, `deps`, `depsview` | `wiki/`, `index.md`, `deps/` | — |
| V7 index-first navigation | `index`, `read`, `grep`, `ls` | `wiki/`, `index.md` | grep and ls: `wiki/` |

To add a variant (e.g. V8): add one row to `VARIANTS` in `bin/q`, extend the `V[0-7]` pattern in `bin/new-run`, add a block to `harness/make-protocols.py` and re-run it.

Harness limits (all variants): output of any call capped at 12,000 characters (ends with `[truncated]`, plus the next line range for `q read`); `q grep` ≤ 60 lines (`--max-count N`, N ≤ 60); `q ls` ≤ 200 lines; at most 8 calls per question between `q start` and `q answer` (calls refused because the subcommand is not allowed in the variant are logged but do not count toward the 8); qmd commands run `qmd search|vsearch|query --no-rerank -n 5 -c wiki --json`, printed as `wiki/<slug>.md:<line> score <s> <title>` + a 240-character snippet.

## Run a querier
A querier gets one file: its `PROTOCOL-V<n>.md` (it also reads `questions.md`). What it runs first:
```bash
eval "$($B/bin/new-run V4 haiku)"       # prints and sets: export MM_RUN=$B/results/V4-haiku MM_VARIANT=V4 PATH=$B/bin:$PATH
q start Q01
q query "which allocation method is the default for a new user share"
q read wiki/unraid-shares.md
q answer Q01 "High-water (recommended)." --pages unraid-shares.md --confidence high
```
If each tool call is a fresh shell, prefix every command with `export MM_RUN=$B/results/V4-haiku MM_VARIANT=V4 PATH=$B/bin:$PATH;`.
Every call appends `{ts, ts_ns, qid, variant, cmd, args, bytes_out, chars_out, ms, refused}` to `$MM_RUN/log.jsonl`; answers go to `$MM_RUN/answers.tsv` (`qid answer pages confidence`).

## Metrics
```bash
$B/bin/metrics.py $B/results/V4-haiku                          # writes results/V4-haiku/metrics.tsv
$B/bin/metrics.py $B/results/V4-haiku --expected expected.tsv  # adds expected-page recall per question
```
`expected.tsv`: `qid<TAB>page1.md,page2.md`. Recall = |expected ∩ (pages read ∪ pages cited)| / |expected|. "Tokens" in metrics.tsv is the harness proxy (characters printed ÷ 4), not Console usage.

## qmd
Collection `wiki` = `vault/wiki/**/*.md` only (raw/ is not indexed):
```bash
qmd collection add $B/vault/wiki --name wiki
qmd embed
qmd ls wiki
```
Retrieval quality with `qmd bench` once the auditor releases the key:
```bash
$B/bin/make-bench-fixture.py key.tsv $B/results/qmd-bench-fixture.json      # key.tsv: qid<TAB>question<TAB>expected_pages
qmd ls wiki                                                                 # bench reports zeros silently if the collection is missing
qmd bench $B/results/qmd-bench-fixture.json -c wiki --json > $B/results/qmd-bench.json
```
`qmd bench` always runs four backends (bm25, vector, hybrid, full); `full` uses the reranker model. A two-question trial is in `results/_selftest-bench/`.

## Rebuild steps (builder)
```bash
python3 $B/bin/lint-wiki.py          # 0 errors expected
python3 $B/bin/build-deps.py         # regenerates vault/deps/
(cd /tmp && qmd update && qmd embed) # after wiki edits
bash $B/harness/selftest.sh          # re-runs the protocol self-tests into results/_selftest-*
```
