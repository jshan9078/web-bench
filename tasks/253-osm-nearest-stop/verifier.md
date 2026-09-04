# 253-osm-nearest-stop, verifier

**Method:** LLM-as-judge (Claude).

## Pass criteria

The judge runs an Overpass query for highway=bus_stop / railway=tram_stop / subway entrances within 150 m of the library's main entrance (approx 43.6717, -79.3868) and passes the run only if the reported stop name matches the nearest one (by distance) and the street is right; screenshots must show the map or query result panel.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually navigated to and evidence it captured THIS run.
