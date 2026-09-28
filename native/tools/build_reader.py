"""Render native lesson views without making another required curriculum."""
from pathlib import Path
import html,json,os,re
from urllib.parse import urlsplit,unquote
import mistune
ROOT=Path(__file__).resolve().parents[2]
CSS='''*{box-sizing:border-box}body{margin:0;background:#f4f6f9;color:#1e293b;font:17px/1.6 system-ui,sans-serif}header{background:#11243b;color:white;padding:28px max(24px,calc((100vw - 1120px)/2))}header a{color:#bfdcff}main{max-width:1168px;margin:28px auto;padding:0 24px}h1{font-size:clamp(28px,4vw,44px);line-height:1.15}h2{line-height:1.25;margin-top:32px}h3{line-height:1.3}a{color:#075ca8;overflow-wrap:anywhere}p{max-width:100ch}.intro,.notice,.card,.metrics{background:white;border:1px solid #d9e0e8;border-radius:10px;padding:22px;margin:18px 0}.notice{border-left:5px solid #b7771b}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(285px,1fr));gap:16px}.card{margin:0;min-width:0}.small{font-size:14px;color:#506075}.tag{font-size:13px;font-weight:700;letter-spacing:.08em}pre{overflow:auto;background:#eaf0f6;padding:16px;border-radius:6px;font-size:14px}code{overflow-wrap:anywhere}table{display:block;max-width:100%;overflow:auto;border-collapse:collapse;background:white}th,td{padding:10px;text-align:left;border-bottom:1px solid #dae1ea;vertical-align:top}input{width:100%;font:inherit;padding:13px;border:1px solid #aab8c7;border-radius:6px}.metrics{display:flex;gap:32px;flex-wrap:wrap}.metrics strong{font-size:28px;display:block}.actions{display:flex;flex-wrap:wrap;gap:16px}details{background:white;padding:10px;margin:12px 0}summary{cursor:pointer}img{max-width:100%}footer{margin:32px 0;font-size:14px;color:#506075} .hidden{display:none!important} @media(max-width:500px){main{padding:0 14px}header{padding:24px 16px}.card,.intro,.notice{padding:16px}}'''
md=mistune.create_markdown(plugins=['table','strikethrough'])
def rel(src,dest):return os.path.relpath(dest,src.parent).replace(os.sep,'/')
def shell(title,content,src):
 home=html.escape(rel(src,ROOT/'START_NATIVE.html'))
 return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>{CSS}</style></head><body><header><div class="tag">LISTENING TO SHAPE · NATIVE16</div><nav><a href="{home}">Native learning home</a> · <a href="{html.escape(rel(src,ROOT/"START_HERE.html"))}">Original course</a></nav></header><main>{content}<footer>One mathematical curriculum. Native agreement, scientific validity and independent learner mastery are different requirements.</footer></main></body></html>'
paths=list((ROOT/'native/guides').rglob('*.md'))+[ROOT/'native/README.md',ROOT/'native/COVERAGE.md']+list((ROOT/'docs/v16').glob('*.md'))
for p in paths:
 dest=p.with_suffix(p.suffix+'.html')
 body=md(p.read_text(encoding='utf8'))
 def fix(m):
  url=m.group(1); u=urlsplit(html.unescape(url))
  if u.scheme or not u.path:return m.group(0)
  target=(p.parent/unquote(u.path)).resolve()
  rendered=target.with_suffix(target.suffix+'.html')
  if target in paths:target=rendered
  elif target.is_relative_to(ROOT) and (ROOT/'reader'/target.relative_to(ROOT).as_posix()).with_suffix(target.suffix+'.html').exists():target=(ROOT/'reader'/target.relative_to(ROOT).as_posix()).with_suffix(target.suffix+'.html')
  return 'href="'+html.escape(rel(dest,target)+('#'+u.fragment if u.fragment else ''))+'"'
 body=re.sub(r'href="([^"]+)"',fix,body)
 pkey=p.stem if p.parent.name=='labs'else None
 if pkey:
  body+=f'<h2>Inspect the executed evidence</h2><p><a href="{rel(dest,ROOT/"native/evidence/acceptance/go"/(pkey+".json"))}">Go result</a> · <a href="{rel(dest,ROOT/"native/evidence/acceptance/rust"/(pkey+".json"))}">Rust result</a></p>'
 dest.write_text(shell(p.stem,body,dest),encoding='utf8')
