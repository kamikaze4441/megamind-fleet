---
tags: [lab, pool, zfs, storage]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/lab/LAB-STATE.md]
---
# tank (ZFS pool on atlas)

tank is the ZFS pool inside [[atlas]]. It holds the shares appdata, media, domains and notes. tank exists only while atlas is running.

## What uses tank
- [[hermes]]: its vdisk lives on tank/domains; hermes cannot boot without tank.
- [[plex]]: reads its library from tank/media and keeps its appdata on tank/appdata.
- [[syncthing]]: syncs tank/notes to [[pebble]].
- [[rclone-backup]]: reads the tank snapshot taken at 05:45 and uploads it at 06:00.

## Notes
The share names follow Unraid's default shares (appdata for container data, domains for VM vdisks) — see [[unraid-shares]] and [[unraid-pools-zfs]] for how pools and shares work on Unraid.

depends_on:: [[atlas]] (the pool is inside atlas and exists only while atlas is running)
derived_from:: [[raw/lab/LAB-STATE.md]]
