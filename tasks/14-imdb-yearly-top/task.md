# 14-imdb-yearly-top

- **kind**: read (LLM-judge)
- **site**: imdb.com
- **what it tests**: advanced search with multiple constraints, then a person-page pivot
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the film satisfies the constraints on the captured search results and the director filmography facts match.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On IMDb, use Advanced Title Search to find the highest-rated feature film RELEASED THIS CALENDAR
YEAR with at least 25,000 ratings. Report its title, current IMDb rating, and current number of
ratings. Then open the director's page and name two OTHER titles from their filmography. End with
the film, rating, ratings count, director, and the two other titles.
```
