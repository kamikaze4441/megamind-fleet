---
tags: [tailscale, exit-node, subnet-router, routing]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/tailscale/exit-nodes.md, raw/tailscale/subnet-routers.md]
---
# Tailscale exit nodes and subnet routers

## Exit nodes
By default Tailscale only routes traffic between tailnet devices. An **exit node** routes all public internet traffic for devices that opt in, using default routes (`0.0.0.0/0`, `::/0`) like a typical VPN — e.g. on untrusted coffee-shop Wi-Fi. Exit nodes are available for all plans.
- Opt-in on all sides: every device must opt in, the device must advertise itself, and an Owner, Admin, or Network admin must allow it.
- Prerequisites: **Tailscale v1.20 or later** on both sides; exit node on Linux, macOS, Windows, Android, iOS, or tvOS.
- Linux: enable IP forwarding first (with `firewalld` you may need `firewall-cmd --permanent --add-masquerade`), then `sudo tailscale set --advertise-exit-node` followed by `sudo tailscale up`.
- Approve: admin console **Machines** page → **Exit Node** badge (filter `property:exit-node`) → **Edit route settings** → **Use as exit node**. `autoApprovers` approves automatically.
- Access: by default any tailnet user can use an exit node. With a custom policy you must grant `dst` `autogroup:internet`; granting the exit node device itself only permits connections to it (e.g. SSH).
- Use on Linux: `sudo tailscale set --exit-node=<exit-node-ip>`; add `--exit-node-allow-lan-access=true` for local network access (off by default); stop with `sudo tailscale set --exit-node=`.
- Caveats: macOS and Windows exit nodes must be kept from sleeping; Windows exit nodes are userspace-only and use a system thread per DNS query; consider "Run Unattended".

## Subnet routers
A subnet router is a tailnet device used as a gateway that advertises routes, so devices can be reached without installing Tailscale. Subnet routers use SNAT by default; disable with `tailscale up --snat-subnet-routes=false` (Linux only).
1. Linux: enable IP forwarding — `echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf`, the same for `net.ipv6.conf.all.forwarding = 1`, then `sudo sysctl -p /etc/sysctl.d/99-tailscale.conf`.
2. Advertise: `sudo tailscale set --advertise-routes=192.0.2.0/24,198.51.100.0/24` (Apple TV supports IPv4 subnets only). For default routes use an exit node instead.
3. Approve in **Machines** → **Subnets** badge (filter `property:subnet`) → select routes → **Save** (skip with `autoApprovers`).
4. Add access rules (grants) for the subnets in the tailnet policy file — route approval and access rules are separate mechanisms.
5. Verify: ping the router's address from `tailscale ip -4`.
6. Android, iOS, macOS, tvOS and Windows pick up routes automatically; Linux clients need `sudo tailscale set --accept-routes`.
For high availability, use `--advertise-routes` alone and avoid `--accept-routes` on the routers. Unraid specifics: [[unraid-tailscale]]; policy syntax: [[tailscale-acls-ssh]].

derived_from:: [[raw/tailscale/exit-nodes.md]]
derived_from:: [[raw/tailscale/subnet-routers.md]]
