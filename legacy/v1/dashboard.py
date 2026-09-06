#!/usr/bin/env python3
"""Render results/*.json (+ raw/*.json) into a self-contained, interactive dashboard.html:
  - sortable config leaderboard (click a column header)
  - click a config row to expand its 7 runs: embedded run video + the full CLI command trace
  - effort-scaling charts (tokens / wall / cli calls vs effort) per Claude model
Only pass@1 (no pass@2). No thinking-tokens column (Claude doesn't report it). Open the file from
results/ so the ../raw/*.mp4 video paths resolve.

    python3 dashboard.py            # -> results/dashboard.html
"""
import json, statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
RAW = HERE / "raw"
EFFORTS = ["low", "medium", "high", "xhigh", "max"]


def load_results():
    out = []
    for f in sorted(RES.glob("*/*.json")):
        if f.name in ("current.json", "verdicts.json"):
            continue
        try:
            out.append(json.loads(f.read_text()))
        except Exception:
            pass
    return out


def cmd_str(e):
    if e.get("batch"):
        return "batch: " + ", ".join(e["batch"])
    a = e.get("action") or "?"
    p = e.get("params") or {}
    if a == "navigate":
        return f"navigate {p.get('url', '')}"
    if a == "click":
        if "x" in p and "y" in p:
            return f"click --at {p['x']},{p['y']}"
        return f"click {p.get('selector') or p.get('text') or p.get('label') or ''}".rstrip()
    if a == "type":
        return f"type {p.get('selector', '')} {str(p.get('text_value', ''))[:40]}".rstrip()
    if a == "eval":
        return f"eval {str(p.get('expression', ''))[:60]}"
    if a in ("snapshot", "text", "screenshot", "scroll", "press_key", "hover", "wait"):
        extra = " ".join(f"{k}={v}" for k, v in p.items() if k not in ("snap",))
        return (a + (" " + extra if extra else "")).strip()
    return a


def run_detail(task, run):
    """Return {commands, answer} for a run from its raw bundle."""
    f = RAW / f"{task}.{run}.json"
    if not f.exists():
        return {"commands": [], "answer": ""}
    try:
        b = json.loads(f.read_text())
    except Exception:
        return {"commands": [], "answer": ""}
    cmds = [{"c": cmd_str(e), "ok": e.get("ok", True), "dur": round(e.get("dur", 0), 2)}
            for e in b.get("requests_log", [])]
    return {"commands": cmds, "answer": b.get("agent_result_text") or ""}


def main():
    rows = load_results()
    tasks = sorted({r["task"] for r in rows})
    cfgs = {}
    for r in rows:
        cfgs.setdefault(r.get("config", r["run"]), []).append(r)
    med = lambda a, k: round(statistics.median([x.get(k) or 0 for x in a]), 1) if a else 0

    configs = {}
    for cfg, att in cfgs.items():
        r0 = att[0]
        runs = {}
        for r in att:
            t = r["task"]; run = r["run"]; det = run_detail(t, run)
            runs[t] = {"ok": bool(r["success"]) if not r.get("needs_judge") else None,
                       "video": f"{t}.{run}.mp4" if (RAW / f"{t}.{run}.mp4").exists() else None,
                       "cli_calls": r["cli_calls"], "wall_s": r["wall_s"],
                       "agent_tokens": r.get("agent_tokens"),
                       "commands": det["commands"], "answer": det["answer"]}
        configs[cfg] = {
            "harness": r0.get("harness", "claude"), "model": r0.get("model", ""), "effort": r0.get("effort", ""),
            "npass": sum(1 for t in tasks if runs.get(t, {}).get("ok")), "ntasks": len(tasks),
            "agent_tokens": med(att, "agent_tokens"), "tool_tokens": med(att, "tool_output_tokens"),
            "wall_s": med(att, "wall_s"), "cli_calls": med(att, "cli_calls"),
            "cli_time_s": med(att, "cli_time_s"), "cpu_s": med(att, "daemon_cpu_s"),
            "rss_mb": med(att, "daemon_rss_mb"), "runs": runs}

    claude_models = sorted({c["model"] for c in configs.values()
                            if c["harness"].startswith("claude") and c["effort"] in EFFORTS})
    scaling = {m: {"efforts": [], "agent_tokens": [], "wall_s": [], "cli_calls": []} for m in claude_models}
    for m in claude_models:
        for e in EFFORTS:
            k = f"{m}-{e}"
            if k in configs:
                c = configs[k]
                scaling[m]["efforts"].append(e)
                for mk in ("agent_tokens", "wall_s", "cli_calls"):
                    scaling[m][mk].append(c[mk])

    data = {"tasks": tasks, "configs": configs, "efforts": EFFORTS, "claude_models": claude_models, "scaling": scaling}
    (RES / "dashboard.html").write_text(TEMPLATE.replace("/*DATA*/", json.dumps(data)))
    print(f">> {RES/'dashboard.html'}  ({len(rows)} results, {len(configs)} configs, {len(tasks)} tasks)")


