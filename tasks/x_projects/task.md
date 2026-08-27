# x_projects

- **kind**: read (LLM-judge)
- **site**: x.com profile + a linked article
- **what it tests**: Multi-hop: profile, then project links, then read the SLM article.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: projects and links are present and the benchmarked models match the article.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open the X (Twitter) profile at https://x.com/jshan9078. Based on what's shown there (bio, pinned post, posts) and the links it points to, produce: (1) a list of ALL the projects this person has built or worked on, (2) a direct link to each project, and (3) for the on-device SLM vulnerability-detection research project specifically, which models were benchmarked — you will likely need to open that project's article/blog link and read it. Base your answer only on what you actually read on the pages. End with the project list (name + link each) and, for the SLM research, the list of benchmarked models.
```
