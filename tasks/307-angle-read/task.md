# 307-angle-read

- **kind**: angle estimation without a scale (programmatic)
- **site**: localhost widget (widgetapp/angleread.py, port 8947)
- **what it tests**: estimating an angle between two rays within 2 degrees
- **discrimination hypothesis**: fine geometric estimation; no reference marks.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted angle is within 2 degrees.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8947/ . The page shows an IMAGE of two rays from a common vertex (read it 
from screenshots; there is no protractor). Report the angle between the rays in degrees, within 2 
degrees, enter it in the form and submit. Do NOT read the page source or call the site's HTTP 
endpoints directly. End with the angle.
```
