# 177-hover-megamenu

- **kind**: hover-only navigation (programmatic)
- **site**: localhost widget (widgetapp/megamenu.py, port 8861)
- **what it tests**: reaching a third-level category through a hover mega menu whose submenus exist only while hovered, then acting on the right product
- **discrimination hypothesis**: no links are present until hovered, so the agent must use hover (or reason about the structure) to open two levels; a decoy 'Orbit Mini' and 'Orbit Basic' sit nearby.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the wishlist contains exactly Orbit Plus and the Turntables page was visited.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8861/ . It is a retailer site whose only navigation is a hover mega menu 
(submenus appear when you hover a department, then a category; nothing is listed until hovered; 
site search is unavailable). Navigate to the Turntables category page and add the product "Orbit 
Plus" (and nothing else) to the wishlist. Do NOT read the page source or call the site's HTTP 
endpoints directly. End with a one-line confirmation.
```
