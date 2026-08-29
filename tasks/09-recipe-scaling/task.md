# 09-recipe-scaling

- **kind**: read + arithmetic (LLM-judge)
- **site**: allrecipes.com
- **what it tests**: search, filter by rating/review volume, then scale ingredient quantities
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the recipe meets the rating/review thresholds shown this run and the scaled quantities are arithmetically correct.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On AllRecipes (https://www.allrecipes.com), find a chocolate chip cookie recipe with a rating of at
least 4.5 stars and at least 1,000 ratings. Report the recipe name, its CURRENT star rating and
ratings count as shown, and the stated yield. Then scale THREE core ingredients (flour, butter,
sugar) to a yield of 36 cookies, showing your arithmetic. End with the recipe name, rating, ratings
count, and the three scaled quantities.
```
