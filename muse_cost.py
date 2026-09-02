"""Per-run cost for muse-harness runs from captured token usage.

Muse Spark 1.2 pricing (Meta list rates, per 1M tokens): input $1.25, cached input $0.15,
output $4.25. No separate cache-write rate; cached_tokens (== cache_read_tokens) are billed
at the cached-input rate and the remaining input at the full rate. reasoning_tokens are a
subset of output_tokens per the usage records, so output is billed as-is.

Usage records come from the muse session log (session.jsonl payload_type runtime.session
events with a "usage" object), summed per run by the harness.
"""
import json, glob, sys

PRICING = {  # model -> (input, cached_input, output) $/M
    "muse-spark-1.2-contributor": (1.25, 0.15, 4.25),
    # 1.3 runs use the contributor model but are priced at the standard (non-contributor) list
    # rates, which are identical to 1.2's: $1.25 in / $0.15 cached / $4.25 out.
    "muse-spark-1.3-contributor": (1.25, 0.15, 4.25),
    "muse-spark-1.3": (1.25, 0.15, 4.25),
}

def run_cost(model, u):
    pi, pc, po = PRICING[model]
    cached = u.get("cached_tokens", 0)
    uncached = u.get("input_tokens", 0) - cached
    return (uncached / 1e6 * pi
            + cached / 1e6 * pc
            + u.get("output_tokens", 0) / 1e6 * po)

if __name__ == "__main__":
    pat = sys.argv[1] if len(sys.argv) > 1 else "*"
    total = 0.0
    for f in sorted(glob.glob(f"raw/{pat}.json")):
        d = json.load(open(f))
        if d.get("harness") != "muse": continue
        u = d.get("agent_usage_raw") or {}
        c = run_cost(d["model"], u)
        total += c
        hit = u.get("cached_tokens", 0) / max(1, u.get("input_tokens", 1))
        print(f"{d['task']:30} {d['config']:14} ${c:6.4f}  cache-hit {hit:5.1%}")
    print(f"{'TOTAL':45} ${total:.2f}")
