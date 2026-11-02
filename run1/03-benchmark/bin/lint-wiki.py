#!/usr/bin/env python3
# Measures wiki fidelity/structure: frontmatter, word counts, derived_from/depends_on lines, and that every number and `code` span on a page appears in its cited raw files.
"""Usage: lint-wiki.py [VAULT]   (default: $B/vault). Exit 1 if any ERROR.

Checks per wiki/*.md (text below a '## Superseded' heading is ignored for the number/code checks):
  - frontmatter has tags, created, updated, sources; every source exists under vault/
  - one 'derived_from:: [[raw/<path>]]' line per source, and no extra ones
  - 'depends_on:: [[slug]] (reason)': target page exists, reason non-empty, only on pages citing raw/lab/
  - body word count (excluding frontmatter, derived_from/depends_on lines, table pipes): WARN outside 150-400
  - every number token and every `backtick span` in the body occurs in the concatenated cited raw text
    (raw text is compared both verbatim and with markdown backslash-escapes removed)
"""
import os, re, sys, glob

B = "/workspace/megamind-fleet/run1/03-benchmark"
vault = sys.argv[1] if len(sys.argv) > 1 else f"{B}/vault"
wiki = os.path.join(vault, "wiki")
pages = sorted(glob.glob(f"{wiki}/*.md"))
slugs = {os.path.basename(p)[:-3] for p in pages}
errors = warns = 0

def report(kind, page, msg):
    global errors, warns
    if kind == "ERROR": errors += 1
    else: warns += 1
    print(f"{kind}\t{os.path.basename(page)}\t{msg}")

NUM = re.compile(r"(?<![\w.])\d+(?:[.,:]\d+)*(?![\w])")
CODE = re.compile(r"`([^`\n]+)`")

for p in pages:
    text = open(p).read()
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not m:
        report("ERROR", p, "no frontmatter"); continue
    fm, body = m.group(1), m.group(2)
    meta = {}
    for line in fm.splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    for k in ("tags", "created", "updated", "sources"):
        if k not in meta: report("ERROR", p, f"frontmatter missing {k}")
    sources = [s.strip() for s in meta.get("sources", "").strip("[]").split(",") if s.strip()]
    for s in sources:
        if not os.path.exists(os.path.join(vault, s)): report("ERROR", p, f"source missing: {s}")
    main = re.split(r"^## Superseded\s*$", body, maxsplit=1, flags=re.M)[0]
    derived = re.findall(r"^derived_from:: \[\[(.+?)\]\]\s*$", main, re.M)
    if sorted(derived) != sorted(sources):
        report("ERROR", p, f"derived_from {derived} != sources {sources}")
    for line in re.findall(r"^depends_on::.*$", main, re.M):
        dm = re.match(r"depends_on:: \[\[([^\]]+)\]\] \((.+)\)\s*$", line)
        if not dm: report("ERROR", p, f"malformed: {line}"); continue
        if dm.group(1) not in slugs: report("ERROR", p, f"depends_on target missing: {dm.group(1)}")
        if not any(s.startswith("raw/lab/") for s in sources):
            report("ERROR", p, "depends_on on a page that does not cite raw/lab/")
    prose = "\n".join(l for l in main.splitlines() if not l.startswith(("derived_from::", "depends_on::")))
    words = [w for w in prose.split() if not re.fullmatch(r"\|[-|: ]*", w)]
    if not 150 <= len(words) <= 400:
        report("WARN", p, f"body has {len(words)} words (target 150-400)")
    raw = ""
    for s in sources:
        fp = os.path.join(vault, s)
        if os.path.exists(fp) and not fp.endswith(".pdf"):
            raw += open(fp, errors="replace").read() + "\n"
    raw_unesc = re.sub(r"\\([\\`*_{}\[\]()#+\-.!|<>~])", r"\1", raw)
    def present(t): return t in raw or t in raw_unesc
    scan = re.sub(r"\[\[[^\]]*\]\]", " ", prose)          # wikilinks are not facts
    for code in set(CODE.findall(scan)):
        if not present(code): report("ERROR", p, f"code span not in raw: `{code}`")
    for num in set(NUM.findall(CODE.sub(" ", scan))):
        if not present(num): report("ERROR", p, f"number not in raw: {num}")

print(f"# {len(pages)} pages, {errors} errors, {warns} warnings")
sys.exit(1 if errors else 0)
