# 335-chat-stream

- **kind**: counting over video (programmatic)
- **site**: localhost widget (widgetapp/chatstream.py, port 8969)
- **what it tests**: reading a fast chat feed and filtering by user and content
- **discrimination hypothesis**: messages scroll off after ~14 arrivals (about 20 s); a similar username is a decoy.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8969/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It is a 2-minute recording of a live 
stream with a chat panel on the right where messages arrive every second or two and scroll away. 
Count exactly how many messages from the user mira (not mira_b) contained a question mark, enter 
the number in the form under the player and submit. Do NOT read the page source or call the site's 
HTTP endpoints directly. End with the count.
```
