# Mini-MEGAMIND benchmark — results and recommendation (run 1)

Director's judgement over the builder's harness logs (`results/*/metrics.tsv`), the auditor's grades (`grading/*.md`, `grading/summary.md`) and `qmd bench` (`results/qmd-bench.json`). Date: 2026-11-02. One run per variant, 30 questions, Haiku 5.5 for every variant and Sonnet 5.5 for V7; see Caveats before reading any number as more than indicative.

## The question

Which query protocol over the same Karpathy-style wiki (37 pages, `index.md`, `depends_on::` edges, qmd 2.8.3 over `wiki/` only) answers 20 factual and 10 dependency questions correctly with the fewest characters read (the token proxy) and the least wall time?

## Variants

| V | Protocol | Tools the querier may use |
| --- | --- | --- |
| V0 | raw-only control | `q grep` over `raw/`, `q read` of raw files; no wiki |
| V1 | index → pages | `q index`, `q read` wiki pages |
| V2 | index + BM25 | V1 + `qmd search` |
| V3 | index + vector | V1 + `qmd vsearch` |
| V4 | index + hybrid (no rerank) | V1 + `qmd query --no-rerank` |
| V5 | V4 + edges | V4 + `q deps <slug>` (page's `depends_on::` lines above `## Superseded` + one hop of `rg` backlinks) |
| V6 | V5 + generated view | V5 + `q depsview <slug>` (`deps/<slug>.md`, rebuilt from scratch) |
| V7 | index-first file navigation (Anthropic's knowledge-wiki quickstart pattern, `02-research/a-managed-agents.md`) | `q index`, wikilinks, `q read`, `q grep`/`q ls` over `wiki/`; scripted refusal |

## Results

Correctness is the auditor's (score: correct 1, partial 0.5, wrong/unknown 0). Tokens* = characters printed by the harness ÷ 4 (what the querier had to read; not Console usage). Wall = `q start` → `q answer`. Page recall = expected pages ∩ (read ∪ cited) / expected, from `grading/expected-pages.tsv` (V0: against the expected raw files).

| Run | Score /30 | Factual /20 | Dependency /10 | Unknowns (honest) | Median tokens* | Total tokens* | Median wall s | Total wall s | Median calls | Page recall (sum /30) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V0 Haiku | 28 | 18 | 10 | 2 (0: the manual has Q18, Q20) | 806 | 22,800 | 2.7 | 120 | 1 | 30.0 (raw files) |
| V1 Haiku | 27 | 17 | 10 | 2 (2) + Q14 wrong | 1,906 | 55,789 | 2.8 | 85 | 2 | 25.4 |
| V2 Haiku | 27 | 17 | 10 | 2 (2) + Q14 wrong | 662 | 19,609 | 4.2 | 136 | 2 | 25.8 |
| V3 Haiku | 27 | 17 | 10 | 3 (3) | 738 | 23,503 | 53.2 | 3,844 | 2 | 26.0 |
| V4 Haiku | 27 | 17 | 10 | 3 (3) | 617 | 22,105 | 88.5 | 3,616 | 2 | 26.6 |
| V5 Haiku | 26 | 17 | 9 | 2 (2) + Q14 wrong; Q26, Q30 partial | 417 | 17,571 | 17.2 | 2,769 | 2 | 26.8 |
| V6 Haiku | 26 | 17 | 9 | 2 (2) + Q14 wrong; Q26, Q27 partial | 426 | 21,072 | 9.8 | 2,758 | 1 | 28.7 |
| V7 Haiku | 27 | 17 | 10 | 3 (3) | 426 | 17,917 | 3.2 | 119 | 1 | 26.6 |
| V7 Sonnet | 27 | 17 | 10 | 3 (3); citation slips on Q22, Q26 | 1,974 | 55,007 | 7.8 | 266 | 2 | 26.6 |

Split by question type (medians):

| Run | Tokens* factual | Tokens* dependency | Wall s factual | Wall s dependency |
| --- | --- | --- | --- | --- |
| V0 Haiku | 625 | 806 | 3.1 | 2.5 |
| V1 Haiku | 2,038 | 1,706 | 2.2 | 3.3 |
| V2 Haiku | 802 | 446 | 4.1 | 4.8 |
| V3 Haiku | 764 | 645 | 139.6 | 18.2 |
| V4 Haiku | 562 | 617 | 107.9 | 66.2 |
| V5 Haiku | 475 | 234 | 103.1 | 5.1 |
| V6 Haiku | 680 | 243 | 67.3 | 3.7 |
| V7 Haiku | 651 | 298 | 2.6 | 4.4 |
| V7 Sonnet | 2,079 | 1,632 | 7.2 | 10.4 |

### `qmd bench` (retrieval only, 27 queries, top-k 3; the three facts the wiki lacks are excluded)

`qmd bench grading/bench-fixture.json -c wiki --json` → `results/qmd-bench.json`; 74 min wall on this CPU (the `full` backend alone ≈140 s per query). Queries are the question texts as written.

| Backend | recall@1 | recall@3 | recall@5 | MRR | avg latency |
| --- | --- | --- | --- | --- | --- |
| bm25 (`search`) | 0.04 | 0.04 | 0.04 | 0.04 | 1.8 ms |
| vector (`vsearch`) | 0.65 | 0.80 | 0.84 | 0.94 | 393 ms |
| hybrid (`query --no-rerank`) | 0.55 | 0.76 | 0.80 | 0.85 | 22.8 s |
| full (`query`, reranked) | 0.55 | 0.81 | 0.85 | 0.85 | 140 s |

Two facts behind the table. (i) **BM25 fails on question-shaped queries**: qmd's FTS5 search requires every term to match, so a full question returned nothing for 26 of 27 queries (the director re-ran the 27 questions by hand with the same result); the V2 querier found its pages (25.8/30 page recall) because it learned to send one distinctive keyword (`Modelfile`, `MagicDNS`, `setcap`), and several of its first multi-word calls returned "(no results)" (`results/V2-haiku/log.jsonl`). (ii) **Vector search itself is fast; the query-expansion model is the cost.** In `qmd bench` the vector backend averaged 393 ms per query, while the CLI's `vsearch` in V3 took 4–120 s because qmd 2.8.3 runs the 1.7B expansion model before the vector search (builder, `environment.md`). Hybrid and full add 20–140 s for no recall gain over vector on this corpus.


## Reading the numbers

1. **Correctness does not separate the wiki variants.** Every wiki variant scored 27/30 on Haiku: all 10 dependency questions right in every run, 17/20 factual. The three misses are the same three facts in every run — Q03, Q13, Q14 — which the auditor confirmed are absent from all 37 wiki pages (the builder condensed 1.77 MB of raw text into ~30 pages and lost them). V0 found two of those three in `raw/` and so scored 28, but missed two manual facts the wiki variants found. So on this corpus the wiki's coverage, not the search tool, bounds correctness: an ingest that keeps every number, flag and limit matters more than the retrieval mode.
2. **Tokens: edges and index-first navigation win; the bare index loses.** Reading `index.md` and then whole pages (V1) costs 3× the characters of any search variant because every question re-reads the index and a full page. The cheapest protocols were V5 (417 median) — its `q deps` output answers a dependency question in ~234 tokens — and V7/V6 (426); only V7 kept full dependency correctness. Among the search tools BM25 (V2, 662), hybrid (V4, 617) and vector (V3, 738) are close; the search results themselves are small, the page read dominates.
3. **Time: anything that runs qmd's LLM query expansion is 10–30× slower on CPU; the vector search alone is not.** In qmd 2.8.3 `vsearch` and `query` both load a 1.7B query-expansion model; on this shared 4-vCPU sandbox a single call took 4–120 s and several hit the 295 s tool timeout. BM25 (`search`) answered in 0.25 s per call. V7 (no qmd at all) was as fast as V0. The master prompt's rule — rerank off, the default mode set by `qmd bench` on the real vault — stands, and this run adds: on a 2-vCPU VM, `vsearch`/`query` are only acceptable if their expansion cache is warm or the expansion model can be disabled (`qmd bench`'s vector backend ran in 0.4 s per query and had the best MRR, 0.94); whether the CLI exposes a no-expansion vector search is not verified — check qmd's options on the VM before making any mode the default. BM25 needs keyword queries, not questions (bench: 0.04 recall on question text).
4. **Dependency questions: the pages' edges answered everything; the edge-walking tools over-propagated one weak edge.** V0–V4 and V7 (which read the lab pages and followed links by hand) answered all 10 dependency questions, including the stale edge planted under `## Superseded` (no run was fooled). V5 and V6 — the only runs with `q deps` / `q depsview` — were the only runs to lose dependency points (9/10 each): on Q26 ("what breaks if gate stops") both reported hermes, Plex, Syncthing and tank stopping "via atlas", because `atlas depends_on:: [[gate]]` exists with the reason "e-mail notifications go out through gate" and the tools walk every edge as a hard dependency two hops out; V6 also added gate to what Plex and hermes "need" (Q21, Q24). §7 rule 2 defines an edge as "fails **or degrades** without", so a mechanical walk cannot tell a fatal edge from a cosmetic one; a model reading the page with the reasons in view could, and did. The `q deps` output is the cheapest dependency path (234 tokens median) and the `deps/` view costs the same (243) with higher page recall (28.7 vs 26.8) — but under §5a's kill rule (the view must beat the `rg` arm on page recall *and* in `/query` on correct answers and tokens) neither tool earns its place yet: both lost correctness. The fix is in the edge grammar, not the tool: see `06-amendments.md` G1 (a severity word in the reason, `(fails: …)` / `(degrades: …)`, so a walker can stop at "degrades"). No re-run was possible within the budget.
5. **Sonnet on V7 was as correct as Haiku and read 4.6× more.** Sonnet opened more pages (median 2 calls vs 1, 1,974 tokens vs 426) for the same 27/30 — it verified more and cited pages it had only grepped (two citation slips noted by the auditor). For a read-mostly vault, Haiku with a tight protocol is the better default for querying; Sonnet earns its cost in synthesis, not retrieval. This matches §6's table.

## Recommendation

**Winner: V7 — index-first file navigation (Anthropic's knowledge-wiki pattern): read `index.md` once, follow wikilinks, `rg` within `wiki/`, read the dependency edges on the page itself.** It tied the best correctness of any wiki variant (27/30 on both Haiku and Sonnet, 10/10 on dependencies), read the fewest characters of the fully-correct runs (426 median), and was as fast as the raw-grep control (3.2 s median) because it runs no model. Runner-up for tokens: V5 (417) — but its edge walker cost a dependency point. BM25 (`qmd search`, V2) is the only search tool cheap enough on CPU today (0.25 s per call, 662 tokens). Concretely, for `/query` on the VM:

1. Read `index.md` once per session (not per question) — the index-first variants' advantage came from that; then follow wikilinks and `rg` within `wiki/`.
2. For "what needs X / what breaks if X": read the page's `depends_on::` lines above `## Superseded` with their reasons, then one hop of `rg` backlinks — read by the model, not expanded by a tool, until the edge reason carries a severity word (06 G1). This is §4's "the page plus `rg` backlinks at first"; the `deps/` view stays gated (§5a) — this run gives no reason to build it and one reason not to.
3. `qmd search` (BM25) with one to three distinctive keywords — never the question text — when the index and links do not lead to the page; vector search is the better fallback for natural-language questions (recall@3 0.80, MRR 0.94, 0.4 s per query in the bench) **if** qmd can run it without the 1.7B expansion step; `query --no-rerank`/reranking never on 2 vCPUs (22–140 s per query here for no recall gain).
4. Fix coverage before tuning retrieval: the ingest skill's fidelity rule (every number, flag, label and limit on a page appears verbatim in the cited raw file) should be paired with its inverse for the owner's priority sources — a lint that lists numbers and settings in `raw/` that no page carries ("concepts lacking a page", §7 rule 7, made concrete).

What this does **not** decide: the real vault's qmd default mode (that is Track A's `qmd bench` on the owner's golden set, §4); whether Sonnet's extra reading pays off on harder, multi-page questions (none were in this set); the VM's actual latency (2 vCPU, no contention from other runs).

## Caveats

- Sandbox CPU is shared and unknown ("Intel Xeon @ 2.10GHz", 4 vCPU); V3/V4 ran in parallel with each other and V5/V6 with each other and with V7-Sonnet, so their wall times include contention and tool timeouts; V0/V1/V2/V7 ran as a batch of four light runs. Treat wall times as ordinal.
- One run per variant; 30 questions; a single wiki built by one builder. Differences of one question are noise.
- The builder read `questions.md` after writing all pages and changed no page afterwards (`vault-notes.md`); the three facts the wiki lacks were therefore not tuned in or out.
- The token proxy counts characters the harness printed, not the models' context (the protocol sheet, the question list and the model's own reasoning are excluded, and the Console's per-thread tokens include them — read them off the Threads tab with the names in `09-cost.md`).
- Index-first variants benefit from a querier that remembers `index.md` across questions within one thread; a fresh session per question would pay the index read every time (V1's figures approximate that worst case).
- V0's page recall is measured against the expected raw files, not wiki pages.
- `qmd bench` measures retrieval of the expected page into the top 3, not answer correctness; dependency questions ask for several pages and penalise single-page retrieval.
- Sonnet ran only V7 (owner's budget steering at 03:15 Pacific ended the second re-run).
- The Managed Agents knowledge-wiki pattern (V7) was approximated with the same harness; the quickstart's own `_index.md` is generated by a "dream", MEGAMIND's `index.md` is hand-maintained (§7), which this run did not test.

## Files

`environment.md` · `corpus.md` · `raw.sha256` · `vault/` · `vault-notes.md` · `bin/q`, `bin/metrics.py`, `bin/build-deps.py`, `bin/make-bench-fixture.py` · `PROTOCOL-V0..V7.md` · `questions.md` · `grading/` (key, expected pages, per-run grades, summary) · `results/<variant>-<model>/{answers.tsv,log.jsonl,metrics.tsv}` · `results/qmd-bench.json`.
