"""Local v6 reader: retained course plus case studies, no remote assets or fonts."""
from pathlib import Path
import json,os,re,html
import mistune
import build_reader as base
R=Path(__file__).resolve().parents[1]
MD=mistune.create_markdown(escape=False,plugins=['table','strikethrough','url']);base.MD=MD
from urllib.parse import urlsplit,unquote
MAP={}
STAGES=json.loads((R/'docs/v6/stage_transfer.json').read_text())
DATA=json.loads((R/'data/industries/catalog.json').read_text())['datasets']
def esc(x):return html.escape(str(x),quote=True)
def rel(p,d):return Path(os.path.relpath(p,d.parent)).as_posix()
def dest(p):return MAP.get((R/p).resolve(),R/p)
def st(n):return R/f'site/v6/stages/{n:02d}.html'
def rewrite(rendered,source,destination):
    def sub(m):
        attr,q,url=m.groups();p=urlsplit(html.unescape(url))
        if p.scheme or p.netloc or not p.path:return m.group(0)
        t=(source.parent/unquote(p.path)).resolve();t=MAP.get(t,t)
        return f'{attr}={q}{esc(rel(t,destination)+("?"+p.query if p.query else "")+("#"+p.fragment if p.fragment else ""))}{q}'
    return re.sub(r'(href|src)=(["\'])(.*?)\2',sub,rendered)
