# Environment (benchmark 03, run 1)

Recorded by builder B1 on 2026-11-02. **CPU is shared and unknown; timings are indicative only.**

## Sandbox

| fact | value | source |
|---|---|---|
| OS | Ubuntu 24.04.5 LTS, kernel 6.18.44-fc-v185 x86_64 (Firecracker-style VM) | `/etc/os-release`, `uname -a` |
| CPUs | 4 (`nproc`) | `nproc` |
| CPU model | `Intel(R) Xeon(R) Processor @ 2.10GHz` (generic name; exact SKU hidden); flags include avx2, avx512f, avx512_vnni, fma, f16c | `/proc/cpuinfo` |
| GPU | none (`nvidia-smi` not found) — qmd models run on CPU | |
| RAM | 16,477,352 kB (15 GiB), no swap | `/proc/meminfo`, `free -h` |
| Disk | `/dev/vda` 252G, 30G available at start | `df -h /` |
| user / HOME | root, `HOME=/root` (qmd cache therefore under `/root/.cache/qmd/`) | |
| npm global prefix | `/home/claude/.npm-global` (qmd binary `/home/claude/.npm-global/bin/qmd`) | `npm config get prefix` |

## Versions (`--version` output)

| tool | version |
|---|---|
| node | v22.22.0 |
| npm | 10.9.4 |
| qmd | `qmd 2.8.3 (facd35e)` — installed with `npm install -g @tobilu/qmd@2.8.3` (17.5 s wall, 159 packages). 2.8.3 is the newest version on npm (`npm view @tobilu/qmd versions` → … 2.5.3, 2.8.3), so no substitution was needed. |
| python3 | Python 3.11.17 (pypdf 3.17.4 present; html2text **not** installed — not needed, pandoc used) |
| ripgrep | ripgrep 14.1.0 |
| pandoc | pandoc 3.1.3 |
| pdftotext | pdftotext version 24.02.0 (poppler) |
| git | git version 2.43.0 |
| curl | curl 8.5.0 |

## qmd upstream (read-only clone, nothing executed)

- Clone: `GIT_LFS_SKIP_SMUDGE=1 git clone -q --depth 1 --filter=blob:none --no-checkout https://github.com/tobi/qmd /tmp/b1/qmd`
- HEAD `86d2365d17fc682e491c2c53d1e4a884aee8682a`, committed 2026-10-14T20:04:06-07:00 ("Merge pull request #1072 from tobi/types/check-whole-project").
- Licence: `MIT License` — `Copyright (c) 2024-2026 Tobi Lutke` (`git show HEAD:LICENSE`).
- The npm build reports commit `facd35e`, which differs from the clone HEAD `86d2365`; the README was read at HEAD, and the flags below were checked against `qmd --help` of the installed 2.8.3 binary: `search`, `vsearch`, `query`, `--no-rerank`, `-n`, `--format files|json`, `--full-path`, `bench`, `embed [-f] [-c]`, `pull` all present; `qmd --help` reports `Index: /root/.cache/qmd/index.sqlite`.

### Commands learned from the README (flags confirmed in `qmd --help`; behaviour verified in step 2)

| purpose | command |
|---|---|
| add collection | `qmd collection add <dir> --name <name> [--mask "**/*.md"]` |
| list files | `qmd ls <collection>` |
| embed | `qmd embed` (900 tokens/chunk, 15% overlap); `qmd embed -f` re-embeds |
| BM25 | `qmd search "<q>"` |
| vector | `qmd vsearch "<q>"` |
| hybrid | `qmd query "<q>" --no-rerank` (RRF only; README: "faster on CPU"; query expansion still runs) |
| output | `-n <num>` (default 5, or 20 for `--files`/`--json`), `--json`, `--files`, `--format cli|json|csv|md|xml|files`, `--full-path`, `--min-score`, `-c <collection>` |
| bench | `qmd bench <fixture.json> -c <collection> [--json]`; fixture = `{description, version: 1, collection, queries: [{id, query, type, expected_files, expected_in_top_k}]}`; backends bm25 / vector / hybrid / full |
| index location | `~/.cache/qmd/index.sqlite`; config `~/.config/qmd/index.yml` |

### Models (README table; actual downloads recorded in step 2)

| model | role | README size |
|---|---|---|
| `embeddinggemma-300M-Q8_0` | embeddings (vsearch, query, embed) | ~300MB |
| `qwen3-reranker-0.6b-q8_0` | rerank (not used: `--no-rerank`) | ~640MB |
| `qmd-query-expansion-1.7B-q4_k_m` | query expansion (`qmd query`) | ~1.1GB |

Cache: `~/.cache/qmd/models/` (= `/root/.cache/qmd/models/` here). Downloaded in step 2 (sizes from `ls -la`, bytes):

| file | downloaded by | bytes |
|---|---|---|
| `hf_ggml-org_embeddinggemma-300M-Q8_0.gguf` | first `qmd embed` | 333,590,944 |
| `hf_tobil_qmd-query-expansion-1.7B-q4_k_m.gguf` | first `qmd vsearch` (see note) | 1,282,438,912 |
| `hf_ggml-org_qwen3-reranker-0.6b-q8_0.gguf` | `qmd bench` (backend `full`) only; the harness never reranks | 639,153,184 |

## Index build (step 2)

