---
tags: [lab, service, caddy, proxy]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/lab/LAB-STATE.md]
---
# Reverse proxy (Caddy)

The reverse proxy is a Caddy container on [[atlas]] that fronts [[plex]] and the [[wiki-search]] service on port 443. It needs atlas, and outside access to it needs [[gate]] to forward port 443.

## Notes
- Only outside access is tied to the port forward on gate.
- The services it fronts have their own dependencies: Plex needs atlas and [[tank]]; the wiki search service needs [[hermes]].

## Background
Unraid container network types and port mappings: [[unraid-docker-vms]].

depends_on:: [[atlas]] (Caddy container on atlas)
depends_on:: [[gate]] (outside access needs gate to forward port 443)
derived_from:: [[raw/lab/LAB-STATE.md]]
