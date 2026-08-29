# 46-gmaps-save-place

- **kind**: signed-in action (LLM-judge)
- **site**: google.com/maps
- **what it tests**: place search, a private save action on the user's account, list verification
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the Want to go screenshot shows the place saved this run, with matching live rating/review figures.
- **requires**: signed-in browser profile

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
You are running on a browser profile where the user is already signed in to Google. If a login
page appears anyway, show the window and ask the user to sign in, then continue. On Google Maps
(https://www.google.com/maps), search for the CN Tower, Toronto. From its place card, report the
current star rating and number of reviews, then use the Save control to add it to the WANT TO GO
list. Open your saved places (Saved, then Want to go) and take a screenshot showing the CN Tower
in the list. Do not modify any other saved places or lists. End with the rating, the review
count, and confirmation it appears in Want to go.
```
