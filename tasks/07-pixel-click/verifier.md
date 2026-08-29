# 07-pixel-click, verifier

**Method:** programmatic state check (no LLM).

The `pixel_click` canvas app renders numbered circles as an **image** (not in the DOM), and its server hit-tests every `browser <sid> click --at X,Y` against the true circle positions, recording the click order. The harness captures the server's click log as `pixel_state`.

**PASS** iff the server reports every circle was clicked in **ascending numeric order** (`pixel_state.complete == true`). This is fully objective, so there is no judge and no re-scoring step.
