---
tags: [syncthing, stignore, firewall, ports]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/syncthing/ignoring.md, raw/syncthing/firewall.md]
---
# Syncthing ignore patterns and firewall setup

## `.stignore`
Files not to be synced are listed in `.stignore`, which must be in the root of the synced folder. It is never synced itself, but can `#include` files that are. The *first* pattern that matches decides a file's fate.
- `foo` matches `foo`, `subdir/foo` and any directory named `foo`.
- `*` does not cross the directory separator (`te*ne` matches `telephone` but not `tele/phone`); `**` does (`te**ne` matches `tele/sub/dir/phone`).
- `?` one character; `[a-z]` range; `{banana,pineapple}` alternatives; `\` escapes (on Windows use `|`, or put `#escape=\` at the top of the file).
- `/foo` matches in the folder root only.
- `!` negates (include); negated patterns below the root force scanning of otherwise ignored directories, except top-level rooted ones like `!/foo`.
- `(?i)` case-insensitive (always so on Mac OS and Windows); `(?d)` allows deletion of ignored files that block directory removal (e.g. `(?d).DS_Store`). Prefixes combine as `(?d)(?i)` but not (?di).
- `//` starts a comment only at the start of a line.
- A pattern ending in `/` matches the directory's content but not the directory itself.
Default patterns for auto-accepted folders were added in version 1.19.0; the `|` escape and `#escape=X` in version 2.0.0.

## Ports and router
- Local firewall: **22000/TCP** (TCP sync), **22000/UDP** (QUIC sync), **21027/UDP** (discovery broadcasts on IPv4 and multicasts on IPv6).
- Router: enable UPnP on Syncthing and the router, or forward **22000/TCP** and **22000/UDP** with identical external and internal ports. A port forward on one device lets others connect to it even behind NAT. Without port forwarding, relaying may work but performs poorly compared with a direct connection.
- Local discovery needs broad-/multicasts, often blocked between subnets. With static IPs, replace the default `dynamic` address with something like `tcp://192.168.1.xxx:22000` followed by `dynamic`.
- `ufw`: `sudo ufw allow syncthing` (and `syncthing-gui` only for external GUI access; check with `sudo ufw status verbose`). Firewalld: `sudo firewall-cmd --zone=public --add-service=syncthing --permanent` then `sudo firewall-cmd --reload`.

## Remote web GUI
Change *GUI Listen Address* from `127.0.0.1:8384` to `0.0.0.0:8384` and open the port, or tunnel instead: `ssh -L 9999:localhost:8384 machine`. Syncthing can use a SOCKS5 proxy for outbound connections. Device and folder basics: [[syncthing-folders-versioning]].

derived_from:: [[raw/syncthing/ignoring.md]]
derived_from:: [[raw/syncthing/firewall.md]]
