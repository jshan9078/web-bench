# 82-blur-validation

- **kind**: action + form state (programmatic)
- **site**: localhost test site (widgetapp/blurform.py, port 8802)
- **what it tests**: blur-only validation (rules revealed only after leaving a field), a dependent field that appears late, a silent failed submit, and a pre-ticked option that silently overwrites the entered address
- **discrimination hypothesis**: every element is a real checkout pattern; agents that never blur a field never learn the postal format, agents that submit once and stop never notice the silent failure, and agents that leave the pre-ticked option save the wrong address while seeing a success reference.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: a recorded submission with no validation errors equals the requested address exactly.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8802/ and save this SHIPPING address exactly: Mara Lindqvist, 48 Rue Sainte-Anne,
Québec, Canada, province QC, postal code G1R 3X3, phone +1 418 555 0147. The form validates fields only
when you leave them, and any format rule is shown in that message; some fields appear only after a
country is chosen. Make sure the address actually saved (the page shows a reference) and that it is the
address above, not the billing address the form offers. Work through the page's UI only: do NOT read the
page source or call the site's HTTP endpoints directly. End with the reference shown.
```
