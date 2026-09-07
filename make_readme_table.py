#!/usr/bin/env python3
"""Rewrite the results table in README.md from the site data (src/data/webbench-v2.json produced by make_v2_site.py)."""
import json, re
v = json.load(open("/Users/jonathan/Desktop/personal-site/jshan9078.github.io/src/data/webbench-v2.json"))
rows = v["webRows"]
tbl = "| Configuration | Pass@1 | Median seconds | Median cost |\n|---|---|---|---|\n" + "\n".join(f"| {r['model']} {r['thinking']} | {r['passes']}/{r['tasks']} ({r['score']:.0f}%) | {r['time']:.0f} | ${r['cost']:.2f} |" for r in rows)
s = open("README.md").read()
new = re.sub(r"(## Results\n\n)\| Configuration \|.*?\n\n", lambda m: m.group(1) + tbl + "\n\n", s, count=1, flags=re.S)
assert new != s or tbl in s; open("README.md", "w").write(new); print("README table rows:", len(rows))
