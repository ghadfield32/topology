"""Rebuild the offline v2 course, including linked workbooks and executed practice.

Run: python scripts/build_reader_v2.py
Only trusted course-authored Markdown is rendered. No CDN, remote API or font file.
"""
from __future__ import annotations
import html
import json
import os
from pathlib import Path
import re
from urllib.parse import urlsplit, unquote
import mistune
import nbformat
import build_reader as base

ROOT=Path(__file__).resolve().parents[1]
META=json.loads((ROOT/'docs/stage_metadata.json').read_text())
MD=mistune.create_markdown(escape=False,plugins=['table','strikethrough','url'])
MAP={}

def relative(path:Path,destination:Path)->str:
    return Path(os.path.relpath(path,destination.parent)).as_posix()

def esc(text):return html.escape(str(text),quote=True)

def shell(title,body,destination,current=None,extra_js=''):
    destination.parent.mkdir(parents=True,exist_ok=True)
    def url(path):return relative(ROOT/path,destination)
    nav=''.join(f'<a class="{"current" if current==s["n"] else ""}" href="{url(f"site/hubs/{s["n"]:02d}.html")}"><span class="n">{s["n"]:02d}</span>{esc(base.SHORT[s["n"]])}</a>' for s in META)
    tools=[('site/docs/START_YOUR_FIRST_SESSION.html','Your first session'),('site/foundations/00_numbers_symbols_and_types.html','Numbers & notation primer'),('site/foundations/01_python_from_zero.html','Python from zero'),('site/docs/PROOF_ATLAS.html','Proof atlas'),('site/flashcards.html','102 conceptual cards'),('site/retrieval.html','39 delayed-recall questions'),('site/docs/LEARNING_SYSTEM_V2.html','Learning record & review'),('site/docs/GLOSSARY.html','Glossary'),('site/docs/BRING_YOUR_OWN_DATA.html','Try your own CSV'),('site/docs/FINAL_ASSESSMENT.html','Final assessment'),('site/docs/SOURCES.html','Free readings & sources'),('site/docs/VERIFICATION.html','Execution & limitations'),('site/docs/README.html','Python setup')]
    nav+='<p class="nav-title">Tools for learning</p>'+''.join(f'<a href="{url(p)}">{esc(label)}</a>' for p,label in tools)
    text=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="A staged beginner course with worked lessons, code practice, real datasets and explicit mastery checks."><title>{esc(title)} | Listening to Shape 2.0</title><link rel="stylesheet" href="{url('site/assets/course.css')}"></head><body><div class="layout"><aside class="side"><a class="brand" href="{url('START_HERE.html')}"><small>Independent learning companion · 2.0</small>Listening to Shape<br>Learning System</a><p class="nav-title">The 13-stage path</p><nav aria-label="Course navigation">{nav}</nav></aside><main class="main"><div class="wrap">{body}<footer>Learning System 2.0 · Original teaching material, not the book text or an author-endorsed course. Reference execution, learner evidence and scientific validation are different claims. <a href="{url('START_HERE.html')}">Course home</a> · <a href="{url('site/docs/SOURCES.html')}">Sources</a> · <a href="{url('LICENSE.md')}">Use & attribution</a></footer></div></main></div>{extra_js}</body></html>'''
    destination.write_text(text,encoding='utf-8')

def rewrite_links(rendered,source,destination):
    def replace(m):
        attr,quote,href=m.groups();decoded=html.unescape(href);parts=urlsplit(decoded)
        if parts.scheme or parts.netloc or not parts.path:return m.group(0)
        target=(source.parent/unquote(parts.path)).resolve()
        final=MAP.get(target,target)
        out=relative(final,destination)
        if parts.query:out+='?'+parts.query
        if parts.fragment:out+='#'+parts.fragment
        return f'{attr}={quote}{esc(out)}{quote}'
    return re.sub(r'(href|src)=([\"\'])(.*?)\2',replace,rendered)

def markdown_page(source,destination,stage=None):
    text=source.read_text(encoding='utf-8')
    title=next((line.lstrip('# ').strip() for line in text.splitlines() if line.startswith('# ')),source.stem)
    body=rewrite_links(MD(text),source,destination)
    bar=''
    if stage is not None:
        hub=relative(ROOT/f'site/hubs/{stage:02d}.html',destination)
        bar=f'<div class="toolbar"><a class="button primary" href="{hub}">Stage {stage:02d} hub</a><a class="button" href="{relative(source,destination)}">Markdown source</a></div>'
    shell(title,bar+'<article>'+body+'</article>',destination,stage)

def notebook_page(source,destination,n,learner=False):
    body=base.notebook_html(source)
    if learner:
        body=body.replace('Code · executed cell None','Code · your unexecuted assignment')
        note='These five exercises deliberately contain unfinished functions. Read the hint, write your own implementation, then run the adjacent check. No execution or mastery is claimed for the starter file.'
    else:note='These are executed reference answers. Attempt your own notebook first; reference checks are not your assessment score.'
    toolbar=f'<div class="toolbar"><a class="button primary" href="{relative(ROOT/f"site/hubs/{n:02d}.html",destination)}">Stage {n:02d} hub</a><a class="button" href="{relative(source,destination)}" download>Open notebook file</a></div>'
    shell(f'Stage {n:02d} '+('your coding practice' if learner else 'executed coding answers'),toolbar+f'<div class="callout"><p>{esc(note)}</p></div><article>'+body+'</article>',destination,n)

def build():
    base.shell=shell;base.MD=MD;base.build()
    additions=[]
    def register(source,destination,n=None):
        MAP[(ROOT/source).resolve()]=ROOT/destination
        additions.append((ROOT/source,ROOT/destination,n))
    for s in META:
        n=s['n'];tag=f'{n:02d}'
        register(f'stages/{tag}/README.md',f'site/hubs/{tag}.html',n)
        register(f'lessons/{tag}_lesson.md',f'site/stages/{tag}.html',n)
        register(f'workbooks/{tag}_workbook.md',f'site/workbooks/{tag}.html',n)
        register(f'solutions/{tag}_solutions.md',f'site/solutions/{tag}.html',n)
        register(f'practice/{tag}_solutions.md',f'site/practice/solutions/{tag}.html',n)
        MAP[(ROOT/f'notebooks/{tag}_lab.ipynb').resolve()]=ROOT/f'site/notebooks/{tag}.html'
        for role in ['learner','answers']:
            MAP[(ROOT/f'practice/{role}/{tag}_practice.ipynb').resolve()]=ROOT/f'site/practice/{role}/{tag}.html'
    for p in sorted((ROOT/'foundations').glob('*.md')):register(str(p.relative_to(ROOT)),f'site/foundations/{p.stem}.html')
    for p in sorted((ROOT/'docs').glob('*.md')):register(str(p.relative_to(ROOT)),f'site/docs/{p.stem}.html')
    for source,dest in [('README.md','site/docs/README.html'),('practice/retrieval.md','site/retrieval.html'),('my_work/README.md','site/docs/YOUR_WORK.html'),('data/README.md','site/docs/DATA_README.html'),('progress/README.md','site/docs/PROGRESS_README.html')]:register(source,dest)
    for source,destination,n in additions:markdown_page(source,destination,n)
    for n in range(13):
        for role in ['learner','answers']:
            notebook_page(ROOT/f'practice/{role}/{n:02d}_practice.ipynb',ROOT/f'site/practice/{role}/{n:02d}.html',n,role=='learner')
    cards=''.join(f'<a class="stage-card" href="site/hubs/{n:02d}.html"><span class="badge">Stage {n:02d}</span><strong>{esc(base.SHORT[n])}</strong><p>Lesson · beginner workbook · real-data lab · five coding exercises · mastery check</p></a>' for n in range(13))
    primerlinks=''.join(f'<li><a href="site/foundations/{p.stem}.html">{esc(p.read_text().splitlines()[0].lstrip("# "))}</a></li>' for p in sorted((ROOT/'foundations').glob('*.md')))
    home='''<header class="hero"><p class="eyebrow">From your first data table to a defended analysis</p><h1>Understand shape.<br>Build it. Test it.</h1><p class="lead">A beginner-first learning system for topology, homology and persistence. Every stage connects an explanation to mathematics, real data, your own code and an honest mastery check.</p></header><div class="toolbar"><a class="button primary" href="site/hubs/00.html">Begin Stage 00</a><a class="button" href="site/docs/START_YOUR_FIRST_SESSION.html">Your first session</a><a class="button" href="site/docs/README.html">Run the notebooks</a></div>
