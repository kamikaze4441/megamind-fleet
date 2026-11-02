---
tags: [lab, device, macbook, laptop]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/lab/LAB-STATE.md]
---
# pebble (MacBook)

pebble is a MacBook. Away from home it reaches [[hermes]] and [[plex]] only through [[tailscale]] via [[atlas]], so pebble's remote access needs Tailscale.

## Sync
[[syncthing]] on atlas syncs tank/notes to pebble. Syncthing to pebble runs over Tailscale only (no relays, no LAN discovery).

## Exit node
atlas is the tailnet's only exit node; pebble's traffic away from home therefore depends on atlas and on [[gate]] (Tailscale needs gate to reach the internet). Adding hermes as a second exit node is pending.

## Background
How exit nodes and subnet routes work: [[tailscale-exit-nodes-subnets]]; MagicDNS names: [[tailscale-magicdns]].

depends_on:: [[tailscale]] (remote access to hermes and Plex away from home goes only through Tailscale via atlas)
derived_from:: [[raw/lab/LAB-STATE.md]]
