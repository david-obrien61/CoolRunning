# CoolRunning Project Backlog

## Project Goal
Build a fully local, cloud-free smart home system using a stripped-down Home Assistant Core as the backend engine. All sensor data, automation logic, and device control runs on a standalone server with no dependency on external cloud services.

---

## Server

| Item | Detail |
|---|---|
| Machine | HP ProDesk 600 G6 Microtower |
| OS | Debian Linux |
| Containers | Docker + Portainer |
| RAM | 16GB DDR4 (game server hosting paused until upgrade) |
| Storage | 1TB Seagate HDD ("Shelly") — ext4, mounted `/mnt/vault` |
| Additional drives | Two 500GB HDDs — pending "Bumper Method" install |
| MQTT Broker | Eclipse Mosquitto — running in Docker via Portainer |
| Remote Access | SSH from Mac — `ssh andrew@192.168.1.200` |

---

## Hardware Inventory

### Purchased & On-Hand
| Device | Purpose | Protocol | Status |
|---|---|---|---|
| Home Assistant ZBT-2 (x2) | Zigbee coordinator + Thread/Matter border router | Zigbee / Thread | 1 paired as coordinator, 1 pending Thread setup |
| Sonoff SNZB-02D x8 | Environmental monitoring — all rooms | Zigbee | Paired & live ✅ |
| Eve Energy Outlet (Matter) 3-Pack x2 | Power monitoring — 6 outlets total | Matter / Thread | Delivered — Thread router needed before pairing |
| SONOFF NSPanel Pro 120 x2 | 4.7" wall panel + built-in Zigbee gateway + thermostat display | Zigbee / Wi-Fi | Arriving Friday |
| meross Smart Thermostat (Matter, C-wire) | HVAC — heat pump compatible | Matter / Wi-Fi | Arriving Friday — replaces returned Ecobee |
| SONOFF MINI Duo-L x3 | Dual-channel no-neutral Zigbee switch | Zigbee 3.0 | Arriving Friday |
| SONOFF Zigbee Smart Switch (no neutral) | Single-channel no-neutral switch | Zigbee | Arriving Thursday |
| SONOFF iFAN04 WiFi x1 | Ceiling fan + light controller | Wi-Fi (NOT Zigbee) | Arriving Sunday — integrate via SonoffLAN or ESPHome |
| Apple TV | HomeKit hub on local network | HomeKit | On network |

### To Purchase — Voice Satellites (5 units)
| Component | Spec | Qty | Est. Cost |
|---|---|---|---|
| ESP32-S3 Mini dev board | Lolin S3 Mini or equivalent | 5 | $40 |
| INMP441 MEMS microphone | I2S microphone module | 5 | $20 |
| MAX98357A I2S amp + 1W 8ohm 28mm speaker | Amp board + speaker | 5 | $25 |
| 5V relay module | Single channel — 11 total (2 per double-gang, 1 per single) | 11 | $22 |
| Decora wall plates | Single-gang x2, double-gang x3 | 5 | $10 |
| 22 AWG hookup wire | Assorted colors — 10ft each red/black/white/green | 1 set | $8 |
| Small perfboard 5x7cm | Component mounting | 5 | $5 |
| Heat shrink tubing | Assorted sizes | 1 set | $5 |
| Speaker grille mesh | Cut to fit plate opening | 1 | $6 |
| USB microphone | Bench test for Whisper before satellites built | 1 | $15 |
| Small USB speaker | Bench test for Piper TTS before satellites built | 1 | $12 |
| Deep single-gang boxes 2.5in | Kitchen + dining | 5 | $10 |
| Deep double-gang boxes 2.5in | Master, bedroom 2, bedroom 3 | 3 | $9 |
| **Voice satellite subtotal** | | | **~$187** |

### To Purchase — Fans & Light Controllers
| Device | Model | Qty | Est. Cost | Location |
|---|---|---|---|---|
| Zigbee fan + light controller | Sonoff iFan04-H | 4 | $88 | All pull-chain ceiling fans |
| RF fan bridge | Bond Bridge Pro | 1 | $69 | Remote-controlled fan room |
| Pico remote + bracket | Lutron PJ2-1BRL | 2 | $44 | Kitchen + dining secondary switch |

