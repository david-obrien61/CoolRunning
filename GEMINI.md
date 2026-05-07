# Project: CoolRunning

## Status
- Current phase: Active development
- Last worked on: May 7, 2026 — Amazon order review, hardware inventory updated, meross thermostat replaces Ecobee (not heat pump compatible), backlog updated through CR-025

## Architecture
- **Backend:** Home Assistant Core fork (Apache 2.0), Python 3.14.4, systemd service
- **Server:** HP ProDesk 600 G6, Debian Linux 12, IP `192.168.1.200`
- **Containers:** Docker + Portainer — Mosquitto MQTT running; Whisper, Piper, Ollama, Grafana, InfluxDB planned as Docker containers
- **Sensor mesh:** Zigbee via ZBT-2 coordinator, ZHA integration in HA
- **Thread/Matter:** Second ZBT-2 pending as Thread border router — blocks Eve Energy + meross pairing
- **Voice pipeline:** Wyoming protocol — Whisper + Piper + Ollama qwen2.5:3b + OpenWakeWord (Docker)
- **Voice satellites:** 5x ESP32-S3 in-wall units (mic + speaker + relay) running ESPHome — parts not yet ordered
- **No cloud:** nabucasa removed. HomeKit Controller preferred over vendor cloud APIs.
- **Key decision:** HA Core Python process, NOT HA OS — no add-on store
- **Key decision:** All mains-connected hardware must be UL-listed (insurance compliance)
- **Note to Gemini:** Claude Code executes implementation. Gemini designed the original architecture. Both AIs share this file for continuity.

## Active Tasks
- [ ] Set up Thread border router (second ZBT-2) — blocks Eve Energy and meross
- [ ] Install arriving hardware (Thu/Fri/Sun — see hardware table below)
- [ ] Pair Eve Energy Matter outlets x6 (delivered, waiting on Thread)
- [ ] Verify MQTT bridge publishes Sonoff data per-room
- [ ] Deploy voice pipeline Docker containers
- [ ] Order and build ESP32-S3 voice satellite units x5 (~$187 in parts)
- [ ] Deploy InfluxDB + Grafana for sensor history
- [ ] Build automations: thermal alert, attic overheat, goodnight/morning scenes

## Off Limits / Don't Touch
- Do not re-add nabucasa or aiogithubapi dependencies
- Do not use eWeLink, Ecobee cloud, or any vendor cloud APIs
- Do not design DIY relay builds inside wall boxes or panels (insurance)
- Do not downgrade Python below 3.14

## Coding Standards
- Python 3.14.4 — `except TypeA, TypeB:` without parentheses is valid
- MQTT topic pattern: `coolrunning/<domain>/<room>/<entity>`
- Git workflow: changes on Mac → push to GitHub → `git pull` on server → `systemctl restart coolrunning`
- All integrations must be local-only

## Hardware On-Hand
| Device | Protocol | Status |
|---|---|---|
| ZBT-2 x2 | Zigbee / Thread | 1 coordinator active, 1 pending Thread |
| Sonoff SNZB-02D x8 | Zigbee | Live — all rooms ✅ |
| Eve Energy Matter x6 | Matter / Thread | Delivered — pending Thread router |
| SONOFF NSPanel Pro 120 x2 | Zigbee / Wi-Fi | Arriving Friday |
| meross Smart Thermostat | Matter | Arriving Friday — heat pump, C-wire |
| SONOFF MINI Duo-L x3 | Zigbee | Arriving Friday |
| SONOFF Zigbee Switch (no neutral) x1 | Zigbee | Arriving Thursday |
| SONOFF iFAN04 | Wi-Fi | Arriving Sunday — SonoffLAN integration |

## Rooms
Living Room, Kitchen, Dining Room, Master Bedroom, Bedroom 2, Bedroom 3 (office), Bedroom 4, Utility Room, Washroom, Hallway, Foyer, Attic

## Reference
- Full task list: `BACKLOG.md`
- Claude context: `CLAUDE.md`
- GitHub: `https://github.com/david-obrien61/CoolRunning`
- Web UI: `http://192.168.1.200:8123`
