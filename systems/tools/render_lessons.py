"""Render the source Markdown, never introduce another required lesson."""
from pathlib import Path
import html,os,re
ROOT=Path(__file__).resolve().parents[2]
def render():
 import mistune
 md=mistune.create_markdown(escape=True,plugins=['table','strikethrough'])
 files=[]
 for area in ['docs/v17','systems/lessons','systems/contracts']:
  files += list((ROOT/area).glob('*.md'))
 files += [ROOT/'systems/README.md',ROOT/'systems/deploy/README.md']
 known=set(files)
 for f in files:
  body=md(f.read_text(encoding='utf8'))
  def link(m):
   raw=m.group(1);target=(f.parent/raw).resolve()
   return 'href="'+(raw+'.html'if target in known else raw)+'"'
  body=re.sub(r'href="([^"#:]+\.md)"',link,body)
  back=os.path.relpath(ROOT/'LEARN_TOPOLOGY.html',f.parent).replace(os.sep,'/')
  page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><style>body{font:18px/1.65 system-ui;max-width:960px;padding:28px;margin:auto;color:#172733}h1{line-height:1.2}pre{overflow:auto;padding:18px;background:#f0f3f2}code{font-size:.88em}table{border-collapse:collapse;display:block;overflow:auto}td,th{border-bottom:1px solid #ddd;padding:9px}a{color:#175b75;overflow-wrap:anywhere}</style><p><a href="'+back+'">← Course home</a> · <a href="'+f.name+'">Markdown source</a></p>'+body+'</html>'
  f.with_name(f.name+'.html').write_text(page,encoding='utf8')
 portal=ROOT/'LEARN_TOPOLOGY.html';text=portal.read_text()
 def portal_link(m):
  raw=m.group(1)
  if (ROOT/(raw+'.html')).exists():dest=raw+'.html'
  elif (ROOT/'reader'/(raw+'.html')).exists():dest='reader/'+raw+'.html'
  else:dest=raw
  return 'href="'+dest+'"'
 text=re.sub(r'href="([^"#:]+\.md)"',portal_link,text);portal.write_text(text,encoding='utf8')
 print('Rendered',len(files),'Markdown sources; each remains one lesson.')
if __name__=='__main__':render()
