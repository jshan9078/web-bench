# 180-radio-tuner

- **kind**: needle reading against fine ticks with keyboard control (programmatic)
- **site**: localhost widget (widgetapp/tuner.py, port 8864)
- **what it tests**: reading a needle on a 0.2 MHz scale to within 0.1 MHz while driving it with keyboard steps, and confirming exactly once
- **discrimination hypothesis**: the same skill that beat every config on the dial (integer target on fine ticks) in a realistic wrapper; over- or under-shooting by two ticks, or confirming twice, fails.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: a single confirm within 0.1 MHz of the target.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8864/ . It is an FM tuner rendered as an IMAGE with a linear dial (88 to 108 
MHz, small ticks every 0.2 MHz) and a red needle; the current frequency is never printed, so read 
the needle against the scale from screenshots. The arrow keys move the needle by 0.1 MHz per press 
(Shift+arrow: 1.0 MHz); use the keyboard (press ArrowRight, ArrowLeft, Shift+ArrowRight, etc.). 
Tune to the station stated under the image, within 0.1 MHz, then press Enter exactly once to 
confirm. Do NOT read the page source or call the site's HTTP endpoints directly. End with the 
frequency you confirmed.
```
