---
name: browser-cli
description: Use a local browser daemon plus CLI to run authenticated, multi-session browser automation for any coding agent.
license: Complete terms in LICENSE.txt
---

This skill enables an agent to control a local Playwright browser through `browser` and `browser-daemon` commands. Use it for navigation, snapshots, form interactions, extraction and screenshots on authenticated sites, including localhost apps.

## When To Use

- Capturing screenshots for verification during frontend development
- Clicking through flows, filling forms, pressing keys
- Visiting websites or localhost apps and extracting information
- Working on sites that require the user to log in manually

## Decision Guide

**`browser capture <url>` (standalone)**: you only need a screenshot of a public/localhost page, no interaction, no daemon.

**Daemon commands**: anything interactive, authenticated, or multi-step.

## Quick Capture

```bash
browser capture https://example.com              # viewport JPEG -> /tmp/browser_capture_<ts>.jpg
browser capture https://example.com -f -o ./full.jpg
browser capture http://localhost:3000
```

## Setup Checklist

```bash
uv tool install browser-automation-cli && browser install    # one-time; downloads headless Chromium (~196 MB)
# or skip the download and use the installed Chrome/Edge/Brave:  browser engine system
export PATH="$HOME/.local/bin:$PATH"                         # if commands are not found
# the daemon auto-starts on the first command (run `browser daemon &` yourself to manage it; BROWSER_NO_AUTOSTART=1 disables)
browser create                                               # prints session id
```

Install this skill into an agent with `browser install skill` (Claude Code, Codex and OpenCode are auto-detected).

If a site needs login: `browser <id> show` → ask the user to log in in the window → `browser <id> hide`. Never ask for credentials.

## Session Model

