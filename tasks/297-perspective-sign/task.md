# 297-perspective-sign

- **kind**: reading perspective-warped text (programmatic)
- **site**: localhost widget (widgetapp/perspectivesign.py, port 8941)
- **what it tests**: reading names and numbers on a sign photographed at a steep angle
- **discrimination hypothesis**: warped, small text; the three rows must be aligned correctly; exact number.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted distance equals the sign's.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8941/ . The page shows a street photo with a road sign seen at a steep angle 
(read it from screenshots). The question under the photo names a destination; report the distance 
in km shown for it on the sign, enter it in the form and submit. Do NOT read the page source or 
call the site's HTTP endpoints directly. End with the distance.
```
