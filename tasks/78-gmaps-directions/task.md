# 78-gmaps-directions

- **kind**: read + navigation (LLM-judge)
- **site**: google.com/maps
- **what it tests**: driving a map UI with no API: directions entry, travel-mode switching, opening step-by-step details, reading route summaries for two modes
- **discrimination hypothesis**: the map UI is dense, stateful, and largely non-textual; agents that read the default (driving) route, skip the details panel, or report the wrong mode's duration fail. Live traffic and schedules make it pretraining-proof.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: walking time, distance, first turn instruction, transit duration, and first transit line match the captured directions panel.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open Google Maps (https://www.google.com/maps). Get directions from "Union Station, Toronto" to
"Royal Ontario Museum" and switch the travel mode to WALKING. Report the walking time and distance shown
for the recommended route, and the first turn instruction from the step-by-step directions (open the
details to read the steps). Then switch to TRANSIT and report the duration Google shows for the option it marks as "Best"
(not merely the first listed) and which transit line that option uses first. If a consent or sign-in interstitial appears, dismiss
it without signing in. Base everything on what the page shows. End with those five items.
```
