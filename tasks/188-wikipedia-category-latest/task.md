# 188-wikipedia-category-latest

- **kind**: real-site tool navigation (LLM-judge)
- **site**: en.wikipedia.org (signed-out)
- **what it tests**: finding the most recently edited article in a category using MediaWiki's history or Related changes tools and reading the revision's timestamp and editor
- **discrimination hypothesis**: requires either visiting each article's history or knowing the Related changes tool; the judge verifies against the MediaWiki API (categorymembers + revisions), so a wrong article or misread timestamp fails.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: The judge verifies via the MediaWiki API (list=categorymembers for the category, then the latest revision timestamp and user of each member article) that the reported article is the most recently edited member and that the timestamp and username match; captured pages must show the history or Related changes view used.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open English Wikipedia (https://en.wikipedia.org) and go to the category page "Category:Public 
libraries in Toronto". Among the ARTICLES directly in that category (not subcategories), find the 
one whose most recent edit is the latest in time. Report the article title, the date and time (UTC) 
of that edit, and the editor's username, as shown on that article's history page. Use the site's 
own tools (each article's View history, or the Related changes tool on the category page) and read 
everything from the pages; do not guess. End with those three items.
```
