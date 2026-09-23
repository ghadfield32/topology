"""Build one offline rendering per retained source; old render paths become aliases.

Source lessons are never changed by this script. The manifest identifies the
single primary lesson per stage; optional practice is not another required text.
"""
from pathlib import Path
from urllib.parse import urlsplit, unquote, quote
import html,json,os,re,hashlib
import mistune
import nbformat
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1]
OUT=R/'reader'
MD=mistune.create_markdown(escape=False,plugins=['table','strikethrough','url'])
SKIP={'.venv','venv','.uv-cache','build','dist','node_modules','site','reader','reports','.git','.pytest_cache','__pycache__','my_work','.ipynb_checkpoints'}
CAT=json.loads((R/'curriculum/catalog.json').read_text())
MAP={};ALIASES={};stats={}
def esc(x):return html.escape(str(x),quote=True)
def relative(p,parent):return Path(os.path.relpath(p,parent)).as_posix()
def destination(p):return OUT/(p.relative_to(R).as_posix()+'.html')
def slug(s):
 s=html.unescape(s).strip().lower();return re.sub(r'[^\w\s-]','',s).replace(' ','-')
def rewrite(body,source,d):
 def sub(m):
  attr,q,url=m.groups();u=urlsplit(html.unescape(url))
  if u.scheme or u.netloc or not u.path:return m.group(0)
  target=(source.parent/unquote(u.path)).resolve()
  target=MAP.get(target,ALIASES.get(target,target))
  out=relative(target,d.parent)+('?' +u.query if u.query else '')+('#'+u.fragment if u.fragment else '')
  return f'{attr}={q}{esc(out)}{q}'
 return re.sub(r'(href|src)=("|\')(.*?)\2',sub,body)
def article(text,source,d):
 b=BeautifulSoup(MD(text),'html.parser');seen={}
 for h in b.find_all(re.compile('^h[1-6]$')):
  id=slug(h.get_text());n=seen.get(id,0);seen[id]=n+1;h['id']=id+(f'-{n}' if n else '')
 for tag in b.find_all(['script','iframe']):tag.decompose()
 return rewrite(str(b),source,d)
