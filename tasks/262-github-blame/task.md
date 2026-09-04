# 262-github-blame

- **kind**: real-site code navigation (LLM-judge)
- **site**: github.com/pallets/flask (signed-out)
- **what it tests**: navigating to a file, switching to Blame view, locating a specific line and reading its commit metadata
- **discrimination hypothesis**: blame view needs the right line among hundreds, and the commit metadata sits in the gutter or commit page; the judge verifies via the GitHub GraphQL blame API or git.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: The judge determines via gh api (graphql blame on src/flask/app.py at main, or a local git blame of a fresh clone) the commit that last changed the 'def run(' line, and passes only if the reported short hash, author and date match; screenshots must show the blame view.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open https://github.com/pallets/flask (no sign-in needed). Open the file src/flask/app.py on the 
main branch and use the Blame view to find which commit last changed the line that defines "def 
run(" (the Flask.run method definition line). Report the short commit hash, the commit's author and 
its date as shown in the blame gutter or commit page. Read everything from the pages; do not guess. 
If a consent or sign-in interstitial appears, dismiss it without signing in. End with those three 
items.
```
