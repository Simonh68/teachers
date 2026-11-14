import os
import shutil
from playwright.sync_api import sync_playwright

BASE = os.getenv("ENEMY_READER_URL", "https://simonh68.github.io/teachers/grade11/the-enemy/read-along/")
COUNTS = [111, 186, 118, 158, 45]
CHECKS = [
    [14, 32, 55, 72, 87, 111], [27, 59, 88, 132, 161, 186],
    [27, 39, 58, 63, 77, 118], [17, 43, 72, 110, 127, 158], [11, 20, 30, 35, 41, 45],
]

def close_pairing(page):
    close = page.locator("#teachers-qr-remote-host").get_by_role("button", name="סגור / Close")
    if close.is_visible():
        close.click()

def assert_plays(page):
    page.locator("[data-action=replay]").click()
    page.wait_for_function("!!document.querySelector('.word.on') && !audio.paused", timeout=20000)
    page.locator("#play").click()

def document_position(locator):
    return locator.evaluate("""el => {
        const box=el.getBoundingClientRect();
        return [box.left+scrollX,box.top+scrollY];
    }""")

def swipe(page, delta):
    page.locator("#app").evaluate("""(el, dx) => {
        const point = x => new Touch({identifier: 1, target: el, clientX: x, clientY: 140});
        el.dispatchEvent(new TouchEvent('touchstart', {bubbles:true,touches:[point(180)]}));
        el.dispatchEvent(new TouchEvent('touchend', {bubbles:true,changedTouches:[point(180+dx)]}));
    }""", delta)

