# 344-graph-degree

- **kind**: exact visual counting or tracing (programmatic)
- **site**: localhost widget (widgetapp/graphdegree.py, port 8978)
- **what it tests**: reading edge incidence for every node of a diagram
- **discrimination hypothesis**: requires tracing ~30 edges to their endpoints; crossings confuse.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8978/ . The page shows an IMAGE (read it from screenshots). It shows a 
network diagram with 22 numbered nodes and about 30 edges. Count exactly how many nodes have 
exactly three edges, enter the number in the form and submit. Do NOT read the page source or call 
the site's HTTP endpoints directly. End with the count.
```
