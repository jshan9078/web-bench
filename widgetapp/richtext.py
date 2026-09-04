#!/usr/bin/env python3
"""247-rich-text-format: a contenteditable document editor with a toolbar (Bold, H2, bullet list) and keyboard
shortcuts. Task: bold one phrase, turn one line into an H2 heading, insert a three-item bullet list after a
given paragraph, then Save. Selection and structure editing without a mouse drag. complete = saved HTML has
exactly the required structure and nothing else changed."""
import json, sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base
S = {"saved": None}
DOC = ("<p>Project Harbor kicks off on Monday. The first milestone is the vendor shortlist.</p>"
       "<p>Budget review</p>"
       "<p>Please send your travel receipts to finance by Friday; late receipts cannot be reimbursed this quarter.</p>"
       "<p>Questions go to the programme office.</p>")


def reset(): S["saved"] = None
def render(): return b""
def click(x, y): return {"ignored": True}


def post(path, data, ctype):
    if path == "/__save": S["saved"] = str(data.get("html") or ""); return (json.dumps({"ok": True}), "application/json")
    return None


def norm(h):
    h = re.sub(r"<br\s*/?>", "", h).replace("<strong>", "<b>").replace("</strong>", "</b>")
    h = re.sub(r"<p>\s*(<ul>.*?</ul>)\s*</p>", r"\1", h, flags=re.S)      # editors often wrap an inserted list in a <p>
    h = re.sub(r"<p>\s*</p>", "", h)
    return re.sub(r"\s+", " ", h).strip()


def state():
    h = norm(S["saved"] or ""); ok = False
    if h:
        ok = ("<b>vendor shortlist</b>" in h and h.count("<b>") == 1 and "<h2>Budget review</h2>" in h and h.count("<h2>") == 1
              and re.search(r"reimbursed this quarter\.</p>\s*<ul>\s*<li>Flights</li>\s*<li>Hotels</li>\s*<li>Meals</li>\s*</ul>\s*<p>Questions", h) is not None
              and "Project Harbor kicks off on Monday." in h and "Questions go to the programme office." in h)
    return {"saved": S["saved"], "complete": ok}


PAGE = r"""<!doctype html><meta charset=utf-8><title>Docs: Kickoff note</title>
<style>body{font:15px system-ui;margin:0;background:#f8fafc;color:#0f172a}header{display:flex;gap:8px;padding:10px 16px;background:#fff;border-bottom:1px solid #e2e8f0;align-items:center}button{font:inherit;padding:6px 10px;border:1px solid #cbd5e1;background:#fff;border-radius:6px;cursor:pointer}
#ed{max-width:720px;margin:24px auto;background:#fff;padding:32px;min-height:400px;border:1px solid #e2e8f0;outline:none;line-height:1.6}#ed h2{font-size:22px}#msg{color:#15803d;margin-left:auto}</style>
<header><b>Kickoff note</b><button id=b title="Bold (Ctrl/Cmd+B)"><b>B</b></button><button id=h2 title="Heading 2">H2</button><button id=p title="Paragraph">P</button><button id=ul title="Bullet list">• List</button><button id=save>Save</button><span id=msg></span></header>
<div id=ed contenteditable=true spellcheck=false>__DOC__</div>
<p style="max-width:720px;margin:0 auto;color:#64748b;font-size:13px">Select text with the keyboard (Shift+Arrow, Shift+End) or the mouse, then use the toolbar or Ctrl/Cmd+B. H2 and P apply to the current block; the list button turns the current block into a bullet item (Enter adds another item).</p>
<script>(function(){var ed=document.getElementById('ed');function cmd(c,v){ed.focus();document.execCommand(c,false,v||null)}
document.getElementById('b').onclick=function(){cmd('bold')};document.getElementById('h2').onclick=function(){cmd('formatBlock','h2')};document.getElementById('p').onclick=function(){cmd('formatBlock','p')};document.getElementById('ul').onclick=function(){cmd('insertUnorderedList')};
ed.addEventListener('keydown',function(e){if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='b'){e.preventDefault();cmd('bold')}});
document.getElementById('save').onclick=function(){fetch('/__save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({html:ed.innerHTML})}).then(function(){document.getElementById('msg').textContent='Saved'})}})();</script>"""


def page(): return PAGE.replace("__DOC__", DOC)


if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8909)
