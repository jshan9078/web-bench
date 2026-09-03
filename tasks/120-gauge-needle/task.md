# 120-gauge-needle

- **kind**: needle interpolation (programmatic)
- **site**: localhost widget (widgetapp/gauge.py, port 8838)
- **what it tests**: reading a needle between 0.2-bar minor ticks on a 270-degree gauge to within 0.15 bar, on the second of two gauges
- **discrimination hypothesis**: needle-angle interpolation is the skill every config failed on the dial; gauge 1 is the decoy and the tolerance is under one minor tick.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted pressure is within 0.15 bar of gauge 2.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8838/ . It is a photo of a boiler-room panel with two analog pressure gauges 
(read it from screenshots). Report the pressure shown on GAUGE 2 in bar, to within 0.15 bar (the 
minor ticks are 0.2 bar apart), enter it in the form below the photo and submit. Do NOT read the 
page source or call the site's HTTP endpoints directly. End with the reading.
```
