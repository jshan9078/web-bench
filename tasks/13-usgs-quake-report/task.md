# 13-usgs-quake-report

- **kind**: read (LLM-judge)
- **site**: earthquake.usgs.gov
- **what it tests**: interactive data map/list filtering and event-page reading
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the reported event is the largest of the past 24h on the captured feed and its details match its event page.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On the USGS earthquakes site (https://earthquake.usgs.gov/earthquakes/map/), configure the feed to
show earthquakes from the past 24 hours worldwide (any magnitude range that includes the largest).
Identify the LARGEST magnitude event in that window, open its event page, and report: magnitude,
the named location, depth in km, and the UTC origin time. End with those four facts plus the event
page URL.
```
