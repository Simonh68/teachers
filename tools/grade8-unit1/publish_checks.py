"""Run every publication check without suppressing failures.

The legacy boundary probe sought before media metadata had loaded and changed
sentenceIndex without loading that sentence's recording. Replace that probe
with real playback of each clip on every page, waiting for finite duration
before seeking near the end. The app's own ended handler must advance between
clips and stop at the page boundary. All other acceptance checks stay blocking.
"""
from pathlib import Path

source = Path(__file__).with_name('verify.py')
text = source.read_text()
old = """    page.goto(base+'?view=chunks&p=0');page.locator('#play').click();page.wait_for_function('!audio.paused')
    page.evaluate('sentenceIndex=D.pages[pos].at(-1);audio.currentTime=audio.duration-.05');page.wait_for_timeout(500)
    assert page.evaluate('audio.paused') and page.evaluate('pos')==0;record('Chunk playback pauses at page boundary')
"""
new = """    for page_index, ids in enumerate(data['pages']):
        page.goto(base+'?view=chunks&p='+str(page_index))
        page.locator('#play').click()
        for idx in ids:
            page.wait_for_function(
                'idx => sentenceIndex === idx && !audio.paused && !audio.seeking '
                '&& audio.readyState >= 2 && Number.isFinite(audio.duration) '
                '&& audio.duration > 0 && audio.currentTime > 0 '
                '&& audio.currentSrc === new URL(D.story[idx].audio,location.href).href',
                arg=idx, timeout=15000)
            page.evaluate('audio.currentTime=Math.max(0,audio.duration-.10)')
        page.wait_for_function(
            'i => audio.ended && audio.paused && !chain && pos === i',
            arg=page_index, timeout=10000)
        assert page.evaluate('sentenceIndex') == ids[-1]
        assert page.locator('.word.playing').count() == 0
    record('All 10 reading pages play their actual clips and stop at the page boundary')
"""
assert text.count(old) == 1, 'Audio test changed; review before publication'
text = text.replace(old, new)
# The actual pointer must operate the controls; do not write app or browser state.
old_activation = "    locator.evaluate('(element)=>element.click()')"
assert text.count(old_activation) == 1, 'Activation helper changed; review before publication'
text = text.replace(old_activation, '    locator.click()')
text = text.replace(
    "record('DOM activation: progress toggle, reload persistence, history reset and restore')",
    "record('Pointer activation: progress toggle, reload persistence, history reset and restore')")
namespace = {'__file__': str(source), '__name__': '__main__'}
exec(compile(text, str(source), 'exec'), namespace)
print('Every publication check passed; no failed checks were suppressed.', flush=True)
