# 79-gmaps-place-hours

- **kind**: read + navigation (LLM-judge)
- **site**: google.com/maps
- **what it tests**: place search, reading a place card (address, hours by weekday, rating), using the card's Nearby search and reading a distance from the results
- **discrimination hypothesis**: the hours widget must be expanded to see a specific weekday, the open/closed badge is time-dependent, and Nearby results are ranked by the map viewport; agents that report today's hours as Sunday's, or the first nearby result without checking distance, fail.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: address, next-Sunday hours, rating and review count, open/closed status, and the nearest coffee shop with its shown distance or time match the captured cards.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open Google Maps (https://www.google.com/maps) and search for "Toronto Reference Library". From its
place card report: the full street address, the opening hours listed for next Sunday (expand the hours; if the card only shows a single day's
hours in this signed-out view, say exactly that rather than guessing), the star rating and
number of reviews, and whether Google currently marks it as open or closed. Then use the place card's
"Nearby" search to find the closest coffee shop and report its name and the distance or walking time Google
shows from the library; if the results list shows no distance, get one from Directions between the two
places. Never estimate a distance yourself. If a consent or sign-in interstitial appears, dismiss it without signing in. Base
everything on what the page shows. End with those items.
```
