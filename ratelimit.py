#!/usr/bin/env python3
"""Rate-limit detection for run streams (rule 2026-09-04: a run in which the model hit a provider rate limit or quota
is invalid, because retries distort the wall-clock measurement). Markers are harness-specific API error strings; plain
"429" is not used because it matches ordinary numbers. Usage: ratelimit.py <stream-file>... (prints hits per file)."""
import re, sys
PAT = re.compile(r'rate_limit_error|overloaded_error|"Retrying in|Retrying in \d|429 Too Many|status 429|HTTP 429|HTTP error: 429|Reconnecting\.\.\.|hit your usage limit|quota reached|RESOURCE_EXHAUSTED|Individual quota|rate limit exceeded|Rate limit reached|rate_limit_exceeded|insufficient_quota')
def hits(path, limit=3):
    out = []
    try:
        with open(path, "rb") as f:
            for line in f:
                m = PAT.search(line.decode("utf-8", "replace"))
                if m:
                    out.append(m.group(0))
                    if len(out) >= limit: break
    except FileNotFoundError: pass
    return out
if __name__ == "__main__":
    for p in sys.argv[1:]:
        h = hits(p); print(f"{p}: {len(h)} {h[:2]}" if h else f"{p}: clean")
