#!/usr/bin/env python3
"""312-hover-menu: a menu bar whose submenus open only on hover (no click handlers on the parents; click closes
them). Reach Data > Export > Legacy formats > "CSV (semicolon)" and click it; a decoy "CSV (comma)" sits nearby
and a decoy Export button exists in the toolbar. complete = the correct item was activated."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
S = {"activated": []}


def reset(): S["activated"] = []
def render(): return b""
def click(x, y): return {"ignored": True}
def get(path): return None


def post(path, data, ctype):
    if path == "/__act": S["activated"].append(str(data.get("item"))); return (json.dumps({"ok": True}), "application/json")
    return None


def state(): return {"activated": S["activated"], "complete": bool(S["activated"]) and S["activated"][-1] == "csv-semicolon" and S["activated"].count("csv-comma") == 0 and S["activated"].count("toolbar-export") == 0}


def page():
    return """<!doctype html><meta charset=utf-8><title>Ledger</title><style>body{font:14px system-ui;margin:0;background:#f8fafc;color:#0f172a}#bar{display:flex;background:#1e293b;color:#fff}#bar>li{list-style:none;position:relative;padding:10px 16px;cursor:default}#bar>li:hover{background:#334155}ul{margin:0;padding:0}li ul{display:none;position:absolute;top:100%;left:0;background:#fff;color:#0f172a;min-width:190px;box-shadow:0 4px 12px rgba(0,0,0,.2);z-index:5}li li ul{top:0;left:100%}li:hover>ul{display:block}li li{list-style:none;position:relative;padding:8px 14px;white-space:nowrap}li li:hover{background:#e2e8f0}#tb{padding:12px}button{font:inherit;padding:6px 12px}#log{padding:12px;color:#475569}</style>
<ul id=bar><li>File<ul><li data-i=new>New ledger</li><li data-i=open>Open</li></ul></li><li>Data<ul><li data-i=import>Import</li><li>Export &#9656;<ul><li data-i=csv-comma>CSV (comma)</li><li>Legacy formats &#9656;<ul><li data-i=csv-semicolon>CSV (semicolon)</li><li data-i=tsv>TSV</li><li data-i=sylk>SYLK</li></ul></li><li data-i=xlsx>Excel workbook</li></ul></li></ul></li><li>View<ul><li data-i=zoom>Zoom</li></ul></li></ul>
<div id=tb><button data-i=toolbar-export>Export</button> <button data-i=refresh>Refresh</button></div><div id=log></div>
<script>(function(){document.querySelectorAll('[data-i]').forEach(function(el){el.addEventListener('click',function(e){e.stopPropagation();var i=el.getAttribute('data-i');fetch('/__act',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({item:i})}).then(function(){document.getElementById('log').textContent='Ran: '+el.textContent.trim()});if(el.closest('#bar')){document.querySelectorAll('#bar ul').forEach(function(u){u.style.display='none'});setTimeout(function(){document.querySelectorAll('#bar ul').forEach(function(u){u.style.display=''})},300)}})});})();</script>"""


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8950)
