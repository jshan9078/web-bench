# 32-desmos-intersections

- **kind**: action + vision (LLM-judge)
- **site**: desmos.com
- **what it tests**: plotting expressions, then reading tool-computed intersection coordinates
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: screenshot shows both curves and the clicked intersection label matches the reported coordinates.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open the Desmos graphing calculator (https://www.desmos.com/calculator). In the expression list,
enter y = sin(x) + cos(2x) and, as a second expression, y = x/3. Count how many intersection
points of the two curves are visible in the default viewport. If + or ^ does not register from key presses, open Desmos's on-screen keyboard (bottom-left
toggle) and click the symbol buttons instead. Then ZOOM IN on the LEFTMOST visible
intersection (so your click can land precisely) and click directly on it so Desmos labels its
coordinates, and report those coordinates to two
decimals exactly as displayed. Take a screenshot showing the curves and the labeled point. End
with the visible-intersection count and the coordinates.
```
