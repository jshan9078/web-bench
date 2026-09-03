# 163-gmaps-route-options

- **kind**: real-site route building and options (LLM-judge)
- **site**: google.com/maps (signed-out)
- **what it tests**: building a three-point driving route in the order required when the UI appends destinations at the end, then applying two route options and reading the updated totals
- **discrimination hypothesis**: the middle stop cannot be inserted directly without drag, so the agent must find an order-preserving way (e.g. build Union to library first, then add the zoo); the options panel is a second level; agents that report the wrong order's totals or skip an option fail against the captured panel.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: Captured evidence must show (1) the two-point route with its distance and time, (2) a three-point route in the order Union Station, Toronto Reference Library, Toronto Zoo with its totals, (3) the same route with both Avoid tolls and Avoid highways enabled and its totals. Reported figures must match the captured panels; a route in the wrong order, missing option, or estimated figure fails.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open Google Maps (https://www.google.com/maps) and get DRIVING directions from "Union Station, 
Toronto" to "Toronto Zoo". Report the recommended route's distance and travel time. Then make the 
trip go via "Toronto Reference Library" BEFORE the zoo (three-point route: Union Station, then the 
library, then the zoo; use Add destination and arrange the order however the UI allows) and report 
the new total distance and time. Finally open the route Options, enable both "Avoid tolls" and 
"Avoid highways", and report the resulting total distance and time for the three-point route. Never 
estimate; read every figure from the page. If a consent or sign-in interstitial appears, dismiss it 
without signing in. End with the three distance/time pairs.
```
