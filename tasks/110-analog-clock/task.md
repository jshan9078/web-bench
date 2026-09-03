# 110-analog-clock

- **kind**: analog clock reading (programmatic)
- **site**: localhost widget (widgetapp/analogclock.py, port 8830)
- **what it tests**: reading hour and minute hands on a clock face with only four numerals (Tokyo clock among three)
- **discrimination hypothesis**: analog clocks are a documented vision-model weakness (hour hand offset, hand confusion); the tolerance of 2 minutes is generous for a human and strict for a guess.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted time is within 2 minutes of the Tokyo clock (12-hour).

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8830/ . It is a photo of three office wall clocks labelled by city (read it 
from screenshots). What time does the TOKYO clock show? Enter it as HH:MM (12-hour, within 2 
minutes) in the form below the photo and submit. Do NOT read the page source or call the site's 
HTTP endpoints directly. End with the time.
```
