# 365-sorter-errors

- **kind**: rule-conditioned event counting (programmatic)
- **site**: localhost widget (widgetapp/sorterrors.py, port 8992)
- **what it tests**: checking each of ~30 routing events against a colour rule
- **discrimination hypothesis**: each event lasts 1.5 s; errors are 20%; both colours and sides matter.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8992/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It shows a colour sorter for 90 
seconds: items drop onto a belt and are diverted left or right; blue items should go LEFT and all 
other colours RIGHT, but the sorter sometimes misroutes. Count exactly how many items went to the 
WRONG side, enter the number in the form under the player and submit. Do NOT read the page source 
or call the site's HTTP endpoints directly. End with the count.
```
