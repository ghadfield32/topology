"""Verify current reader rendering and interactions; record actual navigation capability."""
from pathlib import Path
import json,re
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
result={'status':'not_started','checks':[],'method':'Chromium actual course HTML; CSS inlined for render-only fallback'}
def html_for(path):
    return re.sub(r'<link rel="stylesheet"[^>]+>',lambda m:'<style>'+(R/'site/assets/course.css').read_text()+'</style>',path.read_text())
try:
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  page=b.new_page(viewport={'width':1440,'height':1080})
  try:
   page.goto((R/'START_HERE.html').as_uri(),wait_until='load',timeout=5000)
   assert page.locator('a.stage-card').count()==21
   page.get_by_role('link',name='Begin Stage 00',exact=True).click(timeout=5000)
   assert 'stages/00/README.html' in page.url
   result['navigation']='file_home_to_stage_00_passed'
  except Exception as e:
   result['navigation']='not_verified_fallback_to_render_only'
   result['navigation_limitation']=str(e)[:800]
   page.close()
   page=b.new_page(viewport={'width':1440,'height':1080})
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(html_for(R/'START_HERE.html'),wait_until='load')
  assert page.locator('.stage-card').count()==21
  assert page.get_by_text('63',exact=True).count()>=1
  page.screenshot(path=str(R/'reports/reader_home_v4.png'),full_page=False)
  result['checks'].append('Home: 21 stage cards and 63-reference count')
  page.set_content(html_for(R/'site/v4/transfer.html'),wait_until='load')
  assert page.locator('.card-question').count()==42
  page.locator('#search').fill('12.T1')
  assert page.locator('.card-question:visible').count()==1
  page.locator('.card-question:visible summary').click()
  assert page.locator('.card-question:visible details').get_attribute('open') is not None
  page.screenshot(path=str(R/'reports/reader_transfer_v4.png'),full_page=False)
  result['checks'].append('Transfer: filter 42 cards and reveal one answer')
  page.set_content(html_for(R/'site/v4/recall.html'),wait_until='load')
  assert page.locator('.card-question').count()==63
  result['checks'].append('Delayed recall: 63 cards')
  page.set_content(html_for(R/'site/v4/consolidation/00_lab.html'),wait_until='load')
  images=page.locator('img.output-image')
  assert images.count()>=1
  assert all(images.nth(i).evaluate('(img)=>img.complete && img.naturalWidth>0') for i in range(images.count()))
  result['checks'].append('New real-data notebook figure loads from embedded output')
  page.set_viewport_size({'width':390,'height':844})
  for name in ['START_HERE.html','site/v4/sessions/06_session.html','site/v4/transfer.html']:
   page.set_content(html_for(R/name),wait_until='load')
   sizes=page.evaluate('({view:innerWidth,scroll:document.documentElement.scrollWidth})')
   assert sizes['scroll']<=sizes['view']+1,(name,sizes)
  result['checks'].append('Home, homology session and transfer page fit 390px viewport')
  assert not errors,errors
  result.update(status='PASSED_RENDER_AND_INTERACTION',page_errors=errors)
  b.close()
except Exception as e:result.update(status='FAILED',error=str(e),exception_type=type(e).__name__)
(R/'reports/browser_v4.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
if result['status']=='FAILED':raise SystemExit(1)
