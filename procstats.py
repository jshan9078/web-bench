"""Per-process CPU/RSS sampling helpers (self-contained; ps-based, macOS/Linux).

Extracted from browser-automation-cli's performance-test harness so web-bench runs standalone.
"""
import subprocess


def descendants(root):
    out = subprocess.run(["ps", "-Ao", "pid,ppid"], capture_output=True, text=True).stdout
    kids = {}
    for line in out.splitlines()[1:]:
        a = line.split()
        if len(a) == 2:
            kids.setdefault(int(a[1]), []).append(int(a[0]))
    res, stack = set(), [root]
    while stack:
        x = stack.pop(); res.add(x); stack.extend(kids.get(x, []))
    return res


def cputimes(pids):
    out = subprocess.run(["ps", "-o", "pid,time,rss,comm", "-p", ",".join(map(str, pids))], capture_output=True, text=True).stdout
    res = {}
    for line in out.splitlines()[1:]:
        a = line.split(None, 3)
        if len(a) < 4:
            continue
        t = a[1]; parts = t.split(":")
        secs = float(parts[-1]) + 60 * int(parts[-2]) + (3600 * int(parts[-3]) if len(parts) > 2 else 0)
        res[int(a[0])] = (secs, int(a[2]), a[3])
    return res
