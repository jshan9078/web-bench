#!/usr/bin/env python3
"""Run a command under a wall-clock budget. Usage: budget_exec.py <seconds> <cmd...>
The child runs in its own session/process group and inherits stdin/stdout/stderr (so runners can keep
their stream redirections). On expiry the main child process alone gets SIGTERM first and up to
GRACE_S (default 30) seconds to flush its final event; the signal is KILL_SIGNAL (default INT, the CLI's Ctrl-C path) (the Claude CLI writes its cost-bearing result
event on a graceful shutdown; killing the whole group at once loses it), then the group gets SIGTERM
and, 5 s later, SIGKILL. The wrapper exits 124 (like GNU timeout); otherwise the child's exit code
is passed through."""
import os, signal, subprocess, sys, time
budget = float(sys.argv[1]); cmd = sys.argv[2:]; grace = float(os.environ.get("GRACE_S", "30")); sig = getattr(signal, "SIG" + os.environ.get("KILL_SIGNAL", "INT"))
p = subprocess.Popen(cmd, start_new_session=True)
def wait_until(limit):
    t0 = time.time()
    while p.poll() is None and time.time() - t0 < limit: time.sleep(0.2)
    return p.poll() is not None
try:
    rc = p.wait(timeout=budget)
    sys.exit(rc)
except subprocess.TimeoutExpired:
    sys.stderr.write(f"budget_exec: {budget:.0f}s budget exhausted, terminating {cmd[0]} (pid {p.pid}) gracefully\n")
    try: p.send_signal(sig)
    except ProcessLookupError: pass
    if not wait_until(grace):
        sys.stderr.write(f"budget_exec: no exit after {grace:.0f}s grace, terminating the process group\n")
        try: os.killpg(p.pid, signal.SIGTERM)
        except ProcessLookupError: pass
        if not wait_until(5):
            try: os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError: pass
            p.wait()
    try: os.killpg(p.pid, signal.SIGKILL)   # reap any grandchildren the CLI left behind
    except ProcessLookupError: pass
    sys.exit(124)
