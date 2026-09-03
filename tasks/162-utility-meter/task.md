# 162-utility-meter

- **kind**: dial reading with alternating direction (programmatic)
- **site**: localhost widget (widgetapp/utilitymeter.py, port 8858)
- **what it tests**: reading four pointer dials that alternate direction, taking the passed digit for each
- **discrimination hypothesis**: the classic meter-reading error: reading the nearest digit or ignoring the reversed dials gives a wrong reading; the answer is exact.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted 4-digit reading equals the meter's.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8858/ . It is a photo of an electricity meter with four pointer dials (read 
it from screenshots). Read the meter: for each dial take the digit the pointer has already passed 
(adjacent dials run in opposite directions, as printed), giving a 4-digit reading left to right. 
Enter it in the form below the photo and submit. Do NOT read the page source or call the site's 
HTTP endpoints directly. End with the reading.
```
