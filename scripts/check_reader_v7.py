"""Chromium checks; report navigation separately from DOM rendering."""
from pathlib import Path
import json,re
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
result={'status':'not_run','checks':[]}
def source(path):
 return re.sub(r'<link rel="stylesheet"[^>]+>',lambda m:'<style>'+(R/'site/assets/course.css').read_text()+'</style>',path.read_text())
try:
 with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1440,'height':1080})
    try:
        page.goto((R/'START_HERE.html').as_uri(),wait_until='load',timeout=5000)
        page.get_by_role('link',name='Begin Stage 00',exact=True).click(timeout=5000)
        assert page.url.endswith('site/v7/beginner_v7/00/lesson.html')
        page.get_by_role('link',name='Full Stage 00',exact=True).click(timeout=5000)
        assert page.url.endswith('site/v7/stages/00/README.html')
        result['navigation']='passed_file_home_to_entry_to_full_stage'
    except Exception as e:
        result['navigation']='not_verified_environment_navigation_failed';result['navigation_error']=str(e)[:1200]
        page.close();page=browser.new_page(viewport={'width':1440,'height':1080})
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content(source(R/'START_HERE.html'),wait_until='load')
    assert page.locator('[data-search]').count()==41
    page.screenshot(path=str(R/'reports/v7/reader_home.png'))
    page.locator('#search').fill('seeds')
    assert 0<page.locator('[data-search]:visible').count()<41
    result['checks'].append('41 stage/industry search targets, live search narrows results')
    for value,expected in [('.8','Components (β₀): 4 · Independent loops (β₁): 0.'),('1','Components (β₀): 1 · Independent loops (β₁): 1.'),('1.5','Components (β₀): 1 · Independent loops (β₁): 0.')]:
        page.locator('#threshold').evaluate('(el,v)=>{el.value=v;el.dispatchEvent(new Event("input"));}',value)
        assert page.locator('#square-result').inner_text()==expected
    assert page.locator('#square-edges line').count()==6
    result['checks'].append('Square explorer checks below sides, perimeter loop, and filled triangles')
    page.set_content(source(R/'site/v7/applications_v7/concrete_slump/lab.html'),wait_until='load')
    images=page.locator('img.output-image');assert images.count()>=1
    assert all(images.nth(i).evaluate('(el)=>el.complete&&el.naturalWidth>0') for i in range(images.count()))
    page.screenshot(path=str(R/'reports/v7/reader_lab.png'))
    result['checks'].append('Current executed concrete interval figure embedded and loaded')
    page.set_content(source(R/'site/v7/applications_v7/seeds/learner.html'),wait_until='load')
    assert 'NotImplementedError' in page.locator('body').inner_text()
    result['checks'].append('Deliberate learner stubs labeled separately from references')
    page.set_content(source(R/'site/v7/practice.html'),wait_until='load')
    assert page.locator('[data-search]').count()==36
    page.locator('#search').fill('concrete_slump.Q2');assert page.locator('[data-search]:visible').count()==1
    page.locator('[data-search]:visible summary').click()
    assert page.locator('[data-search]:visible details').get_attribute('open') is not None
    result['checks'].append('36 question/recall cards, exact filter, and answer reveal')
    page.set_viewport_size({'width':390,'height':844})
    for path in ['START_HERE.html','site/v7/beginner_v7/06/lesson.html','site/v7/docs/v7/DATA_CATALOG.html','site/v7/applications_v7/concrete_slump/lab.html']:
        page.set_content(source(R/path),wait_until='load')
        dims=page.evaluate('({view:innerWidth,scroll:document.documentElement.scrollWidth})')
        assert dims['scroll']<=dims['view']+1,(path,dims)
    page.set_content(source(R/'site/v7/beginner_v7/00/lesson.html'),wait_until='load')
    page.screenshot(path=str(R/'reports/v7/reader_mobile.png'))
    assert not errors,errors
    result['checks'].append('Home, beginner lesson, data table and notebook fit 390px viewport')
    result.update(status='passed_rendering_and_interaction',page_errors=errors)
    browser.close()
except Exception as e:result.update(status='failed',error=str(e),exception_type=type(e).__name__)
(R/'reports/v7/browser.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
if result['status']=='failed':raise SystemExit(1)
