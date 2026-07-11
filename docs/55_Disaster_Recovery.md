# 55 — Disaster Recovery

> **Document 55 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines how the system survives a catastrophic failure.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [The Threat Model](#the-threat-model)
3. [Backup Strategies](#backup-strategies)
4. [Failover Mechanisms](#failover-mechanisms)

---

## Purpose of This Document

Space weather monitoring is mission-critical. If the primary cloud region goes offline during a major solar storm, HeliosAI must recover quickly.

## The Threat Model

- **Database Corruption:** Accidental dropping of the Master Catalogue.
- **Region Outage:** `us-east-1` goes down entirely.
- **Data Source Outage:** PRADAN goes offline.

## Backup Strategies

- **PostgreSQL:** Automated nightly snapshots retained for 30 days. Point-in-time recovery (PITR) enabled via WAL archiving to S3.
- **Models:** The MLflow artifact store (S3) is configured with object versioning and cross-region replication.

## Failover Mechanisms

- **Infrastructure:** Because of IaC (`50_Infrastructure.md`), spinning up a replica cluster in a different region takes minutes, not days.
- **Data Source:** If PRADAN fails, the Automated Fetcher (`17_Data_Ingestion.md`) falls back to GOES satellite data from NOAA SWPC as a temporary proxy to maintain baseline operations.

**Next document:** `56_Testing_Strategy.md`
