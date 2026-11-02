---
tags: [unraid, storage, array, parity]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/unraid/array-overview.md]
---
# Unraid array and parity

The Unraid array holds primary storage with optional parity protection; cache pools sit beside it for speed (see [[unraid-pools-zfs]]).

## Parity rules
- Use your largest drives for parity: data disks can't be larger than your parity disks. With dual parity, both parity drives should be at least the size of your largest data disk, but they may differ from each other. No disk can be larger than your smallest parity drive.
- Unraid doesn't support TRIM/Discard for SSDs in the main array, so keep SSDs in cache pools or as unassigned devices.
- Unraid identifies disks by serial number and size, not by SATA port, so drives can move between ports.
- The array will not start if you assign or attach more devices than your license key allows.
- Encryption is disabled by default and requires reformatting drives (which erases data).

## Start/stop
Main tab → **Array Operation** → **Start** or **Stop**. Stopping the array fully stops all Docker containers and network shares, shuts down or hibernates VMs, and unmounts storage. After a disk-setup change the array stays off at boot so you can check the configuration. New array drives are formatted XFS by default; ZFS or BTRFS can be chosen.

## Write modes
Set in ***Settings → Disk Settings*** → **Tunable (md_write_method)**:
- **Read/Modify/Write** (default): 20–40 MB/s, low power, only parity and target drive spin up.
- **Turbo Write (Reconstruct)**: 40–120 MB/s, high power, all drives spin; for large transfers, rebuilds and parity checks; avoid if a drive may be failing.
- **Cache Write**: 50–110 MB/s (SSD), 250–900 MB/s (NVMe); data is not parity-protected until the Mover moves it (typically at 3:40 AM).
- **Auto** is listed as a future feature.

Without a cache drive writes average 20–30 MB/s, with peaks up to 40 MB/s.

## Read speeds
Each file lives on a single disk, so reads are not striped: typical single HDD 70–250 MB/s, SATA SSD 400–550 MB/s. While a disabled disk is reconstructed from parity, reads may slow to 30–60 MB/s.

derived_from:: [[raw/unraid/array-overview.md]]
