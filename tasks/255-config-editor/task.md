# 255-config-editor

- **kind**: code editing under editor automation (programmatic)
- **site**: localhost widget (widgetapp/codeeditor.py, port 8916)
- **what it tests**: making three precise edits in an editor that auto-indents and auto-closes brackets, keeping JSON valid
- **discrimination hypothesis**: auto-closing quotes and brackets duplicate characters for naive typing; the server rejects invalid JSON; a stray change fails.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: saved JSON equals the original with retries 5, tracing true and ap-south-1 appended.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8916/ . It is a web code editor holding a JSON config (it auto-indents on 
Enter and auto-closes brackets and quotes as you type, like an IDE). Make exactly these changes: 
set "retries" to 5, set features.tracing to true, and add "ap-south-1" as the last entry of the 
regions list. Keep the file valid JSON and change nothing else, then Save (the editor reports Saved 
or a JSON error). Do NOT read the page source or call the site's HTTP endpoints directly. End with 
a one-line confirmation.
```
