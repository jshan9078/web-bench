# 81-memory-flow

- **kind**: action + memory (programmatic)
- **site**: localhost test site (widgetapp/memoryflow.py, port 8801)
- **what it tests**: carrying one fact (a code shown once) across an unrelated multi-step flow with no way back, and re-reading correctly if the flow is restarted (a restart issues a new code)
- **discrimination hypothesis**: a realistic pairing flow: agents that do not note the code guess, enter the decoy serial, or restart and then enter the earlier code. Nothing is long; the failure is forgetting or mixing up two codes.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the final submission carries the code current for that flow instance and the room chosen in it (which must be the room the page named).

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8801/ and complete the five-step device pairing. Step 1 shows the device's pairing
code; there is no way back to it, and reloading the page starts over with a different code. Step 2 asks
which room the device is in (the page tells you where it is installed); steps 3 and 4 are options and a
notice. Step 5 asks for the pairing code from step 1 and the room you chose in step 2. Finish the pairing
so the page shows a reference. Work through the page's UI only: do NOT read the page source or call the
site's HTTP endpoints directly. End with the reference and the code you entered.
```
