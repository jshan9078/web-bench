# 127-clock-ticks

- **kind**: analog clock without numerals (programmatic)
- **site**: localhost widget (widgetapp/clockticks.py, port 8839)
- **what it tests**: reading hour and minute hands on a face with ticks only and a second hand as distractor
- **discrimination hypothesis**: with no numerals the hour must be counted from the 12 mark and the hour hand's offset interpreted; the thin second hand invites hand confusion. Tolerance 2 minutes.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted time is within 2 minutes of the clock (12-hour).

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8839/ . It is a photo of a station platform clock with tick marks only (read 
it from screenshots). What time does it show? Enter it as HH:MM (12-hour, within 2 minutes) in the 
form below the photo and submit. Do NOT read the page source or call the site's HTTP endpoints 
directly. End with the time.
```
