# 66-wiki-table-reconcile

- **kind**: action + read + reconciliation (LLM-judge)
- **site**: en.wikipedia.org
- **what it tests**: sorting a wikitable through its column control (state not encoded in the URL), reading the sorted order, opening three articles, comparing infobox values against the list
- **discrimination hypothesis**: three sources of error compound: the wrong table, an unsorted or wrongly-sorted table, and a comparison that needs reading two numbers per building. Agents that assume the table's default order or skip the infobox check fail.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the three buildings are the top of the captured table sorted by year descending, and each article's architect, floor count, and height comparison match the captured pages.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open https://en.wikipedia.org/wiki/List_of_tallest_buildings . In the main ranked table of the world's
tallest buildings, sort by the year-completed column in DESCENDING order using the column's sort control
(URL parameters do not sort this table; click the header and confirm the order changed on the page). Take
the THREE most recently completed buildings shown after sorting. For each, open its own Wikipedia article
and report from its infobox: the architect (or architecture firm), the floor count, and the height in
metres; then state whether that height agrees with the height shown in the list (within 1 m). Report the
sorted top three as displayed plus the three comparisons. End with those items.
```
