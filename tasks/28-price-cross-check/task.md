# 28-price-cross-check

- **kind**: read, cross-site (LLM-judge)
- **site**: amazon.ca + bestbuy.ca
- **what it tests**: same-product price comparison across two retailers
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: both prices match their captured product pages and the difference is computed correctly.
- **requires**: signed-in browser profile

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Find the current price of the Logitech MX Master 3S mouse on BOTH Amazon Canada
(https://www.amazon.ca) and Best Buy Canada (https://www.bestbuy.ca). Make sure both listings are the SAME variant: the standard MX Master 3S in Graphite/Black (not the MX Master 3, not a bundle, not the Bluetooth-only edition, not the Business variant). If Best Buy shows a bot wall, retry or use a fresh session. Report each price, which retailer is cheaper
right now, and the exact difference. End with the two prices and the difference.
```
