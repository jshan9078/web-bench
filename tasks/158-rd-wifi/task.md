# 158-rd-wifi

- **kind**: image-only tray navigation (programmatic)
- **site**: localhost widget (widgetapp/wifitray.py, port 8854)
- **what it tests**: expanding and connecting to one of several similarly named networks in an image-only system tray
- **discrimination hypothesis**: three near-duplicate SSIDs and a two-step expand-then-connect interaction; verifying the connected state needs a fresh screenshot.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the connected network is Northwind-Guest-5G.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8854/ . It is a remote desktop session showing the Wi-Fi tray popup. It is 
rendered as an IMAGE at the page's top-left that responds to clicks (use raw coordinates via click 
--at X,Y; screenshot pixels map 1:1; the image refreshes after each click, so take a fresh 
screenshot to see the result). Connect to the network named exactly "Northwind-Guest-5G" (click the 
network to expand it, then Connect) and confirm it shows as connected. Do not change any other 
setting. Do NOT read the page source or call the site's HTTP endpoints directly. End with a 
one-line confirmation.
```
