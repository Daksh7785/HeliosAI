# 33 — WebSocket System

> **Document 33 of 61.** Complements `32_API_Design.md` with the real-time push contract needed for the dashboard's live alerting (per `README.md`'s Data Flow diagram).

---

## Table of Contents
1. [Purpose](#purpose)
2. [Why WebSockets](#why-websockets)
3. [Channels](#channels)
4. [Message Format](#message-format)
5. [Connection Lifecycle](#connection-lifecycle)
6. [Scaling via Redis Pub/Sub](#scaling-via-redis-pubsub)
7. [Revision History](#revision-history)

---

## Purpose

Specifies how nowcast/forecast triggers reach the dashboard (`39_Dashboard.md`) in real time, satisfying the "visualizes... with visual alerts" requirement from the Problem Statement and `README.md`'s Data Flow diagram.

---

## Why WebSockets

REST polling would add latency proportional to the poll interval, working against the Latency NFR in `README.md`. FastAPI's native WebSocket support (per `07_Tech_Stack.md`) allows server-initiated push the moment a nowcast/forecast event is written, with no client polling delay.

---

## Channels

| Channel | Payload | Trigger |
|---|---|---|
| `ws/catalogue` | New/updated nowcast event | Nowcasting Engine writes a promoted or tentative event |
| `ws/forecasts` | New forecast probability | Forecasting Engine emits a new prediction above a documented display threshold |
| `ws/alerts` | Formatted alert banner payload | Alert Dispatcher (`README.md` Serving Subsystem) fires |

Clients subscribe to one or more channels at connection time; unauthenticated connections are rejected (per `35_Authentication.md`).

---

## Message Format

```json
{
  "channel": "ws/catalogue",
  "type": "event.promoted",
  "data": {
    "event_id": "evt_20260703_0142",
    "class": "M2.4",
    "peak_ts": "2026-07-03T01:47:55Z",
    "confidence": 0.91
  },
  "server_ts": "2026-07-03T01:48:02Z"
}
```

---

## Connection Lifecycle

Standard connect → authenticate → subscribe → receive-push → (heartbeat ping/pong) → disconnect. Reconnection is client-responsibility; the server does not queue missed messages beyond a short buffer, since clients can always reconcile via a REST catalogue query (`32_API_Design.md`) on reconnect — avoiding unbounded server-side message buffering.

---

## Scaling via Redis Pub/Sub

Multiple FastAPI worker processes (behind NGINX, per `07_Tech_Stack.md`) each hold a subset of WebSocket connections; Redis Pub/Sub fans out new events from whichever worker's Celery task produced them to all workers, which then push to their own connected clients — this is the mechanism referenced in `README.md`'s architecture diagram's Redis Pub/Sub component.

---

## Revision History
| Version | Date | Author | Notes |
|---|---|---|---|
| 0.1 | 2026-07-12 | HeliosAI Documentation | Initial WebSocket System spec — channels, message format, scaling via Redis Pub/Sub |
