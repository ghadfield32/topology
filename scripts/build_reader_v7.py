"""Offline v7 reader: stage entry guides, complete source lessons and saved notebooks."""
from pathlib import Path
import json,os,re,html
from urllib.parse import urlsplit,unquote
import mistune
import build_reader as base
R=Path(__file__).resolve().parents[1]
MD=mistune.create_markdown(escape=False,plugins=['table','strikethrough','url']);base.MD=MD
MAP={}
STAGES=json.loads((R/'docs/v7/beginner_map.json').read_text())
NEW=json.loads((R/'docs/v7/new_sections.json').read_text())
OLD=json.loads((R/'data/industries/catalog.json').read_text())['datasets']
def esc(x):return html.escape(str(x),quote=True)
def rel(p,d):return Path(os.path.relpath(p,d.parent)).as_posix()
def dest(p):return MAP.get((R/p).resolve(),R/p)
def rewrite(body,source,d):
 def sub(m):
    attr,q,url=m.groups();u=urlsplit(html.unescape(url))
    if u.scheme or u.netloc or not u.path:return m.group(0)
    t=(source.parent/unquote(u.path)).resolve();t=MAP.get(t,t)
    return f'{attr}={q}{esc(rel(t,d)+("?"+u.query if u.query else "")+("#"+u.fragment if u.fragment else ""))}{q}'
 return re.sub(r'(href|src)=("|\')(.*?)\2',sub,body)
