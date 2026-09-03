# 90-dial-set

- **kind**: action + vision + precision (programmatic)
- **site**: localhost widget (widgetapp/dial.py, port 8810)
- **what it tests**: reading a needle against a tick scale from a screenshot, converting the gap into keyboard turns, verifying, and committing once
- **discrimination hypothesis**: a second precision form (thermostat or gain-knob style) to test whether the crosshair result generalises: estimation against a scale rather than against a ring.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: exactly one confirmation, within one unit of the target.
- **prompt placeholders**: the harness substitutes {TARGET} from the server's per-run target at setup.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8810/ . The page is one image of a gain dial: a needle over a scale from 0 to 100
with a tick every unit and a label every 10; the current value is never printed, so read the needle
against the ticks from a `screenshot`. Turn the dial to exactly {TARGET} using the arrow keys (each press
turns it 0.5; hold Shift for 5), taking fresh screenshots to check, and press Enter ONCE to confirm when
the needle is within one tick of {TARGET}. There is only one confirmation, so verify with a screenshot
before pressing Enter. The page must have keyboard focus (click on it first if needed). Do NOT read the
page source or call the site's HTTP endpoints directly. End by reporting the value you confirmed.
```
