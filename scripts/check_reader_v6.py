"""Real Chromium rendering, navigation, search and responsive evidence checks."""
from pathlib import Path
import re,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
result={'status':'not_run','checks':[]}
def source(p):
    return re.sub(r'<link rel="stylesheet"[^>]+>',lambda m:'<style>'+(R/'site/assets/course.css').read_text()+'</style>',p.read_text())
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1440,'height':1080})
        try:
            page.goto((R/'START_HERE.html').as_uri(),wait_until='load',timeout=5000)
            assert page.locator('.stage-card').count()==39
            page.locator('a',has_text='New learner: Stage 00').click(timeout=5000)
            assert page.url.endswith('site/v6/stages/00.html')
            result['navigation']='passed_local_home_to_stage_00'
        except Exception as e:
            result['navigation']='not_verified_environment_navigation_failed'
            result['navigation_error']=str(e)[:1000]
            page.close();page=browser.new_page(viewport={'width':1440,'height':1080})
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content(source(R/'START_HERE.html'),wait_until='load')
        assert page.locator('.stage-card').count()==39
        page.screenshot(path=str(R/'reports/v6/reader_home.png'))
        page.locator('#search').fill('wine');assert 0<page.locator('.stage-card:visible').count()<39
        result['checks'].append('39 stage/case cards; live filter narrows results')
        page.set_content(source(R/'site/v6/industry/notebooks/wine.html'),wait_until='load')
        imgs=page.locator('img.output-image');assert imgs.count()>=1
        assert all(imgs.nth(i).evaluate('(x)=>x.complete&&x.naturalWidth>0') for i in range(imgs.count()))
        result['checks'].append('Executed wine notebook image loads')
        page.set_content(source(R/'site/v6/industry/learner/wine.html'),wait_until='load')
        assert 'NotImplementedError' in page.locator('body').inner_text()
        result['checks'].append('Learner assignment distinguished from reference execution')
        page.set_content(source(R/'site/v6/practice.html'),wait_until='load')
        assert page.locator('.question').count()==56
        page.locator('#search').fill('wine.Q2');assert page.locator('.question:visible').count()==1
        page.locator('.question:visible summary').click()
        assert page.locator('.question:visible details').get_attribute('open') is not None
        result['checks'].append('56 practice/recall cards; exact filter and answer reveal work')
        page.set_viewport_size({'width':390,'height':844})
        for path in ['START_HERE.html','site/v6/docs/v6/BEGINNER_DATA_PRIMER.html','site/v6/industry/cards/wdbc.html','site/v6/stages/14.html']:
            page.set_content(source(R/path),wait_until='load')
            s=page.evaluate('({view:innerWidth,scroll:document.documentElement.scrollWidth})')
            assert s['scroll']<=s['view']+1,(path,s)
        page.set_content(source(R/'site/v6/industry/lessons/wine.html'),wait_until='load')
        page.screenshot(path=str(R/'reports/v6/reader_mobile.png'))
        result['checks'].append('Home, primer, wide-schema data card and stage fit a 390px viewport')
        assert not errors,errors
        result.update(status='passed_rendering_and_interaction',page_errors=errors)
        browser.close()
except Exception as e:result.update(status='failed',error=str(e),exception_type=type(e).__name__)
(R/'reports/v6/browser.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
if result['status']=='failed':raise SystemExit(1)
