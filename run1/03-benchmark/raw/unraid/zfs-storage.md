<!-- source: https://docs.unraid.net/unraid-os/advanced-configurations/optimize-storage/zfs-storage/ | fetched: 2026-11-02 | effective-url: https://docs.unraid.net/unraid-os/advanced-configurations/optimize-storage/zfs-storage/ -->

- [](/)
- [Unraid OS](/category/unraid-os/)
- [Advanced configurations](/category/advanced-configurations/)
- [Optimize storage](/category/optimize-storage/)
- ZFS storage

On this page

# ZFS storage

Special thanks

We’d like to express our thanks to Ed Rawlings ([Spaceinvader One](https://www.youtube.com/c/SpaceinvaderOne)) for the expertise and guidance that this ZFS storage documentation has been adapted from. His tutorials and insights have assisted countless Unraid users in mastering advanced storage techniques. We appreciate his continued contributions to the Unraid community.

ZFS brings advanced data integrity, flexible storage configurations, and high performance to your Unraid system. This guide explains ZFS core concepts and walks you through managing ZFS pools directly from the Unraid WebGUI. Whether you're setting up new ZFS storage or integrating an existing pool, you’ll find the steps and context you need to get started confidently.

------------------------------------------------------------------------

## Why ZFS?

ZFS is a modern file system and volume manager designed to protect your data, prevent corruption, and simplify storage management.

With ZFS, you gain:

- Automatic data integrity checks and self-healing
- Built-in RAID support (mirrors, RAIDZ)
- Snapshots and clones for easy backups and rollbacks
- ZFS send/receive for efficient replication
- On-the-fly compression

Unraid supports ZFS for any storage pool. You can create a new ZFS pool, import one from another system, or use Unraid’s unique hybrid ZFS setup: add a ZFS-formatted disk directly to the Unraid array (not a pool) and combine ZFS features with Unraid’s parity protection.

Example

You can use ZFS snapshots and replication on a single disk as a backup target, or replicate a fast SSD ZFS pool to a ZFS disk in the array protected by Unraid parity - getting the best of both worlds.

![](/assets/images/zfs1-7d3225a7572f3fd1a8b480c1d4cb3878.png)

note

The hybrid ZFS-in-array approach is helpful for specific backup or replication scenarios but is not a replacement for a full ZFS pool. ZFS disks in the array are managed individually; you do not get the combined performance, redundancy, or self-healing of a true multi-disk ZFS pool. For full ZFS functionality, always use dedicated ZFS pools.

### Pools, vdevs, and redundancy

A ZFS pool (called a "zpool") is made up of one or more vdevs (virtual devices). Each vdev is a group of physical disks with its own redundancy level. ZFS writes data across vdevs, but each vdev is responsible for its fault tolerance.

caution

Redundancy is always per vdev. If any vdev fails, the entire pool fails, even if other vdevs are healthy. Plan your vdevs with care!

![](/assets/images/zfs2-42a54028aaac6693c7ffce885e5a3544.png)

------------------------------------------------------------------------

## Creating a ZFS pool

To create a ZFS pool using the WebGUI:

1.  Stop the array.
2.  Click **Add Pool**.

![](/assets/images/zfs3-928ecd72806a2ef8596203be7c6febc1.png)

3.  Choose a name for your pool (for example, `raptor`).
4.  Set the number of slots to match the number of disks you want in your primary data vdev(s).

note

This initial slot count is for data vdevs only. Support vdevs (such as log or cache drives) can be added separately after creating the pool.

![](/assets/images/zfs4-51f62e8e6abc68ecc5cc1a3f19136944.png)

5.  Assign disks to the pool (disk order does not matter).

![](/assets/images/zfs5-8f7deb8956dfd2319f29f128561e181d.png)

6.  Click the pool name (e.g., `raptor`) to open its configuration screen.
7.  Set the file system type to `zfs` or `zfs-encrypted` (for LUKS encryption).

![](/assets/images/zfs6-5a4b8dd6607276ef936ce7af3d8de720.png)

8.  Choose your allocation profile - this determines your pool's redundancy and performance.

tip

Before finalizing, review the sections on allocation profiles and topology to make an informed choice.

![](/assets/images/zfs7-c3e81c27ed07333e6b801dea7332805f.png)

![](/assets/images/zfs8-1a5abc69d7342e0253b477cacb65eb66.png)

9.  Enable compression if desired (recommended for most workloads).
10. Click **Done**, then start the array.

------------------------------------------------------------------------

## Adding a ZFS disk to the array (Hybrid setup)")

You can add a standalone ZFS disk to your Unraid array (not a ZFS pool) to combine ZFS features with Unraid's parity protection.

What this enables

- **Parity protection:** The ZFS disk is protected by Unraid’s array parity, ensuring your data is safe from single (or multiple, depending on your parity drives) disk failures.

- **Data integrity:** ZFS provides block-level integrity checks (checksums). While a single disk can’t self-heal bit rot, ZFS will detect corruption and alert you, allowing you to restore from backup before silent data loss occurs.

- **ZFS features:** You can utilize ZFS snapshots and replication on this disk, making it ideal for backup targets, specific datasets, or scenarios where you want ZFS features alongside traditional Unraid storage.

To add a ZFS disk to the array:

1.  Go to the **Main** tab in the WebGUI.
2.  Stop the array.
3.  Click on an empty slot under **Array Devices**.
4.  Select the disk you want to add.

![](/assets/images/zfs9-5571b040dcf3114c91ae46ec19737fcf.png)

5.  Under **File system**, choose `zfs` or `zfs-encrypted`.

![](/assets/images/zfs10-574606101e572c9f87c8aca101577c0c.png)

6.  Click **Apply**.
7.  Start the array and let the disk be formatted if needed.

------------------------------------------------------------------------

## Choosing an allocation profile

When you set up a ZFS pool, your allocation profile determines how your data is protected, how your pool performs, and how you can expand it. Here’s a simple comparison to help you decide which profile fits your needs:

![](/assets/images/zfs11-17d97e50511577a9c682777a95a252e7.png)

Profile

Redundancy

Performance

Expansion

Space Efficiency

Typical Use Case

Recommended Drive Count Per vdev

Stripe

None

Fast, but risky

Add more disks

100%

Temporary/scratch storage

Any number

Mirror

1:1 (RAID 1 style)

Excellent for random I/O

Add more mirrors

50%

High performance, easy expansion

2 drives (can add more mirrors)

RAIDZ1

1 disk per vdev

Fast for big files. Not ideal for small or random writes.

Add new vdevs

High

General use, 1-disk fault tolerance

3-6 drives (max 8)

RAIDZ2

2 disks per vdev

Like Z1 but slightly slower writes (extra parity)

Add new vdevs

Moderate

Important data, 2-disk fault tolerance

6-12 drives (max 14)

RAIDZ3

3 disks per vdev

Like Z2, with more write overhead (for maximum safety)

Add new vdevs

Lower

Mission-critical, 3-disk fault tolerance

10-16 drives (max 20)

Optimizing drive counts

The recommended drive counts in the table above work well for most users. For even better performance, you can optimize within those ranges by choosing configurations where the number of data disks (total disks minus parity disks) is a **power of 2** (e.g., 2, 4, 8, 16). This helps align data stripes correctly, preventing wasted space and uneven I/O.

**Examples of optimized configurations:**

- **RAIDZ1**: 3, 5, or 9 drives (data disks = 2, 4, or 8)
- **RAIDZ2**: 4, 6, or 10 drives (data disks = 2, 4, or 8)
- **RAIDZ3**: 5, 9, or 17 drives (data disks = 2, 6, or 14)

Note that these optimizations are optional - the recommendations above should work well for most use cases.

How to choose

- Use **Mirror** if you want the best performance and easy, flexible expansion, and are okay with using more disk space for redundancy.
- Choose **RAIDZ1/2/3** if you want to maximize usable space and store large files, but keep in mind that expansion is less flexible, and random write performance is lower.
- **Stripe** is only suitable for non-critical, temporary data - if any disk fails, you lose everything.

------------------------------------------------------------------------

## Topology and expansion

How you group disks into vdevs affects both data safety and speed.

![](/assets/images/zfs12-58c00418818947874903fa670a4e6bc9.png)

- If you put all your disks into a large RAIDZ2 vdev, you can lose any two disks without losing data. However, expansion means adding another full vdev.
- You'll gain better parallel performance if you split disks into multiple smaller RAIDZ1 vdevs. Be cautious; if two disks fail in the same vdev, you will lose the whole pool.
- ZFS stripes data across vdevs, not individual disks, so more vdevs can lead to better performance for workloads with many small files or random I/O.
- Expanding a ZFS pool usually means adding a new vdev of the same layout, not just a single disk.

tip

Plan your pool’s layout to fit your needs and future growth. Unlike the Unraid array, you can’t add a single disk to an existing vdev using the WebGUI.

------------------------------------------------------------------------

## Compression and RAM

ZFS offers advanced features that can significantly improve Unraid's storage efficiency and performance. Two common topics of interest are compression and memory requirements.

ZFS compression is transparent - it operates in the background, shrinking data before it reaches the disk.

This offers two major benefits:

- **Reduced disk usage:** Less storage space is consumed.
- **Improved performance:** Writing and reading less data can lead to faster operations, especially on modern CPUs.

![](/assets/images/zfs13-6555bbed6a5e86c57ff05c962ad3f8fb.png)

tip

Enable ZFS compression for most Unraid ZFS pools. It's safe, efficient, and rarely impacts compatibility or stability.

**The ZFS RAM Myth** - Click to expand/collapse

You might have come across the outdated advice: “ZFS requires 1 GB of RAM per 1 TB of storage.” This is no longer applicable for most users. ZFS utilizes RAM for its Adaptive Replacement Cache (ARC), which speeds up frequently accessed reads.

Unraid automatically limits ZFS to using a reasonable portion of your system's RAM (usually 1/8th of total RAM). This allows ZFS to perform well without affecting Docker containers, VMs, or the Unraid OS.

![](/assets/images/zfs14-88e0135b5eb29bc6516e169070358140.png)

info

ZFS scales well with available memory. More RAM can enhance cache performance, but ZFS functions reliably with modest hardware. Don’t let old recommendations prevent you from using ZFS on Unraid.

------------------------------------------------------------------------

## Importing ZFS pools created on other systems

Unraid can import ZFS pools created on other platforms with minimal hassle.

**How to import a ZFS pool** - Click to expand/collapse

1.  **Stop the array:** Ensure your Unraid array is stopped.
2.  **Add new pool:** Click **Add Pool**.
3.  **Assign all drives:**
    - Set **Number of Data Slots** to the total number of drives in your ZFS pool (including data vdevs and support vdevs).
    - Assign each drive to the correct slot.
    - *Example:* For a pool with a 4-drive mirrored vdev and a 2-drive L2ARC vdev, set 6 slots and assign all six drives.
4.  **Set file system to "Auto":** Click the pool name (e.g., `raptor`) and set **File System** to **Auto**.
5.  **Finish and start array:** Click **Done**, then start the array.

Automatic detection

Unraid will automatically detect and import the ZFS pool. Support vdevs (like log, cache/L2ARC, special/dedup) are listed under **Subpools** in the WebGUI. There is no need to add subpools separately after initiating the import. Unraid will automatically import them alongside the main data disks when all required drives are assigned.

After importing, running a scrub is highly recommended to verify data integrity.

- Click the pool name (e.g., `raptor`) to open its configuration.
- Under **Pool Status**, check the status and click **Scrub**.

![](/assets/images/zfs15-e52a186cecdd992803b04050ab345ccd.png)

------------------------------------------------------------------------

## Support vdevs (subpools)")

Unraid refers to ZFS support vdevs as subpools. Most users do **not** need these, but advanced users may encounter them:

![](/assets/images/zfs16-523da321626e720dae862d5bd71e0a21.png)

Support vdev (subpool)

Purpose

Risk/Notes

Special vdev

Stores metadata and small files

The pool becomes unreadable if lost.

Dedup vdev

Enables deduplication

Requires vast amounts of RAM; risky for most users. Avoid unless you have expert needs.

Log vdev (SLOG)

Improves sync write performance

Optional. Only beneficial for certain workloads.

Cache vdev (L2ARC)

Provides SSD-based read cache

Optional. Can improve read speeds for large working sets.

Spare vdev

Not supported in Unraid (as of 7.1.2)

caution

Most Unraid users should avoid support vdevs/subpools unless you have a specific and well-understood need. They are designed for specialized workloads and can introduce complexity or risk if misused.

------------------------------------------------------------------------

## Critical support vdev drives not assigned during import

When you import a ZFS pool into Unraid, you need to assign every drive from your original pool, including those used for support vdevs, to the pool slots. Unraid will automatically recognize each drive’s role (data, log, cache, special, or dedup) once the array starts. You don’t need to specify which drive serves what purpose manually.

If you forget to include a drive that was part of a support vdev during the import, the outcome will depend on the vdev’s function:

Vdev type

If drive is missing during import

Result

Special vdev or dedup vdev

Pool will not import or will be unusable

These vdevs store critical metadata or deduplication tables. Without them, ZFS cannot safely mount the pool.

Log (SLOG) vdev

Pool imports, but sync write performance drops.

The pool remains accessible, but you may notice slower performance for workloads that rely on sync writes.

Cache (L2ARC) vdev

Pool imports, but read cache is lost

The pool works normally, but you lose the performance boost from the L2ARC cache. No data is lost.

tip

Always assign every physical drive from your original ZFS pool, including all support vdevs, when importing into Unraid. This ensures smooth detection and integration. For new pools created in Unraid, support vdevs are optional and generally not needed for most users.

------------------------------------------------------------------------

## Expanding storage

ZFS is powerful, but it's important to understand how its storage expansion works - especially if you’re planning for future growth.

Historically, ZFS vdevs have a fixed width. You can’t add a disk to an existing RAIDZ vdev to make it larger.

Ways to expand your pool include:

- **Adding a new vdev:** Grow your pool by adding another vdev (like a new mirror or RAIDZ group). This increases capacity, but you must add disks in sets that match the vdev’s configuration.
- **Replacing drives with larger ones:** Swap each drive in a vdev, one at a time, for a larger disk. See [drive replacement](/unraid-os/using-unraid-to/manage-storage/array/replacing-disks-in-array/#replacing-faileddisabled-disks) for detailed procedures. After all drives are replaced and the pool resolves, the vdev's capacity increases.
- **Creating a new pool:** Starting a new ZFS pool keeps things organized and independent for different data types or workloads.

Planning ahead

Before building your pool, consider how much storage you’ll need - not just today, but in the future. ZFS rewards good planning, especially if you want to avoid disruptive upgrades later.

------------------------------------------------------------------------

## Using ZFS pools on an existing Unraid server

If you're running a traditional Unraid array and want to add ZFS pools, here are some effective ways to integrate them:

Use case

Description

Details / Examples

Fast SSD/NVMe pool for appdata & Docker

Store the appdata share for fast, responsive containers and databases. This supports snapshots for easy rollbacks and can also host VMs for high I/O.

Many users choose a 2-drive ZFS mirror for this. It's easy to expand and delivers strong performance.

ZFS pool for important data

Use a ZFS mirror or RAIDZ2 pool for irreplaceable files like photos, tax records, and user share data. ZFS checks for corruption and self-heals with redundancy.

This setup protects critical data with automatic integrity checks and self-healing capabilities.

Daily backup or replication target

Use a ZFS disk (even within the Unraid array) as a replication target. You can replicate other pools locally or from another Unraid server.

Utilize `zfs send/receive` or tools like Syncoid for fast and reliable backups and restores.

Snapshot-based recovery pool

Keep point-in-time snapshots of critical data or containers. snapshots can be auto-scheduled and are space-efficient.

This feature enables quick recovery from accidental deletions or misconfigurations.

## Avoiding common ZFS mistakes

ZFS is a powerful file system, but there are several common pitfalls that can undermine its benefits. It’s important to keep the following points in mind before configuring your pool for a smoother experience:

- **Drive size mismatch in RAIDZ:** ZFS treats all disks in a RAIDZ vdev as the size of the smallest one. To ensure the best efficiency, always use identically sized drives within each vdev.

- **Expanding RAIDZ vdevs via the WebGUI:** RAIDZ expansion is available via the WebGUI in Unraid 7.2 and later. Earlier versions (7.1.x) supported expansion via CLI only. For step-by-step instructions, see [RAIDZ expansion](/unraid-os/using-unraid-to/manage-storage/cache-pools/#raidz-expansion).

- **ZFS disk vs. full zpool:** A single ZFS-formatted disk in the Unraid array does not offer the redundancy or features of a dedicated ZFS pool. To leverage advanced functionality, use standalone pools.

- **Deduplication without adequate RAM:** Deduplication requires significant memory, and enabling it without enough RAM can severely impact performance. Only enable deduplication if you fully understand the requirements.

- **Vdev redundancy is local:** Redundancy in ZFS is local to each vdev and not shared across the pool. Make sure to plan your vdev layout to achieve the level of resilience you need.

[Edit this page](https://github.com/unraid/docs/edit/main/docs/unraid-os/advanced-configurations/optimize-storage/zfs-storage.mdx)

[](/category/optimize-storage/)

Previous

Optimize storage

[](/unraid-os/troubleshooting/)

Next

Troubleshooting

- [Why ZFS?](#why-zfs)
  - [Pools, vdevs, and redundancy](#pools-vdevs-and-redundancy)
- [Creating a ZFS pool](#creating-a-zfs-pool)
- [Adding a ZFS disk to the array (Hybrid setup)](#adding-a-zfs-disk-to-the-array-hybrid-setup)
- [Choosing an allocation profile](#choosing-an-allocation-profile)
- [Topology and expansion](#topology-and-expansion)
- [Compression and RAM](#compression-and-ram)
- [Importing ZFS pools created on other systems](#importing-zfs-pools-created-on-other-systems)
- [Support vdevs (subpools)](#support-vdevs-subpools)
- [Critical support vdev drives not assigned during import](#critical-support-vdev-drives-not-assigned-during-import)
- [Expanding storage](#expanding-storage)
- [Using ZFS pools on an existing Unraid server](#using-zfs-pools-on-an-existing-unraid-server)
- [Avoiding common ZFS mistakes](#avoiding-common-zfs-mistakes)

Documentation

- [Home](/)
- [Contribute on GitHub](https://github.com/unraid/docs)
- [Contribute translations](https://unraid.crowdin.com/unraid-docs)

Community

- [Forums](https://forums.unraid.net)
- [Discord](https://discord.unraid.net/)
- [Feature and Bug Tracker](https://product.unraid.net/)

More

- [Unraid Home](https://unraid.net)
- [Unraid Connect](https://connect.myunraid.net)
- [Newsletter](https://newsletter.unraid.net)
- [Blog](https://unraid.net/blog)

License

- [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

![Unraid Logo](/img/un-mark-gradient.svg)![Unraid Logo](/img/un-mark-gradient.svg)

Copyright © 2005-2026 Lime Technology, Inc.  
Unraid® is a registered trademark of Lime Technology, Inc.
