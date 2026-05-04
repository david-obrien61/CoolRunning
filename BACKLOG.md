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
| Remote Access | SSH from Windows laptop at `192.168.1.200` |

---

## Hardware Inventory

### Purchased & On-Hand
| Device | Purpose | Protocol | Status |
|---|---|---|---|
| Home Assistant ZBT-2 | Zigbee USB coordinator / antenna for server | Zigbee | Purchased |
| Sonoff SNZB Temperature & Humidity Sensor | Environmental monitoring | Zigbee | Purchased |
| Evo Energy Smart Outlets | Power control & monitoring — utility room freezer & refrigerators | TBD | Purchased |

### Under Consideration
| Device | Purpose | Protocol | Est. Cost | Notes |
|---|---|---|---|---|
| Apollo Automation MSR-2 | Full environmental sensor — temp, pressure, humidity, CO2, light, UV, mmWave occupancy | ESPHome / Wi-Fi | ~$35–$50 | Pre-flashed ESPHome, no cloud, best data density per device |
| Shelly Plug US Gen4 | Smart plug with power monitoring — appliances, lights | Wi-Fi / Zigbee / Matter | ~$20 | Local MQTT out of the box, supports 15A, top pick for appliance control |
| TP-Link Kasa KP-115 | Budget smart plug with energy monitoring | Wi-Fi | ~$10–$14 | HA has native local integration, slim form fits double outlets |
| Emporia Smart Plug (4-pack) | Budget bulk power monitoring | Wi-Fi (ESPHome flash) | ~$33/4pk (~$8 ea) | Requires ESPHome flash to go local; best price per plug |
| Eve Energy (2-pack) | Premium local smart plug — Thread mesh | Matter / Thread | ~$65/2pk | No cloud required, dedicated mesh keeps smart traffic off Wi-Fi |
| Shelly Pro 3EM | Whole-panel energy monitoring | Wi-Fi / MQTT | ~$120 | DIN-rail mount in breaker panel, local MQTT out of the box, no flash needed |
| Emporia Vue Gen 3 | Whole-panel energy monitoring | Wi-Fi (ESPHome flash) | ~$80 | CT clamp snap-on to main lines, community-supported ESPHome flash |

---

## Architecture Decisions (Locked)

- **Backend:** Home Assistant Core (Apache 2.0 fork — CoolRunning)
- **Communication backbone:** MQTT via local Eclipse Mosquitto broker
- **Sensor mesh:** Zigbee (ZBT-2 coordinator plugged into server)
- **No cloud:** `hass-nabucasa` and GitHub update checks must be disabled
- **Visualization:** Ignition OS SCADA dashboards fed by MQTT topics
- **Insurance compliance:** All high-voltage hardware is commercially certified (UL-listed). No DIY relay builds inside wall boxes or panels.

---

## Sensor Reference

| Sensor / Integration | Data Points | Topic Pattern | Notes |
|---|---|---|---|
| Sonoff SNZB (Zigbee) | Temperature, Humidity | `coolrunning/environment/<room>` | First deployed sensor, utility room / living spaces |
| Apollo MSR-2 (ESPHome) | Temp, Pressure, Humidity, CO2, Light, UV, Occupancy | `coolrunning/environment/<room>` | Best multi-sensor candidate for bedrooms, living room |
| BME680 / BME688 (Ignition tile already built) | Temp, Pressure, Humidity, VOC / Air Quality | `coolrunning/environment/<room>` | Schema in `ignition_schemas/bme680_tile.json` |
| Evo Energy Outlets | Power state, Energy (W), Cumulative (kWh) | `coolrunning/power/<room>/<appliance>` | Utility room — freezer, refrigerators |
| Shelly Plug / Kasa KP-115 | Power state, Wattage, kWh | `coolrunning/power/<room>/<appliance>` | General appliance and lighting control |
| Shelly Pro 3EM / Emporia Vue | Whole-house circuit-level power draw | `coolrunning/energy/panel/<circuit>` | Phase 2 — panel-level monitoring |

---

## Backlog

### Phase 0 — Server Hardening (Complete Before Deploying CoolRunning)

- [x] **CR-000** — Make `/mnt/vault` mount reboot-proof via fstab
  - **Preferred (safe):** Use UUID instead of `/dev/sda1` so device name changes don't break the mount
  ```bash
  # On the server, run:
  blkid /dev/sda1
  # Copy the UUID, then add to fstab:
  echo "UUID=<your-uuid-here> /mnt/vault ext4 defaults 0 2" >> /etc/fstab
  # Verify:
  mount -a
  ```
  - **Quick method (from prior session):** `echo "/dev/sda1 /mnt/vault ext4 defaults 0 2" >> /etc/fstab`
  - UUID method is strongly preferred — device names can shift on reboot

---

### Phase 1 — Environmental Monitoring (Temperature First)

- [ ] **CR-001** — Pair ZBT-2 Zigbee coordinator with CoolRunning server
  - Install ZHA (Zigbee Home Automation) or Zigbee2MQTT integration
  - Confirm ZBT-2 is recognized and coordinator is live

