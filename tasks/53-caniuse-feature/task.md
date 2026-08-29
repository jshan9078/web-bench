# 53-caniuse-feature

- **kind**: read (LLM-judge)
- **site**: caniuse.com
- **what it tests**: reading live support tables and usage statistics
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the usage percentage and support facts match the captured table.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On Can I Use (https://caniuse.com), look up the CSS :has() selector. Report the CURRENT global
support percentage shown, and, from the support table, which of the major browsers (Chrome,
Firefox, Safari, Edge) was the LAST to ship full support, with the version number that first
supported it. Take a screenshot of the table. End with the global percentage and the last-to-ship
browser and version.
```
