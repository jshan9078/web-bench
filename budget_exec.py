#!/usr/bin/env python3
"""Run a command under a wall-clock budget. Usage: budget_exec.py <seconds> <cmd...>
The child runs in its own session/process group and inherits stdin/stdout/stderr (so runners can keep
their stream redirections). On expiry the whole group gets SIGTERM, then SIGKILL after 5 s, and this
wrapper exits 124 (like GNU timeout). Otherwise the child's exit code is passed through."""
import os, signal, subprocess, sys, time
budget = float(sys.argv[1]); cmd = sys.argv[2:]
p = subprocess.Popen(cmd, start_new_session=True)
try:
    rc = p.wait(timeout=budget)
    sys.exit(rc)
except subprocess.TimeoutExpired:
    sys.stderr.write(f"budget_exec: {budget:.0f}s budget exhausted, terminating {cmd[0]} (pgid {p.pid})\n")
    try: os.killpg(p.pid, signal.SIGTERM)
    except ProcessLookupError: pass
    t0 = time.time()
    while p.poll() is None and time.time() - t0 < 5: time.sleep(0.2)
    if p.poll() is None:
        try: os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError: pass
        p.wait()
    sys.exit(124)
