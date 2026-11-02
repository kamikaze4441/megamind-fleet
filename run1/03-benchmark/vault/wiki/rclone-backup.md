---
tags: [lab, service, backup, rclone]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/lab/LAB-STATE.md]
---
# Nightly rclone backup

The nightly rclone backup runs on [[atlas]] at 06:00. It reads the [[tank]] snapshot taken at 05:45 and uploads it to the cloud drive remote "offsite-crypt". The backup needs tank and needs [[gate]] for internet access.

## Notes
- The backup result is one of the Unraid notifications atlas sends by email through gate.
- It is a job on atlas, alongside Plex, the reverse proxy and Syncthing containers.

## Background
ZFS snapshots on Unraid: [[unraid-pools-zfs]].

depends_on:: [[atlas]] (the job runs on atlas)
depends_on:: [[tank]] (reads the tank snapshot taken at 05:45)
depends_on:: [[gate]] (needs gate for internet access to upload)
derived_from:: [[raw/lab/LAB-STATE.md]]
