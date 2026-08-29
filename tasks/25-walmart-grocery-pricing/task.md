# 25-walmart-grocery-pricing

- **kind**: action + cart (LLM-judge)
- **site**: walmart.ca
- **what it tests**: multi-item price research with one cart action and a screenshot
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: each price matches a captured product page, the total is correct, and the eggs are in the cart.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On Walmart Canada (https://www.walmart.ca), price out this grocery list by finding a sensible
cheapest option for each: 2L milk, a dozen eggs, a loaf of sandwich bread, and 1kg of bananas.
Report each chosen product and price, and the four-item total. If Walmart shows a robot check (press-and-hold), show the window and ask the user to clear it, or retry in a fresh session. Then add ONLY the eggs to the cart
and take a screenshot of the cart showing them. Do NOT proceed to checkout, sign up for anything, or place any order. End with the four items, prices,
total, and confirmation the eggs are in the cart.
```