CSS='''
:root{color-scheme:dark;--bg:#10171f;--paper:#17232f;--ink:#edf3f9;--dim:#b8c8d6;--line:#344655;--accent:#8ed7ef}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.7 system-ui,-apple-system,Segoe UI,sans-serif}a{color:var(--accent);text-underline-offset:3px}a:focus,input:focus,summary:focus{outline:3px solid var(--accent);outline-offset:3px}.top{padding:16px 5%;border-bottom:1px solid var(--line);display:flex;gap:22px;flex-wrap:wrap;align-items:center}.top strong{margin-right:auto}.layout{display:grid;grid-template-columns:240px minmax(0,1fr);max-width:1500px;margin:auto}.side{padding:28px 18px;border-right:1px solid var(--line);font-size:14px}.side a{display:block;padding:5px 9px;text-decoration:none}.side a:hover{background:var(--paper)}main{padding:36px 5%;min-width:0;max-width:1080px}.eyebrow{color:var(--accent);text-transform:uppercase;letter-spacing:2px;font-size:12px;font-weight:700}h1{font-size:clamp(28px,4vw,44px);line-height:1.2}h2{font-size:27px;line-height:1.35;margin-top:2.3em}h3{font-size:21px}p,li,td{overflow-wrap:anywhere}p{max-width:86ch}pre{background:#0b1118;border:1px solid var(--line);padding:18px;overflow:auto;font-size:14px;line-height:1.6;border-radius:8px}code{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}p code,li code{font-size:.88em;padding:2px 4px;background:var(--paper);overflow-wrap:anywhere}table{border-collapse:collapse;display:block;overflow:auto;max-width:100%;font-size:14px}th,td{padding:12px 14px;border:1px solid var(--line);text-align:left;vertical-align:top}th{background:var(--paper)}img{max-width:100%;height:auto;background:white;border-radius:6px}.notice{padding:18px 20px;background:var(--paper);border-left:4px solid var(--accent);border-radius:3px}.muted{color:var(--dim);font-size:14px}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin:25px 0}.card{display:block;text-decoration:none;padding:22px;background:var(--paper);border:1px solid var(--line);border-radius:10px;color:var(--ink)}.card span{display:block;color:var(--accent);font-size:12px;letter-spacing:1px}.card h3{margin:10px 0}.card p{font-size:14px;color:var(--dim)}.search{width:100%;max-width:650px;border:1px solid var(--line);padding:15px;background:var(--paper);color:var(--ink);font:inherit;border-radius:8px}details{margin:18px 0;padding:16px;background:var(--paper);border:1px solid var(--line);border-radius:8px}summary{cursor:pointer;font-weight:650}.cell{margin:28px 0}.output{border-left:3px solid var(--line);padding-left:16px}.cell-label{color:var(--dim);font-size:12px}hr{border:0;border-top:1px solid var(--line);margin:35px 0}[hidden]{display:none!important}.skip{position:absolute;left:-10000px}.skip:focus{left:20px;top:10px}.back{display:block;margin:32px 0}.historical{background:#2b2620;border-left:4px solid #dcc58d;padding:12px}.source{font-size:13px;color:var(--dim)}.scroll{overflow:auto}
@media(max-width:860px){.layout{display:block}.side{border-right:0;border-bottom:1px solid var(--line)}.side nav{max-height:150px;overflow:auto;display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}.side h3{margin:0}.top{padding:14px 20px}main{padding:26px 20px}pre{font-size:12px}table{font-size:12px}.cards{grid-template-columns:1fr}}
@media print{.side,.top,.search{display:none}body{background:white;color:black}main{max-width:none}a{color:black}pre{white-space:pre-wrap}}
'''
def shell(title,body,d,source=None,js=''):
 home=relative(R/'START_HERE.html',d.parent)
 nav=''.join('<a href="'+esc(relative(destination(R/('curriculum/stages/'+s['id']+'.md')),d.parent))+'">'+s['id']+' · '+esc(s['title'])+'</a>' for s in CAT['stages'])
 src=''
 if source:
  rel=source.relative_to(R).as_posix();src=f'<p class="source">Source: <a href="{esc(relative(source,d.parent))}">{esc(rel)}</a> · Readable source notation; no online math renderer.</p>'
  if re.search(r'(?:docs/(?:v[2-8])/|README_v\d|VERIFICATION|BUILD_LEDGER)',rel) and 'docs/release/' not in rel:
   src+='<p class="historical">Historical record or optional reference. Use the release verification report for current execution results.</p>'
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} · Listening to Shape</title><link rel="stylesheet" href="{esc(relative(OUT/'assets/course.css',d.parent))}"></head><body><a class="skip" href="#content">Skip to lesson</a><header class="top"><strong>Listening to Shape</strong><a href="{esc(home)}">Course home</a><a href="{esc(relative(destination(R/'curriculum/SITUATIONS.md'),d.parent))}">Choose a situation</a><a href="{esc(relative(destination(R/'curriculum/APPLICATIONS.md'),d.parent))}">Datasets & cases</a><a href="{esc(relative(destination(R/'docs/release/VERIFICATION.md'),d.parent))}">Verification</a></header><div class="layout"><aside class="side"><h3>One required route</h3><p class="muted">31 stages · progress is not auto-assessed</p><nav aria-label="Stages">{nav}</nav></aside><main id="content">{src}{body}<a class="back" href="{esc(home)}">Back to the course home</a></main></div>{js}</body></html>'''
def notebook(p,d):
 b=nbformat.read(p,as_version=4);items=[];learner='learner' in p.parts or 'practice' in p.parts and 'answers' not in p.parts
 title=next((c.source.splitlines()[0].lstrip('# ') for c in b.cells if c.cell_type=='markdown' and c.source.strip()),p.stem)
 status='Independent assignment: unfinished functions are intentional. Do not run this as a reference verification.' if learner else 'Worked reference: saved outputs are included. Use the course runner for a fresh isolated execution.'
 items.append(f'<p class="notice">{esc(status)}</p>')
 for c in b.cells:
  if c.cell_type=='markdown':items.append(article(c.source,p,d))
  elif c.cell_type=='code':
   outs=[]
   for o in c.get('outputs',[]):
    if o.output_type=='stream':outs.append('<pre>'+esc(o.text)+'</pre>')
    elif o.output_type=='error':outs.append('<pre>'+esc(o.get('ename','')+': '+o.get('evalue',''))+'</pre>')
    elif 'image/png' in o.get('data',{}):
     dat=o.data['image/png'];dat=''.join(dat) if isinstance(dat,list) else dat
     outs.append(f'<img alt="Saved analytical output from the preceding code cell" src="data:image/png;base64,{dat}">')
    elif 'text/html' in o.get('data',{}):
     dat=o.data['text/html'];dat=''.join(dat) if isinstance(dat,list) else dat
     bb=BeautifulSoup(dat,'html.parser')
     for tag in bb.find_all(['script','iframe','style']):tag.decompose()
     outs.append('<div class="scroll">'+str(bb)+'</div>')
    elif 'text/plain' in o.get('data',{}):outs.append('<pre>'+esc(o.data['text/plain'])+'</pre>')
   items.append(f'<section class="cell"><p class="cell-label">Code · execution {esc(c.get("execution_count") or "not executed")}</p><pre><code>{esc(c.source)}</code></pre><div class="output">'+''.join(outs)+'</div></section>')
 body=''.join(items)
 if any(x in p.parts for x in ['answers','solutions']):body='<h1>Reference answers</h1><p>Attempt the independent work first.</p><details><summary>Reveal worked answers and outputs</summary>'+body+'</details>'
 return title,body

def old_mapping(source_pages):
 """Resolve prior generated pages by original path, explicit notebook link or title."""
 bytitle={}
 for p in source_pages:
  if p.suffix=='.md':
   first=next((x for x in p.read_text().splitlines() if x.startswith('# ')),p.stem)
   bytitle.setdefault(re.sub(r'[^a-z0-9]','',first[2:].lower()),[]).append(p)
 prior=R/'reports/v9/reader_build.json'
 if prior.exists():
  oldreport=json.loads(prior.read_text())
  stats.update({k:oldreport[k] for k in ['old_html_count','old_html_bytes','aliased_pages','unique_legacy_pages_retained']})
  return {(R/x['old']).resolve():R/x['canonical'] for x in oldreport['alias_records']}
 aliases={};unresolved=[];before=0
 old=list((R/'site').rglob('*.html'))
 explicit={'site/v8/sports.html':'sports_v8/README.md','site/v8/datasets.html':'docs/v8/SPORTS_DATASETS.md',
           'site/v8/start.html':'docs/v9/FIRST_SESSION.md','site/v8/verification.html':'docs/v9/VERIFICATION.md',
           'site/v8/bridge.html':'docs/v8/CORE_TO_SPORTS.md','site/v8/sources.html':'docs/v8/SOURCE_AUDIT.md'}
 for p in old:
  before+=p.stat().st_size;key=p.relative_to(R).as_posix();candidate=None
  if key in explicit and (R/explicit[key]).exists():candidate=R/explicit[key]
  raw=p.read_text();tail=re.sub(r'^site/(?:v[2-8]/)?','',key);stem=tail[:-5]
  candidates=[R/(stem+'.md'),R/(stem+'.ipynb'),R/stem/'README.md']
  if key.startswith('site/v8/'):
   n=p.stem
   if re.fullmatch('S[0-6][0-6]',n):candidates.insert(0,R/f'sports_v8/lessons/{n}.md')
   if re.fullmatch('S[0-6][0-6]_lab',n):candidates.insert(0,R/f'sports_v8/notebooks/{n[:3]}.ipynb')
   if re.fullmatch('S[0-6][0-6]_answers',n):candidates.insert(0,R/f'sports_v8/solutions/{n[:3]}.ipynb')
  if not candidate:candidate=next((x for x in candidates if x in MAP),None)
  if candidate not in MAP:candidate=None
  if not candidate:
   # Download links in rendered notebooks point to the exact source.
   b=BeautifulSoup(raw,'html.parser')
   links=[]
   for a in b.find_all('a',href=True):
    u=urlsplit(a['href'])
    if not u.scheme and u.path.endswith('.ipynb'):links.append((p.parent/unquote(u.path)).resolve())
   unique=[q for q in dict.fromkeys(links) if q in MAP]
   if len(unique)==1:candidate=unique[0]
   if not candidate:
    h=b.find('h1')
    if h:
     title=re.sub(r'[^a-z0-9]','',h.get_text().lower());matches=bytitle.get(title,[])
     if matches:candidate=matches[0]
  if candidate:aliases[p.resolve()]=MAP[candidate]
  else:unresolved.append(key)
 stats.update(old_html_count=len(old),old_html_bytes=before,aliased_pages=len(aliases),unique_legacy_pages_retained=unresolved)
 return aliases

def main():
 OUT.mkdir(exist_ok=True);(OUT/'assets').mkdir(exist_ok=True);(OUT/'assets/course.css').write_text(CSS)
 for p in R.rglob('*'):
  if p.suffix not in ('.md','.ipynb') or SKIP&set(p.relative_to(R).parts):continue
  if p.name.startswith('COMPLETE_COURSE_V') or p.name=='COURSE_GUIDE.md':continue
  MAP[p.resolve()]=destination(p)
 ALIASES.update(old_mapping(list(MAP)))
 for p,d in MAP.items():
  d.parent.mkdir(parents=True,exist_ok=True)
  if p.suffix=='.md':
   t=p.read_text();title=next((x[2:] for x in t.splitlines() if x.startswith('# ')),p.stem);body=article(t,p,d)
  else:title,body=notebook(p,d)
  d.write_text(shell(title,body,d,p))
 prior_path=R/'reports/v9/reader_build.json'
 prior_aliases={x['old']:x for x in json.loads(prior_path.read_text()).get('alias_records',[])} if prior_path.exists() else {}
 alias_report=[]
 for p,d in ALIASES.items():
  before=prior_aliases.get(p.relative_to(R).as_posix(),{}).get('previous_bytes',p.stat().st_size);target=relative(d,p.parent)
  p.write_text(f'<!doctype html><html lang="en"><meta charset="utf-8"><meta http-equiv="refresh" content="0;url={esc(target)}"><title>Canonical course page</title><p>This older rendered copy has moved to <a href="{esc(target)}">the canonical source page</a>. Your learning files are unchanged.</p></html>')
  alias_report.append({'old':p.relative_to(R).as_posix(),'canonical':d.relative_to(R).as_posix(),'previous_bytes':before,'alias_bytes':p.stat().st_size})
 home=R/'START_HERE.html';href=lambda x:esc(relative(MAP[(R/x).resolve()],home.parent))
 cards=''.join(f'<a class="card" data-search="{esc(s["id"]+" "+s["title"]+" "+s["track"])}" href="{href("curriculum/stages/"+s["id"]+".md")}"><span>STAGE {s["id"]} · {esc(s["track"])}</span><h3>{esc(s["title"])}</h3><p>{esc(s["gate"])}</p></a>' for s in CAT['stages'])
 body=f'''<p class="eyebrow">Version 10 · Repository-ready course and reproducible evidence</p><h1>Learn shape.<br>Build evidence.</h1><p>One primary lesson per stage. Begin with observations and notation, then build through topology, geometry and scientific machine learning. Apply the same foundations across industries and sports.</p><p class="notice"><strong>New learner:</strong> start Stage 00. <strong>Continuing learner:</strong> preserve your answer files and progress logs. Running a notebook does not automatically assess your understanding.</p><div class="cards"><a class="card" href="{href('docs/release/FIRST_RUN.md')}"><span>START</span><h3>Git, uv, and your first experiment</h3><p>No installation to read. One primary lesson per stage. Explicit setup and verification profiles.</p></a><a class="card" href="{href('curriculum/SITUATIONS.md')}"><span>APPLY</span><h3>What situation are you facing?</h3><p>Choose the right calculation, assumptions, and checks.</p></a><a class="card" href="{href('sports_v9/lesson.md')}"><span>SPORTS UPDATE</span><h3>2025–26 ACB data readiness</h3><p>Verified ten-game metadata; full tracking is a separate acquisition.</p></a><a class="card" href="{href('docs/release/VERIFICATION.md')}"><span>EVIDENCE</span><h3>What ran, and what did not</h3><p>Fresh kernels, explicit prerequisites, and remaining limits.</p></a></div><p class="notice"><strong>Verification boundary:</strong> reference code is executed locally. Docker runtime and an independently resolved uv install remain blocked on this build host; their configuration is not labeled a passed deployment. <a href="{href('docs/release/DOCKER.md')}">Docker instructions</a> · <a href="{href('docs/release/GIT_IMPORT.md')}">Import into Git safely</a> · <a href="{href('docs/release/AGENT_HANDOFF.md')}">Copy/paste implementation handoff</a></p><h2>The 31-stage learning route</h2><p>Read the primary lesson, predict the worked lab, then attempt the independent assignment. Optional repair explanations are not extra mandatory chapters.</p><label for="stage-search">Find a stage or topic</label><br><input class="search" id="stage-search" type="search" placeholder="Try homology, geometry, physics, or 06"><p id="search-count" class="muted" aria-live="polite">31 stages</p><div class="cards">{cards}</div><h2>Industry cases and additional practice</h2><p><a href="{href('curriculum/APPLICATIONS.md')}">Choose a dataset and case</a> · <a href="{href('docs/v9/CLAIMS_AND_LIMITS.md')}">Source claims and interpretation limits</a> · <a href="{href('docs/v9/DEDUPLICATION.md')}">What was consolidated</a></p>'''
 js='''<script>(()=>{const q=document.getElementById('stage-search'),cards=[...document.querySelectorAll('[data-search]')];q.addEventListener('input',()=>{let n=0;for(const c of cards){c.hidden=!c.dataset.search.toLowerCase().includes(q.value.toLowerCase());if(!c.hidden)n++}document.getElementById('search-count').textContent=n+' matching stages'});})();</script>'''
 home.write_text(shell('Course home',body,home,js=js))
 # The previous top-level home is an alias, not a second syllabus.
 for name in ['CORE_READER.html']:
  (R/name).write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=START_HERE.html"><title>Course home</title><a href="START_HERE.html">Open the canonical course home</a></html>')
 stats.update(canonical_source_pages=len(MAP),required_primary_lessons=len({s['lesson'] for s in CAT['stages']}),alias_records=alias_report,
              source_map={p.relative_to(R).as_posix():d.relative_to(R).as_posix() for p,d in MAP.items()})
 (R/'reports/release').mkdir(parents=True,exist_ok=True)
 (R/'reports/release/reader_build.json').write_text(json.dumps(stats,indent=2)+'\n')
 print(json.dumps({k:v for k,v in stats.items() if k not in ['alias_records','source_map','unique_legacy_pages_retained']},indent=2))
if __name__=='__main__':main()
