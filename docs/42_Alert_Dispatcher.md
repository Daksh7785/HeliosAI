# 42 — Alert Dispatcher

> **Document 42 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines the external notification system.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Dispatcher Mechanics](#dispatcher-mechanics)
3. [Supported Channels](#supported-channels)
4. [Debouncing and Rate Limiting](#debouncing-and-rate-limiting)

---

## Purpose of This Document

While WebSockets (`33_WebSocket_System.md`) alert users actively looking at the Dashboard, the Alert Dispatcher reaches users who are offline.

## Dispatcher Mechanics

The Alert Dispatcher is a background service (typically a Celery task) triggered by the API when a new high-severity event is added to the Master Catalogue or a high-probability forecast is generated.

## Supported Channels

- **Email:** SMTP integration for daily summaries or high-priority M/X class warnings.
- **Webhooks:** Generic POST payloads allowing institutional users to integrate HeliosAI alerts into their own Slack/Discord/Teams or internal monitoring systems.

## Debouncing and Rate Limiting

To prevent alert fatigue during complex, multi-peaked flare events or prolonged solar storms, the dispatcher implements a debounce mechanism. If a C-class alert is sent, and an M-class threshold is crossed 2 minutes later, the system will escalate the alert. However, minor probability fluctuations (e.g., forecast dropping from 85% to 82% and back) will not trigger successive emails.

**Next document:** `43_Catalogue_Explorer.md`
