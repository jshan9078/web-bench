# 96-slide-diff

- **kind**: video navigation + comparison across two moments (programmatic)
- **site**: localhost widget (widgetapp/slidediff.py, port 8816)
- **what it tests**: reading two frames far apart in a video and diffing them by content: the corrected table lists rows in a different order and rewords one label without changing its amount
- **discrimination hypothesis**: positional comparison picks the wrong row; label-based comparison flags the reworded row; agents that read only the corrected table have nothing to compare against. Both tables are on screen for 25 s or more, far above any harness round-trip.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: a submission names the changed row (label substring) and its amount equals the corrected value (digits compared).

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8816/ . It is a recording of a presentation playing in a video player (the 
video autoplays; use the player controls, the keyboard shortcuts, or click a transcript line to 
seek). The slides are burned into the video, so read them from screenshots. The presenter shows a 
DRAFT budget table early in the talk and a CORRECTED version near the end. Exactly one line item's 
AMOUNT changed between the two tables. Report that line item and its corrected amount. Enter both 
in the form under the player and submit. Do NOT read the page source or call the site's HTTP 
endpoints directly. End with the item and amount.
```
