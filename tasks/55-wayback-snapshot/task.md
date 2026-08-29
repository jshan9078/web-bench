# 55-wayback-snapshot

- **kind**: read + vision (LLM-judge)
- **site**: web.archive.org
- **what it tests**: archive navigation to a dated snapshot and precise visual reading of it
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: headline and menu items match the snapshot screenshot from this run.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On the Wayback Machine (https://web.archive.org), find a snapshot of apple.com from mid-June 2010
(use the calendar to pick a capture on or near June 15, 2010). Open the snapshot, dismiss or scroll past any Internet Archive donation banner (it is not part
of the archived page), take a
SCREENSHOT, and report: the main marketing headline text EXACTLY as worded on the page, and any
three items from the site's navigation bar exactly as labeled. End with the snapshot date you
opened, the exact headline, and the three nav items.
```
