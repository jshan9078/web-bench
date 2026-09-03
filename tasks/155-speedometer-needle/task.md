# 155-speedometer-needle

- **kind**: sub-tick needle interpolation (programmatic)
- **site**: localhost widget (widgetapp/speedo.py, port 8851)
- **what it tests**: reading a speedometer needle between 10 km/h ticks to within 2 km/h, ignoring the tachometer
- **discrimination hypothesis**: the tolerance is a fifth of a tick spacing, the ratio at which the dial beat every config; nearest-tick or nearest-5 answers fail.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted speed is within 2 km/h of the needle.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8851/ . It is a photo of a car's instrument cluster (read it from 
screenshots). Report the speed shown by the SPEEDOMETER needle in km/h, within 2 km/h (ticks are 
every 10 km/h; not the tachometer), enter it in the form below the photo and submit. Do NOT read 
the page source or call the site's HTTP endpoints directly. End with the speed.
```
