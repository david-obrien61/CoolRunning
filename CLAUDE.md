# Project: CoolRunning

## Status
- Current phase: Active development
- Last worked on: May 7, 2026 — Amazon order review, hardware inventory updated, meross thermostat replaces Ecobee, backlog updated through CR-025

## Architecture
- **Backend:** Home Assistant Core fork (Apache 2.0), Python 3.14.4, running as systemd service (`coolrunning.service`)
- **Server:** HP ProDesk 600 G6, Debian Linux 12, IP `192.168.1.200`, SSH as `andrew` then `su -`
- **Storage:** 1TB HDD ext4 at `/mnt/vault` (UUID fstab, reboot-proof)
- **Containers:** Docker + Portainer — Mosquitto MQTT running; Whisper, Piper, Ollama, Grafana, InfluxDB planned
- **Sensor mesh:** Zigbee via ZBT-2 coordinator (`/dev/ttyACM0`), ZHA integration
- **Thread/Matter:** Second ZBT-2 pending setup as Thread border router — required before Eve Energy outlets and meross thermostat can pair
- **Voice pipeline:** Wyoming protocol — Whisper (STT) + Piper (TTS) + Ollama qwen2.5:3b + OpenWakeWord, all as Docker containers
- **No cloud:** nabucasa and aiogithubapi removed from codebase and requirements.txt
- **Key decision:** HA Core Python process, NOT HA OS — no add-on store. All supporting services run as Docker containers.
- **Key decision:** HomeKit Controller preferred over vendor cloud APIs for any HomeKit-capable device
- **Key decision:** Insurance compliance locked — all mains-connected hardware must be UL-listed commercial products

## Active Tasks
- [ ] Set up Thread border router (second ZBT-2) — blocks Eve Energy and meross pairing
- [ ] Install SONOFF Zigbee Smart Switch no-neutral (arriving Thursday)
- [ ] Install SONOFF NSPanel Pro 120 x2 (arriving Friday) — wall panels + Zigbee gateway
- [ ] Install meross Smart Thermostat via Matter (arriving Friday, C-wire required, heat pump mode)
- [ ] Install SONOFF MINI Duo-L x3 dual-channel Zigbee (arriving Friday)
- [ ] Install SONOFF iFAN04 WiFi (arriving Sunday) — use SonoffLAN integration, NOT eWeLink cloud
- [ ] Pair Eve Energy Matter outlets x6 (delivered, waiting on Thread router)
- [ ] Verify MQTT bridge publishes Sonoff sensor data per-room (CR-003)
- [ ] Deploy voice pipeline Docker containers (Whisper, Piper, Ollama, OpenWakeWord)
- [ ] Order ESP32-S3 voice satellite parts (~$187 — see BACKLOG.md)

## Off Limits / Don't Touch
- `coolrunning-core/homeassistant/components/cloud/` — cloud component, leave intact but it will fail to load (dependency missing by design)
- Do not re-add `hass-nabucasa` or `aiogithubapi` to requirements.txt
- Do not downgrade Python below 3.14 — codebase uses `except TypeA, TypeB:` syntax that requires 3.14
- Do not amend or rebase commits already pushed to GitHub
- Do not use eWeLink or Ecobee cloud APIs — local integrations only
- Do not design DIY relay builds inside wall boxes or breaker panels — insurance compliance

## Coding Standards
- Python 3.14.4 — `except TypeA, TypeB:` without parentheses is valid and intentional
- All changes made on Mac, committed and pushed to `github.com/david-obrien61/CoolRunning`, then `git pull` + `systemctl restart coolrunning` on server
- MQTT topic pattern: `coolrunning/<domain>/<room>/<entity>`
- No cloud API calls — all integrations must operate on local network only
- Commit messages include `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`

## Key File Locations
```
/mnt/vault/coolrunning/coolrunning-core/   # Source code (git repo)
/mnt/vault/coolrunning/coolrunning-core/venv/  # Python 3.14.4 virtualenv
/mnt/vault/homeassistant/                  # Runtime config + database
/etc/systemd/system/coolrunning.service    # Service definition
```

## Hardware On-Hand
| Device | Protocol | Status |
|---|---|---|
| ZBT-2 x2 | Zigbee / Thread | 1 active as coordinator, 1 pending Thread setup |
| Sonoff SNZB-02D x8 | Zigbee | Live — all rooms ✅ |
| Eve Energy Matter x6 | Matter / Thread | Delivered — pending Thread router |
| SONOFF NSPanel Pro 120 x2 | Zigbee / Wi-Fi | Arriving Friday |
| meross Smart Thermostat | Matter | Arriving Friday |
| SONOFF MINI Duo-L x3 | Zigbee | Arriving Friday |
| SONOFF Zigbee Switch (no neutral) | Zigbee | Arriving Thursday |
| SONOFF iFAN04 | Wi-Fi | Arriving Sunday |

## Reference
- Full task list: `BACKLOG.md`
- Gemini context: `GEMINI.md`
- Ignition SCADA tile: `ignition_schemas/bme680_tile.json`
- HA Core code notes: `coolrunning-core/CLAUDE.md`
