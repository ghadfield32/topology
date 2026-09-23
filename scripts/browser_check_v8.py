"""Optional authoring QA; set-content fallback is not file-navigation evidence."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

R=Path(__file__).resolve().parents[1]
report={'actual_file_navigation':False,'desktop_render':False,'mobile_render':False,'search':False,'answer_reveal':False,'executed_figure':False,'page_errors':[]}

def inline_page(path: Path) -> str:
    from bs4 import BeautifulSoup
    soup=BeautifulSoup(path.read_text(), 'html.parser')
    for link in soup.select('link[rel="stylesheet"]'):
        css=(path.parent / link['href']).resolve()
        style=soup.new_tag('style'); style.string=css.read_text(); link.replace_with(style)
    return str(soup)

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
    page=browser.new_page(viewport={'width':1280,'height':950},device_scale_factor=1)
    try:
        page.goto((R/'START_HERE.html').as_uri(),wait_until='load',timeout=8000)
        report['actual_file_navigation']=True
    except Exception as e:
        report['navigation_error']=str(e)
        # The failed navigation may still be changing execution contexts.
        # Render on a fresh page rather than racing that navigation.
        page.close()
        page=browser.new_page(viewport={'width':1280,'height':950},device_scale_factor=1)
        page.set_content(inline_page(R/'START_HERE.html'),wait_until='domcontentloaded',timeout=15000)
        report['render_method']='fresh-page set_content with inline local CSS; file navigation NOT established'
    page.on('pageerror',lambda e:report['page_errors'].append(str(e)))
    assert page.locator('h1').count()==1
    report['desktop_render']=True
    page.screenshot(path=str(R/'reports/v8/reader_desktop.png'),full_page=False)
    page.locator('#course-search').fill('homology')
    visible=page.locator('.searchable:visible').count()
    assert 0<visible<31
    report['search']=True;report['search_visible_cards']=visible
    page.locator('#course-search').fill('')
    page.set_viewport_size({'width':390,'height':844})
    page.evaluate('window.scrollTo(0,0)')
    page.screenshot(path=str(R/'reports/v8/reader_mobile.png'),full_page=False)
    report['mobile_render']=True
    report['home_mobile_no_horizontal_overflow']=page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
    lesson=browser.new_page(viewport={'width':1000,'height':900})
    lesson.set_content(inline_page(R/'site/v8/S00.html'),wait_until='domcontentloaded')
    assert lesson.locator('details').count()==1
    lesson.locator('summary').click()
    assert lesson.locator('details').get_attribute('open') is not None
    report['answer_reveal']=True
    lesson.set_content(inline_page(R/'site/v8/S02_lab.html'),wait_until='load')
    assert lesson.locator('img').count()>=1
    assert lesson.locator('img').first.evaluate('(img)=>img.complete && img.naturalWidth>0')
    report['executed_figure']=True
    browser.close()
(R/'reports/v8/browser.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
