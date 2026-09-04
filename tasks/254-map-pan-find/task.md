# 254-map-pan-find

- **kind**: canvas map exploration (programmatic)
- **site**: localhost widget (widgetapp/mapapp.py, port 8915)
- **what it tests**: panning and zooming a canvas map with keys or buttons to locate a named place and read its street and cross street
- **discrimination hypothesis**: labels appear only at higher zoom where the view covers a fraction of the map, so a systematic sweep is needed; misreading the rotated avenue label or the east-west street fails.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submission names the place's street and cross street.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8915/ . It is a web map drawn on a canvas (read it from screenshots): pan 
with the arrow buttons or arrow keys after clicking the map, zoom with the +/- buttons; street 
names show from zoom 2 and place names from zoom 3. The form under the map names a place to find. 
Explore the map until you find it, then enter the street it is on (an east-west street such as King 
St) and the cross street at its corner (an avenue such as 3rd Ave) in the form and submit. Do NOT 
read the page source or call the site's HTTP endpoints directly. End with the two street names.
```
