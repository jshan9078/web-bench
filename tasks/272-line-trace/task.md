# 272-line-trace

- **kind**: visual line tracing (programmatic)
- **site**: localhost widget (widgetapp/linetrace.py, port 8925)
- **what it tests**: following one of six tangled curves across an image to its endpoint
- **discrimination hypothesis**: line tracing is a documented vision-model weakness; the answer is a single letter, exact.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted letter is cable 3's endpoint.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8925/ . The page shows an IMAGE of six tangled cables running from numbered 
starts on the left to lettered ends on the right (read it from screenshots). Trace cable 3 and 
report which letter it connects to; enter the letter in the form below the image and submit. Do NOT 
read the page source or call the site's HTTP endpoints directly. End with the letter.
```
