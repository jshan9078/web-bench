#!/usr/bin/env python3
"""Per-run USD cost from the captured bundle. claude: costUSD reported by the CLI in the stream's final result event
(fallback: none); muse/codex/agy: the repo's per-harness price tables applied to agent_usage_raw.
Usage: run_cost.py <raw-json> [stream-file]"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
def cost(raw_path, stream_path=None):
    d = json.load(open(raw_path)); h = d.get("harness"); u = d.get("agent_usage_raw") or {}
    try:
        if h == "claude":
            sp = stream_path or (os.path.join(os.path.dirname(raw_path), d["stream_file"]) if d.get("stream_file") else None)
            if sp and os.path.exists(sp):
                with open(sp, "rb") as f:
                    f.seek(max(0, os.path.getsize(sp) - 200000)); tail = f.read().decode("utf-8", "replace")
                import re
                for line in reversed(tail.splitlines()):
                    if '"type":"result"' in line.replace(" ", "") or '"type":"result"' in line:
                        m = re.search(r'"(?:total_cost_usd|costUSD|cost_usd)"\s*:\s*([0-9.]+)', line)
                        if m: return float(m.group(1))
            return None
        if h == "muse": import muse_cost; return muse_cost.run_cost(d.get("model"), u)
        if h == "codex": import codex_cost; return codex_cost.run_cost(d.get("model"), u)
        if h == "agy": import gemini_cost; return gemini_cost.run_cost(u)
    except Exception: return None
    return None
if __name__ == "__main__": print(cost(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
