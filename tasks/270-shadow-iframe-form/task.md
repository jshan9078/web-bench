# 270-shadow-iframe-form

- **kind**: nested shadow DOM and iframe form filling (programmatic)
- **site**: localhost widget (widgetapp/shadowform.py, port 8931)
- **what it tests**: locating and filling inputs that sit inside an open shadow root within an iframe within another shadow root, with slotted labels
- **discrimination hypothesis**: snapshots may flatten or miss nested roots; typing into the wrong scope or failing to reach the inner submit fails.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted values equal the four requested values.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8931/ . It is a delivery request page whose form is nested inside a component 
and an embedded frame. Fill the form with: Reference HB-7731, Quantity 14, Contact email 
ana.silva@example.com, Delivery note "leave at reception", and submit it (the form shows 
Submitted). Do NOT read the page source or call the site's HTTP endpoints directly. End with a 
one-line confirmation.
```
