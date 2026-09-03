# 156-thermometer-read

- **kind**: column reading against fine ticks (programmatic)
- **site**: localhost widget (widgetapp/thermo.py, port 8852)
- **what it tests**: reading a liquid column against 1-degree ticks to within half a tick, with a printed set point as decoy
- **discrimination hypothesis**: half-tick precision on a dense scale; reporting the set point or the nearest whole degree fails when the true value is x.3 or x.7.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted temperature is within 0.5 degrees of the column.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8852/ . It is a lab check photo of an analog thermometer next to a set-point 
label (read it from screenshots). Report the temperature the thermometer's column shows, in degrees 
C within 0.5 (ticks are every 1 degree), enter it in the form below the photo and submit. Do NOT 
read the page source or call the site's HTTP endpoints directly. End with the temperature.
```
