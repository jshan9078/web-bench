# 87-gcal-scheduling

- **kind**: action + scheduling (LLM-judge)
- **site**: calendar.google.com (signed-in profile)
- **what it tests**: reading a week of existing events for a time-window conflict, creating an event with non-default notification and visibility, verifying, and cleaning up
- **discrimination hypothesis**: the first free day is a judgement over real calendar state, and the two settings live behind different controls in the event editor; agents that take the first weekday, leave the default notification, or skip the visibility toggle fail on captured evidence.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the chosen day is the first conflict-free weekday on the captured week, the event has the requested times, notification, and visibility, and the cleanup is shown.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
You are running on a browser profile where the user is already signed in. If a login page appears anyway,
show the window and ask the user to sign in, then continue. Reruns must start fresh: if a leftover
"webbench planning review" event exists from a previous run, delete it first. On Google Calendar
(https://calendar.google.com), look at NEXT week (Monday to Friday) and find the FIRST weekday on which the
calendar has no event overlapping 14:00-16:00 (an all-day event, including a holiday, overlaps the whole day
and therefore counts as a conflict). On that day create an event titled "webbench planning
review" from 14:30 to 15:15, set its notification to 30 minutes before (replace the default), and set its
visibility to Private. Save it, navigate so that day is visible, and take a screenshot showing the event on
the grid; open the event to confirm the notification and visibility settings. Do not modify any other
event. Then delete the event and confirm it is gone, noting the cleanup. If every weekday has a conflict,
say so and create nothing. End with the exact date you used (or "no free day") and the settings you
confirmed.
```
