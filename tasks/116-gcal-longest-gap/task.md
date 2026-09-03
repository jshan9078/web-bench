# 116-gcal-longest-gap

- **kind**: action + scheduling judgement (LLM-judge)
- **site**: calendar.google.com (signed-in profile)
- **what it tests**: computing the longest free stretch across a week of real events under a stated rule (all-day events block the day), placing an event in its middle, removing the default notification, verifying and cleaning up
- **discrimination hypothesis**: the answer is a judgement over the whole week rather than the first free slot; agents that ignore all-day events, take the first free day, mis-centre the event, or leave the default reminder fail on captured evidence (the all-day rule is exactly what beat one config on 87).
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: From the captured week view, the chosen day must have the longest 09:00-17:00 free stretch with all-day events treated as fully blocking (earlier day on ties). The event must cover the middle 60 minutes of that stretch within 15 minutes, show no notification in the details or editor, appear on the grid screenshot, and be shown deleted afterwards. Wrong day, wrong placement, a remaining reminder, or missing cleanup fails.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
You are running on a browser profile where the user is already signed in. If a login page appears 
anyway, show the window and ask the user to sign in, then continue. Reruns must start fresh: if a 
leftover "webbench deep work" event exists from a previous run, delete it first. On Google Calendar 
(https://calendar.google.com), look at NEXT week (Monday to Friday) within working hours 
09:00-17:00. Treat an all-day event (including a holiday) as blocking its whole day. Find the 
weekday with the LONGEST uninterrupted free stretch inside 09:00-17:00 (if two days tie, take the 
earlier one). On that day create an event titled "webbench deep work" that covers the middle 60 
minutes of that free stretch (start rounded to the nearest 15 minutes), and remove ALL 
notifications from it (no reminder). Save it, navigate so that day is visible, take a screenshot 
showing the event on the grid, and open it to confirm it has no notification. Do not modify any 
other event. Then delete the event and confirm it is gone, noting the cleanup. End with the date, 
the free stretch you found (start-end), and the event's start and end times.
```
