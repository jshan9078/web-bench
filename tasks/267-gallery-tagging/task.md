# 267-gallery-tagging

- **kind**: visual classification across a gallery with a lightbox (programmatic)
- **site**: localhost widget (widgetapp/phototag.py, port 8924)
- **what it tests**: opening photos, telling red cars from red trucks and blue cars at thumbnail or full size, tagging exactly the right set, and saving
- **discrimination hypothesis**: thumbnails are small and the decoys share colour or shape; missing one photo or tagging a decoy fails.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the saved 'red car' tag set equals the photos containing a red car.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8924/ . It is a photo library of 24 thumbnails with a viewer (open a photo to 
see it large, add or remove tags, move with Prev/Next). Add the tag "red car" to every photo that 
shows a red CAR (not a red truck, not a blue car) and to no other photo, then click Save tags. Do 
NOT read the page source or call the site's HTTP endpoints directly. End with the photo numbers you 
tagged.
```
