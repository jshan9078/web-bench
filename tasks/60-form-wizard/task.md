# 60-form-wizard

- **kind**: action + vision + timing (programmatic)
- **site**: localhost widget (widgetapp/wizard.py, port 8794)
- **what it tests**: multi-step form state, reading a decision table that exists only as an image, waiting out a disabled control behind a spinner, handling a confirmation modal with a checkbox
- **discrimination hypothesis**: every element is a real-site pattern (image-only pricing, delayed enablement, modal confirm). Agents that click the disabled button and give up, pick the cheapest option without checking the arrival day, or 'place order' without ticking the box all fail objectively.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted order has the exact name and email, the cheapest option that arrives by Thursday, and confirmed=true, submitted after the spinner completed.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8794/ and complete the four-step checkout wizard for this customer: full name
"Priya Raman", email "priya.raman@example.org". In step 2 the shipping options (price and arrival day)
are shown ONLY as an image; screenshot it, and choose the CHEAPEST option that arrives BY THURSDAY (Thursday
or earlier). Note that the cheapest option overall may arrive too late. Step 3 shows a spinner for several
seconds before Continue becomes enabled; wait for it rather than giving up. When the confirmation dialog
appears, tick the confirmation checkbox and place the order. Finish when step 4 shows an order reference,
and report that reference plus the option letter you chose. Do NOT read the page source or call the site's
HTTP endpoints directly.
```
