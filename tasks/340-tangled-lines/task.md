# 340-tangled-lines

- **kind**: exact visual counting or tracing (programmatic)
- **site**: localhost widget (widgetapp/tangledlines.py, port 8974)
- **what it tests**: following one curve through many crossings
- **discrimination hypothesis**: line trace failed Sonnet 5 low twice; eight lines with three control points each.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8974/ . The page shows an IMAGE (read it from screenshots). Eight black lines 
run from letters A to H on the left to numbers 1 to 8 on the right, crossing many times. Answer the 
question under the image (which number the line from the named letter ends at), enter it in the 
form and submit. Do NOT read the page source or call the site's HTTP endpoints directly. End with 
the number.
```
