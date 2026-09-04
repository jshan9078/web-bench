# 244-dog-park

- **kind**: object counting per event over video (programmatic)
- **site**: localhost widget (widgetapp/dogpark.py, port 8907)
- **what it tests**: counting dogs (zero to two per person) entering through a gate
- **discrimination hypothesis**: people with two dogs and people without dogs are the traps; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of dogs.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8907/ . It is a 2-minute dog park gate camera clip in a player (canvas video 
with play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). People 
walk through the gate from the left; some have no dog, some have one dog on a lead, and some have 
two. Count exactly how many dogs entered during the clip, enter the number in the form under the 
player and submit. Do NOT read the page source or call the site's HTTP endpoints directly. End with 
the count.
```
