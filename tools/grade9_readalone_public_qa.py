"""Verify the actual public deployment, not just repository files."""
import json,time,urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];OUT=R/'grade9-ra-qa';OUT.mkdir(exist_ok=True)
root='https://simonh68.github.io/teachers/'
expected=json.loads((R/'grade9/unit-1/read-alone/build-report.json').read_text())
for attempt in range(20):
 try:
  remote=json.load(urllib.request.urlopen(root+'grade9/unit-1/read-alone/build-report.json?check='+str(time.time()),timeout=25))
  if remote['audio_sha256']==expected['audio_sha256'] and remote['full_deck_slides']==142 and remote['passages']==expected['passages']:break
 except Exception:pass
 time.sleep(4)
else:raise AssertionError('New reader not visible on public site')
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 context=browser.new_context(viewport={'width':390,'height':844})
 page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 for mode in ['text','sentences']:
  page.goto(root+'grade9/unit-1/read-alone/?mode='+mode,wait_until='networkidle')
  page.wait_for_function('window.TeachersReadAlone?.data && window.TeachersReadAlone?.clip',timeout=45000)
  assert page.evaluate('TeachersReadAlone.data.sentences.length')==46
  assert page.locator('#raText').inner_text()
  page.locator('[data-ra-play]').click()
  page.wait_for_function('!TeachersReadAlone.audio.paused && TeachersReadAlone.audio.currentTime > TeachersReadAlone.clip.start + .1',timeout=20000)
  page.wait_for_function('document.querySelector(".ra-spoken")',timeout=10000)
  page.locator('#raSpeed').select_option('0.25')
  assert page.evaluate('TeachersReadAlone.audio.playbackRate')==.25
  before=page.evaluate('TeachersReadAlone.audio.currentTime');page.wait_for_timeout(700)
  assert page.evaluate('TeachersReadAlone.audio.currentTime')>before+.03
  hit=page.locator('.ra-hit').first;hit.click()
  assert page.locator('#raTip').is_visible()
  assert page.locator('#raMeaningDock').bounding_box()['y']>=page.locator('#raText').bounding_box()['y']
  page.screenshot(path=str(OUT/('public-'+mode+'.png')))
  page.evaluate('TeachersReadAlone.stop()')
 page.goto(root+'grade9/unit-1/',wait_until='networkidle');assert page.locator('#read-alone-links a').count()>=2
 page.goto(root+'grade9/unit-1/teacher.html',wait_until='networkidle');assert page.locator('#read-alone-teacher-text').count()==1
 page.goto(root+'grade9/the-message-without-a-voice/#slide-36',wait_until='networkidle')
 page.wait_for_function('window.TeachersReadAlone?.data');assert page.locator('.slide').count()==142
 assert page.locator('.slide.active').get_attribute('id')=='slide-36'
 assert not errors,errors
 browser.close()
report={'public_url':root+'grade9/unit-1/read-alone/','public_modes':['text','sentences'],'real_audio_playback':True,'quarter_speed':True,'word_highlight':True,'translation_strip':True,'unit_navigation':True,'teacher_guide':True,'original_slide_36_anchor':True,'passed':True,'audio_sha256':expected['audio_sha256']}
(OUT/'public-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
