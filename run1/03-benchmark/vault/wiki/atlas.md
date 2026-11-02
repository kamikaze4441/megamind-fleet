---
tags: [lab, host, unraid, server]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/lab/LAB-STATE.md]
---
# atlas (Unraid server)

atlas is the lab's Unraid server at 10.77.0.10. It belongs to the fictional lab "lab77" (all names and 10.77.x.x addresses are invented).

## What runs on atlas
- The ZFS pool [[tank]] lives inside atlas.
- The Debian VM [[hermes]] (wiki repo and wiki search service).
- Docker containers: [[plex]], the Caddy [[reverse-proxy]] and [[syncthing]].
- The [[tailscale]] Unraid plugin: atlas is the tailnet's only exit node and advertises the subnet route 10.77.0.0/24.
- The nightly [[rclone-backup]] at 06:00.

## Power
atlas is powered through the UPS [[apc-1]]. apc-1's USB link tells atlas to shut down cleanly after 5 minutes on battery, so atlas needs apc-1. The apc-1 battery replacement is pending (self-test warning on 2026-10-28), so runtime on battery is unverified.

## Notifications
Unraid notifications from atlas (parity check, UPS on battery, backup result) are sent by the email agent through [[gate]], so notifications need gate. Settings background: [[unraid-notifications-ups]].

## Single point of failure
Because atlas is the only exit node, it is a single point of failure for remote access until hermes is added as a second exit node (pending).

depends_on:: [[apc-1]] (powered through the UPS; USB link triggers clean shutdown after 5 minutes on battery)
depends_on:: [[gate]] (Unraid email notifications are sent through gate)
derived_from:: [[raw/lab/LAB-STATE.md]]
