# 76-settings-maze

- **kind**: action + navigation (programmatic)
- **site**: localhost test site (widgetapp/settingsmaze.py, port 8798)
- **what it tests**: multi-level navigation on a settings product: top-level tabs, a nested tab strip, an accordion, a custom toggle inside a shadow root inside an iframe, an unsaved-changes modal that interrupts tab switches, a footer Save that is the only way to persist, decoy settings (alerts vs digest, billing email)
- **discrimination hypothesis**: the changes are trivial; reaching them is not. Agents lose edits to the discard modal, never find the toggle (iframe plus shadow DOM defeat naive snapshots), flip the wrong notification setting, or forget to save. The verdict is an exact comparison of the saved state.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: saved settings equal defaults plus exactly the three requested changes.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8798/ , an account-settings app. Make exactly these three changes and save them:
(1) set the display name to "J. Halvorsen"; (2) under Notifications, set the EMAIL DIGEST frequency to
Monthly (leave the immediate email alerts as they are); (3) under Security, turn Two-step verification ON.
Change nothing else (in particular do not touch the billing email). The app has no autosave: use the
"Save changes" button in the footer, and note that switching top-level tabs with unsaved changes asks
whether to discard them. Work through the page's UI only: do NOT read the page source or call the site's
HTTP endpoints directly. End by confirming the three saved values.
```
