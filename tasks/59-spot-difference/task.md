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
the original and the RIGHT panel differs from it in exactly FIVE places, the way a design review does: a
shape whose colour shifted slightly, a shape that is missing, a shape moved by a few pixels, a shape that
is slightly smaller, and a small shape that was added. Nothing is in the DOM; take a `screenshot` to see
the panels. Click each of the five differences ON THE RIGHT PANEL where the right panel differs (for the
moved shape either its old or new spot counts; for the missing shape, where it should have been), using
`browser <sid> click --at X,Y`. You have a budget of two wrong clicks, so compare carefully before
clicking. Finish once all five are clicked. Do NOT read the page source or call the site's HTTP endpoints
directly; interact visually.
```