### To Purchase — Switches & Outdoor
| Device | Model | Qty | Est. Cost | Location |
|---|---|---|---|---|
| In-wall Zigbee switch (no neutral) | Sonoff ZBMINIL2 | 4 | $56 | Utility / washroom / hallway / foyer |
| Outdoor Zigbee smart plug | Sonoff S40 | 2 | $30 | String lights + overhang light bar |
| Attic sensor (WiFi, rated 176°F) | Govee H5179 | 1 | $22 | Attic center |

### Under Consideration
| Device | Purpose | Protocol | Est. Cost | Notes |
|---|---|---|---|---|
| Apollo Automation MSR-2 | Full environmental sensor — temp, pressure, humidity, CO2, light, UV, mmWave occupancy | ESPHome / Wi-Fi | ~$35–$50 | Best data density per device |
| Eve Energy outlets (2-pack) | Power monitoring + Thread mesh router | Matter / Thread | ~$65/2pk | No cloud, dedicated mesh |
| Shelly Pro 3EM | Whole-panel energy monitoring | Wi-Fi / MQTT | ~$120 | DIN-rail, local MQTT out of box |
| Emporia Vue Gen 3 | Whole-panel energy monitoring | Wi-Fi (ESPHome flash) | ~$80 | CT clamp, cheaper option |

---

## Architecture Decisions (Locked)

- **Backend:** Home Assistant Core (Apache 2.0 fork — CoolRunning), running as systemd service
- **Communication backbone:** MQTT via local Eclipse Mosquitto broker (Docker)
- **Sensor mesh:** Zigbee via ZBT-2 coordinator
- **Thread/Matter:** Second ZBT-2 as Thread border router (pending setup)
- **No cloud:** nabucasa and GitHub update checks removed
- **Voice pipeline:** Whisper + Piper + Ollama + OpenWakeWord — all running as Docker containers via Portainer
- **Dashboards:** InfluxDB + Grafana (Docker) for time-series data visualization
- **Remote access:** Tailscale VPN (no port forwarding, no cloud dependency)
- **Insurance compliance:** All high-voltage hardware commercially certified (UL-listed). No DIY relay builds inside wall boxes or panels.
- **Thermostat:** Ecobee via HomeKit Controller (local) — NOT Ecobee cloud API

---

## Sensor Reference

| Sensor / Integration | Data Points | MQTT / Entity | Notes |
|---|---|---|---|
| Sonoff SNZB x8 (Zigbee) | Temperature, Humidity | `coolrunning/environment/<room>` | All rooms paired |
| Ecobee (HomeKit Controller) | Temp, humidity, HVAC state, setpoint | HA climate entity | Local via Apple TV hub |
| Govee H5179 (WiFi) | Temperature, Humidity | HA sensor entity | Attic — rated 176°F |
| Apollo MSR-2 (ESPHome) | Temp, Pressure, Humidity, CO2, Light, UV, Occupancy | `coolrunning/environment/<room>` | Under consideration |
| ESP32-S3 satellites (ESPHome) | Voice, relay state | ESPHome / Wyoming | 5 in-wall units |
| Evo Energy Outlets | Power state, Wattage, kWh | `coolrunning/power/utility/<appliance>` | Freezers + refrigerators |
| Sonoff S40 outdoor | Power state, Wattage | `coolrunning/power/outdoor/<device>` | String lights + light bar |
| Sonoff iFan04-H x4 | Fan speed, light state | ZHA entity | Ceiling fans |
| Sonoff ZBMINIL2 x4 | Switch state | ZHA entity | Utility / wash / hall / foyer |

---

## Backlog

### Phase 0 — Server Hardening ✅ Complete
- [x] **CR-000** — `/mnt/vault` mount reboot-proof via fstab (UUID)
- [x] **CR-011** — Remove hass-nabucasa cloud dependency
- [x] **CR-012** — Remove GitHub update checker
- [x] **CR-013** — Commit open changes in views.py and core.py
- [x] **CR-014** — CoolRunning running as systemd service (auto-start on boot)

---

