# 44-gcal-event

- **kind**: signed-in action (LLM-judge)
- **site**: calendar.google.com
- **what it tests**: date navigation and event creation with fields, then visual verification
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: calendar screenshot shows the event on the correct date and time.
- **requires**: signed-in browser profile

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
You are running on a browser profile where the user is already signed in. If a login page appears anyway, show the window and ask the user to sign in, then continue. On Google Calendar (https://calendar.google.com), create an event titled: webbench
sync. Schedule it for NEXT Monday from 10:00 to 10:30, and set the location field to: Online (the field has aggressive place autocomplete; make sure
plain Online sticks rather than an auto-selected real place).
Save it, navigate the calendar so next Monday is visible, and take a screenshot showing the event
on the grid. Do not modify any other events. End with the exact date you used and confirmation
the event is visible.
```
