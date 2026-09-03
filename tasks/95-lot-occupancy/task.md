# 95-lot-occupancy

- **kind**: video review + state accumulated over time (programmatic)
- **site**: localhost widget (widgetapp/parkinglot.py, port 8815)
- **what it tests**: tracking occupancy through a sequence of arrivals and departures that look identical on the timeline; no single frame answers the question and a departure before the fourth arrival makes 'the fourth arrival' wrong
- **discrimination hypothesis**: agents that count arrivals, or stop at the first frame showing four cars without confirming it is the FIRST such moment, report the wrong time; reading the clock while the fourth car is still rolling in is outside the window. Eight motion marks over four minutes fit comfortably in the budget.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: a submitted HH:MM:SS is within 1 s before to 4 s after the fourth car comes to rest at the first moment occupancy reaches four.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8815/ . It is playback of a 4-minute top-down parking-camera recording 
rendered on a canvas (read frames from screenshots), with a timeline that marks motion events, a 
seek bar, step buttons and a speed control. Cars arrive and leave during the recording. Report the 
camera clock burned into the frame (HH:MM:SS) at the moment the lot FIRST holds exactly four parked 
cars (cars stationary in bays; a car still driving in or out does not count). Enter it in the form 
under the player and submit. Do NOT read the page source or call the site's HTTP endpoints 
directly. End with the time.
```