Collection over `vault/wiki/` only (raw/ is not indexed); index `/root/.cache/qmd/index.sqlite` (3.4 MB after embedding):
```bash
qmd collection add /workspace/megamind-fleet/run1/03-benchmark/vault/wiki --name wiki   # 307 ms; "Indexed: 37 new"
qmd embed                                                                               # 28,682 ms wall incl. model download; "Embedded 51 chunks from 37 documents in 28s"
qmd ls wiki                                                                             # 37 files
```
Timings from `date +%s%N` around each command; log in `harness/logs/qmd-embed.log`. qmd warns "no GPU acceleration, running on CPU (slow)".

Verified (each returned results for a sample query, `-c wiki --json`):

| command (as the harness runs it) | sample query | results | wall time |
|---|---|---|---|
| `qmd search "<q>" -n 5 -c wiki --json` | `exit node approve` | 2 | 249 ms |
| `qmd vsearch "<q>" -n 5 -c wiki --json` | `what happens when the UPS battery runs low` | 1 (`apc-1.md`) | 29,046 ms first call (model download), 4,280 ms repeated |
| `qmd vsearch …` | `how do I make a container start after the database` | 5 | — |
| `qmd query "<q>" --no-rerank -n 5 -c wiki --json` | `what breaks if the UPS fails` | 5 (`apc-1.md` first) | 12,184 ms first, 4,616 ms repeated |
| `qmd query … --no-rerank` / `qmd vsearch …`, new queries | two new questions | 5 | 12,317–13,152 ms |

Observations that matter for the comparison:
- **In qmd 2.8.3 `vsearch` also runs LLM query expansion** (it prints `vec:`/`hyde:` sub-queries and loaded the 1.7B expansion model), although the README calls it "Vector semantic search only". So V3 and V4 both pay the expansion model on CPU (~4–13 s per new query); only `search` (BM25, V2) is LLM-free (~0.25 s).
- `vsearch` can return fewer than `-n 5` results (one result above).
- qmd caches expansions per query string (a repeated query took ~4.5 s instead of ~12 s). `bin/new-run` runs `qmd cleanup` (which reports "Cleared N cached API responses"; embeddings are kept) so a run does not inherit another run's cache. Within a run, repeating a query is a legitimate cache hit.
- Timings vary by more than 2× between identical-looking calls (one uncached `query` took 51.6 s during the harness smoke test, others 4–13 s): CPU is shared.

`qmd bench` (trial with 2 builder questions, `results/_selftest-bench/`): 148.7 s wall; per-query latency bm25 1–6 ms, vector 29–3,976 ms, hybrid 38–8,361 ms, full 59,810–75,937 ms. A 24-question bench therefore needs roughly 30 min, dominated by `full`.

## Vault build (step 2)

- karpathy-llm-wiki clone (read-only, nothing executed): `GIT_LFS_SKIP_SMUDGE=1 git clone -q --depth 1 --filter=blob:none --no-checkout https://github.com/Astro-Han/karpathy-llm-wiki /tmp/b1/kwiki`; HEAD `eafcc77001e496cc43499e4923b663aec722c813`, committed 2026-07-24T00:57:31+08:00 ("fix: align log inventory and examples"); `MIT License`, `Copyright (c) 2026 Yuhan Lei`. Files read: `SKILL.md`, `references/{article,index,raw,archive}-template.md`, `examples/log-sample.md`.
- 37 wiki pages (22 topic + 15 lab), `bin/lint-wiki.py`: 0 errors, 14 warnings (lab pages under 150 words).
- `bin/build-deps.py`: 37 pages, 22 edges, "22 pages have no edges".

## Notes on sources (step 1)

- `https://tailscale.com/kb/…` URLs now redirect to `https://tailscale.com/docs/…`; every article serves Markdown with `.md` appended (`https://tailscale.com/docs/llms.txt`). The six Tailscale sources were fetched from `/docs/…md`.
- `https://docs.ollama.com/api.md` redirects to `https://docs.ollama.com/api/introduction.md` (2.6 kB, short overview page); kept as the "API" source.
- `docs.unraid.net` has no `llms.txt` and no `.md` variants; pages were taken from `sitemap.xml` and converted from HTML.
- `docs.syncthing.net` is Sphinx HTML; converted from HTML.
- Manual: APC's manufacturer download (`se.com/…/download/document/…`) returned HTTP 403 to curl; the Denon AVR-X1700H owner's manual on `assets.denon.com` was used instead.

## Failures and deviations

Step 2:
- `qmd vsearch` is not LLM-free in 2.8.3 (see Index build); V3 is therefore "vector + query expansion", not pure vector search.
- Lab wiki pages are 69–186 words, below the 150–400 target, because the lab note gives 1–3 facts per subject; not padded.
- 37 pages instead of "about 30" (one page per lab host/service/device/pool gives 15 lab pages; 22 topic pages cover 36 sources).
- `ripgrep` honours `$B/.gitignore` (which ignores `raw/*`), so `q grep` and `q deps` run `rg --no-ignore`.
- Questions file `questions.md` lives in `$B/` and is readable by the builder; see `vault-notes.md` for when it was first opened.

Step 1:

- `curl https://www.se.com/us/en/download/document/SPD_ASTE-6Z7VA7_EN/` (APC Back-UPS manual) → HTTP 403. Not used.
- `api.github.com` rate-limited (unauthenticated) while checking repo licences; licences were read from the repos' LICENSE/README files instead.
- One Tailscale page (`raw/tailscale/unraid.md`) contained an example `tskey-client-…` auth key in a shell snippet; it was replaced with `tskey-[REDACTED-BY-BENCHMARK]` under the credential rule (the only edit beyond HTML→text in `raw/`).
