# 16-transit-directions

- **kind**: read (LLM-judge)
- **site**: google.com/maps
- **what it tests**: transit routing with live schedule reading
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the route and the next departure times match the directions panel captured this run.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On Google Maps (https://www.google.com/maps), get TRANSIT directions from Union Station, Toronto to
Toronto Pearson International Airport, departing now. Report the TOP-LISTED route card (line or
service name), its total duration, the departure time it shows, and the service frequency if
stated (for example every 15 min). End with route, duration, departure time, and frequency.
```
