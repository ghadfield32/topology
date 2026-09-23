"""Self-contained HTML sports reader plus navigation into retained v7 core pages."""
from pathlib import Path
import html,re,json,base64
import mistune,nbformat
R=Path(__file__).resolve().parents[1]
OUT=R/'site/v8';OUT.mkdir(parents=True,exist_ok=True)
md=mistune.create_markdown(escape=True,plugins=['table'])
STYLE='''
:root{--ink:#122c3d;--muted:#516673;--paper:#fff;--soft:#f3f6f5;--line:#dce5e4;--accent:#0d635f}
*{box-sizing:border-box}body{margin:0;color:var(--ink);background:var(--soft);font:17px/1.65 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}a{color:var(--accent);text-underline-offset:3px}header{background:var(--ink);color:white;padding:28px max(5vw,20px)}header a{color:white}main{max-width:1100px;margin:auto;padding:32px 24px 60px}h1{font-size:clamp(30px,4vw,46px);line-height:1.18;letter-spacing:-.02em}h2{font-size:25px;margin-top:36px}h3{font-size:20px}p{max-width:85ch}.eyebrow{font-size:13px;text-transform:uppercase;letter-spacing:.14em}nav{display:flex;flex-wrap:wrap;gap:18px;font-size:15px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(285px,1fr));gap:18px}.card{background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:22px;margin:14px 0}.card h3{margin:7px 0}.badge{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}.muted{color:var(--muted)}.note{border-left:4px solid var(--accent);padding:14px 20px;background:#eaf3f1}.button{display:inline-block;padding:9px 14px;background:var(--accent);color:white;border-radius:8px;text-decoration:none;margin-right:8px;margin-top:8px}pre{padding:18px;overflow:auto;background:#edf1f3;border-radius:8px;font:14px/1.55 ui-monospace,Consolas,monospace}code{font-family:ui-monospace,Consolas,monospace;font-size:.9em;overflow-wrap:anywhere}pre code{font-size:inherit;overflow-wrap:normal}table{border-collapse:collapse;width:100%;font-size:14px;display:block;overflow:auto;margin:20px 0}th,td{padding:12px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top;min-width:95px}th{background:#e4eeeb}img{max-width:100%;height:auto}details{padding:15px;border:1px solid var(--line);background:white;border-radius:10px;margin:20px 0}summary{cursor:pointer;font-weight:650}input{width:100%;padding:13px 16px;font:inherit;border:1px solid var(--line);border-radius:9px;margin-bottom:18px}[hidden]{display:none!important}.result{background:white;padding:16px;border:1px solid var(--line);overflow:auto}.foot{margin-top:40px;padding-top:20px;border-top:1px solid var(--line);font-size:14px;color:var(--muted)}:focus-visible{outline:3px solid #b87113;outline-offset:3px}@media(max-width:600px){main{padding:22px 16px}nav{gap:12px}.card{padding:17px}table{font-size:13px}}
'''
(OUT/'style.css').write_text(STYLE)

