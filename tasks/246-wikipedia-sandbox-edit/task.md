# 246-wikipedia-sandbox-edit

- **kind**: real-site editing and verification (LLM-judge)
- **site**: en.wikipedia.org (signed-out edit of the Sandbox)
- **what it tests**: making an anonymous edit through Wikipedia's editor (visual or source), publishing with a summary, and verifying in the page history
- **discrimination hypothesis**: the editor UI, the publish dialog with summary, and the history check are three distinct real-site interactions; the judge verifies via the MediaWiki API that a revision with the exact text and summary exists at the reported time.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: The judge queries the sandbox's revisions (action=query&prop=revisions&titles=Wikipedia:Sandbox&rvprop=timestamp|comment|user&rvlimit=50 and rvprop=content for the candidate) and passes the run only if a revision within the run's time window has the summary 'webbench test line' and the content ends with the exact line 'webbench check: harbor 4471', and the run reported that revision's timestamp from the history page. A CAPTCHA/protection report is a pass only if the captured page shows it.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open English Wikipedia's sandbox page (https://en.wikipedia.org/wiki/Wikipedia:Sandbox) and edit it 
(no account needed; use the source editor if the visual editor does not load). Add a new line at 
the END of the page with exactly this text: "webbench check: harbor 4471" and publish the edit with 
the edit summary "webbench test line". Then open the page's View history and confirm your edit 
appears as the latest revision. Do not remove or change anything else on the page. If an edit is 
blocked by a CAPTCHA or a protection notice, say exactly what appeared instead of working around 
it. End with the revision timestamp shown in the history.
```
