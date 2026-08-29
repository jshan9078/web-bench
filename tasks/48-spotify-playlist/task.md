# 48-spotify-playlist

- **kind**: signed-in action (LLM-judge)
- **site**: open.spotify.com
- **what it tests**: playlist creation, search, and adding a track in a web player
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the playlist screenshot shows the track inside the newly created playlist.
- **requires**: signed-in browser profile

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
You are running on a browser profile where the user is already signed in. If a login page appears anyway, show the window and ask the user to sign in, then continue. On the Spotify web player (https://open.spotify.com), create a NEW playlist named:
webbench mix, and immediately make it private (use the playlist's menu: Remove from profile /
Make private), and CONFIRM the follow-up Make private? dialog; the change only sticks once the
Private Playlist label or confirmation toast appears. Then search for the song Bohemian Rhapsody by Queen and add it to that playlist.
Open the playlist and take a screenshot showing the track listed in it. Do not play, follow, or
modify anything else. End with the playlist name and the exact track title and artist you added.
```
