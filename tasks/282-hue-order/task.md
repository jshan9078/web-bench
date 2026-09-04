# 282-hue-order

- **kind**: colour ordering with precise clicks (programmatic)
- **site**: localhost widget (widgetapp/huesort.py, port 8928)
- **what it tests**: ranking nine hues and clicking them in order on an image
- **discrimination hypothesis**: adjacent hues differ by as little as 18 degrees; one swap fails; nine ordered clicks.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the confirmed click order equals hue order.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8928/ . The page shows an IMAGE of nine colour swatches at the top-left (read 
it from screenshots; click with raw coordinates via click --at X,Y; screenshot pixels map 1:1). 
Click the swatches in order of hue, starting from the reddest and proceeding through orange, 
yellow, green, cyan and blue to the most violet (a number appears on each clicked swatch), then 
click Confirm order. Do NOT read the page source or call the site's HTTP endpoints directly. End 
with a one-line confirmation.
```
