# 159-thermostat

- **kind**: image-only stepwise setting (programmatic)
- **site**: localhost widget (widgetapp/thermostat.py, port 8855)
- **what it tests**: reaching an exact setpoint with 0.5-degree steps, choosing a mode, leaving another control untouched, and saving
- **discrimination hypothesis**: five to ten precise clicks with visual verification; overshooting or changing the fan fails.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the saved setpoint and Heat mode match and the fan is unchanged.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8855/ . It is a wall thermostat panel. It is rendered as an IMAGE at the 
page's top-left that responds to clicks (use raw coordinates via click --at X,Y; screenshot pixels 
map 1:1; the image refreshes after each click, so take a fresh screenshot to see the result). The 
text under the image states the target temperature: set it exactly (the +/- buttons move by 0.5), 
set the mode to Heat, leave the fan setting as it is, and press Save. Do NOT read the page source 
or call the site's HTTP endpoints directly. End with the settings you saved.
```
