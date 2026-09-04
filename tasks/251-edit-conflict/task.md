# 251-edit-conflict

- **kind**: conflict resolution dialog (programmatic)
- **site**: localhost widget (widgetapp/conflictform.py, port 8913)
- **what it tests**: editing a record, then resolving a field-by-field conflict dialog so both parties' changes survive, and saving again
- **discrimination hypothesis**: the dialog defaults to 'theirs' for every differing field, which would discard the user's edits; the user must pick per field.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: final record has the new phone and notes, the colleague's address and tier, and the original name.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8913/ . It is an account editor. Change the phone to +1 555 201 4499 and 
replace the notes with exactly "Net 45. Ask for PO number." then save. Saving will report that a 
colleague changed the record meanwhile and show a conflict dialog: resolve it so that the 
colleague's changes to the other fields are kept AND your phone and notes changes are kept, and 
save again until the page confirms the save. Do NOT read the page source or call the site's HTTP 
endpoints directly. End with the final values of all five fields.
```
