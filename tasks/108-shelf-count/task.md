# 108-shelf-count

- **kind**: visual counting (programmatic)
- **site**: localhost widget (widgetapp/shelfcount.py, port 8828)
- **what it tests**: counting several dozen similar objects in a photo, with two colours and partial occlusion, exactly
- **discrimination hypothesis**: vision models lose count past a dozen similar items and double-count or skip partly hidden boxes; a human counts shelf by shelf. Screenshots may be taken freely, so the failure is perception, not tooling.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted count equals the number of blue boxes.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8828/ . It is a warehouse camera photo of three shelves of boxes (read it 
from screenshots; some boxes partly overlap). Count the BLUE boxes exactly, enter the number in the 
form below the photo and submit. Do NOT read the page source or call the site's HTTP endpoints 
directly. End with the count.
```
