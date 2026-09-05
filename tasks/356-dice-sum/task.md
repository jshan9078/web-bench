# 356-dice-sum

- **kind**: exact pip counting on rotated dice (programmatic)
- **site**: localhost widget (widgetapp/dicesum.py, port 8987)
- **what it tests**: reading 36 rotated dice faces and summing
- **discrimination hypothesis**: small pips on rotated coloured dice; one misread face breaks the sum.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8987/ . The page shows an IMAGE (read it from screenshots). It shows 36 dice 
at random angles. Report the total number of pips showing on all dice, enter it in the form and 
submit. Do NOT read the page source or call the site's HTTP endpoints directly. End with the total.
```
