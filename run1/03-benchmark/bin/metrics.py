#!/usr/bin/env python3
# Measures per-question wall time, bytes/chars printed (token proxy = chars/4), calls, pages read/cited and optional expected-page recall from a run's log.jsonl + answers.tsv.
"""Usage: metrics.py <RUN> [--expected expected.tsv]

RUN is a directory created by bin/new-run (log.jsonl, answers.tsv).
Writes RUN/metrics.tsv: one row per answered question, then a footer with medians and totals.

Columns
  qid            question id
  wall_s         seconds from `q start` to `q answer` (harness timestamps)
  calls          harness calls between start and answer (excluding start/answer), refused ones included
  refused        how many of those calls were refused
  bytes_out      UTF-8 bytes printed to the querier for this question (all calls incl. start/answer)
  chars_out      characters printed; tokens_proxy = chars_out / 4
  tokens_proxy   chars_out / 4, rounded
  pages_read     distinct wiki pages opened with a successful `q read` (wiki/<slug>.md)
  raw_read       distinct raw files opened with a successful `q read`
  pages_cited    pages listed in `q answer --pages`
  recall         only with --expected: |expected ∩ (pages_read ∪ raw_read ∪ pages_cited)| / |expected|
  answer_chars   length of the recorded answer

expected.tsv: qid<TAB>expected pages (comma-separated; 'atlas', 'atlas.md', 'wiki/atlas.md' and raw paths accepted).
A header line starting with 'qid' is skipped.
"""
import csv, json, os, re, statistics, sys


def norm(p):
    p = p.strip().strip("[]").strip()
    if not p:
        return None
    p = re.sub(r"^(\./)?(vault/)?", "", p)
    if p.startswith("raw/"):
        return p
    p = re.sub(r"^wiki/", "", p)
    return p if p.endswith(".md") else p + ".md"


def main():
    if len(sys.argv) < 2:
        print(__doc__); return 2
    run = sys.argv[1]
    expected = {}
    if "--expected" in sys.argv:
        path = sys.argv[sys.argv.index("--expected") + 1]
        for row in csv.reader(open(path), delimiter="\t"):
            if not row or row[0].lower() == "qid":
                continue
            expected[row[0]] = {norm(x) for x in row[1].split(",") if norm(x)} if len(row) > 1 else set()

    recs = [json.loads(l) for l in open(os.path.join(run, "log.jsonl")) if l.strip()]
    answers = {}
    with open(os.path.join(run, "answers.tsv")) as f:
        for row in csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE):
            if row and row[0] != "qid":
                answers[row[0]] = row

    per = {}
    for r in recs:
        q = r.get("qid")
        if not q:
            continue
        d = per.setdefault(q, dict(start=None, end=None, calls=0, refused=0, bytes=0, chars=0, read=set(), raw=set()))
        d["bytes"] += r["bytes_out"]; d["chars"] += r["chars_out"]
        if r["cmd"] == "start" and not r["refused"]:
            d["start"] = r["ts_ns"]
        elif r["cmd"] == "answer" and not r["refused"]:
            d["end"] = r["ts_ns"]
        else:
            d["calls"] += 1
            d["refused"] += 1 if r["refused"] else 0
            if r["cmd"] == "read" and not r["refused"] and r["args"]:
                p = norm(r["args"][0])
                if p and p.startswith("raw/"):
                    d["raw"].add(p)
                elif p and p != "index.md" and not p.startswith("deps/"):
                    d["read"].add(p)

    cols = ["qid", "wall_s", "calls", "refused", "bytes_out", "chars_out", "tokens_proxy",
            "pages_read", "raw_read", "pages_cited", "answer_chars"] + (["recall"] if expected else [])
    rows = []
    for q, d in per.items():
        if d["start"] is None or d["end"] is None:
            continue
        a = answers.get(q, [q, "", "", ""])
        cited = {norm(x) for x in (a[2] if len(a) > 2 else "").split(",") if norm(x)}
        row = dict(qid=q, wall_s=round((d["end"] - d["start"]) / 1e9, 1), calls=d["calls"], refused=d["refused"],
                   bytes_out=d["bytes"], chars_out=d["chars"], tokens_proxy=round(d["chars"] / 4),
                   pages_read=",".join(sorted(d["read"])), raw_read=",".join(sorted(d["raw"])),
                   pages_cited=",".join(sorted(cited)), answer_chars=len(a[1]) if len(a) > 1 else 0)
        if expected:
            exp = expected.get(q, set())
            got = d["read"] | d["raw"] | cited
            row["recall"] = round(len(exp & got) / len(exp), 2) if exp else ""
        rows.append(row)
    rows.sort(key=lambda r: r["qid"])

    def med(k):
        v = [r[k] for r in rows if r[k] != ""]
        return round(statistics.median(v), 2) if v else ""

    with open(os.path.join(run, "metrics.tsv"), "w") as f:
        f.write("\t".join(cols) + "\n")
        for r in rows:
            f.write("\t".join(str(r[c]) for c in cols) + "\n")
        f.write("\n")
        f.write(f"# questions\t{len(rows)}\n")
        for k in ("wall_s", "calls", "bytes_out", "chars_out", "tokens_proxy") + (("recall",) if expected else ()):
            tot = sum(r[k] for r in rows if r[k] != "")
            f.write(f"# median_{k}\t{med(k)}\t# total_{k}\t{round(tot, 2)}\n")
        f.write(f"# median_pages_read\t{med_count(rows, 'pages_read')}\n")
        f.write("# token proxy = chars printed by the harness / 4 (not Console usage)\n")
    print(open(os.path.join(run, "metrics.tsv")).read())
    return 0


def med_count(rows, k):
    v = [len(r[k].split(",")) if r[k] else 0 for r in rows]
    return statistics.median(v) if v else ""


if __name__ == "__main__":
    sys.exit(main())