- IDs are 8-char hex. By default all sessions share one persistent **profile** (logins are shared, like tabs in one browser, see Profiles below); use `browser profile ephemeral` or a separate named profile when you need isolated cookies.
- Sessions persist across daemon restarts; `delete` forgets a session (not the profile's logins).
- Hidden sessions are frozen/hibernated when idle; sending the next command wakes them.
- Viewport 1280x800 desktop; `navigator.webdriver` hidden.

## Profiles (persistent logins)

- **Default is a persistent profile named `default`.** The first `create` opens a visible window so the user signs in once; every later session reuses that authenticated profile. Do not ask for credentials; the user logs in in the window.
- `browser profile status`, show the active profile and list existing ones.
- `browser profile <name>` / `browser profile new <name>`, switch to / create a named persistent profile (e.g. a second account). Restart the daemon (`browser shutdown`) to apply.
- `browser profile ephemeral`, make throwaway the default for new sessions.
- **Show/hide is seamless:** `browser <id> show` / `hide` flips a persistent profile between a visible window and headless without closing sessions (they stay, tabs reload, login persists).
- **Per session:** `browser create --profile <name>` gives that session its own persistent login; `--profile` differs across sessions run them concurrently and isolated (each its own Chrome), while the same `--profile` shares one login across sessions (separate tabs). `browser create --ephemeral` is a throwaway isolated session.
- **`browser profile delete <name>`, delete a profile when it is no longer needed.** Each profile is a full Chrome profile on disk (~100 MB and growing with cache/history), so remove ones you do not need to reclaim space. This erases that profile's logins.

## Command Reference

```bash
browser install [--all]                 # download headless Chromium; headed build auto-downloads on first `show`
browser --version | update              # show version / upgrade (daily check; BROWSER_NO_UPDATE_CHECK=1 disables)
browser install skill [target...]       # install this skill into Claude Code / Codex / OpenCode
browser profile [<name>|new <name>|delete <name>|ephemeral|status]   # persistent logins; delete unused profiles (~100 MB each)
browser create [--show] [--profile <name>|--ephemeral]   # new session; pick its profile per session
browser list [--table]                  # JSON list with state/visible
browser <id> show | hide | delete
browser shutdown

browser <id> navigate <url> [-s]        # -s on any action: append a fresh snapshot
browser <id> snapshot [scope] [--all] [--max N] [--json]
browser <id> click <target> [--double] [-s]
browser <id> click --at X,Y [--double]   # click raw viewport pixels (canvas / vision, no DOM target)
browser <id> type <target> <text> [--sequential] [--submit] [-s]   # alias: fill
browser <id> press <key> [target]       # Enter, Tab, Escape, Control+a
browser <id> hover <target>
browser <id> select <target> <value-or-label>
browser <id> scroll [up|down] [px] | scroll <target>
browser <id> text [selector]            # readable text for extraction
browser <id> wait [--text T | --selector S] [--gone] [--timeout ms]
browser <id> screenshot [target] [-o path] [-f] [-q 70]
browser <id> eval <js>
browser <id> console [--clear]
browser <id> back | forward
browser <id> batch                      # JSON lines on stdin, one round-trip
```

**Targets:** `@e12` (ref from snapshot, preferred) · `--text "Create"` · `--role button --name Create` · `--label "Email"` · `--placeholder Search` · CSS selector. Ambiguous CSS selectors are refused; use a ref or text. For canvas / vision cases with no DOM target, `click --at X,Y` clicks raw viewport pixels (take a `screenshot` first; its pixels map 1:1 to click coordinates).

## Snapshot Format

```
url: https://github.com/login
title: Sign in to GitHub · GitHub
h1 "Sign in to GitHub"
@e2 textbox "Username or email address" [required]
@e3 textbox "Password" type="password" [required]
@e5 button "Sign in"
@e8 link "Create an account" href="/signup?source=login"
```

One line per visible interactive element (plus h1–h3 and live regions), **including elements inside same-origin iframes (marked `[frame]`) and open shadow DOM**: target them like any other element. `@eN` refs are stable until navigation; `[below]`/`[above]` mark elements outside the viewport (clicking scrolls automatically). Hidden elements are omitted. Use a scope selector or `--max` on very long pages; `--json` adds bounding boxes and unique selectors.

## Agent Workflow

```bash
browser list                                               # 1. reuse a session if possible
browser <id> navigate http://localhost:3000/settings -s    # 2. page + snapshot in one call
browser <id> type @e4 "My project"                         # 3. act by ref / text / label
browser <id> click --text "Save" -s                        # 4. act and re-observe
browser <id> text "#toast"                                 # 5. verify cheaply; screenshot only if layout matters
```

Batch known steps:

```bash
printf '%s\n' '{"cmd":"type @e4 My project"}' '{"cmd":"click --text Save"}' '{"cmd":"snapshot"}' | browser <id> batch
```

## Output Contract

- Actions: `{"success": true, "url": "...", "title": "..."}`; with `-s` the snapshot text follows (or is printed alone on success).
- `snapshot`: text as above; `--json` → `{success, url, title, scrollY, viewportHeight, viewportWidth, documentHeight, elements[]}`.
- `screenshot`: `{"success": true, "path": "~/.browser-daemon/shots/<id>_<ts>.jpg", "bytes": 54000, "format": "jpeg"}`.
- Errors: `{"success": false, "error": "..."}` with exit code 1.

## Operational Rules

- Do not request credentials; the user authenticates in a shown window.
- Check `success` / exit code before the next step.
- Prefer `@ref` and `--text` targets over guessed CSS selectors; re-`snapshot` after navigation.
- Use `-s` and `batch` to reduce round-trips; use `text` for extraction.
- Reuse session IDs; delete sessions you created when done; leave the daemon running.

## Quick Troubleshooting

- `Daemon not running` → auto-start was disabled or failed; run `browser daemon &` and check ~/.browser-daemon/daemon.log.
- `Session not found` → `browser list`.
- `ref @eN is unknown or stale` → `snapshot` again.
- `strict mode violation` → selector matched several elements; use a ref or `--text`.
- `... is covered by <div#banner> ...` → an overlay blocks the click; dismiss it (e.g. `click --text "Got it"`) and retry.
- Login page appears → `browser <id> show`, ask the user to log in, `hide`.
- Stale Chromium processes → `browser cleanup`.
