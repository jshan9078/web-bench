# 75-map-explorer

- **kind**: action + vision + navigation (programmatic)
- **site**: localhost test site (widgetapp/mapexplorer.py, port 8797)
- **what it tests**: exploring an unfamiliar map UI without search: choosing a zoom level at which labels render, panning toward a described region, keeping orientation across pans, clicking a small marker, reading a popup, taking the one allowed action
- **discrimination hypothesis**: the analogue of "no maps tool, but Google Maps is right there". Agents that never zoom in see no labels; agents that lose orientation while panning burn the budget; agents that route from the wrong marker fail objectively. The target and layout are random per run.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: popup opened for the target place and Route clicked for it and for no other place.
- **prompt placeholders**: the harness substitutes {NAME} and {DISTRICT} from the server's per-run target at setup.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8797/ , a map app with NO search box. The map is an image: pan with the on-screen
arrow buttons (or arrow keys) and zoom with the + and - buttons; place labels only appear once you have
zoomed in. Find the place named "{NAME}" (it is in the {DISTRICT} district of the city) and click its red
marker to open its details popup. Report its category and its distance to City Hall exactly as the popup
shows them, then click the popup's "Route to City Hall" button. Do not route from any other place. Do NOT
read the page source or call the site's HTTP endpoints directly; navigate the map visually. End with the
place name, its category, and the distance.
```
