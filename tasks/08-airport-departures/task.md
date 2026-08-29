# 08-airport-departures

- **kind**: read (LLM-judge)
- **site**: flightaware.com
- **what it tests**: live departures board: find, filter, and read structured flight data
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the reported flights match the live departures board captured this run.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On FlightAware (https://www.flightaware.com), open the live departures board for Toronto Pearson
(YYZ). Find the next THREE departures headed to any United States airport. For each, report the
flight number, airline, destination airport, and scheduled departure time from the board; the
board itself shows no status column, so OPEN EACH FLIGHT'S own page and report its current status
line (for example EN ROUTE, Scheduled, or a lateness note) from there. Base your answer only on
what those pages show right now. End with the three flights, one line each.
```
