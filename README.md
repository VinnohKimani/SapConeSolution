# LastMile: Delivery Layer for Humanitarian Cash Assistance

This repository contains the isolated **Universal USSD Wallet Access (Pillar 3)** prototype for the SAPCONE LastMile delivery platform. Built during the Phase 1 Studio Build, this microservice acts as a lightweight, state-driven gateway that bridges rural feature phones with the central backend using Africa's Talking.

## Current Implementation Progress
* **Language & Framework:** Built using Python 3 and the Flask framework to manage asynchronous USSD webhooks cleanly.
* **Environment Management:** Utilizes `pipenv` for isolated virtual environment package containment and deterministic builds (replacing raw `requirements.txt`).
* **Authentication Logic:** Implements the streamlined **Reference ID + Transaction OTP** authentication state machine, removing local participant PIN registration complexity in the field.
* **Network Exposure:** Leverages an `ngrok` secure tunnel to expose local execution blocks on port `3000` to remote telecom gateway aggregators.

---

## Testing Environment Specifications

### Registered Sandbox Channels
The gateway routing rules are actively mapped to the following Africa's Talking service codes:
* `*384*25423#` (Primary Testing Code)
* `*384*74779#`

### Current Webhook Endpoint
* **Callback URL:** `https://ebf9-197-248-238-33.ngrok-free.app/ussd`

---

## Local Development Execution

### 1. Fire Up the Virtual Environment Shell
Ensure you are inside the managed pipenv directory context before running scripts:
```bash
pipenv shell