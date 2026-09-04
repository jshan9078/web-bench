# 253-osm-nearest-stop

- **kind**: real-site map tool use (LLM-judge)
- **site**: openstreetmap.org (signed-out)
- **what it tests**: using OSM search, zoom and the Query features tool to identify the nearest transit stop to a building entrance
- **discrimination hypothesis**: requires operating the query tool or reading dense map labels at high zoom; the judge verifies with an Overpass query for public_transport stops near the library entrance.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: The judge runs an Overpass query for highway=bus_stop / railway=tram_stop / subway entrances within 150 m of the library's main entrance (approx 43.6717, -79.3868) and passes the run only if the reported stop name matches the nearest one (by distance) and the street is right; screenshots must show the map or query result panel.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open OpenStreetMap (https://www.openstreetmap.org), search for "Toronto Reference Library" and 
centre the map on it. Using the map and its Query features tool (the question-mark icon in the 
right toolbar, then click a feature) or by zooming in and reading the map, find the nearest public 
transport stop (bus, streetcar or subway entrance) to the library's main entrance on Yonge Street, 
and report the stop's name as shown in OpenStreetMap and which street it is on. Read everything 
from the site; do not guess. End with the stop name and street.
```
