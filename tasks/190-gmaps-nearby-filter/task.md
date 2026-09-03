# 190-gmaps-nearby-filter

- **kind**: real-site filtered search (LLM-judge)
- **site**: google.com/maps (signed-out)
- **what it tests**: using Nearby search with filter chips (Open now, Rating 4.0+) and choosing the closest result by walking time from a place card
- **discrimination hypothesis**: the filters live behind chips or an All filters panel; agents that skip a filter, take the first result, or estimate distance fail against the captured list and directions panel.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: Captured evidence must show the Nearby pharmacy results with Open now and Rating 4.0+ applied, and the reported pharmacy must be the one with the shortest walking time among those results as shown on the page (results list or Directions), with name, address, rating and walking time matching the captured panels.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open Google Maps (https://www.google.com/maps), search for "Toronto Reference Library", then use 
its Nearby search for "pharmacy". Apply the results filters Open now and Rating 4.0+ (use the 
filter chips or the All filters panel). Among the filtered results, report the pharmacy with the 
SHORTEST walking time from the library (open Directions for the top candidates if the list shows no 
times), with its name, address, rating and the walking time Google shows. Never estimate; read 
every figure from the page. If a consent or sign-in interstitial appears, dismiss it without 
signing in. End with those items.
```
