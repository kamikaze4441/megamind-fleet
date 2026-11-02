---
tags: [lab, service, qmd, wiki]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/lab/LAB-STATE.md]
---
# Wiki search service (qmd on hermes)

The wiki search service (qmd) runs on [[hermes]] next to the wiki repo (/srv/wiki, a git repository); the wiki search service needs hermes.

## Index and embeddings
- The search index is rebuilt by a systemd timer on hermes at 02:30 every night; when hermes is down the index goes stale.
- The service calls the [[ollama-endpoint]] on titan (http://10.77.0.30:11434) for embeddings. When titan is off, new wiki pages are not embedded, but keyword search still works.

## Access
The Caddy [[reverse-proxy]] on atlas fronts the wiki search service on port 443.

## Background
qmd commands and pipeline: [[qmd-search]].

depends_on:: [[hermes]] (runs on hermes next to the wiki repo)
depends_on:: [[ollama-endpoint]] (calls the Ollama endpoint on titan for embeddings; without it new pages are not embedded (degrades, keyword search still works))
derived_from:: [[raw/lab/LAB-STATE.md]]
