---
tags: [lab, device, ups, power]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/lab/LAB-STATE.md]
---
# apc-1 (UPS)

apc-1 is the UPS that powers [[atlas]]. Its USB link tells atlas to shut down cleanly after 5 minutes on battery, so atlas needs apc-1.

## State
- A battery replacement is pending: the self-test warned on 2026-10-28, and until the battery is replaced the runtime on battery is unverified.
- "UPS on battery" is one of the Unraid notifications atlas sends by email through [[gate]] (see [[atlas]]).

## Why it matters
apc-1 sits at the bottom of the lab's dependency chain: atlas needs it, and the pool [[tank]], the VM [[hermes]], [[plex]], the [[reverse-proxy]], [[syncthing]], [[tailscale]] and the [[rclone-backup]] all need atlas. Unraid's UPS settings page is described in [[unraid-notifications-ups]].

derived_from:: [[raw/lab/LAB-STATE.md]]
