# Corpus (run 1, benchmark 03)

Frozen at the step-1 report; `raw/` is not changed after that. Wiki pages fed by each source: filled in step 2 (column 'wiki pages').

Conversion: `.md` URLs saved verbatim; HTML pages reduced to their main element (`<article>` on docs.unraid.net, `div[role=main]` on docs.syncthing.net) with Python `html.parser`, inline `<svg>` and `data:` images dropped, then `pandoc -f html -t gfm-raw_html --wrap=none`; heading permalink anchors (`[​](#…)`, `[¶](#…)`) removed and `data:` markdown images replaced by `[image: alt]`. Each file starts with a one-line `<!-- source: … | fetched: … -->` comment. Script: `/tmp/b1/fetch.py` (copied to `harness/fetch-corpus.py`).

| id | group | title | URL | licence / terms | fetched | raw path | bytes | wiki pages |
|---|---|---|---|---|---|---|---|---|
| unraid-array | unraid | Arrays | https://docs.unraid.net/unraid-os/using-unraid-to/manage-storage/array/overview/ | CC BY-SA 4.0 (docs.unraid.net footer: documentation content only; © 2005-2026 Lime Technology, Inc.) | 2026-11-02 | raw/unraid/array-overview.md | 14658 | (step 2) |
| unraid-cache-pools | unraid | Cache pools | https://docs.unraid.net/unraid-os/using-unraid-to/manage-storage/cache-pools/ | CC BY-SA 4.0 (docs.unraid.net footer: documentation content only; © 2005-2026 Lime Technology, Inc.) | 2026-11-02 | raw/unraid/cache-pools.md | 30967 | (step 2) |
| unraid-zfs | unraid | ZFS storage | https://docs.unraid.net/unraid-os/advanced-configurations/optimize-storage/zfs-storage/ | CC BY-SA 4.0 (docs.unraid.net footer: documentation content only; © 2005-2026 Lime Technology, Inc.) | 2026-11-02 | raw/unraid/zfs-storage.md | 20491 | (step 2) |
| unraid-shares | unraid | Shares | https://docs.unraid.net/unraid-os/using-unraid-to/manage-storage/shares/ | CC BY-SA 4.0 (docs.unraid.net footer: documentation content only; © 2005-2026 Lime Technology, Inc.) | 2026-11-02 | raw/unraid/shares.md | 28647 | (step 2) |
| unraid-docker | unraid | Managing & customizing containers | https://docs.unraid.net/unraid-os/using-unraid-to/run-docker-containers/managing-and-customizing-containers/ | CC BY-SA 4.0 (docs.unraid.net footer: documentation content only; © 2005-2026 Lime Technology, Inc.) | 2026-11-02 | raw/unraid/docker-managing-containers.md | 17895 | (step 2) |
| unraid-vm-setup | unraid | VM setup | https://docs.unraid.net/unraid-os/using-unraid-to/create-virtual-machines/vm-setup/ | CC BY-SA 4.0 (docs.unraid.net footer: documentation content only; © 2005-2026 Lime Technology, Inc.) | 2026-11-02 | raw/unraid/vm-setup.md | 26914 | (step 2) |
| unraid-tailscale | unraid | Tailscale | https://docs.unraid.net/unraid-os/system-administration/secure-your-server/tailscale/ | CC BY-SA 4.0 (docs.unraid.net footer: documentation content only; © 2005-2026 Lime Technology, Inc.) | 2026-11-02 | raw/unraid/tailscale.md | 15504 | (step 2) |
| unraid-settings | unraid | Customize Unraid settings | https://docs.unraid.net/unraid-os/getting-started/set-up-unraid/customize-unraid-settings/ | CC BY-SA 4.0 (docs.unraid.net footer: documentation content only; © 2005-2026 Lime Technology, Inc.) | 2026-11-02 | raw/unraid/customize-settings-notifications-ups.md | 25741 | (step 2) |
| ollama-api | ollama | Introduction | https://docs.ollama.com/api.md | MIT (docs are built from ollama/ollama repo `docs/`, repo LICENSE MIT, © Ollama); served from https://docs.ollama.com/api/introduction.md | 2026-11-02 | raw/ollama/api.md | 2769 | (step 2) |
| ollama-modelfile | ollama | Modelfile Reference | https://docs.ollama.com/modelfile.md | MIT (docs are built from ollama/ollama repo `docs/`, repo LICENSE MIT, © Ollama) | 2026-11-02 | raw/ollama/modelfile.md | 9360 | (step 2) |
| ollama-gpu | ollama | Hardware support | https://docs.ollama.com/gpu.md | MIT (docs are built from ollama/ollama repo `docs/`, repo LICENSE MIT, © Ollama) | 2026-11-02 | raw/ollama/gpu.md | 9081 | (step 2) |
| ollama-faq | ollama | FAQ | https://docs.ollama.com/faq.md | MIT (docs are built from ollama/ollama repo `docs/`, repo LICENSE MIT, © Ollama) | 2026-11-02 | raw/ollama/faq.md | 18812 | (step 2) |
| ollama-docker | ollama | Docker | https://docs.ollama.com/docker.md | MIT (docs are built from ollama/ollama repo `docs/`, repo LICENSE MIT, © Ollama) | 2026-11-02 | raw/ollama/docker.md | 3120 | (step 2) |
| ollama-openai | ollama | OpenAI compatibility | https://docs.ollama.com/api/openai-compatibility.md | MIT (docs are built from ollama/ollama repo `docs/`, repo LICENSE MIT, © Ollama) | 2026-11-02 | raw/ollama/openai-compatibility.md | 27537 | (step 2) |
| syncthing-getting-started | syncthing | Getting Started | https://docs.syncthing.net/intro/getting-started.html | CC BY 4.0 (syncthing/docs README.rst 'License' section, commit f02059067d50) | 2026-11-02 | raw/syncthing/getting-started.md | 8035 | (step 2) |
| syncthing-foldertypes | syncthing | Folder Types | https://docs.syncthing.net/users/foldertypes.html | CC BY 4.0 (syncthing/docs README.rst 'License' section, commit f02059067d50) | 2026-11-02 | raw/syncthing/foldertypes.md | 2564 | (step 2) |
| syncthing-versioning | syncthing | File Versioning | https://docs.syncthing.net/users/versioning.html | CC BY 4.0 (syncthing/docs README.rst 'License' section, commit f02059067d50) | 2026-11-02 | raw/syncthing/versioning.md | 14082 | (step 2) |
| syncthing-ignoring | syncthing | Ignoring Files | https://docs.syncthing.net/users/ignoring.html | CC BY 4.0 (syncthing/docs README.rst 'License' section, commit f02059067d50) | 2026-11-02 | raw/syncthing/ignoring.md | 7552 | (step 2) |
| syncthing-firewall | syncthing | Firewall Setup | https://docs.syncthing.net/users/firewall.html | CC BY 4.0 (syncthing/docs README.rst 'License' section, commit f02059067d50) | 2026-11-02 | raw/syncthing/firewall.md | 4071 | (step 2) |
| tailscale-exit-nodes | tailscale | Exit nodes (route all traffic) | https://tailscale.com/docs/features/exit-nodes.md | terms not stated as a licence; site footer '© 2026 Tailscale Inc. All rights reserved.'; fetched for private benchmark use only | 2026-11-02 | raw/tailscale/exit-nodes.md | 21816 | (step 2) |
| tailscale-subnet-routers | tailscale | Subnet routers | https://tailscale.com/docs/features/subnet-routers.md | terms not stated as a licence; site footer '© 2026 Tailscale Inc. All rights reserved.'; fetched for private benchmark use only | 2026-11-02 | raw/tailscale/subnet-routers.md | 27658 | (step 2) |
| tailscale-acls | tailscale | Manage permissions using ACLs | https://tailscale.com/docs/features/access-control/acls.md | terms not stated as a licence; site footer '© 2026 Tailscale Inc. All rights reserved.'; fetched for private benchmark use only | 2026-11-02 | raw/tailscale/acls.md | 7405 | (step 2) |
| tailscale-magicdns | tailscale | MagicDNS | https://tailscale.com/docs/features/magicdns.md | terms not stated as a licence; site footer '© 2026 Tailscale Inc. All rights reserved.'; fetched for private benchmark use only | 2026-11-02 | raw/tailscale/magicdns.md | 7100 | (step 2) |
| tailscale-ssh | tailscale | Tailscale SSH | https://tailscale.com/docs/features/tailscale-ssh.md | terms not stated as a licence; site footer '© 2026 Tailscale Inc. All rights reserved.'; fetched for private benchmark use only | 2026-11-02 | raw/tailscale/tailscale-ssh.md | 32766 | (step 2) |
| tailscale-unraid | tailscale | Access Unraid NAS from anywhere | https://tailscale.com/docs/integrations/unraid.md | terms not stated as a licence; site footer '© 2026 Tailscale Inc. All rights reserved.'; fetched for private benchmark use only; 1 example auth key redacted by benchmark | 2026-11-02 | raw/tailscale/unraid.md | 8332 | (step 2) |
| cc-settings | claude-code | Settings files and precedence | https://code.claude.com/docs/en/settings.md | terms not stated as a licence; footer links Anthropic Commercial/Consumer terms; fetched for private benchmark use only | 2026-11-02 | raw/claude-code/settings.md | 44924 | (step 2) |
| cc-permissions | claude-code | Configure permissions | https://code.claude.com/docs/en/permissions.md | terms not stated as a licence; footer links Anthropic Commercial/Consumer terms; fetched for private benchmark use only | 2026-11-02 | raw/claude-code/permissions.md | 90476 | (step 2) |
| cc-hooks | claude-code | Hooks reference | https://code.claude.com/docs/en/hooks.md | terms not stated as a licence; footer links Anthropic Commercial/Consumer terms; fetched for private benchmark use only | 2026-11-02 | raw/claude-code/hooks.md | 284407 | (step 2) |
| cc-skills | claude-code | Extend Claude with skills | https://code.claude.com/docs/en/skills.md | terms not stated as a licence; footer links Anthropic Commercial/Consumer terms; fetched for private benchmark use only | 2026-11-02 | raw/claude-code/skills.md | 119020 | (step 2) |
| cc-sub-agents | claude-code | Create custom subagents | https://code.claude.com/docs/en/sub-agents.md | terms not stated as a licence; footer links Anthropic Commercial/Consumer terms; fetched for private benchmark use only | 2026-11-02 | raw/claude-code/sub-agents.md | 116374 | (step 2) |
| cc-memory | claude-code | How Claude remembers your project | https://code.claude.com/docs/en/memory.md | terms not stated as a licence; footer links Anthropic Commercial/Consumer terms; fetched for private benchmark use only | 2026-11-02 | raw/claude-code/memory.md | 55321 | (step 2) |
| cc-mcp | claude-code | Connect Claude Code to tools via MCP | https://code.claude.com/docs/en/mcp.md | terms not stated as a licence; footer links Anthropic Commercial/Consumer terms; fetched for private benchmark use only | 2026-11-02 | raw/claude-code/mcp.md | 154871 | (step 2) |
| cc-sandboxing | claude-code | Configure the sandboxed Bash tool | https://code.claude.com/docs/en/sandboxing.md | terms not stated as a licence; footer links Anthropic Commercial/Consumer terms; fetched for private benchmark use only | 2026-11-02 | raw/claude-code/sandboxing.md | 107715 | (step 2) |
| qmd-readme | qmd | QMD - Query Markup Documents | https://github.com/tobi/qmd/blob/86d2365d17fc682e491c2c53d1e4a884aee8682a/README.md | MIT (© 2024-2026 Tobi Lutke), pinned HEAD 86d2365d17fc (2026-10-14) | 2026-11-02 | raw/qmd/README.md | 66539 | (step 2) |
| manual-pdf | manual | AVR-X1700H / AVR-X1700H DAB Integrated Network AV Receiver Owner's Manual (PDF, 304 pages) | https://assets.denon.com/DocumentMaster/MASTER/AVR-X1700HE2DAB%20_Owners_Manual.pdf | ©2021 Sound United. All Rights Reserved. (last page); manufacturer-hosted; fetched for private benchmark use only | 2026-11-02 | raw/manual/denon-avr-x1700h-owners-manual.pdf | 12317147 | (step 2) |
| manual-txt | manual | same manual, text extracted with `pdftotext` 24.02.0 (default mode, one form feed per page) | (derived from manual-pdf) | as manual-pdf | 2026-11-02 | raw/manual/denon-avr-x1700h-owners-manual.txt | 338303 | (step 2) |
| lab-state | lab | LAB-STATE: fictional home lab "lab77" | (none; written by builder B1) | fleet-written, CC0 | 2026-11-02 | raw/lab/LAB-STATE.md | 2981 | (step 2) |

## Totals

| group | files | bytes |
|---|---|---|
| unraid | 8 | 180,817 |
| ollama | 6 | 70,679 |
| syncthing | 5 | 36,304 |
| tailscale | 6 | 105,077 |
| claude-code | 8 | 973,108 |
| qmd | 1 | 66,539 |
| manual | 2 | 12,655,450 |
| lab | 1 | 2,981 |
| **all** | 37 | 14,090,955 |

Sources (counting the manual PDF and its .txt as one source): 36. Bytes excluding the PDF binary: 1,773,808.
