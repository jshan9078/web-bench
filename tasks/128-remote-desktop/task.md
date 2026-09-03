# 128-remote-desktop

- **kind**: image-only UI operation (programmatic)
- **site**: localhost widget (widgetapp/remotedesktop.py, port 8842)
- **what it tests**: operating a UI that exists only as an image stream (remote desktop): locating an icon by its glyph, opening a window, flipping the right toggle among similarly named ones, and closing the window, with a screenshot after every click
- **discrimination hypothesis**: no DOM exists for any of it; agents that click from stale screenshots, flip 'Night light schedule', or leave the window open fail. The Display icon is the decoy for Settings.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: Night light is on, every other toggle unchanged, and the Settings window closed.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8842/ . It is a browser-based remote desktop session: the whole desktop is an 
IMAGE at the page's top-left that responds to clicks (click with raw coordinates via click --at 
X,Y; screenshot pixels map 1:1; the image refreshes after each click, so take a fresh screenshot to 
see the result). On the remote desktop, open the Settings app, turn ON the "Night light" toggle 
(not "Night light schedule"), leave every other setting as it is, and close the Settings window. Do 
NOT read the page source or call the site's HTTP endpoints directly. End with a one-line 
confirmation.
```
