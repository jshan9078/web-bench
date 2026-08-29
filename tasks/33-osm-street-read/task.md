# 33-osm-street-read

- **kind**: read + vision (LLM-judge)
- **site**: openstreetmap.org
- **what it tests**: map search, zooming, and reading street names off rendered map tiles
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the streets named are visible on the run's map screenshot at the captured location.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On OpenStreetMap (https://www.openstreetmap.org), search for the Distillery District in Toronto
and zoom in until individual street names around it are legible on the map. Take a SCREENSHOT of
the map. From the rendered map (not from any sidebar text), read and report TWO street names that
border or cross the district, and also report the coordinates from the page URL after zooming.
End with the two street names and the URL coordinates.
```
