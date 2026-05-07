# CoolRunning — Project Context for Claude

## What This Project Is

CoolRunning is a **fully local, cloud-free smart home system** built on a fork of Home Assistant Core (Apache 2.0). It runs on a standalone HP ProDesk server in Liberty Hill, TX. No Nabu Casa cloud, no vendor cloud APIs, no external dependencies required for core operation.

The project is a father-and-son build (Terrence and Andrew O'Brien). Terrence handles systems architecture and server-side engineering. Andrew handles hardware installation and frontend.

---

## Server Infrastructure

| Item | Detail |
|---|---|
| Machine | HP ProDesk 600 G6 Microtower |
| OS | Debian Linux 12 (Bookworm) |
| Python | 3.14.4 via pyenv at `/root/.pyenv/versions/3.14.4` |
| Containers | Docker + Portainer |
| RAM | 16GB DDR4 |
| Storage | 1TB HDD ext4 mounted at `/mnt/vault` (reboot-proof via UUID fstab) |
| SSH | `ssh andrew@192.168.1.200` (user: andrew, su to root for admin) |
| Network | Server IP: 192.168.1.200 |

---

## Current Software Stack

| Service | How It Runs | Status |
|---|---|---|
| CoolRunning (HA Core fork) | Python venv, systemd service `coolrunning.service` | ✅ Running |
| Eclipse Mosquitto MQTT | Docker via Portainer | ✅ Running |
| InfluxDB | Docker via Portainer | Planned |
| Grafana | Docker via Portainer | Planned |
| Wyoming Whisper (STT) | Docker via Portainer | Planned |
| Wyoming Piper (TTS) | Docker via Portainer | Planned |
| Ollama + qwen2.5:3b | Docker via Portainer | Planned |
| OpenWakeWord | Docker via Portainer | Planned |
| Tailscale | Docker via Portainer | Planned |
| ESPHome | Docker via Portainer | Planned |

**Important:** This project uses HA Core (Python process), NOT Home Assistant OS. There is no add-on store. Everything runs as Docker containers or systemd services.

---

## CoolRunning Deployment

```
/mnt/vault/coolrunning/          # git clone of github.com/david-obrien61/CoolRunning
  coolrunning-core/              # HA Core fork
    venv/                        # Python 3.14.4 virtualenv
    homeassistant/               # Modified HA source
  ignition_schemas/              # Ignition SCADA tile definitions
/mnt/vault/homeassistant/        # Runtime config, automations, database
```

**Start/stop/restart:**
```bash
systemctl restart coolrunning
systemctl status coolrunning
journalctl -u coolrunning -f
```

**Update from GitHub:**
```bash
cd /mnt/vault/coolrunning && git pull
systemctl restart coolrunning
```

**Web UI:** `http://192.168.1.200:8123`

---

## Key Modifications to HA Core

| File | Change | Reason |
|---|---|---|
| `homeassistant/helpers/network.py` | Removed `hass_nabucasa` import, stubbed `is_cloud_connection()` to return False | Standalone deployment |
| `homeassistant/components/http/forwarded.py` | Removed `hass_nabucasa` import, disabled cloud request skip | Standalone deployment |
| `homeassistant/components/assist_pipeline/pipeline.py` | Removed `hass_nabucasa` import | Standalone deployment |
| `homeassistant/components/frontend/pr_download.py` | Stubbed to raise HomeAssistantError | Removes aiogithubapi dependency |
| `homeassistant/components/onboarding/views.py` | `.get()` with fallback for translation key | Prevents KeyError during account creation |
| `coolrunning-core/requirements.txt` | Removed `hass-nabucasa` and `aiogithubapi` | Standalone deployment |

---

## Hardware — Installed & Active

| Device | Protocol | Location | Status |
|---|---|---|---|
| ZBT-2 Zigbee coordinator | Zigbee (USB `/dev/ttyACM0`) | Server | ✅ Paired via ZHA |
| ZBT-2 Thread border router | Thread/Matter (USB) | Server | Pending setup |
| Sonoff SNZB-02 x8 | Zigbee | All rooms | ✅ Paired, live data |
| Ecobee Smart Thermostat Enhanced | Wi-Fi / HomeKit | Main HVAC | Arriving — integrate via HomeKit Controller (NOT Ecobee cloud API) |
| Apple TV | HomeKit hub | Living room | On network — bridges Ecobee to HA locally |
| Evo Energy Smart Outlets | TBD | Utility room | Purchased, not installed |

## Hardware — To Purchase

**Voice Satellites (5 units — ~$187 total):**
- ESP32-S3 Mini x5, INMP441 mic x5, MAX98357A amp+speaker x5
- 5V relay x11, perfboard x5, 22AWG wire, heat shrink, speaker grille mesh
- Decora wall plates x5, deep single-gang boxes x5, deep double-gang boxes x3
- USB mic x1 + USB speaker x1 (bench testing)

**Fans & Lights:**
- Sonoff iFan04-H x4 ($88) — ceiling fan Zigbee controllers
- Bond Bridge Pro x1 ($69) — RF fan bridge
- Lutron Pico remote + bracket x2 ($44)
- Sonoff ZBMINIL2 no-neutral x4 ($56) — utility/washroom/hall/foyer
- Sonoff S40 outdoor x2 ($30) — string lights + light bar
- Govee H5179 x1 ($22) — attic sensor (rated 176°F)

---

## Architecture Decisions (Do Not Reverse)

1. **No cloud APIs** — use HomeKit Controller for Ecobee, not Ecobee cloud API. Apply this to any future HomeKit-capable device.
2. **Insurance compliance** — all high-voltage hardware must be commercially certified (UL-listed). No DIY relay builds inside wall boxes or breaker panels.
3. **Python 3.14.4** — the codebase uses Python 3.14 syntax (`except TypeA, TypeB:` without parentheses). Do not downgrade to 3.13.
4. **Docker for services** — all supporting services (Whisper, Piper, Ollama, InfluxDB, Grafana) run as Docker containers via Portainer, not as HA add-ons.
5. **MQTT naming convention** — topics follow `coolrunning/<domain>/<room>/<entity>` pattern.
6. **Git workflow** — all changes made on Mac, committed and pushed to `github.com/david-obrien61/CoolRunning`, then `git pull` on server followed by `systemctl restart coolrunning`.

---

## What Is Done

- [x] Server storage mounted and reboot-proof
- [x] CoolRunning deployed from GitHub, running as systemd service
- [x] All cloud dependencies (nabucasa, aiogithubapi) stripped from codebase
- [x] ZBT-2 Zigbee coordinator active via ZHA
- [x] 8x Sonoff SNZB sensors paired — all rooms live
- [x] Home layout created (living room, kitchen, dining room, master bedroom, bedrooms 2/3/4)

## What Is Next (Priority Order)

1. Install and integrate Ecobee via HomeKit Controller
2. Install Evo Energy outlets — integrate for utility room power monitoring
3. Deploy voice pipeline Docker containers (Whisper, Piper, Ollama, OpenWakeWord)
4. Order and build 5x ESP32-S3 voice satellite units
5. Install Sonoff iFan04-H fan controllers, ZBMINIL2 wall switches, S40 outdoor plugs
6. Deploy InfluxDB + Grafana for sensor history dashboards
7. Configure automations (thermal alert, attic overheat, goodnight/morning scenes)

---

## Reference Files

- `BACKLOG.md` — full phased task list with all hardware and software tasks
- `ignition_schemas/bme680_tile.json` — Ignition SCADA tile template
- `coolrunning-core/homeassistant/core.py` — contains MQTT bridge modification
