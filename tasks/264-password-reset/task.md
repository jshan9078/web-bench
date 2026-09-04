# 264-password-reset

- **kind**: cross-page reset flow (programmatic)
- **site**: localhost widget (widgetapp/pwreset.py, port 8922)
- **what it tests**: requesting a code, finding the newest code on a separate inbox page among decoys, meeting password rules, and signing in
- **discrimination hypothesis**: an older expired code sits in the inbox; the password rules reject short values; the flow spans two pages.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the account is signed in with the new password.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8922/ . It is a portal sign-in page. The account ana.silva has forgotten its 
password: use Forgot password to request a reset code, read the NEW code from the inbox page linked 
on the site (older codes there have expired), set the new password to exactly Harbor-2026-secure! 
and then sign in as ana.silva with it (the page confirms the sign-in). Do NOT read the page source 
or call the site's HTTP endpoints directly. End with a one-line confirmation.
```
