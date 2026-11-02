#!/usr/bin/env python3
# Converts a TSV (qid, question, expected_pages) into the JSON fixture `qmd bench` reads, for retrieval-quality measurement of the qmd collection over vault/wiki.
"""Usage: make-bench-fixture.py <in.tsv> <out.json> [--collection wiki] [--top-k 3] [--type-col]

in.tsv columns: qid<TAB>question<TAB>expected_pages   (header line starting with 'qid' is skipped)
  expected_pages: comma-separated; 'atlas', 'atlas.md' and 'wiki/atlas.md' all become 'atlas.md'
  (expected_files must be collection-relative paths as `qmd ls wiki` shows them; qmd matches by path suffix).
  An optional 4th column is used as the query `type` (exact|semantic|topical|cross-domain|alias); default 'semantic'.

Run it (all four backends: bm25, vector, hybrid, full; `full` needs the reranker model, ~640MB, downloaded on first use):
  qmd ls wiki                     # must list the pages, otherwise bench silently reports zeros
  qmd bench <out.json> -c wiki --json > results/qmd-bench.json
"""
import csv, json, sys


def norm(p):
    p = p.strip().strip("[]").strip()
    if p.startswith("vault/"):
        p = p[len("vault/"):]
    if p.startswith("wiki/"):
        p = p[len("wiki/"):]
    return p if p.endswith(".md") else p + ".md"


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__); return 2
    src, dst = args[0], args[1]
    coll = args[args.index("--collection") + 1] if "--collection" in args else "wiki"
    topk = int(args[args.index("--top-k") + 1]) if "--top-k" in args else 3
    queries = []
    for row in csv.reader(open(src), delimiter="\t"):
        if not row or row[0].strip().lower() == "qid":
            continue
        if len(row) < 3:
            sys.exit(f"bad row (need qid, question, expected_pages): {row}")
        files = [norm(x) for x in row[2].split(",") if x.strip()]
        queries.append({
            "id": row[0].strip(),
            "query": row[1].strip(),
            "type": row[3].strip() if len(row) > 3 and row[3].strip() else "semantic",
            "expected_files": files,
            "expected_in_top_k": max(topk, 1),
        })
    fixture = {"description": f"MEGAMIND run1 benchmark questions over the '{coll}' collection",
               "version": 1, "collection": coll, "queries": queries}
    json.dump(fixture, open(dst, "w"), indent=2, ensure_ascii=False)
    print(f"wrote {dst}: {len(queries)} queries, collection {coll}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
