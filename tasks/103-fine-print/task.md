# 103-fine-print

- **kind**: fine-print reading with a zoom tool (programmatic)
- **site**: localhost widget (widgetapp/fineprint.py, port 8823)
- **what it tests**: recognising that native-size text is not reliably legible and using the page's magnifier before reading a code made of confusable glyphs (3/8/6/5, B/8, S/5, Z/2)
- **discrimination hypothesis**: agents that read the tiny print from an unzoomed screenshot misread one or two glyphs and submit confidently; a LOT number and a part number in similar formats sit on the adjacent lines.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted serial equals the printed one (case-insensitive, hyphens optional).

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8823/ . It is a product-listing photo of a device label. Report the serial 
number printed after "S/N" on the label. The text is small; the page has a magnifier (click the 
photo to zoom into that area). Do NOT read the page source or call the site's HTTP endpoints 
directly. End with the serial number.
```
