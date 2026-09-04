# 263-multi-page-checkout

- **kind**: multi-page checkout with validation and a date rule (programmatic)
- **site**: localhost widget (widgetapp/checkoutflow.py, port 8921)
- **what it tests**: adjusting quantities, passing address validation, choosing a shipping method from a business-day rule, and passing card validation
- **discrimination hypothesis**: the date rule makes Express the cheapest qualifying method (Standard arrives too late); the postcode and card validators reject sloppy input; the cap must be set to zero.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the order has mug 3, tee 1, cap 0, Express shipping, the given address and card.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8921/ . It is a store checkout. Set the cart to 3 Harbor mugs, 1 Harbor tee 
and no cap. Deliver to Ana Silva, 22 Quay Rd Unit 3, postcode M5S 2C6. Choose the CHEAPEST shipping 
method that will arrive by Friday 11 September 2026 (the page states today's date and the estimates 
in business days). Pay with the test card 4242 4242 4242 4242, expiry 12/28, CVC 123, and place the 
order (the page shows an order reference). Do NOT read the page source or call the site's HTTP 
endpoints directly. End with the shipping method and the order reference.
```
