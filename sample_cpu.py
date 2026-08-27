#!/usr/bin/env python3
"""Sample the browser daemon's whole process tree (daemon + every Chromium helper) at a fixed
interval and append one JSON line per sample. Run in the background during an agent run:

    python3 sample_cpu.py results/x.cpu.jsonl 0.25 &
    SAMPLER=$!; ... ; kill $SAMPLER

Each line: {"t": <rel s>, "cpu_pct": <tree CPU% since last sample>, "rss_mb": <tree RSS>}.
CPU% is (sum of per-pid cpu-time deltas)/interval*100 over pids alive in both samples, which is
honest on macOS (unlike `ps pcpu`, a lifetime average).
"""
import json, subprocess, sys, time
from pathlib import Path

pass  # (standalone)
import procstats as bench


def dpid():
    out = subprocess.run(["pgrep", "-f", "daemon.server|browser-daemon|browser daemon"],
                         capture_output=True, text=True).stdout.split()
    return int(out[0]) if out else None


def main():
    out = Path(sys.argv[1]); interval = float(sys.argv[2]) if len(sys.argv) > 2 else 0.25
    out.write_text("")
    t0 = time.time()
    pid = dpid()
    prev = bench.cputimes(bench.descendants(pid)) if pid else {}
    while True:
        time.sleep(interval)
        pid = dpid()
        if not pid:
            continue
        pids = bench.descendants(pid)
        cur = bench.cputimes(pids)
        cpu = sum(cur[p][0] - prev.get(p, (cur[p][0],))[0] for p in cur if p in prev) / interval * 100
        rss = sum(v[1] for v in cur.values()) / 1024
        with out.open("a") as f:
            f.write(json.dumps({"t": round(time.time() - t0, 2),
                                "cpu_pct": round(cpu, 1), "rss_mb": round(rss, 1)}) + "\n")
        prev = cur


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
