"""Check local file destinations and HTML fragment identifiers without internet."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
from html.parser import HTMLParser
import json
ROOT=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.add(a['id'])
  if tag=='a' and a.get('name'):self.ids.add(a['name'])
  for k in ['href','src']:
   if k in a:self.links.append(a[k])
  if tag=='meta' and a.get('http-equiv','').lower()=='refresh':
   c=a.get('content','');pos=c.lower().find('url=')
   if pos>=0:self.links.append(c[pos+4:])
def main():
 pages=list((ROOT/'reference').rglob('*.html'))+list((ROOT/'reader').rglob('*.html'))+list((ROOT/'site').rglob('*.html'))+[ROOT/'START_HERE.html',ROOT/'CORE_READER.html']
 parsed={};errors=[];fragments=[];local=0;external=0
 for p in pages:
  a=Links();a.feed(p.read_text());parsed[p.resolve()]=a
 for p,a in parsed.items():
  for link in a.links:
   try:u=urlsplit(link)
   except ValueError:errors.append({'page':str(p.relative_to(ROOT)),'href':link,'reason':'malformed URL'});continue
   if u.scheme or u.netloc:external+=1;continue
   t=(p.parent/unquote(u.path)).resolve() if u.path else p
   local+=1
   if not t.exists():errors.append({'page':str(p.relative_to(ROOT)),'href':link,'target':str(t),'reason':'missing file'})
   elif u.fragment and t.suffix=='.html':
    b=parsed.get(t)
    if b is None:b=Links();b.feed(t.read_text());parsed[t]=b
    f=unquote(u.fragment)
    if f not in b.ids:fragments.append({'page':str(p.relative_to(ROOT)),'href':link,'fragment':f,'reason':'missing fragment'})
 result={'pages':len(pages),'local_links_checked':local,'external_or_embedded_not_fetched':external,'missing_files':errors,'missing_fragments':fragments}
 (ROOT/'reports/v9/reader_links.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:len(v) if isinstance(v,list) else v for k,v in result.items()},indent=2))
 return int(bool(errors or fragments))
if __name__=='__main__':raise SystemExit(main())
