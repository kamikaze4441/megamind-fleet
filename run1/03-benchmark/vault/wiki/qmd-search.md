---
tags: [qmd, search, bm25, embeddings, tooling]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/qmd/README.md]
---
# QMD (Query Markup Documents) local search

QMD is an on-device search engine for markdown notes and documentation. It combines BM25 full-text search, vector semantic search, and LLM re-ranking, all running locally via node-llama-cpp with GGUF models. Install with `npm install -g @tobilu/qmd`.

## Commands
- Collections: `qmd collection add ~/notes --name notes` (optional `--mask "**/*.md"`), `qmd collection list`, `qmd ls notes`. Context: `qmd context add qmd://notes "Personal notes and ideas"`.
- Embeddings: `qmd embed` (900 tokens/chunk, 15% overlap); `qmd embed -f` re-embeds everything.
- `qmd search` — BM25 full-text search only (no LLM).
- `qmd vsearch` — vector semantic search only.
- `qmd query` — hybrid: FTS + vector + query expansion + re-ranking; `--no-rerank` skips LLM reranking (RRF scores only; faster on CPU).
- `qmd get "docs/api-reference.md"` or by docid `qmd get "#abc123"`; `qmd multi-get "journals/2025-05*.md"`.
- Options: `-n <num>` (default: 5, or 20 for --files/--json), `-c` collection, `--all`, `--min-score`, `--full`, `--format <kind>` (cli, json, csv, md, xml, files), `--full-path`, `--explain`.
- Maintenance: `qmd status`, `qmd update`, `qmd cleanup`. MCP server: `qmd mcp` (or `qmd mcp --http`, default `localhost:8181`).

## Pipeline
Query expansion (fine-tuned model) produces typed sub-queries: `lex` goes to BM25/FTS, `vec` and `hyde` go to vector search. Results are fused with Reciprocal Rank Fusion, `score = Σ(1/(k+rank+1))` where k=60; the original query gets ×2 weight; documents ranking #1 get +0.05, #2-3 get +0.02; the top 30 candidates are reranked, then blended by position (RRF rank 1-3: 75% retrieval, 25% reranker; 4-10: 60/40; 11+: 40/60).

## Models (auto-downloaded to `~/.cache/qmd/models/`)
| Model | Purpose | Size |
|---|---|---|
| `embeddinggemma-300M-Q8_0` | Vector embeddings (default) | ~300MB |
| `qwen3-reranker-0.6b-q8_0` | Re-ranking | ~640MB |
| `qmd-query-expansion-1.7B-q4_k_m` | Query expansion | ~1.1GB |
Override embeddings with `QMD_EMBED_MODEL` and re-run `qmd embed -f`. Requires Node.js >= 22. Index stored in `~/.cache/qmd/index.sqlite`; config in `~/.config/qmd/index.yml`.

## Benchmarking
`qmd bench my-fixture.json -c my-collection` runs each query against four backends — `bm25`, `vector`, `hybrid` (no reranking) and `full` — and reports precision@k, recall, MRR and F1. A fixture is JSON with `description`, `version`, `collection` and `queries` (`id`, `query`, `type`, `expected_files`, `expected_in_top_k`); `expected_files` are collection-relative paths as shown by `qmd ls`. If the collection isn't indexed, bench reports all zeros with no warning.

In this lab the wiki search service on [[hermes]] runs qmd ([[wiki-search]]).

derived_from:: [[raw/qmd/README.md]]
