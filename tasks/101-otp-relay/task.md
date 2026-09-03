# 101-otp-relay

- **kind**: time-sensitive cross-page relay (programmatic)
- **site**: localhost widget (widgetapp/otprelay.py, port 8821)
- **what it tests**: carrying a rotating one-time code from one page to another within its validity, and picking the right account's code
- **discrimination hypothesis**: the server accepts the current or previous 30 s window, so only working from a stale screenshot (reading the code, then doing other things first) or submitting the VPN account's code fails; the countdown ring is visible.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: a submitted code is the current or previous-window Northwind Mail code.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8821/ . It is an authenticator app showing rotating 6-digit codes for two 
accounts. Follow the link to verify a new device for Northwind Mail and enter the current Northwind 
Mail code so the device is verified (the page confirms success). Codes expire, so read a fresh one. 
Do NOT read the page source or call the site's HTTP endpoints directly. End with a one-line 
confirmation.
```