### Phase 1 — Environmental Monitoring ✅ Mostly Complete
- [x] **CR-001** — ZBT-2 Zigbee coordinator paired via ZHA
- [x] **CR-002** — Sonoff SNZB sensors paired — all 8 rooms live
- [ ] **CR-003** — Verify MQTT bridge publishes Sonoff data per-room (refactor topic to `coolrunning/environment/<room>/temperature`)
- [ ] **CR-004** — Move MQTT broker address and topic prefix from `core.py` into `configuration.yaml`
- [ ] **CR-005** — Deploy Ignition BME680 tile wired to live Sonoff data
- [ ] **CR-006** — Tune Sonoff reporting intervals after 48hr baseline monitoring
- [ ] **CR-006b** — Integrate meross Smart Thermostat via Matter *(Ecobee returned — not heat pump compatible. meross arriving Friday, C-wire required. Thread router must be active first. Settings → Matter → scan QR code. Configure heat pump mode in meross app before pairing to HA.)*
- [ ] **CR-006c** — Install and pair Govee H5179 attic sensor *(WiFi, rated 176°F — do NOT use SNZB in attic)*

---

### Phase 2 — Power Monitoring & Appliance Control
- [ ] **CR-007** — Integrate Evo Energy outlets *(not yet installed — confirm protocol first)*
- [ ] **CR-008** — Build Grafana dashboard tile for power monitoring (freezer, fridge 1, fridge 2)
- [ ] **CR-009** — Automation: alert when freezer/fridge wattage drops to near-zero (compressor failure)
- [ ] **CR-010** — Evaluate whole-panel energy monitoring (Shelly Pro 3EM vs Emporia Vue Gen 3)

---

