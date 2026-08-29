# 26-ebay-keyboard-hunt

- **kind**: action (LLM-judge)
- **site**: ebay.ca
- **what it tests**: marketplace filtering on price/format/seller quality before acting
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the listing satisfies all constraints as captured and was added to the cart this run.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On eBay Canada (https://www.ebay.ca), find a mechanical keyboard listed as Buy It Now for under
$75 CAD from a seller with at least 98% positive feedback. Report the listing title, item price,
shipping cost to Canada, and the seller's feedback percentage. Add the item to the cart and take a
screenshot of the cart. Do NOT proceed to checkout, sign up for anything, or place any order. End with those four facts and cart confirmation.
```
