# 125-custom-slider

- **kind**: custom control manipulation (programmatic)
- **site**: localhost widget (widgetapp/rangeslider.py, port 8841)
- **what it tests**: setting a two-handle div slider (no input element) to given bounds by clicking positions on the track and reading the live values back
- **discrimination hypothesis**: each click moves the nearest handle, so a poor first click for the maximum can drag the minimum instead; reaching both bounds within 5 needs iteration against the displayed values.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the applied range matches the stated bounds within 5 dollars each.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8841/ . It is a shop's price filter with a custom two-handle slider (no input 
field; clicking on the track moves the nearest handle and the Min/Max values update). Set the range 
to the bounds stated on the page, each within 5 dollars, then click Apply filter. Do NOT read the 
page source or call the site's HTTP endpoints directly. End with the applied range.
```