<div class="stats"><div class="stat"><strong>13</strong><span>Stages with deeper workbooks</span></div><div class="stat"><strong>65</strong><span>Write-it-yourself coding exercises</span></div><div class="stat"><strong>26</strong><span>Executed reference notebooks</span></div><div class="stat"><strong>39</strong><span>New delayed-recall questions</span></div></div>
<div class="callout"><p><strong>No prerequisites are assumed.</strong> Start with the first table and the notation you need. Read and inspect saved outputs without installing anything. Install Python only when you are ready to change and run code.</p></div>
<section class="card"><h2>One stage, three passes</h2><p><strong>Understand:</strong> read the lesson and workbook; predict a small example.<br><strong>Build:</strong> run the lab, change one condition, then write the five functions yourself.<br><strong>Demonstrate:</strong> solve the conceptual problems, explain a counterexample and recall the idea later without notes.</p><p>The 102 original conceptual exercises remain. Solutions are separate; unfinished learner notebooks are assignments, not failed completed work.</p><div class="toolbar"><a class="button" href="site/docs/LEARNING_SYSTEM_V2.html">How assessment and review work</a><a class="button" href="site/docs/PROOF_ATLAS.html">Read the proof atlas</a></div></section>
<section class="card"><h2>A foundation you can return to</h2><p>Use these primers when notation, Python or proofs get in the way. They are integrated with the stages rather than a barrier before starting.</p><ul>'''+primerlinks+'''</ul></section><h2>Your stage-by-stage route</h2><div class="grid">'''+cards+'''</div>
<section class="card"><h2>Real evidence, not a predetermined success story</h2><p>The labs use bundled Iris measurements and handwritten-digit images. Exact geometric examples establish expected answers; real data test interpretation. The final comparison includes pixels, topology and both together. The exposed demonstration split is not a fresh holdout for future tuning.</p><div class="toolbar"><a class="button" href="site/notebooks/12.html">Executed capstone</a><a class="button" href="site/docs/DATA_README.html">Dataset provenance</a><a class="button" href="site/docs/BRING_YOUR_OWN_DATA.html">Try a small CSV experiment</a></div></section>
<section class="card"><h2>Keep learning without losing the evidence</h2><p>Save your work, record an honest assessment and return for delayed recall. The local CLI records evidence paths and hashes; it does not automatically grade proofs or certify mastery. All learner records start unassessed.</p><div class="toolbar"><a class="button" href="site/docs/LEARNING_SYSTEM_V2.html">Progress and handoff guide</a><a class="button" href="site/retrieval.html">Delayed-recall questions</a><a class="button" href="site/docs/FINAL_ASSESSMENT.html">Cumulative assessment</a></div></section>
<section class="card"><h2>What this release actually verifies</h2><p>The original worked labs and new reference-answer notebooks have execution evidence. Deliberate learner starters are not counted as passes. The verification page separates software tests, package checks and unexecuted optional library comparisons. This is original teaching aligned to the supplied outline, not the actual book text or a claim to exhaust all topology.</p><div class="toolbar"><a class="button primary" href="site/docs/VERIFICATION.html">Read verification and limitations</a><a class="button" href="site/docs/CHANGELOG_V2.html">What changed in version 2</a><a class="button" href="COMPLETE_COURSE_V2.md">Combined reading volume</a></div></section>'''
    shell('Start here',home,ROOT/'START_HERE.html')
    # Keep old progress available without implying synchronization with the new log.
    path=ROOT/'site/progress.html';text=path.read_text();text=text.replace('<div class="wrap">','<div class="wrap"><div class="callout"><p><strong>Legacy browser scratchpad.</strong> This page does not synchronize with the version 2 evidence log. Use <a href="docs/LEARNING_SYSTEM_V2.html">the current learning-system guide</a> for durable records and backup instructions.</p></div>',1);path.write_text(text)
    print(f'Built offline v2 reader: {len(additions)} routed Markdown pages, 26 practice notebook pages, 13 worked labs.')

if __name__=='__main__':build()
