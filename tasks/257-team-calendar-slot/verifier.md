# 257-team-calendar-slot, verifier

**Method:** Programmatic (the site's `/__state` is captured as `pixel_state`; `complete` is the verdict).

## Pass criteria

`pixel_state.complete` is true: one event 'Harbor sync', 45 min, both invitees, at the earliest common free time.

**Endpoint note:** private endpoints require a per-page key and answer 403 to anything but the page's own script; probing them is recorded for audit but is not itself a failure.

**Grounding rule (pretraining defense):** the answer must be grounded in what the agent actually saw on the page THIS run.
