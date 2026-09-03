# 172-nested-modal-terms

- **kind**: stacked modals and in-element scrolling (programmatic)
- **site**: localhost widget (widgetapp/termsmodal.py, port 8860)
- **what it tests**: scrolling a container inside a modal (not the page) to enable a button, then completing a further dialog with a checkbox
- **discrimination hypothesis**: the Accept button is disabled until the inner box reaches its end; page-level scrolling does nothing; agents that click a disabled button or skip the checkbox fail.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the order is confirmed with the terms box scrolled to the end and the checkbox ticked.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8860/ . It is a checkout page. Place the order: this opens a confirmation 
dialog, whose Review terms button opens the terms dialog; the Accept button only enables once the 
terms box inside that dialog has been scrolled to its end. After accepting, a final dialog needs 
its checkbox ticked before Confirm. Complete the flow until the page shows an order reference. Do 
NOT read the page source or call the site's HTTP endpoints directly. End with the reference.
```
