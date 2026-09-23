"""Build an offline v5 entry point without discarding the v4 reader.

All new Markdown and notebooks are rendered locally. No font/model/network
requests. Old stage pages remain available and receive an explicit v5 banner.
"""
from pathlib import Path
import json,os,html,re
from urllib.parse import urlsplit,unquote
import mistune
import build_reader as base
R=Path(__file__).resolve().parents[1]
MD=mistune.create_markdown(escape=False,plugins=['table','strikethrough','url']);base.MD=MD
CORE=json.loads((R/'docs/stage_metadata.json').read_text())
BRIDGE=json.loads((R/'docs/bridge_metadata.json').read_text())
NEW=json.loads((R/'docs/v5/stage_metadata.json').read_text())
ALL=[{'stage':s['n'],'title':s['title']} for s in CORE+BRIDGE]+NEW
MAP={}
def esc(x):return html.escape(str(x),quote=True)
def rel(p,d):return Path(os.path.relpath(p,d.parent)).as_posix()
def target(p):return MAP.get((R/p).resolve(),R/p)
def stage_target(n):return R/f'site/{"v4" if n<21 else "v5"}/stages/{n:02d}/README.html'

def shell(title,body,dest,current=None,script=''):
    nav=''
    for s in ALL:
        n=s['stage']
        if n in [0,13,21]:nav+=f'<p class="nav-title">{ {0:"Shape foundations · 00–12",13:"Spatial geometry · 13–20",21:"Physics and learning · 21–30"}[n]}</p>'
        nav+=f'<a class="{"current" if n==current else ""}" href="{rel(stage_target(n),dest)}"><span class="n">{n:02d}</span>{esc(s["title"])}</a>'
    tools=[('docs/v5/START.md','Start / preserve your work'),('docs/v5/COVERAGE.md','Coverage and depth'),('docs/v5/SOURCE_AUDIT.md','The four source posts, checked'),('docs/v5/SOURCES.md','Free primary readings'),('docs/v5/CONCEPT_GLOSSARY.md','New concept glossary'),('docs/v5/VERIFICATION.md','Verification and limits')]
    nav+='<p class="nav-title">Learning tools</p>'+''.join(f'<a href="{rel(target(p),dest)}">{esc(label)}</a>' for p,label in tools)
    home=rel(R/'START_HERE.html',dest)
    styles='''.search{width:100%;padding:12px;font:inherit;margin:12px 0 18px;border:1px solid var(--line);border-radius:8px;background:var(--paper);color:var(--ink)}.stage-card[hidden],.question[hidden]{display:none}.question{margin-bottom:18px}.answer{padding-top:12px}.table-wrap{max-width:100%;overflow-x:auto}code{overflow-wrap:anywhere}.route{margin-top:36px}.route p{max-width:72ch}.scope{font-size:14px}.side{overflow-y:auto;max-height:100vh}h1{overflow-wrap:anywhere}@media(max-width:800px){.side{max-height:none}}'''
    content=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} | Shape Learning 5</title><link rel="stylesheet" href="{rel(R/'site/assets/course.css',dest)}"><style>{styles}</style></head><body><div class="layout"><aside class="side"><a class="brand" href="{home}"><small>Independent learning companion · 5.0</small>Listening to Shape<br>Learning System</a><nav aria-label="Course navigation">{nav}</nav></aside><main class="main"><div class="wrap">{body}<footer>Original course material, not the actual book text or an endorsed course. Mathematical checks, manufactured experiments, empirical validation and learner mastery are separate. <a href="{home}">Course home</a> · <a href="{rel(target('docs/v5/COVERAGE.md'),dest)}">Implementation depth</a></footer></div></main></div>{script}</body></html>'''
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(content)

def rewrite(rendered,source,destination):
    def sub(m):
        attr,q,url=m.groups();p=urlsplit(html.unescape(url))
        if p.scheme or p.netloc or not p.path:return m.group(0)
        source_target=(source.parent/unquote(p.path)).resolve()
        final=MAP.get(source_target,source_target)
        url=rel(final,destination)+(('?' +p.query) if p.query else '')+(('#'+p.fragment) if p.fragment else '')
        return f'{attr}={q}{esc(url)}{q}'
    return re.sub(r'(href|src)=(["\'])(.*?)\2',sub,rendered)

def build():
    for p in R.rglob('*.md'):
        if 'site' in p.relative_to(R).parts:
            continue
        legacy=(R/'site/v4'/p.relative_to(R)).with_suffix('.html')
        if legacy.is_file():
            MAP[p.resolve()]=legacy
    for n in range(21):MAP[(R/f'stages/{n:02d}/README.md').resolve()]=stage_target(n)
    mdpaths=sorted([*(R/'docs/v5').glob('*.md'),*(R/'physics/lessons').glob('*.md'),*(R/'physics/solutions').glob('*.md'),*(R/'foundations').glob('0[78]*.md'),*[R/f'stages/{n}/README.md' for n in range(21,31)]])
    nbpaths=sorted([*(R/'physics/notebooks').glob('*.ipynb'),*(R/'physics/practice/learner').glob('*.ipynb'),*(R/'physics/practice/answers').glob('*.ipynb')])
    for p in mdpaths+nbpaths:MAP[p.resolve()]=(R/'site/v5'/p.relative_to(R)).with_suffix('.html')
    old_notebooks=sorted([*(R/'notebooks').glob('*.ipynb'),*(R/'consolidation').glob('*.ipynb'),*(R/'practice/learner').glob('*.ipynb'),*(R/'practice/answers').glob('*.ipynb')])
    for p in old_notebooks:MAP[p.resolve()]=(R/'site/v4'/p.relative_to(R)).with_suffix('.html')
    nbpaths=old_notebooks+nbpaths
    for source in mdpaths:
        dest=MAP[source.resolve()];text=source.read_text();title=text.splitlines()[0].lstrip('# ')
        m=re.search(r'(?:/)(2[1-9]|30)(?:_|/|\.md)',str(source));n=int(m[1]) if m else None
        rendered=rewrite(MD(text),source,dest).replace('<table>','<div class="table-wrap"><table>').replace('</table>','</table></div>')
        body=f'<div class="toolbar"><a class="button" href="{rel(R/"START_HERE.html",dest)}">Home</a><a class="button" href="{rel(source,dest)}">Markdown file</a></div><article>{rendered}</article>'
        shell(title,body,dest,n)
    for source in nbpaths:
        dest=MAP[source.resolve()];n=int(source.name[:2]);learner='learner' in source.parts
        role='Your coding assignment' if learner else 'Executed reference notebook'
        note='Functions are intentionally unfinished. Write your own implementation, then run the checks.' if learner else 'Saved outputs are evidence of reference execution, not your grade or empirical deployment validation.'
        body=base.notebook_html(source)
        if learner:body=body.replace('Code · executed cell None','Code · your assignment')
        body=f'<div class="toolbar"><a class="button" href="{rel(stage_target(n),dest)}">Stage {n}</a><a class="button" href="{rel(source,dest)}">Notebook file</a></div><div class="callout"><p>{note}</p></div><article>'+rewrite(body,source,dest)+'</article>'
        shell(f'Stage {n}: {role}',body,dest,n)
    questions=[]
    for s in NEW:
        for family,key in [('Q','questions'),('R','recall')]:
            questions += [{'id':f'{s["stage"]}.{family}{i+1}','question':q,'answer':a} for i,(q,a) in enumerate(s[key])]
    cards=''.join(f'<section class="card question" data-search="{esc(q["id"]+" "+q["question"])}"><p class="badge">{q["id"]}</p><h2>{esc(q["question"])}</h2><details><summary>Reveal criteria after attempting</summary><div class="answer">{MD(q["answer"])}</div></details></section>' for q in questions)
    script='''<script>(()=>{const input=document.querySelector('#search');const cards=[...document.querySelectorAll('[data-search]')];input.addEventListener('input',()=>{const q=input.value.toLowerCase().trim();let n=0;for(const c of cards){const ok=c.dataset.search.toLowerCase().includes(q);c.hidden=!ok;if(ok)n++;}document.querySelector('#count').textContent=n+' matching entries';});})();</script>'''
    body='<header class="hero"><p class="eyebrow">Explain · derive · remember</p><h1>Physics practice and recall</h1><p class="lead">60 conceptual questions and 30 delayed-recall prompts. Answer first; opening a solution does not mark progress.</p></header><label for="search">Filter by concept or ID</label><input id="search" class="search" type="search" placeholder="Try 24.Q1 or projection"><p id="count">90 entries</p>'+cards
    shell('Physics practice and recall',body,R/'site/v5/practice.html',script=script)
    home='''<header class="hero"><p class="eyebrow">Complete combined course · version 5</p><h1>Learn shape.<br>Understand motion.<br>Test every claim.</h1><p class="lead">A beginner-first path through topology, geometry and scientific machine learning. Preserve your earlier work; the new physics track builds on it.</p></header>'''
    home+=f'<div class="toolbar"><a class="button primary" href="{rel(stage_target(0),R/"START_HERE.html")}">New learner: begin Stage 00</a><a class="button" href="{rel(target("docs/v5/START.md"),R/"START_HERE.html")}">Continue / setup / migrate</a><a class="button" href="{rel(target("docs/v5/SOURCE_AUDIT.md"),R/"START_HERE.html")}">Read the source audit</a></div>'
    home+='''<div class="stats"><div class="stat"><strong>31</strong><span>Stage learning sections</span></div><div class="stat"><strong>83</strong><span>Reference notebooks</span></div><div class="stat"><strong>119</strong><span>Coding exercises</span></div><div class="stat"><strong>5</strong><span>Real data sources</span></div></div><div class="callout"><p><strong>You do not need to know the subject already.</strong> Eight primers support the lessons. Predict a result, calculate it, run it, and explain its limits. Saved outputs can be read offline. Neural examples use CPU PyTorch, not a GPU.</p></div>'''
    home+=f'<section class="card"><h2>The new ideas are tested, not just repeated</h2><p>Work through Hamiltonian and Lagrangian models, symplectic integration, constraints, PINNs, gradient conflicts and neural operators. Keep continuous equations, numerical updates and measured validation distinct.</p><p><a href="{rel(target("docs/v5/COVERAGE.md"),R/"START_HERE.html")}">See which concepts are implemented and which require deeper study</a> · <a href="site/v5/practice.html">Practice the new questions</a></p><p class="scope">Full paper benchmarks, trained VGGT inference and independent sports/clinical/climate validation are not claimed. The actual book text remains unaudited.</p></section>'
    home+='<label for="search">Find a stage by number or concept</label><input id="search" class="search" type="search" placeholder="Try 06, homology, gradient, or Hamiltonian"><p id="count">31 stages</p>'
    groups=[(0,13,'01 / Learn the language of shape'),(13,21,'02 / Geometry, cameras and spatial evidence'),(21,31,'03 / Dynamics, constraints and scientific learning')]
    for lo,hi,title in groups:
        home+=f'<section class="route"><h2>{title}</h2><div class="grid">'
        for s in ALL[lo:hi]:
            n=s['stage'];blurb='Read → calculate → run → practice → assess.' if n<21 else s['data_role']
            home+=f'<a class="stage-card" data-search="{esc(str(n)+" "+s["title"])}" href="{rel(stage_target(n),R/"START_HERE.html")}"><span class="badge">Stage {n:02d}</span><strong>{esc(s["title"])}</strong><p>{esc(blurb)}</p></a>'
        home+='</div></section>'
    home+='<section class="card"><h2>Reference work is not your assessment</h2><p>All 31 learning stages start unassessed in the fresh log. Migrate your older evidence to resume without losing attempts. The CLI records evidence and calculates review dates; it does not certify proofs or run background reminders.</p></section>'
    shell('The complete staged learning system',home,R/'START_HERE.html',script=script)
    # Make the transition from the preserved geometry track visible.
    for n in range(21):
        p=stage_target(n)
        if p.exists():
            text=p.read_text();text=re.sub(r'<!-- V5BANNER -->.*?<!-- /V5BANNER -->','',text,flags=re.S)
            banner=f'<!-- V5BANNER --><div class="callout"><p>Preserved foundation/geometry stage in the complete v5 course. <a href="{rel(R/"START_HERE.html",p)}">All 31 stages</a> · <a href="{rel(stage_target(21),p)}">Physics continuation, Stage 21</a></p></div><!-- /V5BANNER -->'
            text=text.replace('<div class="wrap">','<div class="wrap">'+banner,1);p.write_text(text)
    print(json.dumps({'new_markdown_pages':len(mdpaths),'refreshed_notebook_pages':len(nbpaths),'stage_cards':31,'question_cards':len(questions)},indent=2))
if __name__=='__main__':build()
