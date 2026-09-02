"""Per-run cost for agy (Antigravity / Gemini) runs from captured token usage.

Gemini 3.x Flash pricing (public introductory rates, per 1M tokens): input $0.75,
output $3.75 (thinking tokens are part of output), cache read $0.075. Gemini 3.8 Flash
uses the same rates as 3.7 Flash. These rates double on 2027-01-01.

agy usage convention (from the stream's result.usage): `input_tokens` is the NON-cached input
(cache_read_tokens are billed separately at the cache-read rate), `output_tokens` already
includes `thinking_tokens`. So cost sums three lines: input, cache-read, output.
"""
import json, glob, sys

RATES = (0.75, 0.075, 3.75)  # (input, cache_read, output) $/M

def run_cost(u):
    pi, pc, po = RATES
    return (u.get("input_tokens", 0) / 1e6 * pi
            + u.get("cache_read_tokens", 0) / 1e6 * pc
            + u.get("output_tokens", 0) / 1e6 * po)

if __name__ == "__main__":
    pat = sys.argv[1] if len(sys.argv) > 1 else "*"
    total = 0.0
    for f in sorted(glob.glob(f"raw/{pat}.json")):
        d = json.load(open(f))
        if d.get("harness") != "agy":
            continue
        u = d.get("agent_usage_raw") or {}
        c = run_cost(u)
        total += c
        cr = u.get("cache_read_tokens", 0); it = u.get("input_tokens", 0)
        hit = cr / max(1, cr + it)
        print(f"{d['task']:30} {d['config']:22} ${c:6.4f}  cache-read {hit:5.1%}")
    print(f"{'TOTAL':53} ${total:.2f}")
