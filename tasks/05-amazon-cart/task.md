# 05-amazon-cart

- **kind**: action (LLM-judge)
- **site**: amazon.ca
- **what it tests**: Open two product pages and add both to the cart.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: cart screenshot shows both items and the trace shows the adds.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Add BOTH of these Amazon products to the cart, quantity 1 each:
  1. https://www.amazon.ca/dp/0735211299
  2. https://www.amazon.ca/dp/0132350882
For each: open the product page and click 'Add to Cart'. If any upsell pop-up appears (warranty, subscription, audiobook/Kindle, 'protect your purchase'), dismiss it (no thanks / skip). When done, open the cart so both items are visible. Do NOT proceed to checkout or place an order.
```
