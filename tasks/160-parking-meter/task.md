# 160-parking-meter

- **kind**: image-only arithmetic stepping (programmatic)
- **site**: localhost widget (widgetapp/parkmeter.py, port 8856)
- **what it tests**: composing an exact duration from +15 min, +1 h and -15 min buttons on an image panel and paying for the right zone
- **discrimination hypothesis**: exactness (no rounding), zone selection first, and a display that must be read back after each press.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: paid record equals the stated zone and minutes.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8856/ . It is a pay-and-display parking meter. It is rendered as an IMAGE at 
the page's top-left that responds to clicks (use raw coordinates via click --at X,Y; screenshot 
pixels map 1:1; the image refreshes after each click, so take a fresh screenshot to see the 
result). The text under the image states the zone and the exact duration: select that zone, add 
time until the display shows exactly that duration, then press PAY (the display shows PAID). Do NOT 
read the page source or call the site's HTTP endpoints directly. End with the zone and duration 
paid.
```
