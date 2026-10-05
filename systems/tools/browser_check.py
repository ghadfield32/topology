import json,re
from pathlib import Path
from playwright.sync_api import sync_playwright
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args()
r=Path(__file__).resolve().parents[2];e=Path(a.output);e.mkdir(parents=True,exist_ok=False);results={}
with sync_playwright()as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=b.new_page(viewport={'width':1200,'height':900});errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
 try:
  page.goto((r/'LEARN_TOPOLOGY.html').as_uri(),timeout=5000);results['direct_file_navigation']='passed'
 except Exception as ex:
  results['direct_file_navigation']='blocked: '+str(ex)[:350];page.close();page=b.new_page(viewport={'width':1200,'height':900});page.on('pageerror',lambda err:errors.append(str(err)));page.set_content((r/'LEARN_TOPOLOGY.html').read_text())
 assert page.locator('h1').count()==1
 page.locator('#filter').fill('homology');assert page.locator('#core tbody tr:visible').count()>=1
 results['filter']='passed';page.screenshot(path=str(e/'portal_desktop.png'),full_page=True)
 page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth+3');page.screenshot(path=str(e/'portal_mobile.png'),full_page=True)
 page.set_viewport_size({'width':1100,'height':900})
 js=(r/'systems/typescript/build/shape.js').read_text();text=(r/'systems/typescript/index.html').read_text().replace('<script src="build/shape.js"></script>','<script>'+js+'</script>')
 page.set_content(text);page.locator('#file').set_input_files(str(r/'systems/evidence/demo/trajectory.json'));page.wait_for_function("document.querySelector('#status').textContent.includes('7 observed')")
 def opaque():return page.evaluate("Array.from(document.querySelector('canvas').getContext('2d').getImageData(0,0,880,440).data).filter((v,i)=>i%4===3&&v>0).length")
 assert opaque()>0
 results['real_json_view']='passed';page.locator('#yaw').fill('40');page.locator('#yaw').dispatch_event('input');page.screenshot(path=str(e/'trajectory_viewer.png'),full_page=True)
 page.locator('#file').set_input_files({'name':'invalid.json','mimeType':'application/json','buffer':b'{"units":"feet"}'});page.wait_for_function("document.querySelector('#status').textContent.includes('Expected')")
 results['invalid_json_rejected']='passed';results['old_result_cleared_after_error']=opaque()==0;results['browser_errors']=errors
 b.close()
(e/'browser_checks.json').write_text(json.dumps(results,indent=2));print(results)

if results.get('old_result_cleared_after_error') is not True or results.get('browser_errors'):raise SystemExit(1)
