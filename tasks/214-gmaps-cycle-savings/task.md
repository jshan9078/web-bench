# 214-gmaps-cycle-savings

- **kind**: real-site multi-query reading (LLM-judge)
- **site**: google.com/maps (signed-out)
- **what it tests**: running four directions queries (two destinations, two modes), reading each recommended time, and comparing savings
- **discrimination hypothesis**: four separate readings must be kept straight; misattributing a mode or destination changes the comparison; the judge checks each reported time against the captured panel for that query.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: Captured evidence must show walking and cycling directions from the library to each destination; the four reported times must match the captured panels and the stated larger saving must follow from them.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open Google Maps (https://www.google.com/maps). For each of these two destinations from "Toronto 
Reference Library": (a) "Toronto City Hall" and (b) "Casa Loma", get both WALKING and CYCLING 
directions and read the recommended route's time for each mode. Report all four times, and state 
which destination has the larger time saving from cycling instead of walking (in minutes). Never 
estimate; read every figure from the page. If a consent or sign-in interstitial appears, dismiss it 
without signing in. End with those items.
```
