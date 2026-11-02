---
tags: [syncthing, sync, folder-types, versioning]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/syncthing/getting-started.md, raw/syncthing/foldertypes.md, raw/syncthing/versioning.md]
---
# Syncthing devices, folder types and file versioning

## Getting started
Syncthing synchronises folders between "devices". Start the `syncthing` binary; it creates a `Default Folder` in a directory called `Sync` in your home directory, and the admin GUI is at `http://localhost:8384/` (cookies required). The startup log shows QUIC and TCP listeners on port 22000 and a relay listener.

Two devices *only* connect if each is configured with the other's device ID. Device IDs are generated at first start, are essentially part of the public key, and don't need to be kept secret. On both devices click "Add Remote Device", enter the other side's ID, select the folders to share and "Save"; the device connects after a minute or so. Connection problems: see the firewall notes in [[syncthing-ignore-firewall]].

## Folder types
- **Send & Receive** (standard): sends and receives changes.
- **Send Only**: for a "reference copy"; changes from other devices are ignored (received but not applied). When out of sync, a red "Override Changes" button enforces this host's state on the cluster — remote changes are overwritten and files missing here are deleted.
- **Receive Only** (added in version 0.14.50): cluster changes are applied, local changes are not sent; useful for backup destinations. A red "Revert Local Changes" button undoes local modifications. Conflicts are resolved with the cluster version as the winner.

## File versioning
Configured per folder, per device; default is no versioning. Versioning applies only to changes received *from other devices*, never to local edits. Versions go to `.stversions` inside the folder by default; a custom path should be on the same filesystem.
- **Trash Can**: replaced/deleted files moved to `.stversions`; `cleanoutDays` removes old ones (zero = never).
- **Simple**: also keeps a number of versions ("Keep Versions"); example config uses `keep` 5.
- **Staggered**: first hour keeps the oldest version per 30-seconds interval, first day one per hour, first 30 days one per day, then one per week until **Maximum Age** (`maxAge`, in days; 365 keeps a year; 0 keeps versions forever).
- **External**: runs a command with `%FOLDER_PATH%` and `%FILE_PATH%` (since 2.1.2 also `$FOLDER_PATH`/`$FILE_PATH`); shell wrapping such as sh -c is invalid.
`versioning.type` is one of `trashcan`, `simple`, `staggered`, `external`, or empty to disable.

derived_from:: [[raw/syncthing/getting-started.md]]
derived_from:: [[raw/syncthing/foldertypes.md]]
derived_from:: [[raw/syncthing/versioning.md]]
