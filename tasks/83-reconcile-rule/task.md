# 83-reconcile-rule

- **kind**: read + reasoning + action (programmatic)
- **site**: localhost test site (widgetapp/reconcile.py, port 8803)
- **what it tests**: reading a site's own precedence rule, comparing two timestamps (list snapshot versus detail update), and acting on the correct page only
- **discrimination hypothesis**: a realistic data-consistency situation with a stated rule; agents that trust the detail page by default, or the list by default, are right only half the time, and the verify button exists on both pages so the action itself encodes the decision.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: exactly one verify click, on the page the policy makes authoritative for the target part.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8803/ , a parts catalogue. The inventory list and a part's detail page can show
different stock counts; the site's Data policy page states which one is authoritative and when. For the
part "{NAME}", determine the authoritative stock count according to that policy (compare the times the
policy refers to) and press "Mark verified" on the authoritative page for that part, and only there.
Report the count and which page you verified on. Work through the page's UI only: do NOT read the page
source or call the site's HTTP endpoints directly. End with the count and the page.
```
