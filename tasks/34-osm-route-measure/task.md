# 34-osm-route-measure

- **kind**: read + vision (LLM-judge)
- **site**: openstreetmap.org
- **what it tests**: using a routing widget and reading live-computed distance/time plus the drawn route
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: distance, time, and instructions match the routing panel captured this run.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On OpenStreetMap (https://www.openstreetmap.org), use the directions feature to get FOOT (walking)
directions from Union Station, Toronto to St. Lawrence Market, Toronto. Report the total distance
and estimated time the routing panel shows, plus the first TWO turn-by-turn instructions. Take a
SCREENSHOT showing the route line drawn on the map. End with the distance, the time, and the two
instructions.
```
