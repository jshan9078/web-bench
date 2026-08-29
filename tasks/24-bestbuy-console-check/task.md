# 24-bestbuy-console-check

- **kind**: read (LLM-judge)
- **site**: bestbuy.ca
- **what it tests**: retail search, product-page reading, availability interpretation
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: name, price, rating, and availability match the captured product page.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On Best Buy Canada (https://www.bestbuy.ca), find the current standard PlayStation 5 console
listing (disc edition if both exist). Report the exact product name, current price, star rating
and number of reviews, and whether it is shown as available for online purchase right now. Best Buy sometimes shows an access-denied bot wall; if that happens, retry the navigation or start a fresh session and continue. End with those four facts.
```
