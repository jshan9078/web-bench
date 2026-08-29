# 50-google-flights-nonstop

- **kind**: read (LLM-judge)
- **site**: google.com/travel/flights
- **what it tests**: date pickers, round-trip configuration, filtering, and reading live fares
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: both options are nonstop with prices/times matching the captured results.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On Google Flights (https://www.google.com/travel/flights), search a ROUND TRIP from Toronto (YYZ)
to Tokyo, Japan as a city destination (search Tokyo generally, covering both NRT and HND; picking a single airport can leave only one nonstop result). Departure: the first Monday of the month after next; return: one week
later. Use the date picker, then apply the NONSTOP-only filter. Report the TWO cheapest nonstop
options: airline, total price, and departure times for the outbound leg. End with the exact dates
you selected and the two options.
```
