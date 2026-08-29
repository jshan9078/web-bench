# 35-gmaps-traffic-read

- **kind**: read + vision (LLM-judge)
- **site**: google.com/maps
- **what it tests**: toggling a live map layer and reading conditions visually off the rendered map
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the congestion report matches the traffic colors visible in the run's screenshot.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On Google Maps (https://www.google.com/maps), center the map on downtown Toronto and enable the
live TRAFFIC layer. Zoom so the Gardiner Expressway corridor is visible, take a SCREENSHOT, and
from the traffic colors on the map report the CURRENT congestion along the Gardiner: roughly what
share looks green versus orange versus red, and where the worst stretch is. Also state what the
map legend says the worst color you saw means. End with the congestion report.
```
