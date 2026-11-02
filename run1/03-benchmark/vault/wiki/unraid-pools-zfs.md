---
tags: [unraid, storage, cache-pool, zfs]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/unraid/cache-pools.md, raw/unraid/zfs-storage.md]
---
# Unraid cache pools and ZFS pools

A cache pool is one or more drives (typically SSDs) that hold data before the Mover transfers it to the array ([[unraid-array-parity]]), or that host Docker containers, app data and VM disks. You can create and name several pools, e.g. one for downloads and one for VMs.

## Pool modes
- **Single device mode**: no redundancy; XFS or ZFS may be used, but a non-BTRFS/non-ZFS device must be reformatted before more devices are added. That is why BTRFS is the default file system for cache pools.
- **Multi-device mode**: BTRFS or ZFS mirrors data; you can lose one device without losing data.

## Minimum free space
Set per pool in **Main** → pool name → **Individual Pool Settings**. Unraid stops writing to the pool when free space drops below it and sends files to the array (when the share has Secondary storage). Best practice: at least the size of the largest file, preferably double — largest file 30 GB → set 60 GB. **Do not set the minimum free space to 0** (disk full errors).

## ZFS on Unraid
ZFS brings integrity checks and self-healing, mirrors and RAIDZ, snapshots and clones, send/receive replication and on-the-fly compression. A zpool is made of vdevs; redundancy is always per vdev, and if any vdev fails the entire pool fails.

Create a pool: stop the array, **Add Pool**, name it (example `raptor`), set slots for the data vdevs, assign disks, set file system `zfs` or `zfs-encrypted`, choose an allocation profile, enable compression (recommended), **Done**, start the array.

A hybrid setup puts a single `zfs` disk in the array: parity-protected and checksummed, but it cannot self-heal and is not a replacement for a full pool.

## Expansion and RAM
Only single-vdev RAIDZ1/2/3 pools can grow one drive at a time, starting with Unraid 7.2 (earlier 7.1.x by CLI only); the new drive must be at least as large as the smallest drive in the pool, and an "invalid expansion" warning means **Upgrade Pool** is needed first. Mirrored pools grow by mirror pairs; multi-vdev pools by whole vdevs. For a two-device pool you plan to grow, choose **RAIDZ1** instead of the default mirror.

The "1 GB of RAM per 1 TB" rule is outdated; Unraid limits ZFS ARC to usually 1/8th of total RAM. Deduplication needs significant memory. RAIDZ treats every disk as the size of the smallest.

derived_from:: [[raw/unraid/cache-pools.md]]
derived_from:: [[raw/unraid/zfs-storage.md]]
