# 72-amazon-quantity-edit, verifier

**Method:** LLM-as-judge (Claude).

Judging is **fully offline** from a captured evidence bundle, so a verdict can be re-derived
without re-running the model. For each run the judge is given the task prompt, the agent's final
answer and result text, the end-state page URL and text excerpt, the full browser command trace,
and the run's screenshots, video, and full model stream.

## Pass criteria

The harness-captured cart_after screenshot and cart_evidence text outrank the agent's claims: they must
show exactly one line item, matching the reported title, with quantity 2. Any other item in the cart, a
quantity other than 2, or an empty cart fails. cart_before must be empty (harness-cleared) so the item was
added this run. The reported subtotal must match the captured cart.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually
navigated to and evidence it captured THIS run. A correct-sounding answer with no supporting
navigation or capture in the trace fails, and where the live page disagrees with the answer, the
captured page wins.