def article(text,source,d):return rewrite(MD(text),source,d).replace('<table>','<div class="table-wrap"><table>').replace('</table>','</table></div>')
EXTRA='''.side{overflow:auto}.side nav a{font-size:12px}.search{display:block;width:100%;padding:13px;background:var(--paper);color:var(--ink);border:1px solid var(--line);border-radius:8px;font:inherit;margin:10px 0}[data-search][hidden]{display:none}.entry-links{display:flex;gap:8px;flex-wrap:wrap}input[type=range]{width:100%;max-width:500px}code{overflow-wrap:anywhere}pre code{overflow-wrap:normal}.answer{padding-top:10px}.experiment-grid{display:grid;grid-template-columns:260px 1fr;gap:20px;align-items:center}.experiment-grid svg{width:100%;height:auto}.tip{font-size:14px;color:var(--muted)}@media(max-width:760px){.experiment-grid{grid-template-columns:1fr}.experiment-grid svg{max-width:270px;margin:auto}}'''
def shell(title,body,d,js=''):
 nav='<p class="nav-title">Your learning route</p>'
 for p,t in [('docs/v7/START.md','Start / preserve your work'),('docs/v7/LEARNING_ROUTE.md','Full learning route'),('docs/v7/UNCERTAINTY_PRIMER.md','Evidence from zero'),('docs/v7/DATA_CATALOG.md','15 observed sources'),('docs/v7/COVERAGE.md','Scope and mastery'),('docs/v7/VERIFICATION.md','Verification and limits'),('docs/v7/SOURCE_AUDIT.md','Source claims vs checks')]:nav+=f'<a href="{rel(dest(p),d)}">{t}</a>'
 nav+=f'<a href="{rel(R/"site/v7/practice.html",d)}">New practice / recall</a><p class="nav-title">New real-data & methods labs</p>'
 for s in NEW:nav+=f'<a href="{rel(dest(s["path"]+"/lesson.md"),d)}">{esc(s["title"])}</a>'
 nav+='<p class="nav-title">31 core stages</p>'
 for s in STAGES:nav+=f'<a href="{rel(dest(s["guide"]),d)}"><span class="n">{s["stage"]:02d}</span>{esc(s["title"])}</a>'
 out=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} | Listening to Shape v7</title><link rel="stylesheet" href="{rel(R/'site/assets/course.css',d)}"><style>{EXTRA}</style></head><body><div class="layout"><aside class="side"><a class="brand" href="{rel(R/'START_HERE.html',d)}"><small>Beginner to independent evidence</small>Listening to Shape<br>Learning Lab · v7</a><nav aria-label="Course navigation">{nav}</nav></aside><main class="main"><div class="wrap">{body}<footer>Original learning companion, not the full book or professional certification. Reference execution is not learner mastery. All new required data are bundled; external readings require internet. <a href="{rel(R/'START_HERE.html',d)}">Home</a> · <a href="{rel(dest('docs/v7/VERIFICATION.md'),d)}">Current verification</a></footer></div></main></div>{js}</body></html>'''
 d.parent.mkdir(parents=True,exist_ok=True);d.write_text(out)
SEARCH='''<script>(()=>{const input=document.querySelector('#search');if(!input)return;const cards=[...document.querySelectorAll('[data-search]')];input.addEventListener('input',()=>{const q=input.value.trim().toLowerCase();let count=0;for(const c of cards){c.hidden=!c.dataset.search.toLowerCase().includes(q);if(!c.hidden)count++;}document.querySelector('#count').textContent=count+' matching sections';});})();</script>'''
EXPLORER='''<section class="card"><p class="eyebrow">One exact example · no setup</p><h2>When does a square have a loop?</h2><p>Four points at the corners of a unit square. An edge enters when its length is at most the threshold. Triangles enter when all their edges do. This is an exact constructed control, not observed data.</p><div class="experiment-grid"><svg viewBox="0 0 240 240" role="img" aria-label="A unit-square Rips filtration"><polygon id="square-fill" points="40,40 200,40 200,200 40,200" fill="currentColor" opacity="0.12" visibility="hidden"/><g id="square-edges" stroke="currentColor" stroke-width="2"></g><g fill="currentColor"><circle cx="40" cy="40" r="5"/><circle cx="200" cy="40" r="5"/><circle cx="200" cy="200" r="5"/><circle cx="40" cy="200" r="5"/></g><g fill="currentColor" font-size="13"><text x="20" y="30">(0,1)</text><text x="175" y="30">(1,1)</text><text x="175" y="225">(1,0)</text><text x="20" y="225">(0,0)</text></g></svg><div><label for="threshold">Edge-distance threshold: <output id="threshold-value">0.80</output></label><input id="threshold" type="range" min="0" max="1.6" step=".01" value=".8"><p id="square-result" aria-live="polite"></p><p class="tip">At 1 the perimeter appears. At √2 ≈ 1.4142 the diagonals and triangles fill the loop. Shading is schematic; it does not display higher-dimensional simplices.</p></div></div></section>'''
SQUARE_JS='''<script>(()=>{const slider=document.querySelector('#threshold');if(!slider)return;const vertices=[[40,40],[200,40],[200,200],[40,200]],pairs=[[0,1,1],[1,2,1],[2,3,1],[3,0,1],[0,2,Math.SQRT2],[1,3,Math.SQRT2]];function draw(){const e=Number(slider.value);document.querySelector('#threshold-value').textContent=e.toFixed(2);const g=document.querySelector('#square-edges');g.replaceChildren();for(const [a,b,length] of pairs){if(e<length)continue;const line=document.createElementNS('http://www.w3.org/2000/svg','line');line.setAttribute('x1',vertices[a][0]);line.setAttribute('y1',vertices[a][1]);line.setAttribute('x2',vertices[b][0]);line.setAttribute('y2',vertices[b][1]);g.appendChild(line);}const filled=e>=Math.SQRT2;document.querySelector('#square-fill').setAttribute('visibility',filled?'visible':'hidden');document.querySelector('#square-result').textContent='Components (β₀): '+(e<1?4:1)+' · Independent loops (β₁): '+(e>=1&&!filled?1:0)+'.';}slider.addEventListener('input',draw);draw();})();</script>'''
def build():
 mdpaths=[]
 for p in R.rglob('*.md'):
    relative=p.relative_to(R)
    if 'site' in relative.parts or 'reports' in relative.parts or 'preserved' in p.name.lower() or p.name.startswith('COMPLETE_COURSE') or p.name=='COURSE_GUIDE.md' or p.name in ['BUILD_PLAN.md','BUILD_REVIEW.md','DESIGN.md']:continue
    mdpaths.append(p)
 nbpaths=sorted(p for p in R.rglob('*.ipynb') if 'site' not in p.relative_to(R).parts and '.ipynb_checkpoints' not in p.parts)
 for p in mdpaths+nbpaths:MAP[p.resolve()]=(R/'site/v7'/p.relative_to(R)).with_suffix('.html')
 for p in mdpaths:
    d=MAP[p.resolve()];txt=p.read_text();title=next((x.lstrip('# ') for x in txt.splitlines() if x.strip()),p.stem)
    toolbar=f'<div class="toolbar"><a class="button" href="{rel(R/"START_HERE.html",d)}">Home</a><a class="button" href="{rel(p,d)}">Markdown source</a></div>'
    if 'beginner_v7' in p.parts:
        n=int(p.parent.name);toolbar+=f'<div class="toolbar"><a class="button primary" href="{rel(dest(f"stages/{n:02d}/README.md"),d)}">Full Stage {n:02d}</a>'
        if n>0:toolbar+=f'<a class="button" href="{rel(dest(f"beginner_v7/{n-1:02d}/lesson.md"),d)}">Previous entry</a>'
        if n<30:toolbar+=f'<a class="button" href="{rel(dest(f"beginner_v7/{n+1:02d}/lesson.md"),d)}">Next entry</a>'
        toolbar+='</div>'
    # Old verification pages remain visible but explicitly historical.
    note=''
    if 'VERIFICATION' in p.name and 'v7' not in p.parts:note='<div class="callout"><p>Historical verification record. Use the current v7 report for this archive’s executed checks and limitations.</p></div>'
    shell(title,toolbar+note+'<article>'+article(txt,p,d)+'</article>',d)
 for p in nbpaths:
    d=MAP[p.resolve()];learner='learner' in p.parts or p.name=='learner.ipynb'
    note='Independent assignment: deliberate missing functions are yours to implement.' if learner else 'Executed reference. Explain and modify it before treating it as your own independent solution.'
    toolbar=f'<div class="toolbar"><a class="button" href="{rel(R/"START_HERE.html",d)}">Home</a><a class="button" href="{rel(p,d)}">Notebook file</a></div>'
    if (p.parent/'lesson.md').exists():toolbar+=f'<a class="button" href="{rel(dest(str((p.parent/"lesson.md").relative_to(R))),d)}">Lesson and data context</a>'
    body=base.notebook_html(p)
    if learner:body=body.replace('Code · executed cell None','Code · independent assignment')
    shell(p.stem+' notebook',toolbar+f'<div class="callout"><p>{note}</p></div><article>'+rewrite(body,p,d)+'</article>',d)
 d=R/'site/v7/practice.html';questions=json.loads((R/'docs/v7/questions.json').read_text())
 cards=''.join(f'<section class="card" data-search="{esc(q["id"]+" "+q["question"])}"><p class="eyebrow">{esc(q["id"])}</p><h2>{esc(q["question"])}</h2><details><summary>Reveal criteria after attempting</summary><div class="answer">{MD(q["answer"])}</div></details></section>' for q in questions)
 shell('New questions and delayed recall','<header class="hero"><p class="eyebrow">Try · explain · then reveal</p><h1>Practice the transfer.</h1><p class="lead">24 conceptual questions and 12 delayed-recall prompts from the four new sections. These cards reuse the written questions, not additional counted exercises.</p></header><label for="search">Filter questions</label><input id="search" class="search" type="search" placeholder="Try seeds, radius, gradients"><p id="count">36 prompts</p>'+cards,d,SEARCH)
 d=R/'START_HERE.html';body='''<header class="hero"><p class="eyebrow">One foundation · Many domains · Traceable evidence</p><h1>Learn the shape.<br>Understand the result.</h1><p class="lead">Start with no subject background. Build from a hand calculation to tested code, observed data and a conclusion you can defend.</p></header>'''
 body+=f'<div class="toolbar"><a class="button primary" href="{rel(dest("beginner_v7/00/lesson.md"),d)}">Begin Stage 00</a><a class="button" href="{rel(dest("docs/v7/START.md"),d)}">Continue / set up / preserve work</a><a class="button" href="{rel(dest("docs/v7/DATA_CATALOG.md"),d)}">Explore the data</a></div>'
 body+='''<div class="stats"><div class="stat"><strong>31</strong><span>Core stages with entry guides</span></div><div class="stat"><strong>10 + 2</strong><span>Industry cases + new methods labs</span></div><div class="stat"><strong>107</strong><span>Executed reference notebooks</span></div><div class="stat"><strong>15</strong><span>Included observed data sources</span></div></div><div class="callout"><p><strong>One stage at a time.</strong> Read → predict → calculate → run → explain → solve independently → revisit. New entry guides supplement, not replace, the original full-stage lessons and practice. Industry cases are parallel applications, not ten extra prerequisites.</p></div>'''
 body+=EXPLORER
 body+='<h2>New real-data and evidence laboratories</h2><div class="grid">'
 for s in NEW:
    body+=f'<a class="stage-card" href="{rel(dest(s["path"]+"/lesson.md"),d)}"><span class="badge">{s["type"]} · four coding exercises</span><strong>{esc(s["title"])}</strong><p>Lesson, worked lab, learner code, reference answers and interpretation.</p></a>'
 body+='</div><h2>Choose your next stage or industry</h2><label for="search">Filter by topic or domain</label><input id="search" class="search" type="search" placeholder="Try homology, camera, physics, seeds or transport"><p id="count">41 stage and industry links</p><div class="grid">'
 for s in STAGES:
    body+=f'<a class="stage-card" data-search="{esc(str(s["stage"])+" "+s["title"]+" "+s["vocabulary"])}" href="{rel(dest(s["guide"]),d)}"><span class="badge">Stage {s["stage"]:02d}</span><strong>{esc(s["title"])}</strong><p>{esc(s["question"])}</p></a>'
 for s in OLD:
    body+=f'<a class="stage-card" data-search="{esc(s["id"]+" "+s["sector"]+" "+s["title"])}" href="{rel(dest("industry/lessons/"+s["id"]+".md"),d)}"><span class="badge">Industry · retained</span><strong>{esc(s["title"])}</strong><p>{s["rows"]} source-format rows · read the observation-unit definition.</p></a>'
 for s in NEW[:2]:body+=f'<a class="stage-card" data-search="{esc(s["id"]+" "+s["title"])}" href="{rel(dest(s["path"]+"/lesson.md"),d)}"><span class="badge">Industry · new</span><strong>{esc(s["title"])}</strong><p>New official-source numeric snapshot with acquisition limitations stated.</p></a>'
 body+='</div>'
 body+=f'<section class="card"><h2>Read the evidence before adopting a result</h2><p>The new UCI tables were transcribed from complete official web-retrieved numeric text because direct container downloads failed. Local integrity checks do not replace independent provider verification. Optional Ripser/GUDHI comparisons and trained VGGT inference are not claimed as completed. The actual book audit remains open.</p><div class="toolbar"><a class="button" href="{rel(dest("docs/v7/VERIFICATION.md"),d)}">Current verification</a><a class="button" href="{rel(dest("docs/v7/SOURCE_AUDIT.md"),d)}">Claims and sources</a><a class="button" href="{rel(dest("docs/v7/UNCERTAINTY_PRIMER.md"),d)}">Uncertainty from zero</a><a class="button" href="{rel(R/"site/v7/practice.html",d)}">Practice / recall</a></div></section>'
 shell('Start here',body,d,SEARCH+SQUARE_JS)
 # Reword old banners without altering historical lesson claims or report values.
 for p in (R/'site').rglob('*.html'):
    if 'v7' in p.relative_to(R/'site').parts:continue
    text=p.read_text();text=re.sub(r'Current v[2-6] course home','Current course home',text)
    p.write_text(text)
 (R/'reports/v7/reader_build.json').write_text(json.dumps({'markdown_pages':len(mdpaths),'notebook_pages':len(nbpaths),'new_reference_count':8,'core_entry_pages':31,'observed_sources':15,'industry_cases':10,'methods_labs':2},indent=2))
 print('Reader built:',len(mdpaths),'Markdown pages;',len(nbpaths),'notebook pages.')
if __name__=='__main__':build()
