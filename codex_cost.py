"""Per-run cost for codex-harness runs from captured token usage.

Official API pricing (developers.openai.com, standard tier, short context, per 1M tokens),
as of 2026-08-31. These list prices ALREADY include the promotional cuts (Luna -80%,
Terra -20% on 2026-07-30; Sol -20% on 2026-08-21, promised at least through 2026-11-21).
Short-context rates apply below a 272K-token request context; verify_short_context()
checks the largest single turn in each stream.
"""
import json, glob, sys

PRICING = {  # model -> (input, cached_input, cache_write, output) $/M
    "gpt-5.6-sol":   (4.00, 0.40, 5.00, 20.00),
    "gpt-5.6-terra": (2.00, 0.20, 2.50, 12.00),
    "gpt-5.6-luna":  (0.20, 0.02, 0.25, 1.20),
}

def run_cost(model, u):
    pi, pc, pw, po = PRICING[model]
    uncached = u.get("input_tokens", 0) - u.get("cached_input_tokens", 0) - u.get("cache_write_input_tokens", 0)
    return (uncached / 1e6 * pi
            + u.get("cached_input_tokens", 0) / 1e6 * pc
            + u.get("cache_write_input_tokens", 0) / 1e6 * pw
            + u.get("output_tokens", 0) / 1e6 * po)

def max_turn_input(stream_path):
    m = 0
    for l in open(stream_path, errors="ignore"):
        try: d = json.loads(l)
        except Exception: continue
        if d.get("type") == "turn.completed":
            m = max(m, (d.get("usage") or {}).get("input_tokens", 0))
    return m

if __name__ == "__main__":
    pat = sys.argv[1] if len(sys.argv) > 1 else "*"
    total = 0.0
    for f in sorted(glob.glob(f"raw/{pat}.json")):
        d = json.load(open(f))
        if d.get("harness") != "codex": continue
        c = run_cost(d["model"], d.get("agent_usage_raw") or {})
        total += c
        mt = max_turn_input(f.replace(".json", ".stream.txt"))
        flag = "  [LONG-CONTEXT?]" if mt > 272_000 else ""
        print(f"{d['task']:30} {d['config']:14} ${c:6.3f}  max-turn-in {mt:>7}{flag}")
    print(f"{'TOTAL':45} ${total:.2f}")
