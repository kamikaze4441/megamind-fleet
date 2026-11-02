---
tags: [unraid, docker, vm, containers]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/unraid/docker-managing-containers.md, raw/unraid/vm-setup.md]
---
# Unraid Docker containers and VMs

## Container template settings
- **Network type**: **Bridge (default)** — only explicitly mapped ports are reachable; **Host** — shares the server's network stack; **None**; **Custom (macvlan/ipvlan)** — own LAN IP. Docker cannot join two networks on the same subnet, so switching between wired and wireless needs a Docker restart and container reconfiguration.
- **Volume mappings**: container path (e.g. `/config`) ↔ host path (e.g. `/mnt/user/appdata/myapp`), read-only or read/write. Keep app data in the `appdata` share. Paths are case-sensitive; host paths are created automatically if missing. In the app, use the container path: map `/mnt/user/media` to `/unraid_media` and set the library to `/unraid_media`.
- **Port mappings**: in bridge mode three containers using port 8000 can map to 8000, 8001 and 8002 on the host. Only modify the host port.
- **Environment variables**: e.g. `TZ=America/New_York`, `PUID=99` and `PGID=100`, `UMASK=022`.

## Startup order
Toggle **Auto-Start** on the **Docker** tab so a container starts with the array. By default auto-start containers start as quickly as possible in Docker-tab order. To change: unlock the list with the padlock icon, drag to reorder, switch to **Advanced View**, and enter a wait time (in seconds) in the **wait** field of the **AutoStart** column — e.g. start a database or VPN before the apps that need it. There is no built-in test; stop all containers and start them by hand in order.

Health indicator: Healthy, Unhealthy (failed health check), No health check. Unraid has no native scheduled start/stop; use the **User Scripts plugin** (***Settings → User Scripts***) with a `cron` expression such as `0 3 * * 1` (3:00 AM every Monday) and `docker start "container-name"`.

## VMs (VM Manager)
Before creating a VM, configure the `isos` and `domains` shares and upload the OS ISO (and VirtIO drivers ISO for Windows) to `isos`. **Add VM** → template → name → **Autostart** → CPU cores → **Initial Memory** → **OS Install ISO** → **Primary vDisk** → **Graphics Card** (VNC or a physical GPU) → **USB Devices** (no hot-plugging; the boot USB cannot be assigned) → **Create VM**.

Unraid 7.x adds VM clones and snapshots, user VM templates (7.1+), inline XML editing and GPU sharing (`VirGL`, `QXL`). Snapshot metadata is stored in `/etc/libvirt/qemu/snapshotdb/VM_name/`; QCOW2 disks support snapshots. VirtFS (`9p`) shares give host–guest file system integration. A vDisk can be expanded (e.g. `100G`) with the VM stopped but cannot be shrunk from the GUI.

derived_from:: [[raw/unraid/docker-managing-containers.md]]
derived_from:: [[raw/unraid/vm-setup.md]]
