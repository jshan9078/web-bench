# 314-fine-gauge

- **kind**: sub-tick needle estimation (programmatic)
- **site**: localhost widget (widgetapp/finegauge.py, port 8952)
- **what it tests**: estimating a needle position to a tenth of the tick spacing
- **discrimination hypothesis**: finer than a fifth of a tick separated configs before; a tenth is harder.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value is within 1 unit.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8952/ . The page shows an IMAGE of a gauge with labelled ticks every 10 units 
and no minor ticks (read it from screenshots). Report the value the needle indicates, within 1 
unit, enter it in the form and submit. Do NOT read the page source or call the site's HTTP 
endpoints directly. End with the value.
```
