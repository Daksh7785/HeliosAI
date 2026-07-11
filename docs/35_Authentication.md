# 35 — Authentication

> **Document 35 of 61** in the HeliosAI documentation set (see `README.md` → Repository Structure). Defines how users verify their identity to the Serving Layer.

---

## Table of Contents

1. [Purpose of This Document](#purpose-of-this-document)
2. [Authentication Protocol](#authentication-protocol)
3. [Token Management](#token-management)
4. [Integration with FastAPI](#integration-with-fastapi)

---

## Purpose of This Document

HeliosAI is intended for operational and research use, necessitating secure access controls. This document defines the authentication mechanisms protecting the REST and WebSocket APIs.

## Authentication Protocol

HeliosAI uses **JSON Web Tokens (JWT)** via OAuth2 with Password Flow (Bearer tokens). 
- Clients (Dashboard, CLI) authenticate via the `/api/v1/auth/login` endpoint using an email and password.
- The backend issues an access token (short-lived) and a refresh token (long-lived).

## Token Management

- Tokens are signed using HS256 with a secret key managed by the deployment environment (`54_Secrets_Management.md`).
- WebSocket connections authenticate by passing the JWT in the initial connection handshake (query parameter or initial payload frame, depending on the client library).

## Integration with FastAPI

Authentication logic is implemented using the `FastAPI-Users` library, which handles password hashing (bcrypt), token generation, and user database models (`users.py` in `shared/db/models/`) out-of-the-box.

**Next document:** `36_Authorization.md`
