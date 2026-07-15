# LastMile: Delivery Layer for Humanitarian Cash Assistance

This subsystem implements the isolated **Universal USSD Wallet Access (Pillar 3)** for the SAPCONE LastMile delivery platform. It functions as a lightweight, state-driven gateway mapping basic feature phone sessions directly to verification mechanisms using an Africa's Talking integration profile.

## Core Flow Mechanism
1. **Dial:** Participant/Proxy dials the custom assigned USSD string (`*483*700#`).
2. **Identify:** User supplies their unique, non-PII `Reference ID`.
3. **Verify:** User verifies the transaction by entering the system-generated `OTP` sent to the registered mobile number (enforcing caller ID cross-verification).
4. **Trigger:** The application executes validation and triggers back-end handlers for Stellar/Soroban asset swapping and local mobile money (M-Pesa) off-ramping.

---

## Local Development & Sandboxing

### Prerequisites
* Python 3.8+
* [Ngrok](https://ngrok.com/) account (for web-hook exposure)
* Africa's Talking Sandbox Account

### 1. Installation
Install the gateway framework dependencies:
```bash
pip install -r requirements.txt