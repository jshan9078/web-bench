# 250-crm-merge

- **kind**: search, compare and merge records (programmatic)
- **site**: localhost widget (widgetapp/crmmerge.py, port 8911)
- **what it tests**: finding two records with the same email among 30 (search or sort), comparing dates, and using a merge dialog to keep specific fields
- **discrimination hypothesis**: keeping the newer phone but the older created date requires reading both records; merging the wrong pair or wrong fields fails.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: exactly one record with the duplicate email remains, with the newer phone and older created date, and 30 contacts total.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8911/ . It is a CRM contacts list. One person appears twice with the same 
email address. Find the two duplicate records and merge them into one record that keeps the phone 
number from the more recently created record and the created date from the older record (other 
fields may come from either). Do not change or delete any other contact. Do NOT read the page 
source or call the site's HTTP endpoints directly. End with the merged contact's name, phone and 
created date.
```
