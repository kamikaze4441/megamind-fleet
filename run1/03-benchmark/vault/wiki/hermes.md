---
tags: [lab, host, vm, debian, wiki]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/lab/LAB-STATE.md]
---
# hermes (Debian VM)

hermes is a Debian VM on [[atlas]] at 10.77.0.20, with its vdisk on tank/domains. hermes runs on atlas and stops when atlas stops, and it cannot boot without [[tank]].

## What hermes hosts
- The wiki repo at /srv/wiki, a git repository.
- The [[wiki-search]] service (qmd), which needs hermes.
- A systemd timer that rebuilds the wiki search index at 02:30 every night; when hermes is down the index goes stale.

## Access
Away from home, [[pebble]] reaches hermes only through [[tailscale]] via atlas.

## Pending
hermes is planned as a second Tailscale exit node; until then atlas is a single point of failure for remote access.

depends_on:: [[atlas]] (the VM runs on atlas and stops when atlas stops)
depends_on:: [[tank]] (its vdisk is on tank/domains; it cannot boot without tank)
derived_from:: [[raw/lab/LAB-STATE.md]]

## Superseded