- [ ] **CR-002** — Pair Sonoff SNZB sensor via Zigbee
  - Add to ZHA or Zigbee2MQTT
  - Confirm temperature and humidity readings appear as HA entities

- [ ] **CR-003** — Verify MQTT bridge publishes Sonoff data
  - Current `core.py` modification publishes all `sensor.*` entities to `coolrunning/environment/living_room`
  - Refactor: make MQTT topic per-entity using `entity_id` so each room has its own sub-topic (e.g., `coolrunning/environment/utility_room/temperature`)

- [ ] **CR-004** — Move MQTT config out of `core.py` into `configuration.yaml`
  - Broker address (`127.0.0.1:1883`) and topic prefix (`coolrunning/environment`) are hardcoded
  - Should be driven by config so they can change without touching core code

- [ ] **CR-005** — Deploy Ignition BME680 tile for Sonoff data
  - Schema exists at `ignition_schemas/bme680_tile.json`
  - Wire tile to MQTT topic from CR-003
  - Confirm live temperature and humidity visible on Ignition dashboard

- [ ] **CR-006** — Expand environmental sensors to additional rooms
  - Decide: Apollo MSR-2 (richer data) vs. additional Sonoff SNZB units (cheaper, simpler)
  - Target rooms: kitchen, living room, bedrooms, utility room

---

### Phase 2 — Power Monitoring & Appliance Control (Utility Room First)

- [ ] **CR-007** — Integrate Evo Energy outlets into CoolRunning
  - Confirm protocol (Zigbee, Wi-Fi, or Matter) and add correct HA integration
  - Verify power state and wattage appear as HA entities
  - Map entities to MQTT topic `coolrunning/power/utility_room/<appliance>`

- [ ] **CR-008** — Build Ignition dashboard tile for power monitoring
  - Display wattage and on/off state for freezer and refrigerators
  - Model after `bme680_tile.json` pattern

- [ ] **CR-009** — Automation: alert on abnormal appliance power draw
  - Trigger: freezer or refrigerator wattage drops to near-zero unexpectedly (compressor failure)
  - Action: push notification to server log / future alert channel

- [ ] **CR-010** — Evaluate whole-panel energy monitoring hardware
  - Compare Shelly Pro 3EM (no flash, DIN-rail, local MQTT) vs. Emporia Vue Gen 3 (cheaper, requires ESPHome flash)
  - Decision gate: is panel-level monitoring needed before individual appliance plugs are deployed?

---

### Phase 3 — Server Hardening & Cloud Removal

- [x] **CR-011** — Remove or disable `hass-nabucasa` dependency
  - Remove from `requirements.txt`
  - Confirm no startup errors after removal
  - This is required before standalone / air-gapped deployment

- [x] **CR-012** — Disable GitHub update checker
  - Prevent HA from making outbound calls to GitHub for release checks
  - Set `homeassistant: check_config_updated: false` or remove the relevant component

- [ ] **CR-013** — Review and commit open changes in `views.py` and `core.py`
  - Both files show uncommitted modifications (`git status`)
  - Review, document intent, and commit before deploying to server

- [ ] **CR-014** — Write startup and service management docs
  - How to start CoolRunning on boot (systemd service or Docker container)
  - How to restart safely after config changes

---

### Phase 4 — Ignition SCADA Integration (Expand)

- [ ] **CR-015** — Build Ignition tile schemas for power monitoring entities
  - One tile per appliance (freezer, fridge 1, fridge 2)
  - Show: current wattage, daily kWh, on/off state

- [ ] **CR-016** — Build Ignition room overview dashboard
  - Composite view: environmental data + occupancy (if Apollo MSR-2 deployed) per room
  - Feed from MQTT topics under `coolrunning/environment/<room>/*`

- [ ] **CR-017** — Evaluate replacing Ignition with a custom React Native dashboard
  - Gemini conversation noted this is an option (similar to TorqueAI frontend approach)
  - Decision gate: keep Ignition SCADA or build custom UI?

---

## Open Questions

1. **Evo Energy outlets** — what protocol do they use? (Zigbee, Wi-Fi, Matter?) Determines integration path.
2. **MQTT topic structure** — finalize naming convention before adding more sensors so Ignition tiles do not need to be rewired later.
3. **Panel monitoring** — Shelly Pro 3EM or Emporia Vue Gen 3? Settle before Phase 2 closes.
4. **Custom frontend** — stick with Ignition SCADA or build React Native dashboard (TorqueAI-style)?
5. **Server details** — is this running on the same repurposed tower as TorqueAI, or a dedicated machine?

---

## Notes

- All environmental sensors (low voltage, USB powered) are safe to self-install — no insurance concerns.
- All high-voltage hardware (smart plugs, panel monitors) must be **commercially certified (UL-listed)**. No DIY relay builds inside wall boxes or breaker panels.
- Insurance compliance was a deliberate architectural decision. Do not deviate from this.
- The BME680 Ignition tile schema is already built. New sensor tiles should follow its structure.
