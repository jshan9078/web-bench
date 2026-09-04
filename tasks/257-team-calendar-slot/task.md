# 257-team-calendar-slot

- **kind**: reading a dual-person week grid and creating an event (programmatic)
- **site**: localhost widget (widgetapp/teamcal.py, port 8918)
- **what it tests**: finding the earliest 45-minute gap common to two calendars within working hours, skipping out-of-office days, and creating the event through a form
- **discrimination hypothesis**: overlapping blocks and quarter-hour offsets make the first common gap easy to misjudge; the out-of-office day is a trap.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: one event 'Harbor sync', 45 min, both invitees, at the earliest common free time.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8918/ . It is a team calendar week view showing Dana's and Priya's events 
(working hours 09:00-17:00; an amber bar marks an all-day out-of-office). Using the form under the 
calendar, create a 45-minute event titled "Harbor sync" with BOTH Dana and Priya invited at the 
EARLIEST time in the week when both are free for the full 45 minutes within working hours, skipping 
any day where either is out of office. Create exactly one event. Do NOT read the page source or 
call the site's HTTP endpoints directly. End with the day and start time.
```
