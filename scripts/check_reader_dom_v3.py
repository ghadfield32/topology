from pathlib import Path
import json,re
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
previous=json.loads((R/'reports/browser_v3.json').read_text()) if (R/'reports/browser_v3.json').exists() else {}
result={'method':'Chromium DOM rendering from actual HTML with the same CSS inlined', 'navigation_status':'not_tested_by_this_render_only_script','status':'not_started','checks':[]}
def html_for(path):
    s=path.read_text()
    css=(R/'site/assets/course.css').read_text()
    return re.sub(r'<link rel="stylesheet"[^>]+>',lambda m:'<style>'+css+'</style>',s)
try:
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  page=b.new_page(viewport={'width':1440,'height':1100},device_scale_factor=1)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(html_for(R/'START_HERE.html'),wait_until='load')
  assert page.locator('a.stage-card').count()==21
  assert page.get_by_role('link',name='Begin Stage 00',exact=True).get_attribute('href').endswith('stages/00/README.html')
  page.screenshot(path=str(R/'reports/reader_home_v3.png'),full_page=False)
  result['checks'].append('Home renders 21 stage cards and Stage 00 link')
  page.set_content(html_for(R/'site/v3/recall.html'),wait_until='load')
  assert page.locator('.card-question').count()==63
  page.locator('#search').fill('16.R1')
  assert page.locator('.card-question:visible').count()==1
  page.locator('.card-question:visible summary').click()
  assert page.locator('.card-question:visible details').get_attribute('open') is not None
  page.screenshot(path=str(R/'reports/reader_practice_v3.png'),full_page=False)
  result['checks'].append('Recall query filters 63 cards to one and answer-reveal works')
  page.set_content(html_for(R/'site/v3/notebooks/15_lab.html'),wait_until='load')
  assert page.locator('img.output-image').count()==5
  assert all(page.locator('img.output-image').nth(i).evaluate('(img)=>img.complete && img.naturalWidth>0') for i in range(5))
  result['checks'].append('Stereo notebook renders all five embedded output figures')
  page.set_viewport_size({'width':390,'height':844})
  page.set_content(html_for(R/'START_HERE.html'),wait_until='load')
  widths=page.evaluate('({view:innerWidth,scroll:document.documentElement.scrollWidth})')
  assert widths['scroll']<=widths['view']+1,widths
  result['checks'].append('390px home viewport has no horizontal page overflow')
  assert not errors,errors
  result.update(status='PASSED_RENDER_AND_INTERACTION_ONLY',page_errors=errors)
  b.close()
except Exception as exc:result.update(status='FAILED',error=str(exc),exception_type=type(exc).__name__)
(R/'reports/browser_v3.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
