---
tags: [lab, service, media, docker]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/lab/LAB-STATE.md]
---
# Plex (media server container)

Plex runs as a Docker container on [[atlas]]; it needs atlas. It reads its library from tank/media and keeps its appdata on tank/appdata, so it needs [[tank]].

## Access
- The Caddy [[reverse-proxy]] on atlas fronts Plex on port 443.
- Away from home, [[pebble]] reaches Plex only through [[tailscale]] via atlas.

## Background
Container settings (volume mappings, ports, startup order) on Unraid: [[unraid-docker-vms]].

depends_on:: [[atlas]] (runs as a Docker container on atlas)
depends_on:: [[tank]] (library on tank/media and appdata on tank/appdata)
derived_from:: [[raw/lab/LAB-STATE.md]]

## Superseded
depends_on:: [[titan]] (old transcoding on titan, moved 2026-09)
