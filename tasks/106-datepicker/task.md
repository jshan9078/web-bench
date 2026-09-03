# 106-datepicker

- **kind**: calendar widget navigation (programmatic)
- **site**: localhost widget (widgetapp/datepicker.py, port 8826)
- **what it tests**: navigating a custom calendar (month arrows, month/year selects, blackout dates) to a computed date 14 months out and completing a multi-field form
- **discrimination hypothesis**: off-by-one month or year navigation, choosing a Friday that is not the last one, miscounting the three-night checkout, or leaving guests at one all fail; the calendar shows weekdays so no date arithmetic beyond reading is needed.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the stored booking equals check-in 2027-11-26, check-out 2027-11-29, two guests.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8826/ . It is a hotel booking form whose date fields open a calendar (typing 
is disabled). Book a stay checking in on the LAST Friday of November 2027, checking out three 
nights later, for two guests, and click Confirm booking (the page shows a booking reference). Do 
NOT read the page source or call the site's HTTP endpoints directly. End with the dates you booked.
```
