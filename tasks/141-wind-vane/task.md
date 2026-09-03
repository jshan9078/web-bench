# 141-wind-vane

- **kind**: sub-tick angle interpolation (programmatic)
- **site**: localhost widget (widgetapp/windvane.py, port 8847)
- **what it tests**: reading an arrow's bearing against a compass rose with 10-degree ticks to within 3 degrees
- **discrimination hypothesis**: the tolerance is under a third of a tick spacing (the dial task showed every config failing at a fifth); nearest-tick answers fail.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted bearing is within 3 degrees of the vane.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8847/ . It is a marina weather-station panel with a compass rose and a 
wind-direction arrow, rendered as an IMAGE (read it from screenshots; ticks every 10 degrees, 
labels every 30). Report the direction the arrow points in degrees (0-359, within 3 degrees), enter 
it in the form below the panel and submit. Do NOT read the page source or call the site's HTTP 
endpoints directly. End with the degrees.
```
