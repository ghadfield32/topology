"""Build the self-contained offline reader from course Markdown and executed notebooks.

Run from any working directory with the course's reader extra installed.
No external scripts, font files, APIs, or network resources are embedded.
"""
from __future__ import annotations

import html
import json
from pathlib import Path
import re

import mistune
import nbformat

ROOT = Path(__file__).resolve().parents[1]
META = json.loads((ROOT / "docs/stage_metadata.json").read_text(encoding="utf-8"))
MD = mistune.create_markdown(plugins=["table", "strikethrough", "url"])

CSS = """
:root{color-scheme:light;--bg:#f6f7f9;--paper:#fff;--ink:#1b2936;--muted:#566878;--line:#dce4e9;--accent:#006b65;--tint:#e8f5f1;--code:#f0f3f6;--shadow:0 5px 24px #23334209}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.72 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}a{color:var(--accent);text-underline-offset:3px}a:hover{text-decoration-thickness:2px}.layout{display:grid;grid-template-columns:278px minmax(0,1fr);min-height:100vh}.side{padding:30px 23px;position:sticky;top:0;height:100vh;overflow:auto;border-right:1px solid var(--line);background:var(--paper)}.brand{font-weight:800;line-height:1.25;font-size:21px;letter-spacing:-.4px;text-decoration:none;display:block;color:var(--ink)}.brand small{font-size:11px;letter-spacing:1.4px;text-transform:uppercase;color:var(--muted);display:block;margin-bottom:10px}.nav-title{font-size:11px;letter-spacing:1.3px;text-transform:uppercase;font-weight:800;color:var(--muted);margin:30px 0 8px}.side nav a{display:block;font-size:13px;line-height:1.4;text-decoration:none;padding:8px;border-radius:6px;margin-bottom:3px}.side nav a.current{background:var(--tint);font-weight:750}.side nav .n{font-variant-numeric:tabular-nums;display:inline-block;min-width:26px;color:var(--muted)}.main{padding:44px 6vw 60px;min-width:0}.wrap{max-width:1020px;margin:auto}.eyebrow{text-transform:uppercase;letter-spacing:1.5px;font-size:12px;font-weight:800;color:var(--accent);margin:0 0 14px}.hero h1{font-size:clamp(34px,4.1vw,54px);line-height:1.11;letter-spacing:-1.5px;margin:0 0 20px}.lead{font-size:20px;color:var(--muted);max-width:820px}.card,article{background:var(--paper);border:1px solid var(--line);border-radius:13px;box-shadow:var(--shadow);padding:32px;margin:23px 0}.card h2{margin-top:0}article h1{font-size:31px;line-height:1.25;letter-spacing:-.6px;margin-top:0}h2{font-size:25px;line-height:1.3;margin-top:36px}h3{font-size:20px;line-height:1.4;margin-top:27px}p{margin:15px 0}article p,article li{max-width:85ch}code{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;background:var(--code);border-radius:4px;padding:2px 5px;font-size:.86em}pre{background:var(--code);border:1px solid var(--line);padding:20px;border-radius:8px;overflow:auto;line-height:1.55;font-size:14px;tab-size:4}pre code{padding:0;background:none;font-size:inherit}table{border-collapse:collapse;width:100%;font-size:14px;display:block;overflow-x:auto;margin:24px 0}th,td{text-align:left;vertical-align:top;padding:12px 14px;border-bottom:1px solid var(--line)}th{background:var(--code);font-weight:750}blockquote{border-left:4px solid var(--accent);padding:3px 20px;margin:24px 0;color:var(--muted)}.callout{background:var(--tint);border-left:4px solid var(--accent);border-radius:5px;padding:16px 21px;margin:22px 0}.callout p{margin:0}.toolbar,.pager{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:22px 0}.button,button{border:1px solid var(--line);border-radius:7px;background:var(--paper);color:var(--accent);padding:10px 15px;font:600 14px system-ui;text-decoration:none;cursor:pointer}.button.primary,button.primary{background:var(--accent);border-color:var(--accent);color:#fff}.button:hover,button:hover{filter:brightness(.94)}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:13px;margin:25px 0}.stat{background:var(--paper);border:1px solid var(--line);padding:18px;border-radius:10px}.stat strong{display:block;font-size:28px;line-height:1.15}.stat span{font-size:12px;color:var(--muted)}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:15px}.stage-card{display:block;padding:23px;border:1px solid var(--line);border-radius:10px;background:var(--paper);text-decoration:none;color:var(--ink)}.stage-card strong{display:block;font-size:18px;line-height:1.35}.stage-card p{font-size:13px;color:var(--muted);margin-bottom:0}.badge{display:block;color:var(--accent);font-size:11px;font-weight:800;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px}.subtle{font-size:13px;color:var(--muted)}footer{font-size:12px;color:var(--muted);border-top:1px solid var(--line);padding-top:22px;margin-top:35px}.cell{border-top:1px solid var(--line);padding-top:20px;margin-top:22px}.cell-label{font-size:11px;text-transform:uppercase;letter-spacing:1px;font-weight:800;color:var(--muted)}.output{background:transparent;white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px}.output-image{display:block;max-width:100%;height:auto;margin:20px auto;background:white;border:1px solid var(--line)}details{border:1px solid var(--line);border-radius:8px;padding:15px;margin:15px 0}summary{font-weight:650;cursor:pointer}select,textarea{font:inherit;border:1px solid var(--line);border-radius:6px;background:var(--paper);color:var(--ink);padding:9px;max-width:100%}textarea{width:100%;min-height:65px}.progress-row{border-top:1px solid var(--line);padding:20px 0}.progress-row h3{margin:0 0 10px}.flash-question{font-size:23px;line-height:1.5}.flash-answer{padding:20px;background:var(--tint);border-radius:8px;white-space:pre-wrap}img{max-width:100%}.table-wrap{overflow-x:auto}.table-wrap table{display:table} .sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0)}
@media(max-width:1100px){.layout{grid-template-columns:230px minmax(0,1fr)}.main{padding:32px 4vw}.side{padding:24px 15px}.stats{grid-template-columns:repeat(2,1fr)}}
@media(max-width:760px){.layout{display:block}.side{position:relative;height:auto;border-right:0;border-bottom:1px solid var(--line);padding:18px 22px}.side nav{display:none}.nav-title{display:none}.brand small{margin:0 0 5px}.brand{font-size:18px}.main{padding:25px 17px}.grid{grid-template-columns:1fr}.card,article{padding:22px}.hero h1{font-size:37px}article h1{font-size:27px}.lead{font-size:18px}}
@media(prefers-color-scheme:dark){:root{color-scheme:dark;--bg:#10191f;--paper:#17242d;--ink:#e9f0f3;--muted:#a5b6c1;--line:#30424d;--accent:#77d7c3;--tint:#1b3837;--code:#111e27;--shadow:none}.button.primary,button.primary{color:#102520}.output-image{background:white}}
@media print{.side,.toolbar,.pager,button,footer{display:none}.layout{display:block}.main{padding:0}article,.card{border:0;box-shadow:none;padding:0}body{background:white;color:black;font-size:11pt}.output-image{max-height:240px}pre{white-space:pre-wrap}h2,h3{break-after:avoid}}
"""

