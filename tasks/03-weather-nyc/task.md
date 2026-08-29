# 03-weather-nyc

- **kind**: read (LLM-judge)
- **site**: forecast.weather.gov
- **what it tests**: Navigate to the current NYC (Central Park) forecast.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: conditions and high/low match the page.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Using the U.S. National Weather Service site (https://forecast.weather.gov), find the current forecast for New York, NY (Central Park). Report today's forecasted conditions and high/low temperature as shown on the page.
```
