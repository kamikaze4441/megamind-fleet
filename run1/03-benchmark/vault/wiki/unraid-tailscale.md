---
tags: [unraid, tailscale, remote-access, docker]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/unraid/tailscale.md, raw/tailscale/unraid.md]
---
# Tailscale on Unraid (plugin and containers)

Tailscale is a peer-to-peer overlay network built on WireGuard; official support was added in Unraid v7. Free accounts support up to three users and 100 devices. Machine names in HTTPS certificates are public.

## Install the plugin
Install the official **Tailscale (Plugin)** from Community Apps (ignore legacy options such as Docker); the Tailscale docs say Derek Kaser maintains it on behalf of Unraid. Open ***Settings → Tailscale → Settings***, turn on ***Advanced View***, click **Reauthenticate**, sign in, then **Connect**. Tailscale WebGUI URLs are under ***Settings → Management Access***. The server gets a tailnet `100.x.y.z` address and hostname (e.g. `tower`). Optional: **Include Tailscale peers in /etc/hosts**.

## Exit node and subnet routes
- **Exit node**: Plugins → Tailscale → **Run as Exit Node**, then approve in the admin console Machines page (**Edit route settings** → **Use as exit node**); `autoApprovers` can approve automatically. See [[tailscale-exit-nodes-subnets]].
- **Subnet router**: in the plugin's **Advertise Routes** add the server IP (e.g. `192.168.0.12/32`) or the subnet (e.g. `192.168.0.0/24`), **Apply**, then approve the route on the **Machines** page. From the terminal: `tailscale up --advertise-routes=192.0.2.0/24`.

## Tailscale in Docker containers
Edit a container, enable **Use Tailscale**, give a unique **Tailscale hostname** (its HTTPS certificate is published in a public ledger), optionally make it an exit node or use one, optionally enable **Tailscale SSH**, and choose **Serve** (tailnet-only HTTPS URL) or **Funnel** (public internet). Unraid injects the `tailscale_container_hook` script before the original Entrypoint. Serve and Funnel add no extra authentication. Not every container works with it; test on non-critical containers first.

**Userspace networking**: enabled = cannot initiate connections to other tailnet devices or use Tailscale DNS; disabled = full tailnet access. Exit-node containers always have it enabled; containers that use an exit node always have it disabled.

Persistent state error "Couldn't detect persistent Docker directory for .tailscale_state": set the **State directory** to `/container-path/.tailscale_state` and restart. Containers can also join automatically with an OAuth client and `--advertise-tags=tag:example`.

Update the plugin from the Apps tab; update container Tailscale with **Force update** in **Advanced View**.

derived_from:: [[raw/unraid/tailscale.md]]
derived_from:: [[raw/tailscale/unraid.md]]
