"""Build the complete offline v4 reader. No network, font download or model calls.

Trusted course Markdown is rendered locally; code and notebook outputs are escaped.
The new reader lives in site/v4. Legacy pages are retained for old links.
"""
from __future__ import annotations
import html,json,os,re
from pathlib import Path
from urllib.parse import urlsplit,unquote
import mistune
import build_reader as base
ROOT=Path(__file__).resolve().parents[1]
MD=mistune.create_markdown(escape=False,plugins=['table','strikethrough','url'])
base.MD=MD
CORE=json.loads((ROOT/'docs/stage_metadata.json').read_text())
BRIDGE=json.loads((ROOT/'docs/bridge_metadata.json').read_text())
META=CORE+BRIDGE
MAP={}
def esc(v):return html.escape(str(v),quote=True)
def rel(path,destination):return Path(os.path.relpath(path,destination.parent)).as_posix()
def target(p):return MAP.get((ROOT/p).resolve(),ROOT/p)
def shell(title,body,destination,current=None,script=''):
    destination.parent.mkdir(parents=True,exist_ok=True)
    nav=''
    for s in META:
        n=s['n']
        if n in (0,13):nav+=f'<p class="nav-title">{"Topology foundations" if n==0 else "Applied geometry continuation"}</p>'
        nav+=f'<a class="{"current" if current==n else ""}" href="{rel(target(f"stages/{n:02d}/README.md"),destination)}"><span class="n">{n:02d}</span>{esc(s["title"])}</a>'
    tools=[('docs/START_V4.md','Start / setup'),('docs/COMPLETION_SYSTEM_V4.md','Learn and retain'),('docs/COVERAGE_V4.md','84 explicit outcomes'),('docs/EVIDENCE_MAP_V4.md','Data and evidence map'),('site/v4/transfer.html','42 transfer questions'),('docs/LEARNING_SYSTEM_V3.md','Learning record & migration'),('site/v4/practice.html','150 concept questions'),('site/v4/recall.html','63 delayed-recall questions'),('docs/GLOSSARY.md','Core glossary'),('docs/GLOSSARY_V3.md','Geometry glossary'),('docs/PROOF_ATLAS.md','Core proof atlas'),('docs/GEOMETRY_PROOF_ATLAS_V3.md','Geometry proofs'),('docs/INDEPENDENT_SPATIAL_CAPSTONE_V3.md','Independent capstone'),('optional/README.md','Optional local VGGT'),('docs/SOURCES_V4.md','Checked sources'),('docs/VERIFICATION_V4.md','Verification & limits')]
    nav+='<p class="nav-title">Learning tools</p>'+''.join(f'<a href="{rel(target(p),destination)}">{esc(t)}</a>' for p,t in tools)
    home=rel(ROOT/'START_HERE.html',destination)
    content=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)} | Shape Learning 4.0</title><link rel="stylesheet" href="{rel(ROOT/'site/assets/course.css',destination)}"><style>.search{{display:block;width:100%;font:inherit;padding:12px;border:1px solid var(--line);border-radius:8px;margin:18px 0;background:var(--paper);color:var(--ink)}}.track-label{{margin-top:35px}}.status-note{{font-size:13px;color:var(--muted)}}.answer{{border-top:1px solid var(--line);padding-top:12px;margin-top:12px}}.card-question[hidden]{{display:none}}.breadcrumb{{font-size:13px;margin-bottom:15px}}</style></head><body><div class="layout"><aside class="side"><a class="brand" href="{home}"><small>Independent learning companion · 4.0</small>Listening to Shape<br>Learning System</a><nav aria-label="Course navigation">{nav}</nav></aside><main class="main"><div class="wrap">{body}<footer>Original teaching material, not the book text or an author-endorsed course. Reference execution, learner mastery and real-world validation are different claims. No trained VGGT inference is claimed for the shipped examples. <a href="{home}">Course home</a> · <a href="{rel(target('docs/SOURCES_V4.md'),destination)}">Sources</a> · <a href="{rel(target('docs/VERIFICATION_V4.md'),destination)}">Verification</a></footer></div></main></div>{script}</body></html>'''
    destination.write_text(content,encoding='utf-8')
def rewrite(rendered,source,destination):
    def sub(m):
        attr,quote,url=m.groups();parts=urlsplit(html.unescape(url))
        if parts.scheme or parts.netloc or not parts.path:return m.group(0)
        raw=(source.parent/unquote(parts.path)).resolve();final=MAP.get(raw,raw)
        out=rel(final,destination)
        if parts.query:out+='?'+parts.query
        if parts.fragment:out+='#'+parts.fragment
        return f'{attr}={quote}{esc(out)}{quote}'
    return re.sub(r'(href|src)=([\"\'])(.*?)\2',sub,rendered)
def stage_number(path):
    m=re.search(r'(?:/|^)(\d\d)(?:_|/)',path.relative_to(ROOT).as_posix())
    return int(m.group(1)) if m and int(m.group(1)) in range(21) else None

def build():
    # Existing legacy site is retained. Register all current course documents before rendering links.
    md_paths=sorted(p for p in ROOT.rglob('*.md') if not any(part in {'site','.git','.venv','__pycache__','.pytest_cache'} for part in p.relative_to(ROOT).parts) and not p.name.startswith('COMPLETE_COURSE'))
    nb_paths=sorted([*(ROOT/'notebooks').glob('*.ipynb'),*(ROOT/'consolidation').glob('*.ipynb'),*(ROOT/'practice/answers').glob('*.ipynb'),*(ROOT/'practice/learner').glob('*.ipynb')])
    for source in [*md_paths,*nb_paths]:MAP[source.resolve()]=(ROOT/'site/v4'/source.relative_to(ROOT)).with_suffix('.html')
    for source in md_paths:
        destination=MAP[source.resolve()];text=source.read_text();n=stage_number(source)
        title=next((x.lstrip('# ').strip() for x in text.splitlines() if x.startswith('# ')),source.stem)
        links=f'<a class="button" href="{rel(source,destination)}">Markdown source</a>'
        if n is not None:
            links=f'<a class="button primary" href="{rel(target(f"stages/{n:02d}/README.md"),destination)}">Stage {n:02d} learning section</a>'+links
        body=f'<div class="toolbar"><a class="button" href="{rel(ROOT/"START_HERE.html",destination)}">Course home</a>{links}</div><article>'+rewrite(MD(text),source,destination)+'</article>'
        if source.parts[-3:-1] and source.parent.parent.name=='stages':
            if n is not None:
                prev=f'<a class="button" href="{rel(target(f"stages/{n-1:02d}/README.md"),destination)}">Previous stage</a>' if n else ''
                nxt=f'<a class="button primary" href="{rel(target(f"stages/{n+1:02d}/README.md"),destination)}">Next stage</a>' if n<20 else ''
                body+=f'<div class="pager">{prev}{nxt}</div>'
        shell(title,body,destination,n)
    for source in nb_paths:
        destination=MAP[source.resolve()];n=stage_number(source);learner='learner' in source.parts
        role='Your unexecuted assignment' if learner else 'Executed reference notebook'
        note='The unfinished functions are your exercises. Run their checks after writing your answers. These starter files are intentionally unexecuted.' if learner else 'These are saved reference outputs. Explain and reproduce them, then solve your own exercises. They are not a grade or a model deployment certificate.'
        body=base.notebook_html(source)
        if learner:body=body.replace('Code · executed cell None','Code · your unexecuted assignment')
        body=rewrite(body,source,destination)
        toolbar=f'<div class="toolbar"><a class="button primary" href="{rel(target(f"stages/{n:02d}/README.md"),destination)}">Stage {n:02d} learning section</a><a class="button" href="{rel(source,destination)}">Notebook file</a></div>'
        shell(f'Stage {n:02d}: {role}',toolbar+f'<div class="callout"><p>{esc(note)}</p></div><article>'+body+'</article>',destination,n)
    # Searchable conceptual and delayed-recall libraries: show answer only on demand.
    questions=[]
    for s in CORE:
        for i,(q,a) in enumerate(zip(s['exercises'],s['solutions']),1):questions.append({'id':f'{s["n"]:02d}.Q{i}','stage':s['n'],'question':q,'answer_criteria':a})
    for s in BRIDGE:
        for i,(q,a) in enumerate(zip(s['exercises'],s['answers']),1):questions.append({'id':f'{s["n"]:02d}.Q{i}','stage':s['n'],'question':q,'answer_criteria':a})
    recall=json.loads((ROOT/'practice/retrieval.json').read_text())+json.loads((ROOT/'practice/retrieval_v3.json').read_text())
    transfer=[dict(x,answer_criteria=x['answer']) for x in json.loads((ROOT/'practice/transfer_v4.json').read_text())]
    for name,items,title in [('practice',questions,'150 conceptual questions'),('recall',recall,'63 delayed-recall questions'),('transfer',transfer,'42 independent transfer questions')]:
        cards=''.join(f'<section class="card card-question" data-search="{esc(str(x["stage"])+" "+x["id"]+" "+x["question"])}"><p class="badge">{esc(x["id"])} · Stage {x["stage"]:02d}</p><h2>{esc(x["question"])}</h2><details><summary>Reveal answer criteria after attempting</summary><div class="answer">{MD(str(x["answer_criteria"]))}</div></details></section>' for x in items)
        body=f'<header class="hero"><p class="eyebrow">Attempt · explain · revisit</p><h1>{title}</h1><p class="lead">Recall without the answer open. Mark your evidence in the separate learning log; opening an answer does not assess mastery.</p></header><label for="search">Filter by stage number, exercise ID or words</label><input class="search" id="search" type="search" placeholder="For example: 15, boundary, confidence"><p id="count" class="subtle">{len(items)} questions</p>'+cards
        script='''<script>(()=>{const input=document.getElementById('search');const cards=[...document.querySelectorAll('.card-question')];input.addEventListener('input',()=>{const q=input.value.toLowerCase().trim();let n=0;for(const c of cards){const show=c.dataset.search.toLowerCase().includes(q);c.hidden=!show;if(show)n++;}document.getElementById('count').textContent=n+' matching questions';});})();</script>'''
        shell(title,body,ROOT/f'site/v4/{name}.html',script=script)
    cards=''
    for group,heading in [(CORE,'01 / Foundations of shape'),(BRIDGE,'02 / Geometry, reconstruction and evidence')]:
        cards+=f'<h2 class="track-label">{heading}</h2><div class="grid">'
        for s in group:
            n=s['n'];url=rel(target(f'stages/{n:02d}/README.md'),ROOT/'START_HERE.html')
            short=s.get('subtitle') or 'Learn the concept, inspect the real-data lab, write your own code and demonstrate understanding.'
            cards+=f'<a class="stage-card" href="{url}"><span class="badge">Stage {n:02d}</span><strong>{esc(s["title"])}</strong><p>{esc(short)}</p></a>'
        cards+='</div>'
    home='''<header class="hero"><p class="eyebrow">A complete staged learning system · version 4</p><h1>Understand the idea.<br>Build it yourself.<br>Explain the evidence.</h1><p class="lead">A beginner-first path through topology, persistence and geometry. Each stage connects an explanation, a hand calculation, runnable code, real observations and an independent question.</p></header>'''
    home+=f'<div class="toolbar"><a class="button primary" href="{rel(target("stages/00/README.md"),ROOT/"START_HERE.html")}">Begin Stage 00</a><a class="button" href="{rel(target("docs/START_V4.md"),ROOT/"START_HERE.html")}">Setup & first session</a><a class="button" href="{rel(target("docs/COMPLETION_SYSTEM_V4.md"),ROOT/"START_HERE.html")}">Continue without restarting</a></div>'
    home+='''<div class="stats"><div class="stat"><strong>21</strong><span>Complete learning sections</span></div><div class="stat"><strong>89</strong><span>Write-it-yourself coding exercises</span></div><div class="stat"><strong>63</strong><span>Executed reference notebooks</span></div><div class="stat"><strong>4</strong><span>Bundled real datasets</span></div></div><div class="callout"><p><strong>Start with no assumed topology knowledge.</strong> Six primers cover notation, Python, proofs, linear algebra, calculus and measurement uncertainty. Read saved outputs offline; run the CPU experiments when ready. GPU model inference is optional and has not been executed for the shipped results.</p></div>'''
    home+='<section class="card"><h2>One course, a deeper pass at every stage</h2><p>Version 4 adds 21 guided sessions, 21 consolidation experiments, 42 transfer questions and 84 explicit outcomes. It preserves your existing stage numbers and learning-log format.</p><p>Use the new session for a slower explanation; use independent checks to test the result. Successful reference execution never marks your work complete.</p></section>'
    primerlist=''.join(f'<li><a href="{rel(target(str(p.relative_to(ROOT))),ROOT/"START_HERE.html")}">{esc(p.read_text().splitlines()[0].lstrip("# "))}</a></li>' for p in sorted((ROOT/'foundations').glob('*.md')))
    home+='<section class="card"><h2>The foundations, exactly when you need them</h2><ul>'+primerlist+'</ul><p class="status-note">Each stage: explanation → hand example → code → real data → independent questions → delayed recall.</p></section>'+cards
    shell('The full staged learning system',home,ROOT/'START_HERE.html')
    print(json.dumps({'markdown_pages':len(md_paths),'notebook_pages':len(nb_paths),'concept_cards':len(questions),'recall_cards':len(recall),'stage_sections':len(META),'transfer_cards':len(transfer)},indent=2))
if __name__=='__main__':build()
