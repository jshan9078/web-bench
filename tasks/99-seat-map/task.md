# 99-seat-map

- **kind**: legend + spatial reasoning + pixel clicks (programmatic)
- **site**: localhost widget (widgetapp/seatmap.py, port 8819)
- **what it tests**: reading a seat map legend (available, taken, hatched restricted view, price bands), applying three constraints at once (cheapest band, adjacent, not restricted), and clicking the right seats by coordinates
- **discrimination hypothesis**: the cheapest band has exactly one clean pair; its other adjacent-looking pairs include a hatched restricted seat or straddle the aisle, and the next band has many clean pairs. Agents that miss the hatch, ignore the aisle, or settle for the wrong band fail; a mis-click selects a neighbour.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the confirmed selection equals the unique clean adjacent pair in the cheapest band.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8819/ . It is a theatre seat map rendered as an IMAGE with a legend (read it 
from screenshots; click seats with raw coordinates via click --at X,Y; the image starts at the 
page's top-left so screenshot pixels map 1:1). Select the two CHEAPEST adjacent available seats 
(same row, consecutive seat numbers, not across the aisle) that are NOT restricted view, then click 
Confirm selection. Do NOT read the page source or call the site's HTTP endpoints directly. End with 
the two seat ids.
```