def shell(title,body,d,current=None,js=''):
    nav='<p class="nav-title">Begin / continue</p>'
    for p,t in [('docs/v6/START.md','Start and preserve your work'),('docs/v6/BEGINNER_DATA_PRIMER.md','Data from zero'),('docs/v6/DATA_CATALOG.md','Included datasets'),('docs/v6/OPTIONAL_DATA.md','Optional larger datasets'),('docs/v6/STAGE_MAP.md','31-stage transfer map'),('docs/v6/VERIFICATION.md','Evidence and limitations')]:nav+=f'<a href="{rel(dest(p),d)}">{esc(t)}</a>'
    nav+=f'<a href="{rel(R/"site/v6/practice.html",d)}">Case questions and recall</a>'
    nav+='<p class="nav-title">Eight real-data cases</p>'
    for x in DATA:nav+=f'<a href="{rel(dest("industry/lessons/"+x["id"]+".md"),d)}">{esc(x["sector"].replace("_"," ").title())}</a>'
    nav+='<p class="nav-title">Core course · 31 stages</p>'
    for x in STAGES:nav+=f'<a class="{"current" if current==x["stage"] else ""}" href="{rel(st(x["stage"]),d)}"><span class="n">{x["stage"]:02}</span>{esc(x["title"])}</a>'
    content=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} | Listening to Shape v6</title><link rel="stylesheet" href="{rel(R/'site/assets/course.css',d)}"><style>.side{{overflow-y:auto;max-height:100vh}}.table-wrap{{max-width:100%;overflow-x:auto}}.search{{width:100%;padding:12px;font:inherit;margin:12px 0;border:1px solid var(--line);border-radius:8px;background:var(--paper);color:var(--ink)}}[data-search][hidden]{{display:none}}.route{{margin:36px 0}}code{{overflow-wrap:anywhere}}@media(max-width:800px){{.side{{max-height:none}}}}</style></head><body><div class="layout"><aside class="side"><a class="brand" href="{rel(R/'START_HERE.html',d)}"><small>Complete combined course · 6.0</small>Listening to Shape<br>Across industries</a><nav aria-label="Course navigation">{nav}</nav></aside><main class="main"><div class="wrap">{body}<footer>Original introductory course, not the actual book. Required cases run offline on CPU after setup. Reference execution is not learner mastery or deployment validation. <a href="{rel(R/'START_HERE.html',d)}">Home</a> · <a href="{rel(dest('docs/v6/COVERAGE.md'),d)}">Scope and depth</a></footer></div></main></div>{js}</body></html>'''
    d.parent.mkdir(parents=True,exist_ok=True);d.write_text(content)
def article(text,source,d):return rewrite(MD(text),source,d).replace('<table>','<div class="table-wrap"><table>').replace('</table>','</table></div>')
def build():
    # Resolve links to earlier rendered material where available.
    for p in R.rglob('*.md'):
        if any(x in p.relative_to(R).parts for x in ['site','.venv']):continue
        for ver in ['v5','v4','v3','v2']:
            candidate=(R/'site'/ver/p.relative_to(R)).with_suffix('.html')
            if candidate.exists():MAP[p.resolve()]=candidate;break
    for n in range(31):MAP[(R/f'stages/{n:02d}/README.md').resolve()]=st(n)
    for folder,ver in [('notebooks','v4'),('consolidation','v4'),('practice/learner','v4'),('practice/answers','v4'),('physics/notebooks','v5'),('physics/practice/learner','v5'),('physics/practice/answers','v5')]:
        for p in (R/folder).glob('*.ipynb'):MAP[p.resolve()]=(R/'site'/ver/p.relative_to(R)).with_suffix('.html')
    mdpaths=sorted([*(R/'docs/v6').glob('*.md'),*(R/'industry').rglob('*.md'),R/'README.md'])
    mdpaths=[p for p in mdpaths if p.name not in ['README_v5_preserved.md']]
    nbpaths=sorted((R/'industry').rglob('*.ipynb'))
    for p in mdpaths+nbpaths:MAP[p.resolve()]=(R/'site/v6'/p.relative_to(R)).with_suffix('.html')
    for p in mdpaths:
        d=MAP[p.resolve()];txt=p.read_text();title=txt.splitlines()[0].lstrip('# ')
        toolbar=f'<div class="toolbar"><a class="button" href="{rel(R/"START_HERE.html",d)}">Home</a><a class="button" href="{rel(p,d)}">Markdown file</a></div>'
        shell(title,toolbar+'<article>'+article(txt,p,d)+'</article>',d)
    for p in nbpaths:
        d=MAP[p.resolve()];case=p.stem;learner='learner' in p.parts
        label='Your assignment: fill the deliberate missing functions.' if learner else 'Executed reference: explain the result before using it as your answer.'
        toolbar=f'<div class="toolbar"><a class="button" href="{rel(dest("industry/lessons/"+case+".md"),d)}">Case lesson</a><a class="button" href="{rel(p,d)}">Notebook file</a></div>'
        body=base.notebook_html(p)
        if learner:body=body.replace('Code · executed cell None','Code · independent assignment')
        shell(case+' notebook',toolbar+f'<div class="callout"><p>{label}</p></div><article>'+rewrite(body,p,d)+'</article>',d)
    for x in STAGES:
        n=x['stage'];d=st(n);p=R/f'stages/{n:02d}/README.md';guide=R/f'industry/stage_guides/{n:02d}.md'
        tools=f'<div class="toolbar"><a class="button" href="{rel(R/"START_HERE.html",d)}">Home</a><a class="button" href="{rel(dest("industry/lessons/"+x["case"]+".md"),d)}">Related industry case</a><a class="button" href="{rel(p,d)}">Stage Markdown</a></div>'
        body=tools+'<article>'+article(p.read_text(),p,d)+'</article><section class="route"><p class="eyebrow">Transfer the concept · do not replace the foundation</p><article>'+article(guide.read_text(),guide,d)+'</article></section>'
        pager='<div class="toolbar">'
        if n>0:pager+=f'<a class="button" href="{rel(st(n-1),d)}">Previous stage</a>'
        if n<30:pager+=f'<a class="button" href="{rel(st(n+1),d)}">Next stage</a>'
        shell(f'Stage {n:02d}: '+x['title'],body+pager+'</div>',d,n)
    questions=json.loads((R/'industry/concept_questions.json').read_text())+json.loads((R/'industry/retrieval.json').read_text())
    practice=R/'site/v6/practice.html'
    cards=''.join(f'<section class="card question" data-search="{esc(q["id"]+" "+q["question"])}"><p class="badge">{esc(q["id"])}</p><h2>{esc(q["question"])}</h2><details><summary>Reveal criteria after attempting</summary><div class="answer">{MD(q["answer"])}</div></details></section>' for q in questions)
    jsq='''<script>(()=>{const input=document.querySelector('#search'),cards=[...document.querySelectorAll('[data-search]')];input.addEventListener('input',()=>{const q=input.value.toLowerCase().trim();let n=0;for(const c of cards){c.hidden=!c.dataset.search.toLowerCase().includes(q);if(!c.hidden)n++;}document.querySelector('#count').textContent=n+' matching prompts';});})();</script>'''
    shell('Industry practice and recall','<header class="hero"><p class="eyebrow">Explain before revealing</p><h1>Practice across industries.</h1><p class="lead">32 conceptual questions and 24 delayed-recall prompts. These reuse the case questions; they are not additional counted exercises.</p></header><label for="search">Filter by case or concept</label><input id="search" type="search" class="search" placeholder="Try wine.Q2 or co2"><p id="count">56 prompts</p>'+cards,practice,js=jsq)
    d=R/'START_HERE.html'
    body='''<header class="hero"><p class="eyebrow">Read · predict · calculate · code · explain</p><h1>Learn the shape.<br>Test the evidence.<br>Transfer the idea.</h1><p class="lead">A complete beginner-first course in topology, geometry and scientific machine learning, with eight new real-data cases across industries.</p></header>'''
    body+=f'<div class="toolbar"><a class="button primary" href="{rel(st(0),d)}">New learner: Stage 00</a><a class="button" href="{rel(dest("docs/v6/START.md"),d)}">Continue / set up / preserve work</a><a class="button" href="{rel(dest("docs/v6/DATA_CATALOG.md"),d)}">Explore the included data</a></div>'
    body+='''<div class="stats"><div class="stat"><strong>31 + 8</strong><span>Core stages + case sections</span></div><div class="stat"><strong>99</strong><span>Executed reference notebooks</span></div><div class="stat"><strong>143</strong><span>Independent coding activities</span></div><div class="stat"><strong>13</strong><span>Included observed sources</span></div></div><div class="callout"><p><strong>Begin without prior subject knowledge.</strong> Nine primers support the course. Read saved outputs without installing software. Run the small industry cases on CPU after setup; no dataset download is required. Optional larger datasets are clearly separate acquisition plans.</p></div>'''
    body+=f'<section class="card"><h2>One idea, two contexts—not eight courses at once</h2><p>Complete the core lesson, then use its transfer guide. At first inspect a table and calculate a simple quantity; return to the advanced topology cells after their prerequisites. Preserve your existing stage record. Reference outputs do not grade your learning.</p><div class="toolbar"><a class="button" href="{rel(dest("docs/v6/BEGINNER_DATA_PRIMER.md"),d)}">Data and statistics from zero</a><a class="button" href="{rel(dest("docs/v6/STAGE_MAP.md"),d)}">Concept-to-case map</a></div></section>'
    body+='<h2>Choose a real-data case</h2><label for="search">Filter cases and stages</label><input id="search" class="search" type="search" placeholder="Try wine, homology, time, camera or uncertainty"><p id="count" aria-live="polite">39 learning sections</p><div class="grid">'
    for x in DATA:
        body+=f'<a class="stage-card" data-search="{esc(x["id"]+" "+x["sector"]+" "+x["title"])}" href="{rel(dest("industry/lessons/"+x["id"]+".md"),d)}"><span class="badge">{esc(x["sector"].replace("_"," "))}</span><strong>{esc(x["title"])}</strong><p>{x["rows"]:,} snapshot rows · provenance, units, code and limitations</p></a>'
    body+='</div><h2>The full staged course</h2><div class="grid">'
    for x in STAGES:
        body+=f'<a class="stage-card" data-search="{esc(str(x["stage"])+" "+x["title"]+" "+x["focus"])}" href="{rel(st(x["stage"]),d)}"><span class="badge">Stage {x["stage"]:02d}</span><strong>{esc(x["title"])}</strong><p>{esc(x["focus"])}</p></a>'
    body+='</div>'
    body+=f'<section class="card"><h2>Evidence before a conclusion</h2><p>The 99 reference notebooks were rerun. Data hashes, time support, traveler groups and mathematical properties are checked. Ripser/GUDHI remain optional unexecuted comparisons. Linux CPU execution does not establish Mac, Windows, GPU or clinical validation.</p><div class="toolbar"><a class="button" href="{rel(dest("docs/v6/VERIFICATION.md"),d)}">Read verification</a><a class="button" href="{rel(dest("docs/v6/SOURCE_AUDIT.md"),d)}">Read source audit</a><a class="button" href="{rel(dest("docs/v6/OPTIONAL_DATA.md"),d)}">Plan the next dataset</a></div></section>'
    js='''<script>(()=>{const input=document.querySelector('#search'),cards=[...document.querySelectorAll('[data-search]')];input.addEventListener('input',()=>{const q=input.value.trim().toLowerCase();let n=0;for(const c of cards){c.hidden=!c.dataset.search.toLowerCase().includes(q);if(!c.hidden)n++;}document.querySelector('#count').textContent=n+' matching learning sections';});})();</script>'''
    shell('Start here',body,d,js=js)
    # A small banner distinguishes historical readers from the current path.
    for p in (R/'site').rglob('*.html'):
        if 'v6' in p.relative_to(R/'site').parts:continue
        t=p.read_text();t=re.sub(r'<div id="v6-banner".*?</div>','',t,flags=re.S)
        banner=f'<div id="v6-banner" style="padding:12px;border-bottom:1px solid currentColor;font:14px system-ui"><a href="{rel(R/"START_HERE.html",p)}">Current v6 course home</a> · Earlier lesson retained; current verification and industry transfer guides are on the v6 home.</div>'
        t=re.sub(r'(<body[^>]*>)',r'\1'+banner,t,count=1);p.write_text(t)
    print('Built v6 reader: 31 current stage pages, eight case tracks and preserved legacy readers.')
if __name__=='__main__':build()