TEMPLATE = r"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>webbench results</title>
<style>
:root{--bg:#0b0d12;--card:#151922;--fg:#e7ecf3;--mut:#8b95a7;--line:#232a37;--pass:#7ee787;--fail:#ff7b72;--pend:#8b95a7;
 --opus:#d2a8ff;--sonnet:#79c0ff;--haiku:#7ee787;--agy:#ffa657;--accent:#79c0ff}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;padding:28px}
h1{font-size:24px;margin:0 0 4px}.sub{color:var(--mut);margin:0 0 20px}h2{font-size:17px;margin:26px 0 10px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;overflow-x:auto}
table{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums;white-space:nowrap}
th,td{padding:7px 10px;text-align:right;border-bottom:1px solid var(--line)}
th:first-child,td:first-child{text-align:left}
th{color:var(--mut);font-weight:600;cursor:pointer;user-select:none}
th.sorted{color:var(--fg)}th .arr{opacity:.6;font-size:11px}
tbody tr.cfg{cursor:pointer}tbody tr.cfg:hover{background:#0a0c11}
.tag{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:7px;vertical-align:middle}
.detail{background:#0a0c11}.detail td{padding:0}
.runs{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:12px;padding:14px}
.run{border:1px solid var(--line);border-radius:10px;overflow:hidden;background:var(--card)}
.run h4{margin:0;padding:8px 10px;font-size:13px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--line)}
.run video{width:100%;display:block;background:#000}
.run .novid{padding:18px;color:var(--mut);text-align:center;font-size:12px}
.badge{font-size:11px;padding:1px 7px;border-radius:20px}
.badge.pass{background:rgba(126,231,135,.15);color:var(--pass)}.badge.fail{background:rgba(255,123,114,.15);color:var(--fail)}
.cmds{max-height:200px;overflow:auto;padding:8px 10px;font:11px/1.5 ui-monospace,Menlo,monospace;color:#c9d3e0}
.cmds div{white-space:pre-wrap;word-break:break-all}.cmds .x{color:var(--fail)}.cmds .d{color:var(--mut)}
.lbl{font-size:10px;text-transform:uppercase;letter-spacing:.06em;color:var(--mut);padding:8px 10px 2px;border-top:1px solid var(--line)}
.resp{max-height:260px;overflow:auto;padding:4px 10px 8px;font:12px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;color:#dbe4f0;word-break:break-word}
.resp h3,.resp h4,.resp h5,.resp h6{margin:8px 0 3px;font-size:12.5px;color:var(--fg);font-weight:700}
.resp p{margin:5px 0}.resp ul,.resp ol{margin:4px 0;padding-left:18px}.resp li{margin:1px 0}
.resp code{background:#0a0c11;padding:1px 4px;border-radius:4px;font:11px ui-monospace,Menlo,monospace}
.resp pre.cb{background:#0a0c11;padding:8px;border-radius:6px;overflow:auto;font:11px/1.4 ui-monospace,Menlo,monospace;white-space:pre;margin:6px 0}
.resp table.mdt{border-collapse:collapse;margin:6px 0;font-size:11.5px;display:block;overflow:auto}
.resp table.mdt th,.resp table.mdt td{border:1px solid var(--line);padding:3px 7px;text-align:left;white-space:nowrap}
.resp a{color:var(--accent)}.resp hr{border:0;border-top:1px solid var(--line);margin:8px 0}
.legend{display:flex;gap:14px;flex-wrap:wrap;margin:6px 0 16px;color:var(--mut);font-size:12px}
.legend span{display:inline-flex;align-items:center}
.charts{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}
.chart h3{font-size:13px;color:var(--mut);margin:0 0 6px;font-weight:600}svg{width:100%;height:170px;display:block}
.note{color:var(--mut);font-size:12px;margin-top:20px}.hint{color:var(--mut);font-size:12px;margin:0 0 8px}
</style></head><body>
<h1>webbench — model × thinking-level × CLI</h1>
<p class="sub">Same browser CLI + skill, 7 real-site tasks, pass@1. Click a column to sort; click a row to see that config's run videos + CLI command traces. Medians are per task.</p>
<div class="legend" id="legend"></div>

<h2>Config leaderboard</h2>
<p class="hint">▸ click any row to expand its 7 runs (video + every browser command). Open this file from <code>results/</code> so videos load.</p>
<div class="card"><table id="board"></table></div>

<h2>Effort scaling (Claude)</h2>
<div class="charts" id="charts"></div>

<p class="note">All 18 configs passed all 7 tasks (pass@1), so the differentiator is efficiency. CPU/RSS are the headless daemon+Chromium tree. Videos are headless CDP screencasts. Amazon/X used a logged-in profile.</p>
<script>
const D=/*DATA*/;
const cv=v=>getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const colorFor=c=>{const cf=D.configs[c];return (cf.harness&&cf.harness.indexOf('agy')>=0)?cv('--agy'):(cv('--'+(cf.model||''))||cv('--sonnet'))};
document.getElementById('legend').innerHTML=D.claude_models.map(m=>`<span><i class="tag" style="background:${cv('--'+m)}"></i>${m}</span>`).join('')+`<span><i class="tag" style="background:${cv('--agy')}"></i>gemini (agy)</span>`;

const COLS=[['config','config','s'],['harness','harness','s'],['npass','pass','n'],['agent_tokens','agent tok','n'],['tool_tokens','tool tok','n'],['wall_s','wall s','n'],['cli_calls','cli calls','n'],['cli_time_s','cli s','n'],['cpu_s','cpu s','n'],['rss_mb','rss MB','n']];
let sortKey='agent_tokens', sortDir=1;
function rowsSorted(){
  const keys=Object.keys(D.configs);
  keys.sort((a,b)=>{
    let va,vb;
    if(sortKey==='config'){va=a;vb=b;} else if(sortKey==='harness'){va=D.configs[a].harness;vb=D.configs[b].harness;}
    else {va=D.configs[a][sortKey];vb=D.configs[b][sortKey];}
    if(typeof va==='string') return va.localeCompare(vb)*sortDir;
    return (va-vb)*sortDir;
  });
  return keys;
}
function esc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
// compact markdown -> HTML (escape first, then transform). Handles headers, bold/italic/code,
// links, ul/ol, tables, code fences, hr, paragraphs.
function md(src){
  if(!src||!src.trim()) return '<span class="d">(no response text)</span>';
  const inl=t=>t.replace(/`([^`]+)`/g,'<code>$1</code>')
    .replace(/\*\*([^*]+)\*\*/g,'<b>$1</b>')
    .replace(/(^|[^*])\*([^*\n]+)\*/g,'$1<i>$2</i>')
    .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g,'<a href="$2" target="_blank" rel="noopener">$1</a>');
  const L=esc(src).split('\n'); let h='',i=0;
  const isBreak=s=>/^(\s*([-*]|\d+\.)\s+|#{1,6}\s|\s*\||\s*```|\s*-{3,}\s*$)/.test(s);
  while(i<L.length){
    let l=L[i];
    if(/^\s*```/.test(l)){let b=[];i++;while(i<L.length&&!/^\s*```/.test(L[i])){b.push(L[i]);i++;}i++;h+=`<pre class="cb">${b.join('\n')}</pre>`;continue;}
    let m=l.match(/^(#{1,6})\s+(.*)$/); if(m){const n=Math.min(m[1].length+2,6);h+=`<h${n}>${inl(m[2])}</h${n}>`;i++;continue;}
    if(/^\s*[-*]\s+/.test(l)){h+='<ul>';while(i<L.length&&/^\s*[-*]\s+/.test(L[i])){h+=`<li>${inl(L[i].replace(/^\s*[-*]\s+/,''))}</li>`;i++;}h+='</ul>';continue;}
    if(/^\s*\d+\.\s+/.test(l)){h+='<ol>';while(i<L.length&&/^\s*\d+\.\s+/.test(L[i])){h+=`<li>${inl(L[i].replace(/^\s*\d+\.\s+/,''))}</li>`;i++;}h+='</ol>';continue;}
    if(/^\s*\|(.+)\|\s*$/.test(l)&&i+1<L.length&&/^\s*\|?[\s:|-]+\|?\s*$/.test(L[i+1])){
      const P=r=>r.trim().replace(/^\||\|$/g,'').split('|').map(c=>c.trim());
      const hd=P(l);i+=2;let bd='';
      while(i<L.length&&/\|/.test(L[i])&&L[i].trim()){bd+='<tr>'+P(L[i]).map(c=>`<td>${inl(c)}</td>`).join('')+'</tr>';i++;}
      h+=`<table class="mdt"><thead><tr>${hd.map(c=>`<th>${inl(c)}</th>`).join('')}</tr></thead><tbody>${bd}</tbody></table>`;continue;}
    if(/^\s*-{3,}\s*$/.test(l)){h+='<hr>';i++;continue;}
    if(!l.trim()){i++;continue;}
    let b=[l];i++;while(i<L.length&&L[i].trim()&&!isBreak(L[i])){b.push(L[i]);i++;}
    h+=`<p>${inl(b.join(' '))}</p>`;
  }
  return h;
}
function detailHTML(cfg){
  const c=D.configs[cfg];
  const cards=D.tasks.map(t=>{
    const r=c.runs[t]||{}; const ok=r.ok; const badge=ok===null?'<span class="badge">pend</span>':(ok?'<span class="badge pass">PASS</span>':'<span class="badge fail">FAIL</span>');
    const vid=r.video?`<video controls preload="none" src="../raw/${r.video}"></video>`:'<div class="novid">no video</div>';
    const cmds=(r.commands||[]).map(x=>`<div class="${x.ok?'':'x'}">${x.ok?'':'✗ '}${esc(x.c)} <span class="d">(${x.dur}s)</span></div>`).join('')||'<div class="d">no cli calls</div>';
    return `<div class="run"><h4><span>${t} ${badge}</span><span class="d" style="color:var(--mut);font-weight:400">${r.cli_calls||0} calls · ${r.wall_s||0}s · ${(r.agent_tokens||0).toLocaleString()} tok</span></h4>${vid}`+
      `<div class="lbl">response</div><div class="resp">${md(r.answer)}</div>`+
      `<div class="lbl">cli trace</div><div class="cmds">${cmds}</div></div>`;
  }).join('');
  return `<div class="runs">${cards}</div>`;
}
function render(){
  const head='<thead><tr>'+COLS.map(([k,l])=>`<th data-k="${k}" class="${k===sortKey?'sorted':''}">${l}${k===sortKey?` <span class="arr">${sortDir<0?'▼':'▲'}</span>`:''}</th>`).join('')+'</tr></thead>';
  const body='<tbody>'+rowsSorted().map(cfg=>{
    const c=D.configs[cfg];
    const cells=COLS.map(([k])=>{
      if(k==='config') return `<td><span class="tag" style="background:${colorFor(cfg)}"></span>▸ ${cfg}</td>`;
      if(k==='harness') return `<td style="text-align:left;color:var(--mut)">${c.harness}</td>`;
      if(k==='npass') return `<td><b>${c.npass}/${c.ntasks}</b></td>`;
      return `<td>${(c[k]||0).toLocaleString()}</td>`;
    }).join('');
    return `<tr class="cfg" data-cfg="${cfg}">${cells}</tr><tr class="detail" data-for="${cfg}" style="display:none"><td colspan="${COLS.length}">${detailHTML(cfg)}</td></tr>`;
  }).join('')+'</tbody>';
  const tbl=document.getElementById('board'); tbl.innerHTML=head+body;
  tbl.querySelectorAll('th').forEach(th=>th.onclick=()=>{const k=th.dataset.k;if(k===sortKey)sortDir*=-1;else{sortKey=k;sortDir=(k==='config'||k==='harness')?1:1;}render();});
  tbl.querySelectorAll('tr.cfg').forEach(tr=>tr.onclick=()=>{const d=tbl.querySelector(`tr.detail[data-for="${tr.dataset.cfg}"]`);d.style.display=d.style.display==='none'?'table-row':'none';});
}
render();

// effort-scaling charts (no pass@2)
function lineChart(title,key){
 const series=D.claude_models.map(m=>({m,pts:D.scaling[m].efforts.map((e,i)=>[D.efforts.indexOf(e),D.scaling[m][key][i]])})).filter(s=>s.pts.length);
 const all=series.flatMap(s=>s.pts.map(p=>p[1]));const max=Math.max(...all,1),min=Math.min(...all,0);
 const W=340,H=170,pad=40;const x=i=>pad+(i/(D.efforts.length-1))*(W-pad-8);const y=v=>H-24-((v-min)/((max-min)||1))*(H-24-10);
 const axis=D.efforts.map((e,i)=>`<text x="${x(i)}" y="${H-8}" fill="${cv('--mut')}" font-size="10" text-anchor="middle">${e}</text>`).join('');
 const lines=series.map(s=>{const col=cv('--'+s.m);const path=s.pts.map((p,i)=>`${i?'L':'M'}${x(p[0]).toFixed(1)},${y(p[1]).toFixed(1)}`).join(' ');
   const dots=s.pts.map(p=>`<circle cx="${x(p[0]).toFixed(1)}" cy="${y(p[1]).toFixed(1)}" r="2.5" fill="${col}"/>`).join('');
   return `<path d="${path}" fill="none" stroke="${col}" stroke-width="1.8"/>${dots}`}).join('');
 return `<div class="chart card"><h3>${title} (lower = better)</h3><svg viewBox="0 0 ${W} ${H}">
   <text x="2" y="12" fill="${cv('--mut')}" font-size="10">${max.toLocaleString()}</text>
   <text x="2" y="${H-24}" fill="${cv('--mut')}" font-size="10">${min.toLocaleString()}</text>${axis}${lines}</svg></div>`;
}
document.getElementById('charts').innerHTML=lineChart('agent tokens','agent_tokens')+lineChart('wall time (s)','wall_s')+lineChart('cli calls','cli_calls');
</script></body></html>"""

if __name__ == "__main__":
    main()
