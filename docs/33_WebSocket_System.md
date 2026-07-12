# 33 — WebSocket System

**HeliosAI** — AI-Powered Space Weather Intelligence Platform
Document 33 of 61

---

## 1. Purpose
Defines the real-time alerting and telemetry streaming protocols via WebSockets, resolving the P0-3 blocker identified in the Final Review Report.

---

## 2. Channels

### 2.1 `alerts` Channel
- **Topic**: Pushes critical and warning level alerts to connected UI dashboards.
- **Payload Schema**:
  ```json
  {
    "type": "NOWCAST_ALERT",
    "timestamp": "2026-07-12T12:00:00Z",
    "class_level": "M1.2",
    "message": "Solar flare peak detected."
  }
  ```

### 2.2 `forecasts` Channel
- **Topic**: Real-time push of probability updates.
- **Payload Schema**:
  ```json
  {
    "type": "FORECAST_UPDATE",
    "lead_time_min": 15,
    "probability": 0.85
  }
  ```

---

## 3. Reconnection Policy
Clients implement exponential backoff on disconnect, attempting reconnection up to 5 times before failing gracefully.

**Next document:** `34_Background_Jobs.md` — say **NEXT** to continue.