SHORT = ["Start from zero", "Mathematical toolbox", "Closeness and spaces", "Continuity and good maps", "Groups, paths and homotopy", "Surfaces and simplices", "Homology and Betti numbers", "Shape from data", "Persistence and diagrams", "Implement the algorithm", "Stability and uncertainty", "Representations and evaluation", "Capstone and book audit"]


def esc(x: object) -> str:
    return html.escape(str(x), quote=True)


def shell(title: str, body: str, destination: Path, current: int | None = None, extra_js: str = "") -> None:
    """Write one document. All paths below are relative to that document."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    relative_depth = len(destination.relative_to(ROOT).parts) - 1
    prefix = "../" * relative_depth
    nav = "".join(
        f'<a class="{"current" if current == item["n"] else ""}" href="{prefix}site/stages/{item["n"]:02d}.html"><span class="n">{item["n"]:02d}</span>{esc(SHORT[item["n"]])}</a>'
        for item in META
    )
    nav += f'<p class="nav-title">Tools for learning</p><a href="{prefix}site/flashcards.html">102 practice cards</a><a href="{prefix}site/progress.html">Your learning record</a><a href="{prefix}site/docs/GLOSSARY.html">Glossary & notation</a><a href="{prefix}site/docs/FINAL_ASSESSMENT.html">Final assessment</a><a href="{prefix}site/docs/SOURCES.html">Free readings & sources</a><a href="{prefix}site/docs/VERIFICATION.html">Execution & limitations</a><a href="{prefix}site/docs/README.html">Python setup</a>'
    text = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="A beginner-first course in topology, homology and persistent homology. Original lessons with executed Python labs."><title>{esc(title)} | Listening to Shape Lab</title><link rel="stylesheet" href="{prefix}site/assets/course.css"></head>
<body><div class="layout"><aside class="side"><a class="brand" href="{prefix}START_HERE.html"><small>Independent learning companion</small>Listening to Shape<br>Learning Lab</a><p class="nav-title">The 13-stage path</p><nav aria-label="Course navigation">{nav}</nav></aside><main class="main"><div class="wrap">{body}<footer>Learning Lab 1.0 · Original teaching material, not the book text or an author-endorsed course. Saved outputs document code execution, not your mastery. <a href="{prefix}START_HERE.html">Course home</a> · <a href="{prefix}site/docs/SOURCES.html">Sources</a> · <a href="{prefix}LICENSE.md">Use & attribution</a></footer></div></main></div>{extra_js}</body></html>'''
    destination.write_text(text, encoding="utf-8")


def notebook_html(path: Path) -> str:
    nb = nbformat.read(path, as_version=4)
    rendered: list[str] = []
    for cell in nb.cells:
        if cell.cell_type == "markdown":
            rendered.append(MD(cell.source))
        elif cell.cell_type == "code":
            outputs = []
            for output in cell.get("outputs", []):
                kind = output.output_type
                if kind == "stream":
                    outputs.append(f'<pre class="output">{esc(output.text)}</pre>')
                elif kind in ("execute_result", "display_data"):
                    data = output.data
                    if "image/png" in data:
                        encoded = data["image/png"]
                        if isinstance(encoded, list):
                            encoded = "".join(encoded)
                        outputs.append(f'<img class="output-image" alt="Executed plot from this code cell. See the cell and surrounding text for its interpretation." src="data:image/png;base64,{encoded}">')
                    elif "text/plain" in data:
                        outputs.append(f'<pre class="output">{esc(data["text/plain"])}</pre>')
                    elif "text/html" in data:
                        # Notebook content is course-authored, but retaining only escaped markup
                        # avoids injecting arbitrary HTML if a learner later adds output.
                        outputs.append(f'<pre class="output">{esc(data["text/html"])}</pre>')
                elif kind == "error":
                    raise ValueError(f"Refusing to publish errored cell in {path.name}: {output.ename}")
            count = cell.get("execution_count")
            rendered.append(f'<section class="cell"><p class="cell-label">Code · executed cell {esc(count)}</p><pre><code>{esc(cell.source)}</code></pre>{"".join(outputs)}</section>')
    return "\n".join(rendered)


def build() -> None:
    assets = ROOT / "site/assets"
    assets.mkdir(parents=True, exist_ok=True)
    (assets / "course.css").write_text(CSS, encoding="utf-8")
    execution = json.loads((ROOT / "reports/notebook_execution.json").read_text())
    stage_cards = "".join(f'<a class="stage-card" href="site/stages/{s["n"]:02d}.html"><span class="badge">Stage {s["n"]:02d}</span><strong>{esc(SHORT[s["n"]])}</strong><p>{esc(s["gate"])}</p></a>' for s in META)
    first = '''<header class="hero"><p class="eyebrow">From zero background to a defended analysis</p><h1>Learn to listen<br>to shape.</h1><p class="lead">A complete working course for the agreed introductory scope: read the mathematics, predict the result, run the code, and test your understanding.</p></header><div class="toolbar"><a class="button primary" href="site/stages/00.html">Begin Stage 00</a><a class="button" href="site/docs/README.html">Set up Python</a><a class="button" href="site/docs/CONTINUE_WITH_TUTOR.html">Learn here with your tutor</a></div>
<div class="stats"><div class="stat"><strong>13</strong><span>Beginner-first lesson sections</span></div><div class="stat"><strong>102</strong><span>Original exercises with solutions</span></div><div class="stat"><strong>13</strong><span>Executed Python notebooks</span></div><div class="stat"><strong>2</strong><span>Bundled real datasets</span></div></div>
<div class="callout"><p><strong>Start reading now.</strong> No setup is required to view lessons and saved lab outputs. To change code and run experiments, follow the Python setup. External readings require internet; the included data do not.</p></div>
<section class="card"><h2>The learning loop</h2><p><strong>Read → predict → work by hand → run → explain → solve independently → revisit.</strong></p><p>Begin at Stage 00. Each stage has an explanation, a worked notebook, independent exercises, separate solutions, and a mastery gate. Going faster means removing confusion early—not skipping the reasoning.</p><p class="subtle">The original 24-week schedule is a planning guide, not a deadline. Familiar material can be tested out of; unfamiliar material deserves another example.</p></section>
<section class="card"><h2>What has—and has not—been verified</h2><p><strong>All 13 notebooks have saved successful execution records.</strong> The final verification page reports mathematical tests, data checks and any skipped checks. External Ripser and GUDHI comparisons were not run because these optional packages were unavailable in the build environment.</p><p>This is an independent companion to the supplied topic outline, not the full book. Exact alignment with the actual forthcoming text remains an explicit audit task. Your learning record starts unassessed.</p><div class="toolbar"><a class="button" href="site/docs/VERIFICATION.html">Read the evidence</a><a class="button" href="site/docs/COVERAGE_MAP.html">Inspect topic coverage</a><a class="button" href="site/progress.html">Record your learning</a></div></section>
<h2>The staged learning path</h2>'''
    ending = '''<section class="card"><h2>Use real data without inventing a story</h2><p>The labs use measured Iris samples and real handwritten-digit images. Synthetic geometric examples serve as exact controls. The final comparison includes ordinary pixels, topological descriptors, and both together. A small improvement on one split is not proof of a general benefit.</p><div class="toolbar"><a class="button" href="site/notebooks/12.html">View the executed capstone</a><a class="button" href="site/docs/DATA_README.html">Read the data provenance</a></div></section><section class="card"><h2>Go deeper where the mathematics needs it</h2><p>The glossary, proof guide, cumulative assessment and free reading map make the depth explicit. Elementary proofs are worked here; major theorem proofs have structured deeper-reading assignments. The advanced bridge marks what lies beyond the agreed introductory course.</p><div class="toolbar"><a class="button" href="site/docs/DEEPENING_PROOFS.html">Proof depth guide</a><a class="button" href="site/flashcards.html">Practice retrieval</a><a class="button" href="COURSE_GUIDE.md">Combined Markdown course</a></div></section>'''
    shell("Start here", first + '<div class="grid">' + stage_cards + '</div>' + ending, ROOT / "START_HERE.html")
    for item in META:
        n = item["n"]
        toolbar = f'<div class="toolbar"><a class="button" href="../stages/{n:02d}.html">Lesson</a><a class="button primary" href="../notebooks/{n:02d}.html">Executed lab</a><a class="button" href="../solutions/{n:02d}.html">Worked solutions</a><a class="button" href="../../notebooks/{n:02d}_lab.ipynb" download>Notebook file</a></div>'
        pager = '<nav class="pager" aria-label="Previous and next lesson">'
        if n > 0:
            pager += f'<a class="button" href="../stages/{n-1:02d}.html">← Stage {n-1:02d}</a>'
        if n < 12:
            pager += f'<a class="button" href="../stages/{n+1:02d}.html">Stage {n+1:02d} →</a>'
        pager += '<a class="button" href="../progress.html">Record evidence</a></nav>'
        lesson_text = (ROOT / f"lessons/{n:02d}_lesson.md").read_text(encoding="utf-8")
        shell(f"Stage {n:02d}: {SHORT[n]}", toolbar + '<article>' + MD(lesson_text) + '</article>' + pager, ROOT / f"site/stages/{n:02d}.html", n)
        saved = f'<div class="callout"><p><strong>Saved execution: {esc(execution[f"{n:02d}"]["status"])}</strong> · {execution[f"{n:02d}"]["code_cells"]} code cells. These are actual recorded outputs, not placeholders. To experiment, open the notebook in Jupyter and run from the top.</p></div>'
        shell(f"Executed lab {n:02d}", toolbar + saved + '<article>' + notebook_html(ROOT / f"notebooks/{n:02d}_lab.ipynb") + '</article>' + pager, ROOT / f"site/notebooks/{n:02d}.html", n)
        solutions_text = (ROOT / f"solutions/{n:02d}_solutions.md").read_text(encoding="utf-8")
        shell(f"Solutions {n:02d}", toolbar + '<div class="callout"><p>Attempt the exercises first. A solution you recognize is not yet a solution you can produce independently.</p></div><article>' + MD(solutions_text) + '</article>' + pager, ROOT / f"site/solutions/{n:02d}.html", n)
    docs = {p.stem: p for p in sorted((ROOT / "docs").glob("*.md"))}
    docs.update(README=ROOT / "README.md", DATA_README=ROOT / "data/README.md", PROGRESS_README=ROOT / "progress/README.md")
    for name, path in docs.items():
        shell(name.replace("_", " ").title(), '<article>' + MD(path.read_text(encoding="utf-8")) + '</article>', ROOT / f"site/docs/{name}.html")
    cards = [{"stage": s["n"], "id": f'{s["n"]:02d}.{i+1}', "question": q, "answer": a} for s in META for i, (q, a) in enumerate(zip(s["exercises"], s["solutions"], strict=True))]
    card_json = json.dumps(cards, ensure_ascii=False).replace("<", "\\u003c")
    card_body = '''<p class="eyebrow">Retrieval, not recognition</p><h1>Practice cards</h1><p>Say or write your answer before revealing the solution. These cards reuse the 102 original lesson exercises; they are not 102 additional assessment questions.</p><section class="card"><label for="stageFilter">Stage </label><select id="stageFilter"><option value="all">All stages</option>''' + ''.join(f'<option value="{n}">{n:02d} · {esc(SHORT[n])}</option>' for n in range(13)) + '''</select><p id="cardCount" class="subtle"></p><p id="question" class="flash-question"></p><div id="answer" class="flash-answer" hidden></div><div class="toolbar"><button id="previousCard">Previous</button><button class="primary" id="reveal">Reveal solution</button><button id="nextCard">Next</button></div></section><p class="subtle">After an error, return to that stage's worked example. Revisit the problem after a delay with the answer hidden.</p>'''
    card_js = '<script>"use strict"; const cards=' + card_json + '''; let selected=cards, index=0; const q=document.getElementById("question"),a=document.getElementById("answer"); function draw(){const c=selected[index];q.textContent=c.id+". "+c.question;a.textContent=c.answer;a.hidden=true;document.getElementById("cardCount").textContent=(index+1)+" of "+selected.length+" · Stage "+String(c.stage).padStart(2,"0");}document.getElementById("stageFilter").addEventListener("change",e=>{selected=e.target.value==="all"?cards:cards.filter(c=>c.stage===Number(e.target.value));index=0;draw();});document.getElementById("reveal").onclick=()=>a.hidden=false;document.getElementById("nextCard").onclick=()=>{index=(index+1)%selected.length;draw();};document.getElementById("previousCard").onclick=()=>{index=(index+selected.length-1)%selected.length;draw();};draw();</script>'''
    shell("Practice cards", card_body, ROOT / "site/flashcards.html", extra_js=card_js)
    progress_body = '''<p class="eyebrow">Your evidence, not the software's test score</p><h1>Learning record</h1><p>Manually record what you can explain and solve. No stage is automatically passed by opening a page or running a notebook. Keep the Python validation gate and actual-book audit separate.</p><div class="callout"><p>This record uses browser-local storage where available. It does not change <code>progress/learner_progress.json</code>. Export a backup before changing browsers or moving the course folder. Browser support for local-file storage varies.</p></div><div class="toolbar"><button class="primary" id="exportProgress">Export my record</button><button id="clearProgress">Clear browser record</button></div><p id="storageStatus" class="subtle"></p><section class="card" id="progressRows"></section>'''
    stage_names = json.dumps([{"n": s["n"], "title": SHORT[s["n"]]} for s in META]).replace("<", "\\u003c")
    progress_js = '<script>"use strict"; const stages=' + stage_names + ''';const key="shape-learning-progress-v1"; let record={}; const status=document.getElementById("storageStatus");try{record=JSON.parse(localStorage.getItem(key)||"{}");}catch(e){record={};status.textContent="Storage unavailable: export your record before leaving this page.";}const rows=document.getElementById("progressRows"); const states=["unassessed","read","practiced","independently demonstrated","retained after delay"];function save(){try{localStorage.setItem(key,JSON.stringify(record));status.textContent="Saved in this browser only. Export a backup regularly.";}catch(e){status.textContent="Browser storage unavailable. Export your current record now.";}}stages.forEach(s=>{const row=document.createElement("div");row.className="progress-row";const heading=document.createElement("h3");heading.textContent=String(s.n).padStart(2,"0")+" · "+s.title;row.appendChild(heading);const select=document.createElement("select");select.setAttribute("aria-label","Stage "+s.n+" status");states.forEach(v=>{const o=document.createElement("option");o.value=v;o.textContent=v;select.appendChild(o);});select.value=record[s.n]?.status||"unassessed";row.appendChild(select);const p=document.createElement("p");p.className="subtle";p.textContent="Evidence: which exercise, proof, notebook result or misconception?";row.appendChild(p);const notes=document.createElement("textarea");notes.setAttribute("aria-label","Stage "+s.n+" evidence");notes.value=record[s.n]?.evidence||"";row.appendChild(notes);const update=()=>{record[s.n]={status:select.value,evidence:notes.value,updated_at:new Date().toISOString()};save();};select.addEventListener("change",update);notes.addEventListener("input",update);rows.appendChild(row);});document.getElementById("exportProgress").onclick=()=>{const blob=new Blob([JSON.stringify({course:"Listening to Shape Lab 1.0",kind:"learner self-record; not automated certification",stages:record},null,2)],{type:"application/json"});const url=URL.createObjectURL(blob);const link=document.createElement("a");link.href=url;link.download="my_shape_learning_record.json";link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};document.getElementById("clearProgress").onclick=()=>{if(confirm("Clear only this browser's learning record? Export a backup first.")){record={};try{localStorage.removeItem(key);}catch(e){}location.reload();}};</script>'''
    shell("Learning record", progress_body, ROOT / "site/progress.html", extra_js=progress_js)
    guide = "# Listening to Shape — Complete Course Guide\n\nOriginal beginner-first companion to the supplied introductory learning scope. See README.md for execution and docs/SOURCES.md for references. The actual book text has not been audited.\n\n"
    for item in META:
        guide += "\n\n---\n\n" + (ROOT / f"lessons/{item['n']:02d}_lesson.md").read_text(encoding="utf-8")
    guide += "\n\n---\n\n" + (ROOT / "docs/GLOSSARY.md").read_text(encoding="utf-8")
    guide += "\n\n---\n\n" + (ROOT / "docs/SOURCES.md").read_text(encoding="utf-8")
    (ROOT / "COURSE_GUIDE.md").write_text(guide, encoding="utf-8")
    print(f"Built {len(list((ROOT / 'site').rglob('*.html'))) + 1} offline HTML pages, {len(cards)} practice cards, and COURSE_GUIDE.md.")


if __name__ == "__main__":
    build()
