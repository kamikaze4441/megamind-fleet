---
tags: [unraid, storage, shares]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/unraid/shares.md]
---
# Unraid shares

Shares are folders or drives on the Unraid server that can be accessed over a network. There are two kinds: **User Shares** (Linux FUSE, an aggregated view of same-named top-level folders across cache and array drives) and **Disk Shares** (a whole drive or pool). Both are views of the same underlying files.

## Paths
- User shares live under `/mnt/user` (array plus pools). The deprecated `/mnt/user0` mount point (which excludes pool files) may be removed.
- Disk shares appear as `/mnt/diskX` (e.g. `disk1`) and pools as `/mnt/pool-name`; the most common pool is `cache`. Disk shares are off by default; enable in ***Settings → Global Share Settings***.
- The boot device is mounted at `/boot` and can be shared as 'flash'.
- **Do not mix User Shares and Disk Shares**: never copy or move files between e.g. `/mnt/user/share` and `/mnt/disk1/share` — this can cause file corruption or permanent data loss.

## Primary and secondary storage (Unraid 6.12 and later)
**Primary Storage** is where new files are first written (default **Cache**; any named pool or the array). **Secondary Storage** takes new files when the primary falls below **Minimum Free Space**; options are **None**, **Array** or **Another pool**. The **Mover** transfers files between them on a schedule. Allocation method, split level and included/excluded disks apply only to the array.

In Unraid 6.11 and earlier the per-share **Use Cache for New Files** setting was **Yes**, **No**, **Only** (cache only; writing fails when full) or **Prefer** (Mover moves files back to cache; default for `appdata` and `system`). Since Unraid 6.9 multiple pools can act as cache.

## Allocation methods (array only)
- **High-water** (recommended): switch points at half the largest drive's capacity; with 8TB, 3TB and 2TB drives, first fill the 8TB drive until 4TB free remains.
- **Most-free**: disk with most free space per file; more drive thrashing.
- **Fill-up**: disks in numeric order until the Minimum Free Space threshold.
Split level is numbered from 1 (the share itself); default is Automatically Split Any Directory.

## Default shares
Created when Docker or VM Manager is started: `appdata` (Docker container working files), `system` (Docker files and VM XML templates), `domains` (VM vdisks), `isos` (ISO images; the only share where changing permissions is recommended).

derived_from:: [[raw/unraid/shares.md]]
