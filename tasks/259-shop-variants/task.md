# 259-shop-variants

- **kind**: constrained configuration search on a product page (programmatic)
- **site**: localhost widget (widgetapp/shopvariants.py, port 8919)
- **what it tests**: exploring option combinations for stock and price, applying constraints, quantity and promo code
- **discrimination hypothesis**: stock is only visible per full combination; the cheapest overall is excluded by constraints; the promo must be applied.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: one cart line: the cheapest qualifying in-stock configuration, quantity 2, promo HARBOR10.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8919/ . It is a product page with size, colour and storage options; prices 
differ by configuration and some configurations are out of stock (shown struck through once the 
other options are picked). Add to the cart, with quantity 2 and promo code HARBOR10, the CHEAPEST 
in-stock configuration that is size M or L, NOT red, and has at least 128 GB of storage. Do NOT 
read the page source or call the site's HTTP endpoints directly. End with the configuration and the 
cart total shown.
```