### Phase 3 — Fan & Light Control
- [ ] **CR-018** — Set up Thread border router — configure second ZBT-2 via Thread integration *(required before Eve Energy Matter outlets and meross thermostat can pair)*
- [ ] **CR-019** — Pair Eve Energy Matter outlets x6 *(delivered — waiting on Thread router. Settings → Matter → scan QR code on each outlet)*
- [ ] **CR-020** — Install and integrate SONOFF NSPanel Pro 120 x2 *(arriving Friday — 4.7" wall panel with built-in Zigbee gateway. Pairs via HA NSPanel Pro integration or MQTT. Consider as room dashboard panels.)*
- [ ] **CR-021** — Install meross thermostat *(arriving Friday — heat pump mode, C-wire required. Pair via Matter after Thread router is active)*
- [ ] **CR-022** — Install SONOFF MINI Duo-L x3 *(arriving Friday — dual-channel no-neutral Zigbee. Each unit controls 2 circuits. Pair via ZHA)*
- [ ] **CR-023** — Install SONOFF Zigbee Smart Switch no-neutral *(arriving Thursday — single channel. Pair via ZHA)*
- [ ] **CR-024** — Install and integrate SONOFF iFAN04 WiFi *(arriving Sunday — WiFi version, NOT Zigbee. Use SonoffLAN integration for local control with no cloud. Settings → Add Integration → SonoffLAN)*
- [ ] **CR-025** — Install Sonoff iFan04-H in remaining ceiling fans *(if additional Zigbee fan controllers purchased later)*
- [ ] **CR-020** — Install Sonoff S40 outdoor plugs (string lights + overhang light bar)
- [ ] **CR-021** — Set up Bond Bridge Pro for RF-controlled fan room
- [ ] **CR-022** — Install Lutron Pico remotes for kitchen + dining secondary switch positions
- [ ] **CR-023** — Set up Thread border router — configure second ZBT-2 via Thread/Matter integration
- [ ] **CR-024** — Integrate Philips Hue Bridge (already auto-discovered — press button on bridge, confirm in ZHA/Hue integration)

---

### Phase 4 — Voice Pipeline (Docker containers via Portainer)
- [ ] **CR-025** — Deploy Wyoming Whisper container (speech-to-text)
  ```yaml
  image: rhasspy/wyoming-whisper
  command: --model small-int8 --language en
  ports: ["10300:10300"]
  ```
- [ ] **CR-026** — Deploy Wyoming Piper container (text-to-speech)
  ```yaml
  image: rhasspy/wyoming-piper
  command: --voice en_US-libritts-high
  ports: ["10200:10200"]
  ```
- [ ] **CR-027** — Deploy Ollama container + pull qwen2.5:3b model
  ```bash
  docker exec -it ollama ollama pull qwen2.5:3b
  ```
- [ ] **CR-028** — Deploy Wyoming OpenWakeWord container
  ```yaml
  image: rhasspy/wyoming-openwakeword
  ports: ["10400:10400"]
  ```
- [ ] **CR-029** — Add Wyoming integration in CoolRunning (Settings → Integrations → Wyoming) — auto-discovers Whisper and Piper containers
- [ ] **CR-030** — Configure Voice Assistant pipeline in CoolRunning
  - Name: CoolRunning
  - Wake word: ok_nabu
  - STT: Whisper
  - TTS: Piper
  - Conversation agent: Ollama qwen2.5:3b
- [ ] **CR-031** — Set up Tailscale for remote access (Docker container — no port forwarding needed)

---

### Phase 5 — Voice Satellite Hardware Builds (5 units)
- [ ] **CR-032** — Order all voice satellite parts (see Hardware Inventory above — ~$187)
- [ ] **CR-033** — Flash and bench test Unit 1 (Master Bedroom — double-gang, 2 relays)
  - ESP32-S3 Mini, INMP441 mic, MAX98357A amp, 2x relay
  - Flash ESPHome config, verify WiFi + mic + speaker + relay before wall install
- [ ] **CR-034** — Flash and bench test Unit 2 (Bedroom 2 — double-gang, 2 relays)
- [ ] **CR-035** — Flash and bench test Unit 3 (Bedroom 3 — double-gang, 2 relays)
- [ ] **CR-036** — Flash and bench test Unit 4 (Kitchen — single-gang, 1 relay)
- [ ] **CR-037** — Flash and bench test Unit 5 (Dining Room — single-gang, 1 relay)
- [ ] **CR-038** — Wall install all 5 units (after bench test passes — turn off breaker, photo wiring, install, restore power)
- [ ] **CR-039** — Voice command test sequence from each room (see Section 5.2 of build guide)

---

### Phase 6 — Dashboards & Automations
- [ ] **CR-040** — Deploy InfluxDB container (time-series database for all sensor history)
- [ ] **CR-041** — Deploy Grafana container + connect to InfluxDB
- [ ] **CR-042** — Build Grafana room temperature overview dashboard
- [ ] **CR-043** — Thermal delta alert automation (any room >2°F above house average → notification)
- [ ] **CR-044** — Attic overheat alert automation (above 130°F for 15 min → notification)
- [ ] **CR-045** — UPS battery low alert automation (below 25% → notification)
- [ ] **CR-046** — Goodnight scene (all lights off, bedroom fans on medium, outdoor plugs off)
- [ ] **CR-047** — Good morning scene (kitchen + hallway lights on, fans off)
- [ ] **CR-048** — Vampire device shutdown automation (outlets drawing 0.5W–5W → turn off on command)
- [ ] **CR-049** — Configure Ollama system prompt with full home layout and device map

---

### Phase 7 — Ignition SCADA Integration
- [ ] **CR-005** — Deploy Ignition BME680 tile wired to live Sonoff MQTT data
- [ ] **CR-015** — Build Ignition tile schemas for power monitoring (freezer, fridge 1, fridge 2)
- [ ] **CR-016** — Build Ignition room overview dashboard
- [ ] **CR-017** — Decision: keep Ignition SCADA or build React Native dashboard (TorqueAI-style)?

---

## Open Questions

1. **Evo Energy outlets** — what protocol? (Zigbee, Wi-Fi, Matter?) Determines integration path.
2. **MQTT topic structure** — finalize before adding more sensors so Ignition tiles stay stable.
3. **Panel monitoring** — Shelly Pro 3EM or Emporia Vue Gen 3?
4. **Custom frontend** — Ignition SCADA or React Native dashboard?
5. **UPS** — CyberPower 900VA confirmed on server? NUT integration needed.

---

## Important Notes

- All environmental sensors (low voltage, USB powered) — safe to self-install.
- All high-voltage hardware (smart plugs, fan controllers, wall switches) must be **commercially certified (UL-listed)**. No DIY relay inside wall boxes or breaker panels.
- Insurance compliance is a locked architectural decision.
- Voice satellite relay wiring touches mains — **turn off breaker, verify with tester before touching any wire**.
- Pair one Zigbee sensor at a time. Label each device with a Sharpie before moving to the next.
- Build guide assumes HA OS add-ons — we run Docker containers instead. Same result, different deployment path.
