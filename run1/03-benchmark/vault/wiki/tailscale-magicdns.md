---
tags: [tailscale, dns, magicdns]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/tailscale/magicdns.md]
---
# Tailscale MagicDNS

MagicDNS automatically registers DNS names for devices in your tailnet, so a new server called `my-server` can be reached by that name instead of its Tailscale IP. It is available for all plans.

## Requirements and defaults
- No DNS nameserver is required on Tailscale v1.20 or later; otherwise the tailnet needs at least one DNS nameserver set on the admin console **DNS** page, which receives all queries MagicDNS does not handle.
- Tailnets created on or after October 20, 2022 have MagicDNS enabled by default; otherwise enable it on the **DNS** page.

## Names
MagicDNS uses the device's machine name; renaming the machine changes its DNS entry. Each device gets a **fully qualified domain name** = machine name + tailnet DNS name, e.g. `monitoring.yak-bebop.ts.net`. Tailscale adds search domains, so `ping monitoring` and `ping monitoring.yak-bebop.ts.net` are equivalent. Examples once enabled: `ssh username@monitoring`, `ping monitoring`, or `monitoring` in a browser.
- Devices **shared with you** need Tailscale v1.4 or later and the full domain name (e.g. `ping webserver.example2.ts.net`).
- On macOS, `host` and `nslookup` circumvent system DNS and do not work with MagicDNS (`host johns-iphone-6s` fails while `ping johns-iphone-6s` works).
- Legacy names ending in `.beta.tailscale.net` stopped being supported on **September 13, 2024**; migrate to `.ts.net`. Removing the `beta.tailscale.net` nameserver needs an Owner, Admin, or IT admin and cannot be undone.

## Disabling
Tailnet-wide: toggle the same button on the **DNS** page. Per device, stop accepting network DNS settings: Linux `tailscale set --accept-dns=false`; macOS menu bar → **Preferences** → uncheck **Use Tailscale DNS settings**; Windows hold `SHIFT` while right-clicking the tray icon and deselect **Use Tailscale DNS**.

Tailscale SSH uses MagicDNS names (`ssh device`) — see [[tailscale-acls-ssh]].

derived_from:: [[raw/tailscale/magicdns.md]]
