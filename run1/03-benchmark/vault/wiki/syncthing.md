---
tags: [lab, service, sync, docker]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/lab/LAB-STATE.md]
---
# Syncthing (lab service)

Syncthing runs as a container on [[atlas]] and syncs tank/notes to [[pebble]]. Syncthing needs [[tank]], and Syncthing to pebble runs over [[tailscale]] only (no relays, no LAN discovery).

## Consequences
- If atlas or tank is down, the notes folder does not sync.
- If Tailscale is down, Syncthing cannot reach pebble, because relays and LAN discovery are not used.

## Background
Syncthing folder types and versioning: [[syncthing-folders-versioning]]; ports, relays and discovery: [[syncthing-ignore-firewall]].

depends_on:: [[atlas]] (runs as a container on atlas)
depends_on:: [[tank]] (syncs the tank/notes share)
depends_on:: [[tailscale]] (Syncthing to pebble runs over Tailscale only; no relays, no LAN discovery)
derived_from:: [[raw/lab/LAB-STATE.md]]
