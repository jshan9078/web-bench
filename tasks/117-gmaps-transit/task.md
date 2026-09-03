# 117-gmaps-transit

- **kind**: real-site navigation + transit options (LLM-judge)
- **site**: google.com/maps (signed-out)
- **what it tests**: using the transit directions options (arrive-by date and time) and reading the recommended route's departure time, duration, transfers and first line
- **discrimination hypothesis**: the arrive-by control sits behind an options panel and a date/time picker; agents that report the default depart-now route without saying so, or estimate transfers from the map, fail against the captured route panel.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: Captured evidence must show transit directions between the two places with the arrive-by option set to 9:00 AM next Monday (or an explicit statement that the control was unavailable, with the default route reported instead). The reported departure time, total duration, number of transfers and first line must match the first route shown in the captured panel. Estimated or unsupported values fail.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open Google Maps (https://www.google.com/maps) and get PUBLIC TRANSIT directions from "Toronto 
Reference Library" to "Toronto Pearson International Airport Terminal 1". In the transit options 
set it to ARRIVE BY 9:00 AM next Monday. For the first (recommended) route, report: the suggested 
departure time, the total travel time, the number of transfers, and the name of the first transit 
line or route number. Never estimate or compute these yourself; read them from the route. If the 
arrive-by controls are not available in this signed-out view, say exactly that and report the same 
items for the default route shown instead. If a consent or sign-in interstitial appears, dismiss it 
without signing in. Base everything on what the page shows. End with those items.
```
