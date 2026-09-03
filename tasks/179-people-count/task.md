# 179-people-count

- **kind**: exact counting over video with overlaps (programmatic)
- **site**: localhost widget (widgetapp/peoplecount.py, port 8863)
- **what it tests**: counting 16-24 people crossing a corridor over two minutes, several within a second of each other, excluding a cart
- **discrimination hypothesis**: near-simultaneous crossings and a decoy object make sampled frames unreliable; exactness is required; the earlier vehicle count (10) already beat one config once.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of people.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8863/ . It is a 2-minute lobby camera clip in a player (canvas video with 
play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). Count 
exactly how many PEOPLE cross the corridor during the whole clip (several cross close together; a 
cleaning cart also passes and does not count). Enter the number in the form under the player and 
submit. Do NOT read the page source or call the site's HTTP endpoints directly. End with the count.
```
