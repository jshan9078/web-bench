# 104-receipt-total

- **kind**: photo reading with printed vs handwritten values (programmatic)
- **site**: localhost widget (widgetapp/receipt.py, port 8824)
- **what it tests**: reading a rotated, noisy receipt photo and choosing the handwritten post-tip total over the printed pre-tip total and the printed suggested-tip lines
- **discrimination hypothesis**: agents report the printed TOTAL, or printed total plus a suggested tip, instead of the handwritten total; the handwriting is in a different font and colour.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: a submitted amount within 0.01 of the handwritten total.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8824/ . It is a photo of a restaurant receipt (read it from screenshots). 
Report the amount actually charged INCLUDING the tip that was written on the receipt, enter it in 
the form below the photo and submit. Do NOT read the page source or call the site's HTTP endpoints 
directly. End with the amount.
```
