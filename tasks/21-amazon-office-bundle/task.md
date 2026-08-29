# 21-amazon-office-bundle

- **kind**: action + cart (LLM-judge)
- **site**: amazon.ca
- **what it tests**: multi-item constrained shopping, budget arithmetic, cart verification
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: cart screenshot shows both qualifying items and the trace shows both adds this run.
- **requires**: signed-in browser profile, amazon cart evidence captured

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On Amazon (https://www.amazon.ca), build a small home-office bundle under $100 CAD total
(pre-tax): one wireless mouse rated 4 stars or higher, and one desk lamp rated 4 stars or higher.
Open each product page, confirm the rating, and add both to the cart. Dismiss any upsell pop-up
(no thanks / skip). Open the cart so both items are visible. Do NOT proceed to checkout, sign up for anything, or place any order. End with both product
names, their prices and ratings, and the cart subtotal.
```
