# 23-amazon-filter-hunt

- **kind**: action + cart (LLM-judge)
- **site**: amazon.ca
- **what it tests**: compound filtering and sorting in a category, then acting on the result
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the item satisfies every filter as captured and was added to the cart this run.
- **requires**: signed-in browser profile, amazon cart evidence captured

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On Amazon (https://www.amazon.ca), browse Books, then narrow to Science Fiction. Apply the
paperback format and 4 stars & up filters (there is no price filter; check prices yourself), and
sort by publication date. Open the FIRST result that is already published and priced under $25
(skip pre-orders), report its title, author, price, and publication date, and add it to the cart. Dismiss any upsell
pop-up and open the cart so it is visible. Do NOT proceed to checkout, sign up for anything, or place any order. End with title, author, price, publication
date, and confirmation it is in the cart.
```
