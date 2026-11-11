import shutil
from playwright.sync_api import sync_playwright
base='http://127.0.0.1:8817/grade11/the-enemy/read-along/'
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path=shutil.which('google-chrome') or shutil.which('chromium'),args=['--no-sandbox','--disable-dev-shm-usage','--autoplay-policy=no-user-gesture-required'])
 for width,height in [(390,844),(1280,800)]:
  page=browser.new_page(viewport={'width':width,'height':height});errors=[]
  page.on('pageerror',lambda err:errors.append(str(err)))
  page.goto(base);page.locator('.part-row').first.wait_for();assert page.locator('.part-row').count()==5
  for i in range(5):
   page.locator('.part-row').nth(i).click();page.locator('.chip').first.click();assert page.locator('.chip small').first.is_visible()
   page.locator('[data-action=prep-he]').click();assert page.locator('#prep-he').is_visible()
   if i:assert page.locator('[data-action=begin]').count()==0
   page.locator('#home').click()
  page.locator('.part-row').first.click();page.locator('[data-action=begin]').click();page.locator('.sentence').wait_for()
  assert page.locator('#jump option').count()==111
  page.wait_for_function("document.querySelector('.word.on')!==null",timeout=20000)
  assert page.locator('#play').inner_text().endswith('Pause')
  page.locator('#play').click();page.locator('#auto').uncheck()
  page.locator('[data-action=next]').click();assert 'סדאו' in page.locator('.translation').inner_text()
  page.locator('[data-action=next]').click();assert page.locator('#jump').input_value()=='1'
  page.get_by_role('button',name='← Back').click();assert page.locator('#jump').input_value()=='0'
  for idx in [13,31,54,71,86,110]:
   page.locator('#jump').select_option(str(idx));page.locator('[data-action=next]').click();page.locator('[data-action=next]').click()
   assert page.locator('[data-action=answer]').is_visible();page.locator('[data-action=hint]').click();assert page.locator('#hint').is_visible();page.locator('[data-action=answer]').click(); assert page.locator('#answer').is_visible()
   page.locator('[data-action=next]').click()
  assert page.locator('[data-action=next-part]').inner_text()=='Prepare Part 2 →'
  page.locator('[data-action=next-part]').click();assert 'Inside the house' in page.locator('h2').inner_text()
  page.goto(base+'?part=1&sentence=5');page.locator('.sentence').wait_for()
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.locator('#jump').select_option('110');page.locator('#play').click()
  page.wait_for_function("!!document.querySelector('.word.on')")
  page.locator('#play').click();page.locator('[data-action=rewind]').click();assert int(page.locator('#jump').input_value())<110
  if width==390:
   page.locator('#jump').select_option('1'); before=page.locator('.translation').inner_text()
   page.locator('#app').evaluate('el=>{const t=(x)=>new Touch({identifier:1,target:el,clientX:x,clientY:150});el.dispatchEvent(new TouchEvent("touchstart",{bubbles:true,touches:[t(290)]}));el.dispatchEvent(new TouchEvent("touchend",{bubbles:true,changedTouches:[t(40)]}))}')
   assert page.locator('.translation').inner_text()!=before
  assert not errors,errors
  print('Browser checked',width,height,flush=True);page.close()
 browser.close()
