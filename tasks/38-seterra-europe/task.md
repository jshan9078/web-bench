# 38-seterra-europe

- **kind**: action + vision + pixel (LLM-judge)
- **site**: geoguessr.com/seterra (or seterra.com)
- **what it tests**: map quiz: clicking named countries on a map from visual recognition
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the end-of-attempt score/accuracy shown matches the report, per the final screenshot.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Find and open the free Seterra map quiz for the countries of Europe (search for: Seterra Europe
countries map quiz; it now lives under GeoGuessr). Start the quiz. It names a country and you must
pixel-click it on the map: take a SCREENSHOT, locate the named country, click it, and repeat for
at least the first FIVE prompts. Then take a screenshot showing the quiz's running score or
accuracy display, and stop. End by listing the countries you were asked, and the score/accuracy
the quiz displayed.
```
