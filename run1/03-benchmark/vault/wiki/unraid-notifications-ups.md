---
tags: [unraid, settings, notifications, ups, scheduler]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/unraid/customize-settings-notifications-ups.md]
---
# Unraid notifications, UPS and scheduler settings

## UPS settings
Unraid can be connected to an APC (or compatible) UPS so the system can safely shut down during a power loss while still receiving battery power. The UPS settings page configures the UPS connection and the policies for the shutdown command.

## Notification settings
Path: ***Settings → User Preferences → Notification Settings***.
- **Display and behavior**: **Notifications display** *Detailed* or *Summarized*; **Display position** (*top-right*, *top-left*, *bottom-right*, *bottom-left*, *center*); **Auto-close (seconds)**; **Date format**; **Store notifications to boot drive**.
- **Notification types**: System notifications, Unraid OS update, Plugins update, Docker update, Language update, **Array status notification**. Each can be set to *Never check* or checked daily, weekly, monthly, or in some cases multiple times a day.
- **Delivery methods** per category (*Notices*, *Warnings*, *Alerts*): **Browser**, **Email** (requires SMTP), **Agents** (third-party services).

### SMTP (email)
***Settings → User Preferences → Notification Settings → SMTP Settings***: **Preset service** (*Gmail*, *Outlook/Hotmail*, *Custom*), sending address, comma-separated **Email recipients**, **Email subject prefix** (default *Unraid Status:*), **Mail server** (e.g. `smtp.gmail.com`), **Mail server port** (`465` for SSL/TLS, `587` for STARTTLS, `25` for unencrypted), **Authentication method** *None*, *CRAM-MD5* or *Login*. Use the **TEST** button to verify.

### Notification agents
Built-in agents include Bark, Boxcar, Discord, Gotify, ntfy.sh, Prowl, Pushbits, Pushbullet, Pushover, Pushplus, ServerChan, Slack and Telegram. To configure: select the agent, change **Agent function** from *Disabled* to *Enabled*, fill in webhook URL or token, set **Notification title** (usually *Subject*) and **Notification message** (usually *Description*), click **DONE**. **All notifications** are sent to **all enabled agents**, so several agents can produce duplicates.

## Other settings on the same page
- **Scheduler**: frequency of parity checks, the cache Mover, and TRIM/Discard for SSDs.
- **Power Mode**: **Best power efficiency**, **Balanced operation** or **Best performance**; takes effect immediately, no restart.
- **Tailscale** section appears only with the Tailscale plugin installed (see [[unraid-tailscale]]); **VPN manager** uses WireGuard.

derived_from:: [[raw/unraid/customize-settings-notifications-ups.md]]
