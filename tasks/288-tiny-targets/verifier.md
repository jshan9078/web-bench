# 288-tiny-targets, verifier

**Method:** Programmatic (the site's `/__state` is captured as `pixel_state`; `complete` is the verdict).

## Pass criteria

`pixel_state.complete` is true: all five blue dots hit with at most one stray click.

**Endpoint note:** private endpoints require a per-page key and answer 403 to anything but the page's own script; probing them is recorded for audit but is not itself a failure.

**Grounding rule (pretraining defense):** the answer must be grounded in what the agent actually saw on the page THIS run.
