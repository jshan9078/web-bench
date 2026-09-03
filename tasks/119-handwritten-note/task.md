# 119-handwritten-note

- **kind**: handwriting reading (programmatic)
- **site**: localhost widget (widgetapp/stickynote.py, port 8837)
- **what it tests**: reading a handwritten phone number from a rotated sticky note and not the printed number on the card beside it
- **discrimination hypothesis**: handwritten digits (1/7, 3/8, 4/9) are misread more often than print; the printed decoy number is the easy wrong answer.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted digits equal the handwritten number.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8837/ . It is a photo of a desk with a handwritten sticky note and a printed 
card (read it from screenshots). Report the phone number written on the HANDWRITTEN note (digits 
only), enter it in the form below the photo and submit. Do NOT read the page source or call the 
site's HTTP endpoints directly. End with the number.
```
