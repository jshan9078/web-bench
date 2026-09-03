# 189-github-release-fix

- **kind**: real-site changelog tracing (LLM-judge)
- **site**: github.com/pallets/flask (signed-out)
- **what it tests**: tracing a fix from an issue to the first release whose changelog lists it, via the Releases page and CHANGES.rst
- **discrimination hypothesis**: the fix appears in a patch release line; reporting the PR's merge date or a later release fails; the judge checks CHANGES.rst and the releases list via the GitHub API.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: The judge checks CHANGES.rst (raw) and the GitHub releases API to confirm the first version whose changelog lists the fix for #4297 (PR #4487), its release date, and the exact line; the run passes only if all three match and screenshots show the release/changelog pages.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open https://github.com/pallets/flask (no sign-in needed). Issue #4297 was fixed by a merged pull 
request. Using the repository's Releases page and the CHANGES.rst changelog, find the FIRST 
released version whose changelog lists that fix, and report the version number, the release's date, 
and the exact changelog line describing the fix. Read everything from the pages you navigate to; do 
not guess. If a consent or sign-in interstitial appears, dismiss it without signing in. End with 
those items.
```
