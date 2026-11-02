#!/usr/bin/env python3
# Writes $B/corpus.md from /tmp/b1/fetch-log.json plus the non-fetched sources.
import json, os, re
B = "/workspace/megamind-fleet/run1/03-benchmark"
LIC = {
 "unraid": "CC BY-SA 4.0 (docs.unraid.net footer: documentation content only; © 2005-2026 Lime Technology, Inc.)",
 "ollama": "MIT (docs are built from ollama/ollama repo `docs/`, repo LICENSE MIT, © Ollama)",
 "syncthing": "CC BY 4.0 (syncthing/docs README.rst 'License' section, commit f02059067d50)",
 "tailscale": "terms not stated as a licence; site footer '© 2026 Tailscale Inc. All rights reserved.'; fetched for private benchmark use only",
 "claude-code": "terms not stated as a licence; footer links Anthropic Commercial/Consumer terms; fetched for private benchmark use only",
}
rows = []
for e in json.load(open("/tmp/b1/fetch-log.json")):
    p = f"{B}/{e['path']}"
    title = ""
    for line in open(p):
        m = re.match(r"#\s+(.+)", line)
        if m: title = m.group(1).strip(); break
    note = LIC[e["group"]]
    if e.get("redactions"): note += f"; {e['redactions']} example auth key redacted by benchmark"
    if e["effective"] != e["url"]: note += f"; served from {e['effective']}"
    rows.append((e["id"], e["group"], title, e["url"], note, e["fetched"], e["path"], e["bytes"]))
def add(sid, group, title, url, note, path):
    rows.append((sid, group, title, url, note, "2026-11-02", path, os.path.getsize(f"{B}/{path}")))
add("qmd-readme","qmd","QMD - Query Markup Documents","https://github.com/tobi/qmd/blob/86d2365d17fc682e491c2c53d1e4a884aee8682a/README.md","MIT (© 2024-2026 Tobi Lutke), pinned HEAD 86d2365d17fc (2026-10-14)","raw/qmd/README.md")
add("manual-pdf","manual","AVR-X1700H / AVR-X1700H DAB Integrated Network AV Receiver Owner's Manual (PDF, 304 pages)","https://assets.denon.com/DocumentMaster/MASTER/AVR-X1700HE2DAB%20_Owners_Manual.pdf","©2021 Sound United. All Rights Reserved. (last page); manufacturer-hosted; fetched for private benchmark use only","raw/manual/denon-avr-x1700h-owners-manual.pdf")
add("manual-txt","manual","same manual, text extracted with `pdftotext` 24.02.0 (default mode, one form feed per page)","(derived from manual-pdf)","as manual-pdf","raw/manual/denon-avr-x1700h-owners-manual.txt")
add("lab-state","lab","LAB-STATE: fictional home lab \"lab77\"","(none; written by builder B1)","fleet-written, CC0","raw/lab/LAB-STATE.md")

out = ["# Corpus (run 1, benchmark 03)", "",
 "Frozen at the step-1 report; `raw/` is not changed after that. Column 'wiki pages' lists the `vault/wiki/` pages whose `sources:` cite the file (filled after step 2).", "",
 "Conversion: `.md` URLs saved verbatim; HTML pages reduced to their main element (`<article>` on docs.unraid.net, `div[role=main]` on docs.syncthing.net) with Python `html.parser`, inline `<svg>` and `data:` images dropped, then `pandoc -f html -t gfm-raw_html --wrap=none`; heading permalink anchors (`[​](#…)`, `[¶](#…)`) removed and `data:` markdown images replaced by `[image: alt]`. Each file starts with a one-line `<!-- source: … | fetched: … -->` comment. Script: `/tmp/b1/fetch.py` (copied to `harness/fetch-corpus.py`).", "",
 "| id | group | title | URL | licence / terms | fetched | raw path | bytes | wiki pages |",
 "|---|---|---|---|---|---|---|---|---|"]
import glob
fed = {}
for p in sorted(glob.glob(f"{B}/vault/wiki/*.md")):
    m = re.search(r"^sources:\s*\[(.*)\]", open(p).read(), re.M)
    for s in (m.group(1).split(",") if m else []):
        fed.setdefault(s.strip(), []).append(os.path.basename(p)[:-3])
for r in rows:
    pages = fed.get(r[6]) or (fed.get(r[6][:-4] + ".txt") if r[6].endswith(".pdf") else None)
    out.append("| " + " | ".join(str(x).replace("|","\\|") for x in r) + " | " + (", ".join(pages) if pages else "—") + " |")
tot = sum(r[7] for r in rows)
groups = {}
for r in rows: groups.setdefault(r[1], []).append(r[7])
out += ["", "## Totals", "", "| group | files | bytes |", "|---|---|---|"]
for g, v in groups.items(): out.append(f"| {g} | {len(v)} | {sum(v):,} |")
out.append(f"| **all** | {len(rows)} | {tot:,} |")
out += ["", f"Sources (counting the manual PDF and its .txt as one source): {len(rows)-1}. Bytes excluding the PDF binary: {tot - os.path.getsize(B+'/raw/manual/denon-avr-x1700h-owners-manual.pdf'):,}."]
open(f"{B}/corpus.md","w").write("\n".join(out) + "\n")
print(len(rows), tot)