items=json.loads((ROOT/'native/protocols/labs.json').read_text())['labs']
home=ROOT/'START_NATIVE.html'
intro='''<h1>Learn once.<br>Implement in Go and Rust.</h1><p>Continue your existing course at Stage 01. The Python lessons remain the mathematical reference. The native programs independently load observations, calculate, train small models and save inspectable results.</p>
<div class="metrics"><div><strong>57 + 57</strong>native unit runs passed</div><div><strong>55</strong>source files, both readers</div><div><strong>220</strong>independent science checks</div></div>
<div class="notice"><strong>Scope matters.</strong> These are shared native16 teaching protocols. Some differ from the original Python experiments. Full operation-for-operation equivalence to all 133 notebooks, new Docker/Kubernetes execution, and independent learner mastery are <strong>not certified</strong>. See the per-unit coverage record.</div>
<div class="intro"><h2>Start with one stage</h2><ol><li>Read its primary mathematical lesson once.</li><li>Write a prediction and calculate a small example.</li><li>Run both native implementations and inspect their inputs and outputs.</li><li>Make a private implementation change and test it.</li><li>Explain a limitation; revisit a changed example later.</li></ol><pre>uv run --no-sync python native_course.py compare --lab stage01 --output my_work/native_stage01_01\nuv run --no-sync python native_course.py prepare --lab stage01 --output my_work/native_practice01</pre><p>Use a new output directory for each attempt. Go and Rust compilers must be installed; Cargo dependencies are vendored. No remote dataset download is required for the bundled inputs.</p></div>'''
links=[('Setup and migration','native/guides/SETUP.md.html'),('Three language learning paths','native/guides/LEARNING_PATHS.md.html'),('First session','docs/v16/FIRST_SESSION.md.html'),('Coverage and differences','native/COVERAGE.md.html'),('Verification','docs/v16/VERIFICATION.md.html'),('All execution records','native/evidence/acceptance/index.html'),('Data index','docs/v16/DATA_INDEX.md.html'),('Docker and Kubernetes','native/guides/DEPLOYMENT.md.html')]
intro+='<div class="actions">'+''.join(f'<a href="{u}">{t}</a>'for t,u in links)+'</div><h2>Choose a learning unit</h2><label for="filter">Filter by title or ID</label><input id="filter" placeholder="Try stage01, sports, persistence, neural…"><p id="count">57 units</p><div class="grid" id="cards">'
for x in items:
 key=x['key'];intro+=f'<article class="card" data-key="{html.escape(key+" "+x["title"])}"><div class="tag">{key}</div><h3><a href="native/guides/labs/{key}.md.html">{html.escape(x["title"])}</a></h3><p>{html.escape(x["native_goal"])}</p><p class="small">{html.escape(x["original_scope_gaps"])}</p><p><a href="native/evidence/acceptance/go/{key}.json">Go output</a> · <a href="native/evidence/acceptance/rust/{key}.json">Rust output</a></p></article>'
intro+='</div><script>const f=document.getElementById("filter");f.addEventListener("input",()=>{let n=0;document.querySelectorAll(".card").forEach(c=>{let show=c.dataset.key.toLowerCase().includes(f.value.toLowerCase());c.classList.toggle("hidden",!show);n+=show;});document.getElementById("count").textContent=n+" units";});</script>'
home.write_text(shell('Native16 learning home',intro,home),encoding='utf8')
print('Rendered',len(paths),'guide views and native home')
