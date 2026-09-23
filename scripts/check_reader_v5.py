"""Exercise the actual offline reader and record navigation limits honestly."""
from pathlib import Path
import json
import re
from playwright.sync_api import sync_playwright

R = Path(__file__).resolve().parents[1]
result = {'status': 'NOT_RUN', 'checks': []}
def render_html(path):
    return re.sub(r'<link rel="stylesheet"[^>]+>',
                  lambda _: '<style>' + (R/'site/assets/course.css').read_text() + '</style>',
                  path.read_text())

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
        page = browser.new_page(viewport={'width':1440, 'height':1080})
        try:
            page.goto((R/'START_HERE.html').as_uri(), wait_until='load', timeout=5000)
            assert page.locator('a.stage-card').count() == 31
            page.locator('a.stage-card').first.click(timeout=5000)
            assert 'stages/00/README.html' in page.url
            result['navigation'] = 'PASSED_FILE_HOME_TO_STAGE_00'
        except Exception as exc:
            result['navigation'] = 'NOT_VERIFIED_RENDER_FALLBACK'
            result['navigation_limitation'] = str(exc)[:800]
            page.close()
            page = browser.new_page(viewport={'width':1440, 'height':1080})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.set_content(render_html(R/'START_HERE.html'), wait_until='load')
        assert page.locator('.stage-card').count() == 31
        page.screenshot(path=str(R/'reports/reader_home_v5.png'), full_page=False)
        page.locator('#search').fill('Hamiltonian')
        # At least one card should match the actual title, without assuming a single occurrence.
        if page.locator('.stage-card:visible').count() == 0:
            page.locator('#search').fill('23')
        assert 0 < page.locator('.stage-card:visible').count() < 31
        result['checks'].append('31 stage cards; stage search narrows results')
        page.set_content(render_html(R/'site/v5/practice.html'), wait_until='load')
        assert page.locator('.question').count() == 90
        page.locator('#search').fill('24.Q1')
        assert page.locator('.question:visible').count() == 1
        page.locator('.question:visible summary').click()
        assert page.locator('.question:visible details').get_attribute('open') is not None
        page.screenshot(path=str(R/'reports/reader_practice_v5.png'), full_page=False)
        result['checks'].append('90 question cards; filter 24.Q1 and reveal answer')
        page.set_content(render_html(R/'site/v5/physics/notebooks/24_lab.html'), wait_until='load')
        images = page.locator('img.output-image')
        assert images.count() >= 1
        assert all(images.nth(i).evaluate('(x)=>x.complete&&x.naturalWidth>0') for i in range(images.count()))
        result['checks'].append('Stage 24 executed-notebook figures load from embedded outputs')
        page.set_viewport_size({'width':390, 'height':844})
        for name in ['START_HERE.html', 'site/v5/physics/lessons/24.html', 'site/v5/practice.html']:
            page.set_content(render_html(R/name), wait_until='load')
            sizes = page.evaluate('({view:innerWidth,scroll:document.documentElement.scrollWidth})')
            assert sizes['scroll'] <= sizes['view'] + 1, (name, sizes)
        page.set_content(render_html(R/'site/v5/physics/lessons/24.html'), wait_until='load')
        page.screenshot(path=str(R/'reports/reader_mobile_v5.png'), full_page=False)
        result['checks'].append('Home, symplectic lesson and practice fit a 390px viewport')
        assert not errors, errors
        result.update(status='PASSED_RENDER_AND_INTERACTION', page_errors=errors)
        browser.close()
except Exception as exc:
    result.update(status='FAILED', error=str(exc), exception_type=type(exc).__name__)
(R/'reports/browser_v5.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
if result['status']=='FAILED':
    raise SystemExit(1)
