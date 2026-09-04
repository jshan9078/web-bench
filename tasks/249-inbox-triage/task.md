# 249-inbox-triage

- **kind**: rule-based triage across a thread list (programmatic)
- **site**: localhost widget (widgetapp/inboxtriage.py, port 8910)
- **what it tests**: opening each conversation, reading later replies, and applying archive/label/star/reply actions exactly per rules
- **discrimination hypothesis**: one thread's later reply cancels a request (must not be starred), two automated senders must be archived, two invoices labelled, one reply sent; any extra action fails.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: archived {1,6}, Finance on {3,7}, starred {4} only, one reply 'On it' on thread 2.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8910/ . It is a webmail inbox with eight conversations. Apply these rules to 
the whole inbox: archive newsletters and automated reports; add the label "Finance" to any 
conversation containing an invoice; star any conversation that asks you to do something by a 
specific day AND still needs it (read every message in a thread, a later reply may cancel the 
request); and reply exactly "On it" to the message from your manager Dana asking for a status 
update. Do nothing else. Do NOT read the page source or call the site's HTTP endpoints directly. 
End with a one-line summary of what you did.
```