with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path=shutil.which("google-chrome") or shutil.which("chromium"),
        args=["--no-sandbox", "--disable-dev-shm-usage", "--autoplay-policy=no-user-gesture-required"])
    for width, height in [(390, 844), (1280, 800)]:
        page = browser.new_page(viewport={"width":width, "height":height})
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(BASE+"?verify="+os.getenv("GITHUB_SHA","local"),wait_until="domcontentloaded")
        page.locator(".part-row").first.wait_for()
        assert page.locator(".part-row").count() == 5
        if width >= 900:
            page.locator("#teachers-qr-remote-host").get_by_role("button",name="סגור / Close").wait_for(timeout=10000)
            close_pairing(page)
        for part, total in enumerate(COUNTS, 1):
            page.locator(".part-row").nth(part-1).click()
            language=page.locator("#hebrew-mode")
            if part==1:
                assert language.get_attribute("aria-pressed")=="false"
                assert page.locator("#prep-he").is_hidden()
                assert page.locator(".vocab-label").count()==5
            else:
                assert language.get_attribute("aria-pressed")=="true"
                assert page.locator("#prep-he").is_visible()
                page.locator(".chip").first.click()
                assert page.locator(".chip small").first.is_visible()
            page.locator("[data-action=begin]").click()
            page.locator(".sentence").wait_for()
            assert page.locator("#jump option").count() == total
            assert f"Part {part:02}" in page.locator(".eyebrow").inner_text()
            if part==1:
                page.wait_for_function("!!document.querySelector('.word.on')",timeout=22000)
                page.locator("#play").click()
            page.locator("#auto").uncheck()
            if part==1:
                assert page.locator("[data-gloss]").count()==0
                if width==390:
                    swipe(page,-100)
                    assert page.locator("#jump").input_value()=="1"
                    swipe(page,100)
                else:
                    page.locator(".sentence").click()
                    page.keyboard.press("ArrowRight")
                    assert page.locator("#jump").input_value()=="1"
                    page.keyboard.press("ArrowLeft")
                assert page.locator("#jump").input_value()=="0"
                page.locator("[data-action=next]").click()
                assert page.locator("#jump").input_value()=="1"
                assert not page.locator(".translation").inner_text().strip()
                page.locator("#jump").select_option(str(CHECKS[0][0]-1))
                page.locator("[data-action=next]").click()
                assert page.locator("[data-action=hint]").is_visible()
                page.locator("[data-action=back]").click()
                assert not page.locator(".translation").inner_text().strip()
                language.click()
                assert language.get_attribute("aria-pressed")=="true"
            for idx in [0,total//2,total-1]:
                page.locator("#jump").select_option(str(idx))
                assert_plays(page)
                assert not page.locator(".translation").inner_text().strip()
                sentence=page.locator(".sentence")
                before=document_position(sentence)
                before_text=sentence.inner_text()
                page.locator("[data-action=next]").click()
                assert page.locator(".translation").inner_text().strip()
                assert page.locator("#jump").input_value()==str(idx)
                assert sentence.inner_text()==before_text
                after=document_position(sentence)
                assert all(abs(a-b)<1 for a,b in zip(after,before))
                assert page.evaluate("document.documentElement.scrollWidth<=innerWidth")
            page.locator("[data-action=rewind]").click()
            assert int(page.locator("#jump").input_value())<total-1
            if width==390:
                page.locator("#jump").select_option("1")
                swipe(page,-100)
                assert page.locator(".translation").inner_text().strip()
                swipe(page,100)
                assert not page.locator(".translation").inner_text().strip()
            for number in CHECKS[part-1]:
                page.locator("#jump").select_option(str(number-1))
                page.locator("[data-action=next]").click()
                page.locator("[data-action=next]").click()
                page.locator("[data-action=hint]").click()
                page.locator("[data-action=answer]").click()
                assert page.locator("#hint").is_visible() and page.locator("#answer").is_visible()
                page.locator("[data-action=next]").click()
            assert "Complete" in page.locator(".eyebrow").inner_text()
            if part<5:
                page.locator("[data-action=next-part]").click()
                assert f"Part {part+1:02}" in page.locator(".eyebrow").inner_text()
                page.locator("#home").click()
            else:
                page.locator("[data-action=parts]").click()
            print(f"{width}px: part {part} passed",flush=True)
        page.goto(BASE+"?part=5&sentence=45",wait_until="domcontentloaded")
        page.locator(".sentence").wait_for()
        assert page.locator("#jump").input_value()=="44"
        assert "Strange" in page.locator(".sentence").inner_text()
        assert language.get_attribute("aria-pressed")=="true"
        page.locator("[data-action=next]").click()
        assert page.locator(".translation").inner_text().strip()
        page.reload(wait_until="domcontentloaded")
        page.locator(".sentence").wait_for()
        assert language.get_attribute("aria-pressed")=="true"
        assert page.locator(".translation").inner_text().strip()
        language.click()
        assert language.get_attribute("aria-pressed")=="false"
        assert not page.locator(".translation").inner_text().strip()
        page.goto(BASE+"?part=2&sentence=1&he=1")
        page.locator(".sentence").wait_for()
        assert language.get_attribute("aria-pressed")=="false"
        assert not page.locator(".translation").inner_text().strip()
        page.locator("[data-action=next]").click()
        assert page.locator("#jump").input_value()=="1"
        assert not errors,errors
        page.close()

    # Use two browser contexts so a remote action crosses the actual approved connection.

    host=browser.new_page(viewport={"width":1280,"height":800})
    host.goto(BASE+"?verify="+os.getenv("GITHUB_SHA","local"),wait_until="domcontentloaded")
    pairing=host.locator("#teachers-qr-remote-host")
    pairing.locator("#link").wait_for()
    host.wait_for_function("document.querySelector('#teachers-qr-remote-host').shadowRoot.querySelector('#link').value.length>0",timeout=45000)
    assert pairing.locator("#qr canvas, #qr img").count()>0
    phone=browser.new_page(viewport={"width":390,"height":844})
    phone.goto(pairing.locator("#link").input_value(),wait_until="domcontentloaded")
    remote=phone.locator("#teachers-qr-remote-host")
    pairing.locator("#approve").wait_for(timeout=50000)
    assert remote.locator("#next").is_disabled()
    pairing.locator("#approve").click()
    phone.wait_for_function("window.teachersPhoneRemote.connected",timeout=20000)
    host.locator(".part-row").nth(3).click()
    host.locator("[data-action=begin]").click()
    host.locator(".sentence").wait_for()
    host.locator("#auto").uncheck()
    remote.locator("#next").click()
    host.wait_for_function("document.querySelector('#jump')?.value==='1'")
    assert not host.locator(".translation").inner_text().strip()
    host.locator("#hebrew-mode").click()
    remote.locator("#next").click()
    host.wait_for_function("!!document.querySelector('.translation')?.textContent")
    remote.locator("#previous").click()
    host.wait_for_function("document.querySelector('.translation')?.textContent===''")
    print("QR pairing, approval and navigation passed",flush=True)
    browser.close()
