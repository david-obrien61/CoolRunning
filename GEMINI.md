# CoolRunning — Project Context for Gemini

> This file mirrors CLAUDE.md and is maintained so both AI assistants stay in sync on project status. Update both files together when the project state changes.

---

## What This Project Is

CoolRunning is a **fully local, cloud-free smart home system** built in Liberty Hill, TX by Terrence and Andrew O'Brien. It is a fork of Home Assistant Core (Apache 2.0 license) running on a dedicated HP ProDesk server.

**Origin:** Gemini proposed the architecture (fork HA Core, use MQTT, build ESP32 sensor nodes). Claude Code has been executing the server deployment and managing the codebase. Both AIs are collaborating on this project — Gemini for design and planning, Claude Code for implementation.

---

## Current Implementation Status

### What Is Built and Running

| Component | Status | Notes |
|---|---|---|
| HP ProDesk server (Debian Linux) | ✅ Running | 16GB DDR4, 1TB HDD at `/mnt/vault` |
| CoolRunning (HA Core fork) | ✅ Running | Python 3.14.4, systemd service, auto-starts on boot |
| Mosquitto MQTT broker | ✅ Running | Docker container via Portainer |
| ZBT-2 Zigbee coordinator | ✅ Active | Paired via ZHA, USB at `/dev/ttyACM0` |
| Sonoff SNZB sensors x8 | ✅ Live | All rooms — temperature + humidity streaming |
| Web dashboard | ✅ Live | `http://192.168.1.200:8123` |
| Cloud dependencies | ✅ Removed | nabucasa and aiogithubapi stripped from codebase |

### What Is Arriving / Pending Install

| Device | Status |
|---|---|
| Ecobee Smart Thermostat Enhanced | Arriving — integrate via HomeKit Controller (local, not Ecobee cloud) |
| Evo Energy Smart Outlets | Purchased — not yet installed (utility room, freezers/refrigerators) |

### What Is Planned (Not Yet Started)

- Voice pipeline: Whisper (STT) + Piper (TTS) + Ollama qwen2.5:3b + OpenWakeWord — all Docker containers
- 5x ESP32-S3 in-wall voice satellite units (mic + speaker + relay per room)
- Sonoff iFan04-H x4 (Zigbee ceiling fan controllers)
- Sonoff ZBMINIL2 x4 (no-neutral wall switches)
- Sonoff S40 x2 (outdoor Zigbee plugs)
- Bond Bridge Pro (RF fan bridge)
- Govee H5179 (attic sensor — WiFi, rated 176°F)
- InfluxDB + Grafana (time-series dashboards)
- Tailscale (remote VPN access)

---

## Server Access

```
SSH:      ssh andrew@192.168.1.200  (then: su - for root)
Web UI:   http://192.168.1.200:8123
Git repo: https://github.com/david-obrien61/CoolRunning
```

**Service management:**
```bash
systemctl restart coolrunning
journalctl -u coolrunning -f       # live logs
```

**Update workflow:**
```bash
cd /mnt/vault/coolrunning && git pull
systemctl restart coolrunning
```

---

## Deployment Layout

```
/mnt/vault/coolrunning/            # GitHub repo clone
  coolrunning-core/                # HA Core fork (Python 3.14.4)
    venv/                          # Virtual environment
    requirements.txt               # nabucasa + aiogithubapi removed
/mnt/vault/homeassistant/          # Runtime config, automations, DB
```

---

## Key Architecture Decisions

| Decision | Reason |
|---|---|
| HA Core fork, NOT HA OS | Full code control, no add-on store dependency, runs as Python process |
| Python 3.14.4 (not 3.13) | Codebase uses Python 3.14 syntax — `except TypeA, TypeB:` without parens |
| Docker for all supporting services | Portainer manages Mosquitto, Whisper, Piper, Ollama, Grafana, etc. |
| Ecobee via HomeKit Controller | Fully local — Apple TV on network acts as HomeKit hub. No Ecobee cloud API. |
| No DIY high-voltage hardware | Insurance compliance — all mains-connected hardware must be UL-listed commercial products |
| MQTT topic pattern | `coolrunning/<domain>/<room>/<entity>` |
| Git-based deployment | Changes pushed from Mac to GitHub → pulled on server → service restarted |

---

## Rooms in the Home

Living Room, Kitchen, Dining Room, Master Bedroom, Bedroom 2, Bedroom 3 (office), Bedroom 4, Utility Room, Washroom, Hallway, Foyer, Attic

---

## Voice Satellite Plan (5 Units)

Per Gemini's original design — ESP32-S3 in-wall units replacing existing switches:

| Unit | Location | Box Type | Relays |
|---|---|---|---|
| 1 | Master Bedroom | Deep double-gang | 2 (fan + light) |
| 2 | Bedroom 2 | Deep double-gang | 2 (fan + light) |
| 3 | Bedroom 3 | Deep double-gang | 2 (fan + light) |
| 4 | Kitchen | Deep single-gang | 1 (light) |
| 5 | Dining Room | Deep single-gang | 1 (light) |

Each unit: ESP32-S3 Mini + INMP441 mic + MAX98357A amp + speaker + relay(s)
Firmware: ESPHome with Wyoming voice assistant protocol
Wake word: ok_nabu via OpenWakeWord

**Parts to order (~$187):** See BACKLOG.md → Hardware Inventory → To Purchase

---

## Automation Goals (From Original Design)

- Thermal delta alert: any room >2°F above house average → notification
- Attic overheat alert: above 130°F for 15 min → notification
- Goodnight scene: all lights off, bedroom fans on medium, outdoor plugs off
- Good morning scene: kitchen + hallway lights on
- Vampire device shutdown: outlets drawing 0.5–5W → turn off on voice command
- Freezer/fridge compressor failure: wattage drops to near-zero → alert

---

## Reference Files

| File | Purpose |
|---|---|
| `BACKLOG.md` | Full phased task list — 49 tasks across 7 phases |
| `CLAUDE.md` | Claude Code context (mirrors this file) |
| `ignition_schemas/bme680_tile.json` | Ignition SCADA tile template |
| `coolrunning-core/homeassistant/core.py` | MQTT bridge modification |
| `coolrunning-core/CLAUDE.md` | HA Core code-level instructions (Python syntax, commit rules) |
