# 72-amazon-quantity-edit

- **kind**: action (LLM-judge, cart ground truth)
- **site**: amazon.ca (signed-in profile)
- **what it tests**: adding an item with a specific quantity, then editing the quantity in the cart and removing everything else; verifying the final cart state rather than trusting the confirmation toast
- **discrimination hypothesis**: two-phase cart manipulation with a required correction step: agents that stop after the add-to-cart toast, or change quantity on the product page instead of the cart, end with the wrong quantity. The harness cart screenshot decides.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: cart_after shows exactly one line item, the reported item, at quantity 2, and nothing else.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On Amazon (https://www.amazon.ca), search for "AA batteries" and open the FIRST genuine (non-sponsored)
result. Add it to the cart with QUANTITY 3 (use the quantity selector on the product page or set it in the
cart). Then open the cart and CHANGE that item's quantity to 2. Make sure the cart contains ONLY this item
at quantity 2 (remove anything else that is there). Leave the cart page open. Report the item title, its
unit price, and the cart subtotal shown after the change. Do NOT proceed to checkout, sign up for anything,
or place any order. End with those three values.
```
