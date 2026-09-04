#!/usr/bin/env python3
"""255-config-editor: a web code editor (line-numbered textarea with auto-indent and bracket auto-close, like a
minimal IDE) holding a JSON config. Task: change two values and add one key, keeping the file valid JSON, then
Save (the server validates). complete = saved JSON parses and has exactly the requested changes."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
CFG = {"service": "harbor-api", "replicas": 2, "timeout_ms": 3000, "retries": 1, "features": {"cache": True, "tracing": False}, "regions": ["us-east-1", "eu-west-1"]}
S = {"saved": None, "attempts": []}


def reset(): S["saved"] = None; S["attempts"] = []
def render(): return b""
def click(x, y): return {"ignored": True}


def get(path):
    if path == "/__data": return (json.dumps({"text": json.dumps(CFG, indent=2)}), "application/json")
    return None


def post(path, data, ctype):
    if path == "/__save":
        txt = str(data.get("text") or ""); S["attempts"].append(txt)
        try: obj = json.loads(txt)
        except Exception as e: return (json.dumps({"ok": False, "error": f"Invalid JSON: {e}"}), "application/json")
        S["saved"] = obj; return (json.dumps({"ok": True}), "application/json")
    return None


def state():
    o = S["saved"]; want = json.loads(json.dumps(CFG)); want["retries"] = 5; want["features"]["tracing"] = True; want["regions"].append("ap-south-1")
    return {"saved": o, "attempts": len(S["attempts"]), "complete": o == want}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Config editor: harbor-api.json</title>
<style>body{font:14px system-ui;margin:0;background:#1e1e1e;color:#d4d4d4}header{padding:8px 14px;background:#252526;display:flex;gap:10px;align-items:center}button{font:inherit;padding:5px 10px}#wrap{display:flex}#ln{width:40px;text-align:right;padding:10px 6px;color:#858585;font:13px/20px ui-monospace,Menlo,monospace;white-space:pre;user-select:none}
#ed{flex:1;height:480px;background:#1e1e1e;color:#d4d4d4;border:0;outline:0;resize:none;font:13px/20px ui-monospace,Menlo,monospace;padding:10px;white-space:pre;tab-size:2}#msg{margin-left:auto}#msg.err{color:#f48771}#msg.ok{color:#89d185}</style>
<header><b>harbor-api.json</b><button id=save>Save (Ctrl/Cmd+S)</button><span id=msg></span></header>
<div id=wrap><div id=ln></div><textarea id=ed spellcheck=false></textarea></div>
<p style="color:#858585;font-size:12px;padding:0 14px">Editor behaviour: Enter keeps the current indentation; typing an opening bracket or quote inserts its closing partner; Tab inserts two spaces. The server rejects invalid JSON.</p>
<script>(function(){var ed=document.getElementById('ed');function lines(){var n=ed.value.split('\n').length,s='';for(var i=1;i<=n;i++)s+=i+'\n';document.getElementById('ln').textContent=s}
fetch('/__data').then(r=>r.json()).then(function(j){ed.value=j.text;lines()});ed.addEventListener('input',lines);
ed.addEventListener('keydown',function(e){var s=ed.selectionStart,v=ed.value;if(e.key==='Enter'){e.preventDefault();var ls=v.lastIndexOf('\n',s-1)+1,ind=v.slice(ls).match(/^[ ]*/)[0];var extra=/[{\[]\s*$/.test(v.slice(ls,s))?'  ':'';ed.setRangeText('\n'+ind+extra,s,ed.selectionEnd,'end');lines()}
 else if(e.key==='Tab'){e.preventDefault();ed.setRangeText('  ',s,ed.selectionEnd,'end')}
 else if('{["'.indexOf(e.key)>=0&&ed.selectionStart===ed.selectionEnd){e.preventDefault();var close={'{':'}','[':']','"':'"'}[e.key];ed.setRangeText(e.key+close,s,s,'end');ed.selectionStart=ed.selectionEnd=s+1}
 else if((e.key==='}'||e.key===']'||e.key==='"')&&v[s]===e.key){e.preventDefault();ed.selectionStart=ed.selectionEnd=s+1}
 else if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='s'){e.preventDefault();save()}});
function save(){fetch('/__save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:ed.value})}).then(r=>r.json()).then(function(j){var m=document.getElementById('msg');m.textContent=j.ok?'Saved':j.error;m.className=j.ok?'ok':'err'})}
document.getElementById('save').onclick=save})();</script>"""


def page(): return PAGE


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8916)
