# 248-flight-booking

- **kind**: multi-step wizard with rules (programmatic)
- **site**: localhost widget (widgetapp/flightbook.py, port 8912)
- **what it tests**: reading fare rules, choosing the cheapest qualifying fare across flights, validating passenger entry, and picking a constrained seat pair on a map
- **discrimination hypothesis**: the cheapest fare with a checked bag is Standard on HB205, not the cheapest overall; the seat constraint (window plus adjacent middle, both free) has few valid pairs; a slip at any step fails.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the booking is HB205 Standard for 2 adults on the date, passengers Ana Silva and Tomas Berg, seats a free A+B or E+F pair in one row.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8912/ . It is an airline booking site. Book a flight from Harbor City to 
Northport on 2026-10-21 for 2 adults. Choose the CHEAPEST fare (across all flights that day) that 
INCLUDES a checked bag. Enter the passengers Ana Silva and Tomas Berg. On the seat map choose two 
free seats next to each other in the same row consisting of a window seat and the middle seat 
beside it (A with B, or E with F). Confirm the booking (the page shows a reference). Do NOT read 
the page source or call the site's HTTP endpoints directly. End with the flight, fare, seats and 
reference.
```
