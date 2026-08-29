# 22-amazon-earbud-compare

- **kind**: action + cart (LLM-judge)
- **site**: amazon.ca
- **what it tests**: comparing two live product pages on price, rating, and a spec before acting
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the comparison matches the captured product pages and the higher-rated item was added.
- **requires**: signed-in browser profile, amazon cart evidence captured

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On Amazon (https://www.amazon.ca), search for wireless earbuds. Open the FIRST TWO genuine product
results (skip sponsored listings if identifiable). For each, report price, star rating, number of
ratings, and the claimed battery life from the product details. Add the HIGHER-RATED of the two to
the cart, dismissing any upsell pop-up, and open the cart so it is visible. Do NOT proceed to checkout, sign up for anything, or place any order. End with
the comparison table and which one you added.
```
