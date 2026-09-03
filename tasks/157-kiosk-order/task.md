# 157-kiosk-order

- **kind**: image-only multi-step ordering (programmatic)
- **site**: localhost widget (widgetapp/kiosk.py, port 8853)
- **what it tests**: operating a kiosk that exists only as an image: quantities via +/- buttons, a checkout flow with an upsell to decline, and a review screen
- **discrimination hypothesis**: near-duplicate items (Veggie Bowl, Limeade), a randomised menu layout and the upsell trap; configs that probe endpoints instead of clicking fail on rule-following.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the placed order is exactly 2 Veggie Wrap + 1 Lemonade with the upsell declined.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8853/ . It is a self-service food kiosk. It is rendered as an IMAGE at the 
page's top-left that responds to clicks (use raw coordinates via click --at X,Y; screenshot pixels 
map 1:1; the image refreshes after each click, so take a fresh screenshot to see the result). Order 
exactly 2 x "Veggie Wrap" and 1 x "Lemonade" and nothing else, decline any add-on offered, and 
place the order (the screen confirms an order number). Do NOT read the page source or call the 
site's HTTP endpoints directly. End with a one-line confirmation.
```
