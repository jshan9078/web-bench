# 164-gcal-recurring

- **kind**: real-site custom recurrence (LLM-judge)
- **site**: calendar.google.com (signed-in profile)
- **what it tests**: using the custom recurrence dialog (weekly on two days, ending after N occurrences), setting a colour, verifying on the month view, and deleting a whole series
- **discrimination hypothesis**: the custom recurrence dialog has several controls that must all be set; deleting must target the whole series; verification is on captured month view and event details.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: Captured evidence must show the event created at 09:15-09:30 with recurrence weekly on Tuesday and Thursday ending after 6 occurrences (rule text or six occurrences across three weeks on the month view), colour Sage, and afterwards the series deleted with the month view clear. Wrong days, wrong end condition, wrong colour, or remaining occurrences fail.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
You are running on a browser profile where the user is already signed in. If a login page appears 
anyway, show the window and ask the user to sign in, then continue. Reruns must start fresh: if any 
"webbench standup" events exist from a previous run, delete the whole series first. On Google 
Calendar (https://calendar.google.com) create an event titled "webbench standup" from 09:15 to 
09:30 starting on the NEXT Tuesday, repeating weekly on Tuesday AND Thursday, ending after 6 
occurrences (use the custom recurrence dialog), with the event colour set to Sage. Save it, switch 
to the month view for that month, take a screenshot showing the occurrences, and open one 
occurrence to confirm the recurrence rule text and colour. Then delete the entire series (choose 
"All events") and confirm the month view is clear again. Do not modify any other event. End with 
the six dates you saw and the recurrence text you confirmed.
```
