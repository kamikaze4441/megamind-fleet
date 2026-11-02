---
tags: [lab, device, avr, denon]
created: 2026-11-02
updated: 2026-11-02
sources: [raw/lab/LAB-STATE.md]
---
# aria (living-room AV receiver)

aria is the living-room Denon AVR-X1700H at 10.77.0.40. It gets its network address from [[gate]] (it is the only device that takes its address from gate's DHCP), so its network features need gate.

## Background
The AVR-X1700H uses the network for Internet Radio, streaming services, AirPlay, the HEOS multi-room system and firmware updates; setup, Wi-Fi options, Auto Standby and reset procedures are summarised in [[avr-setup]].

## Notes
aria has no dependency on [[atlas]] in the lab note; only gate.

depends_on:: [[gate]] (gets its network address from gate's DHCP; network features need gate)
derived_from:: [[raw/lab/LAB-STATE.md]]
