# 260-survey-builder

- **kind**: structured editing in a builder UI (programmatic)
- **site**: localhost widget (widgetapp/formbuilder.py, port 8920)
- **what it tests**: adding typed questions, editing labels and options, toggling required flags and ordering with buttons
- **discrimination hypothesis**: four questions with exact labels, options and flags; an extra empty option or wrong order fails.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the published schema equals the specified survey.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8920/ . It is a form builder (add questions, edit labels and options, tick 
Required, reorder with Up/Down). Build exactly this survey in this order and publish it: (1) Short 
text "Full name", required; (2) Multiple choice "Which office?" with options Harbor, Northport, 
Remote (exactly three), required; (3) Rating "Rate the onboarding", not required; (4) Short text 
"Anything else?", not required. Do NOT read the page source or call the site's HTTP endpoints 
directly. End with a one-line confirmation.
```
