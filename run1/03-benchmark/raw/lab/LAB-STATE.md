# LAB-STATE: fictional home lab "lab77" (fleet-written, CC0; all names and 10.77.x.x addresses are invented; last verified 2026-10-30)

## Verified facts
- atlas is the Unraid server at 10.77.0.10; it is powered through the UPS apc-1, and apc-1's USB link tells atlas to shut down cleanly after 5 minutes on battery, so atlas needs apc-1.
- tank is the ZFS pool inside atlas (shares appdata, media, domains, notes); tank exists only while atlas is running.
- hermes is a Debian VM on atlas at 10.77.0.20 with its vdisk on tank/domains; hermes runs on atlas and stops when atlas stops, and it cannot boot without tank.
- hermes hosts the wiki repo (/srv/wiki, a git repository) and the wiki search service (qmd); the wiki search service needs hermes.
- The wiki search index is rebuilt by a systemd timer on hermes at 02:30 every night; when hermes is down the index goes stale.
- The wiki search service calls the Ollama endpoint on titan (http://10.77.0.30:11434) for embeddings; when titan is off, new wiki pages are not embedded but keyword search still works.
- Plex runs as a Docker container on atlas; it needs atlas, and it reads its library from tank/media and keeps its appdata on tank/appdata, so it needs tank.
- The reverse proxy is a Caddy container on atlas that fronts Plex and the wiki search service on port 443; it needs atlas, and outside access to it needs gate to forward port 443.
- gate is the UniFi gateway at 10.77.0.1 and the lab's only route to the internet; atlas, hermes and titan use static addresses, and only aria takes its address from gate's DHCP.
- Syncthing runs as a container on atlas and syncs tank/notes to pebble; Syncthing needs tank, and Syncthing to pebble runs over Tailscale only (no relays, no LAN discovery).
- Tailscale runs as the Unraid plugin on atlas; atlas is the tailnet's only exit node and also advertises the subnet route 10.77.0.0/24, so Tailscale remote access needs atlas, and it needs gate to reach the internet.
- pebble is a MacBook; away from home it reaches hermes and Plex only through Tailscale via atlas, so pebble's remote access needs Tailscale.
- titan is the Windows gaming PC at 10.77.0.30; Ollama runs on titan on its Intel Arc GPU through Vulkan, so the Ollama endpoint needs titan to be awake.
- The nightly rclone backup runs on atlas at 06:00, reads the tank snapshot taken at 05:45 and uploads it to the cloud drive remote "offsite-crypt"; the backup needs tank and needs gate for internet access.
- Unraid notifications from atlas (parity check, UPS on battery, backup result) are sent by the email agent through gate, so notifications need gate.
- aria is the living-room Denon AVR-X1700H at 10.77.0.40; it gets its network address from gate, so its network features need gate.

## Pending
- Replace the apc-1 battery (self-test warning on 2026-10-28); until then runtime on battery is unverified.
- Add hermes as a second exit node; until then atlas is a single point of failure for remote access.
