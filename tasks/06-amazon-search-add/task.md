# 06-amazon-search-add

- **kind**: action (LLM-judge)
- **site**: amazon.ca
- **what it tests**: Search, open the first genuine result, add to cart.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: cart screenshot shows the item and the trace shows search then add.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On Amazon (www.amazon.ca), use the search box to search for `stainless steel water bottle`. Open the first genuine product result, then click 'Add to Cart'. Dismiss any upsell pop-up (no thanks). When done, open the cart so the item is visible. Do NOT proceed to checkout or place an order.
```
