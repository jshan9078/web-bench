# 312-hover-menu

- **kind**: hover-only nested menus with decoys (programmatic)
- **site**: localhost widget (widgetapp/hovermenu.py, port 8950)
- **what it tests**: reaching a third-level menu item that only opens on hover
- **discrimination hypothesis**: clicking parents closes menus; a decoy toolbar Export and a sibling CSV item exist.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last activated item is csv-semicolon and no decoy was run.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8950/ . Using the menu bar (its submenus open on hover), run Data > Export > 
Legacy formats > "CSV (semicolon)". Do not run any other command (the toolbar Export button and 
"CSV (comma)" are different commands). Do NOT read the page source or call the site's HTTP 
endpoints directly. End with the confirmation text shown on the page.
```
