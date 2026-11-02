---
tags: [lab, service, vpn, exit-node]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/lab/LAB-STATE.md]
---
# Tailscale (lab tailnet)

Tailscale runs as the Unraid plugin on [[atlas]]. atlas is the tailnet's only exit node and also advertises the subnet route 10.77.0.0/24, so Tailscale remote access needs atlas, and it needs [[gate]] to reach the internet.

## Who uses it
- [[pebble]]: away from home it reaches [[hermes]] and [[plex]] only through Tailscale via atlas.
- [[syncthing]]: sync to pebble runs over Tailscale only.

## Pending
Add hermes as a second exit node; until then atlas is a single point of failure for remote access.

## Background
Plugin setup on Unraid: [[unraid-tailscale]]; exit nodes and subnet routers: [[tailscale-exit-nodes-subnets]].

depends_on:: [[atlas]] (runs as the Unraid plugin on atlas, the only exit node and subnet router)
depends_on:: [[gate]] (needs gate to reach the internet)
derived_from:: [[raw/lab/LAB-STATE.md]]
