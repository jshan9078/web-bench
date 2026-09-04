# 205-gmaps-transit-compare

- **kind**: real-site route comparison (LLM-judge)
- **site**: google.com/maps (signed-out)
- **what it tests**: setting an arrive-by time and comparing the offered transit routes on two criteria, reading each route's details
- **discrimination hypothesis**: the route with the fewest transfers is usually not the fastest; reading the wrong route's figures, missing the arrive-by setting, or estimating fails against the captured route list.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: Captured evidence must show transit routes with the arrive-by 8:00 AM next Monday setting; the reported fewest-transfers route and fastest route (departure, arrival, total time, transfers) must match the captured route list and details, including the case where they coincide.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open Google Maps (https://www.google.com/maps) and get PUBLIC TRANSIT directions from "Toronto 
Reference Library" to "Toronto Pearson International Airport Terminal 1", set to ARRIVE BY 8:00 AM 
next Monday. Compare the routes Maps offers: report, for the route with the FEWEST transfers, its 
departure time, arrival time, total time and number of transfers, and for the FASTEST route the 
same four items. If both are the same route, say so. Never estimate; read every figure from the 
route list and details. If a consent or sign-in interstitial appears, dismiss it without signing 
in. End with those items.
```
