# 59-spot-difference

- **kind**: vision (programmatic)
- **site**: localhost widget (widgetapp/spotdiff.py, port 8793)
- **what it tests**: careful visual comparison of two panels, precise clicking, distinguishing four kinds of change (recolored, removed, moved, added shape)
- **discrimination hypothesis**: pure perception with no DOM fallback: a model must actually compare the two renders. Weak-vision tiers guess and burn their miss budget; strong-vision tiers find all four in a handful of clicks.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: all four difference regions clicked on the right panel with at most three misses.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8793/ . The page is a single image with two panels side by side: the LEFT panel is
the original and the RIGHT panel differs from it in exactly FOUR places (a shape that changed color, a
shape that is missing, a shape that moved, and a shape that was added). Nothing is in the DOM; take a
`screenshot` to see the panels. Click each of the four differences ON THE RIGHT PANEL, at the location
where the right panel differs (for a moved shape, click its NEW position on the right; for a missing
shape, click where it should have been on the right), using `browser <sid> click --at X,Y`. You have a
budget of three wrong clicks, so compare carefully before clicking. Finish once all four differences are
clicked. Do NOT read the page source or call the site's HTTP endpoints directly; interact visually.
```
