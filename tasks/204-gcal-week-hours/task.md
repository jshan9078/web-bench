# 204-gcal-week-hours

- **kind**: real-site aggregation (LLM-judge)
- **site**: calendar.google.com (signed-in profile)
- **what it tests**: reading every timed event in a week from the calendar grid (opening truncated ones), excluding all-day events, and summing durations
- **discrimination hypothesis**: the sum depends on reading each event's exact times; all-day events and truncated grid entries are the traps; the judge checks the listed events and arithmetic against captured screenshots of the week.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: Captured week view (and any opened events) must show every timed event the agent lists; the listed times must match; the total (to the nearest quarter hour) and the busiest day must follow from them; all-day events must be excluded. A missed or misread event, or arithmetic error, fails.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
You are running on a browser profile where the user is already signed in. If a login page appears 
anyway, show the window and ask the user to sign in, then continue. On Google Calendar 
(https://calendar.google.com), look at NEXT week (Monday to Sunday). Report the total number of 
hours of timed events (events with a start and end time; ignore all-day events and holidays) on the 
calendar that week, and the day with the most timed hours. Read every event's times from the 
calendar (open events if the grid truncates them); do not modify anything. End with the total hours 
(to the nearest quarter hour), the busiest day, and the list of events you counted with their times.
```
