# 210-tray-racks

- **kind**: outcome attribution over video (programmatic)
- **site**: localhost widget (widgetapp/trayracks.py, port 8877)
- **what it tests**: attributing each of 20-28 tray returns to the left or right rack
- **discrimination hypothesis**: the destination is decided by the walk direction over five seconds; the racks' visible stacks offer a check that must be read correctly; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of trays on the left rack.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8877/ . It is a 2-minute cafeteria camera clip in a player (canvas video with 
play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). Diners 
carry their trays from the bottom of the frame to either the LEFT rack or the RIGHT rack. Count 
exactly how many trays were placed on the LEFT rack during the clip, enter the number in the form 
under the player and submit. Do NOT read the page source or call the site's HTTP endpoints 
directly. End with the count.
```
