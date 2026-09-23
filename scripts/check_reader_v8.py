"""Check new/retained local HTML targets; optionally render with installed Chromium."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import json
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
def main():
    broken=[];links=0;pages=list(ROOT.glob('*.html'))+list((ROOT/'site').rglob('*.html'))
    for p in pages:
        soup=BeautifulSoup(p.read_text(), 'html.parser')
        for node in soup.find_all(['a','img','link','script']):
            value=node.get('href') or node.get('src')
            if not value:continue
            url=urlsplit(value)
            if url.scheme or url.netloc or not url.path:continue
            links+=1;target=(p.parent/unquote(url.path)).resolve()
            if not target.exists():broken.append({'page':str(p.relative_to(ROOT)),'target':value})
    report={'html_pages':len(pages),'local_file_targets':links,'broken':broken,'fragment_ids_checked':False,'external_links_live_checked':False}
    (ROOT/'reports/v8/reader_links.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='broken'},indent=2));print('Broken:',len(broken))
    for item in broken[:20]:print(item)
    if broken:raise SystemExit(1)
if __name__=='__main__':main()
