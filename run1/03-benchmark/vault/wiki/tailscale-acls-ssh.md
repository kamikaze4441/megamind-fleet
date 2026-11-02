---
tags: [tailscale, acl, grants, policy, ssh]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/tailscale/acls.md, raw/tailscale/tailscale-ssh.md]
---
# Tailscale ACLs and Tailscale SSH

## ACLs
Access controls are defined in the tailnet policy file as ACLs or grants; both follow a deny-by-default principle. An ACL entry has `"action": "accept"`, a `src` list and a `dst` list of `<destination>:<port>`.
- The default tailnet policy file enables communication between all devices. With no `acls` section, Tailscale applies the default allow all policy; to deny all traffic use an empty object for the `acls` section.
- ACLs are deny-by-default, **directional** (A→B does not allow B→A), **locally enforced** on each device without the coordination server, and do not affect local network traffic.
- Edit via the admin console **Access controls** page, GitOps, or the Tailscale API.
- On all plans: `acls`, `grants`, `groups`, autogroups (e.g. `autogroup:admin`, `autogroup:internet`), `tagOwners`, `autoApprovers`, `nodeAttrs`, `hosts`, `ipsets`, `tests`. SSH rules (`ssh`) are Basic on Personal and Standard, Advanced on Premium and Enterprise.

## Tailscale SSH
Tailscale authenticates and encrypts SSH over WireGuard using node keys, distributes SSH host keys, and authorizes connections from the access control policy; revoking access takes effect within seconds. When enabled, Tailscale claims port `22` on the Tailscale IP address.
- Server side only on Linux and macOS open source `tailscaled` devices, Tailscale v1.24 or later; not on Synology or QNAP. Clients can be any platform.
- Enable on the host: `tailscale set --ssh` (existing SSH connections to the Tailscale IP will hang). Disable: `tailscale set --ssh=false`.
- Connect with the MagicDNS name: `ssh device` (see [[tailscale-magicdns]]).

### `ssh` rules
- `action`: `accept` or `check` (re-authenticate with the identity provider).
- `src`: user, group, tag, `user:*@<domain>` or autogroup — not a bare `*`.
- `dst`: user, tag or autogroup; no port (only port `22`).
- `users`: existing host accounts, e.g. `autogroup:nonroot`, `root`, `localpart:*@<domain>`.
- `checkPeriod`: default 12 hours; minimum one minute, maximum 168 hours; or `always`.
- `acceptEnv`: allowlisted env var names (host needs Tailscale v1.76.0 or later).
The default policy rule: `"action": "check"`, `src` `autogroup:member`, `dst` `autogroup:self`, `users` `autogroup:nonroot` and `root`. Modifying the SSH policy overrides it; removing it disables Tailscale SSH. If both a check and an accept rule match, the check rule applies.

Limits: only tailnet devices (not devices behind subnet routers); port `22` cannot be changed; restarting `tailscaled` stops sessions; check mode only for Tailscale SSH.

derived_from:: [[raw/tailscale/acls.md]]
derived_from:: [[raw/tailscale/tailscale-ssh.md]]
