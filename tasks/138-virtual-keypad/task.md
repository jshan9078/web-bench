# 138-virtual-keypad

- **kind**: image keypad entry (programmatic)
- **site**: localhost widget (widgetapp/keypad.py, port 8844)
- **what it tests**: reading a shuffled key layout from a screenshot and entering a six-digit code by pixel clicks, verifying the dot counter, then pressing Enter
- **discrimination hypothesis**: the layout changes per load so keys cannot be memorised; one mis-click enters the wrong digit and only the dot count is visible. Clear-and-retry is available.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the digits entered on the keypad equal the displayed code.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8844/ . It is a bank sign-in page whose access code must be typed on an IMAGE 
keypad at the page's top-left (the key layout is shuffled; read it from a screenshot and click keys 
with raw coordinates via click --at X,Y; screenshot pixels map 1:1). The page shows the 6-digit 
access code as text. Enter that code on the keypad and press the keypad's Enter key. Do NOT read 
the page source or call the site's HTTP endpoints directly. End with a one-line confirmation.
```
