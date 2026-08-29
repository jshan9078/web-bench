# 41-owid-dataset-read

- **kind**: read (LLM-judge)
- **site**: ourworldindata.org
- **what it tests**: interactive chart manipulation and reading the latest datapoint from the tool
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the latest-year value for Japan matches the chart/table captured this run.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On Our World in Data (https://ourworldindata.org), open the Life Expectancy page and its
interactive chart. Restrict or highlight the series for Japan. Using the chart's own display (the
line endpoint, tooltip, or the Table tab), report the MOST RECENT year available in the dataset
for Japan and the life-expectancy value for that year, exactly as the tool shows. Take a
screenshot of the chart or table showing the value. End with the year and the value.
```
