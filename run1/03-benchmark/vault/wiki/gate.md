---
tags: [lab, network, gateway, unifi]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/lab/LAB-STATE.md]
---
# gate (UniFi gateway)

gate is the UniFi gateway at 10.77.0.1 and the lab's only route to the internet. atlas, hermes and titan use static addresses; only [[aria]] takes its address from gate's DHCP.

## What needs gate
- [[reverse-proxy]]: outside access needs gate to forward port 443.
- [[tailscale]]: needs gate to reach the internet.
- [[rclone-backup]]: needs gate for internet access to upload to the cloud drive.
- Unraid notifications from [[atlas]]: sent by the email agent through gate.
- [[aria]]: gets its network address from gate, so its network features need gate.

derived_from:: [[raw/lab/LAB-STATE.md]]
