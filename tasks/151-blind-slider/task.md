# 151-blind-slider

- **kind**: precision setting without readout (programmatic)
- **site**: localhost widget (widgetapp/blindslider.py, port 8849)
- **what it tests**: setting a level on a bar with no numeric feedback to within 3 points by judging handle position against the bar's ends
- **discrimination hypothesis**: with no readout the agent must compute the pixel for the target and verify the handle visually; off-by-a-few-percent placements fail.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the saved level is within 3 points of the target.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8849/ . It is a sound-settings panel whose volume bar is an IMAGE at the 
page's top-left with no numeric readout (click on the bar with raw coordinates via click --at X,Y 
to set the level; screenshot pixels map 1:1; the image refreshes after each click). Set the volume 
to the percentage stated on the page, within 3 points, then click Save. Do NOT read the page source 
or call the site's HTTP endpoints directly. End with the level you set.
```