def shell(title,body,home=False):
    prefix='site/v8/' if home else ''
    root='' if home else '../../'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} | Listening to Shape v8</title><link rel="stylesheet" href="{prefix}style.css"></head><body><header><div class="eyebrow">Listening to Shape · v8 · Learning by evidence</div><nav aria-label="Main navigation"><a href="{root}START_HERE.html">Home</a><a href="{root}CORE_READER.html">31-stage core & industries</a><a href="{prefix}sports.html">Sports path</a><a href="{prefix}start.html">Setup / preserve work</a><a href="{prefix}datasets.html">Modern dataset guide</a><a href="{prefix}verification.html">Verification</a></nav></header><main>{body}<footer class="foot">Original course companion, not the book text or professional certification. Observed-source excerpts, derived estimates, constructed controls and model predictions are distinct. Source data terms remain attached. Reference execution does not grade your understanding.</footer></main></body></html>'''

def convert_links(text):
    mapping={'../cards/spl.md':'card_spl.html','../cards/skillcorner.md':'card_skillcorner.html'}
    for a,b in mapping.items():text=text.replace(a,b)
    return text

def render_document(path,name):
    text=path.read_text();rendered=md(convert_links(text))
    # Answers remain one click away but initially closed; preserve later mastery text outside.
    rendered=rendered.replace('<h2>Worked answers</h2>','<details><summary>Worked answers — attempt the questions first</summary>')
    if '<details>' in rendered:
        marker=rendered.find('<h2>',rendered.find('<details>'))
        if marker>=0:rendered=rendered[:marker]+'</details>'+rendered[marker:]
        else:rendered+='</details>'
    title=text.splitlines()[0].lstrip('# ')
    (OUT/name).write_text(shell(title,rendered))

def render_nb(path,name):
    b=nbformat.read(path,4);parts=[]
    for c in b.cells:
        if c.cell_type=='markdown':parts.append(md(c.source))
        elif c.cell_type=='code':
            parts.append('<pre><code>'+html.escape(c.source)+'</code></pre>')
            for o in c.get('outputs',[]):
                if o.output_type=='stream':parts.append('<pre class="result">'+html.escape(o.text)+'</pre>')
                elif o.output_type=='error':parts.append('<pre class="result">'+html.escape(o.ename+': '+o.evalue)+'</pre>')
                else:
                    data=o.get('data',{})
                    if 'image/png' in data:parts.append('<img alt="Executed analytical figure; source and axis units are stated in the surrounding cell" src="data:image/png;base64,'+data['image/png']+'">')
                    elif 'text/html' in data:parts.append('<div class="result">'+data['text/html']+'</div>')
                    elif 'text/plain' in data:parts.append('<pre class="result">'+html.escape(data['text/plain'])+'</pre>')
    parts.insert(0,'<p class="note">Saved reference execution. Open the matching .ipynb file in Jupyter to edit and rerun. This page does not execute code.</p>')
    (OUT/name).write_text(shell(path.stem+' executed notebook',''.join(parts)))

def main():
    stages=[]
    for i in range(7):
        sid=f'S{i:02}';p=R/f'sports_v8/lessons/{sid}.md';title=p.read_text().splitlines()[0][2:]
        render_document(p,f'{sid}.html')
        render_nb(R/f'sports_v8/notebooks/{sid}.ipynb',f'{sid}_lab.html')
        render_nb(R/f'sports_v8/solutions/{sid}.ipynb',f'{sid}_answers.html')
        stages.append((sid,title))
    for p,name in [(R/'docs/v8/FIRST_SESSION.md','start.html'),(R/'docs/v8/SPORTS_DATASETS.md','datasets.html'),(R/'docs/v8/CORE_TO_SPORTS_MAP.md','bridge.html'),(R/'docs/v8/SOURCE_AUDIT.md','sources.html'),(R/'sports_v8/cards/spl.md','card_spl.html'),(R/'sports_v8/cards/skillcorner.md','card_skillcorner.html')]:render_document(p,name)
    v=R/'docs/v8/VERIFICATION.md'
    if v.exists():render_document(v,'verification.html')
    sports='<h1>Learn sports data from the first observation.</h1><p>Seven connected sections. Start with units and identity, then motion, models, topology, uncertainty, evaluation and independent work.</p><p class="note">Required examples use two small, selected numeric excerpts. Full modern datasets are acquisition plans, not silently bundled benchmarks.</p><div class="grid">'
    for sid,title in stages:
        sports+=f'<section class="card"><div class="badge">{sid}</div><h3>{html.escape(title.split(" — ",1)[-1])}</h3><a class="button" href="{sid}.html">Learn</a><a class="button" href="{sid}_lab.html">Worked lab</a><p><a href="../../sports_v8/practice/{sid}.ipynb">Learner notebook</a> · <a href="{sid}_answers.html">Coding answers</a> · <a href="../../sports_v8/notebooks/{sid}.ipynb">Editable worked notebook</a></p></section>'
    sports+='</div><h2>Know the sources</h2><p><a href="card_spl.html">Basketball data card</a> · <a href="card_skillcorner.html">Soccer profile card</a> · <a href="datasets.html">Ten modern source plans</a> · <a href="bridge.html">All 31 core bridges</a></p>'
    (OUT/'sports.html').write_text(shell('Sports learning path',sports))
    if not (R/'CORE_READER.html').exists():(R/'CORE_READER.html').write_bytes((R/'START_HERE.html').read_bytes())
    core=json.loads((R/'docs/v8/core_map.json').read_text())
    body='''<div class="eyebrow muted">A complete course, not a pile of links</div><h1>Understand shape.<br>Test it against the world.</h1><p>Beginner foundations, topology and persistent homology, geometry and scientific machine learning—with real cross-industry examples and a new sports path.</p><div class="grid"><section class="card"><div class="badge">Start from zero</div><h3>Learn one concept at a time</h3><p>Read → predict → calculate → run → explain → independently demonstrate.</p><a class="button" href="site/v8/start.html">First session</a><a href="CORE_READER.html">Open complete core reader</a></section><section class="card"><div class="badge">New in v8</div><h3>Basketball and soccer</h3><p>Units, motion, physics assumptions, profile topology, uncertainty and honest evaluation.</p><a class="button" href="site/v8/sports.html">Seven sports sections</a></section><section class="card"><div class="badge">Continue without resetting</div><h3>Preserve your evidence</h3><p>Keep existing answers and logs. New sports items start unassessed, not automatically passed.</p><a class="button" href="site/v8/bridge.html">31-stage application map</a></section></div><section class="note"><strong>What is actually included?</strong> The full prior course and its 15 observed sources, plus two selected, transcribed sports excerpts. Current 2025/2026 video, tracking, wearable and baseball sources are documented separately with access and licensing limits. <a href="site/v8/sources.html">Read the source audit.</a></section><h2>Find your next foundation</h2><label for="course-search">Search a concept or core stage</label><input id="course-search" type="search" placeholder="Try: homology, camera, motion, uncertainty" aria-describedby="search-count"><p id="search-count" aria-live="polite" class="muted">31 core stages</p><div class="grid">'''
    for c in core:
        text=f'{c["stage"]:02} {c["topic"]} {c["sports_task"]} {c["industry_connection"]}'
        body+=f'<section class="card searchable" data-search="{html.escape(text.lower())}"><div class="badge">Core {c["stage"]:02}</div><h3>{html.escape(c["topic"])}</h3><p>{html.escape(c["sports_task"])}</p><a href="site/v7/beginner_v7/{c["stage"]:02}/lesson.html">Beginner entry / full lesson</a><p><a href="site/v8/{c["sports_section"]}.html">Sports bridge {c["sports_section"]}</a></p></section>'
    body+='''</div><section class="card"><h2>Keep results and claims separate</h2><p><a href="site/v8/verification.html">Executed tests and remaining limits</a> · <a href="site/v8/datasets.html">Modern sports dataset catalogue</a> · <a href="CORE_READER.html">Retained cross-industry cases</a> · <a href="site/v8/sources.html">Source audit</a></p></section><script>const q=document.getElementById('course-search');const cards=[...document.querySelectorAll('.searchable')];q.addEventListener('input',()=>{const term=q.value.trim().toLowerCase();let visible=0;for(const c of cards){c.hidden=!c.dataset.search.includes(term);if(!c.hidden)visible++;}document.getElementById('search-count').textContent=visible+' matching core stages';});</script>'''
    (R/'START_HERE.html').write_text(shell('Start here',body,home=True))
    print('Built v8 entry point and',len(list(OUT.glob('*.html'))),'HTML pages.')
if __name__=='__main__':main()
