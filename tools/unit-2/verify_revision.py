"""Check the revised content contract and the recording attached to every word."""
from pathlib import Path
import hashlib, json, re
from html.parser import HTMLParser
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'grade7/unit-2'
data = json.loads((OUT/'content.json').read_text())
reading = json.loads((OUT/'reading/content.json').read_text())
expected = [('horse', 'South America', 'whatsapp'), ('wheelchair', 'Asia', 'email'), ('boat', 'Europe', 'instagram')]
assert [(s['id'], s['region'], s['messageStyle']) for s in data['stories']] == expected
assert [t['id'] for t in reading['texts']] == ['school-calendars', 'horse', 'wheelchair', 'boat']
main = ' '.join(s[1] for s in data['main'])
assert not re.search(r'\b(?:19|20)\d{2}\b|approximately', main, re.I)
assert all(s['he'] and s['en'].endswith('?') and s['source'].startswith('https://') for s in data['stories'])
assert 'states have different rules' in main
for row in data['calendar']:
    assert any(season in row['start'].lower() for season in ['spring', 'summer', 'autumn', 'winter'])
    assert any(season in row['end'].lower() for season in ['spring', 'summer', 'autumn', 'winter'])
    assert 'weeks' in row['summer']
class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(); self.parts=[]; self.links=[]; self.messages=[]; self.anchor=None
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs); classes=attrs.get('class','').split()
        if 'unit-part' in classes:self.parts.append([])
        if 'message-card' in classes:self.messages.append(classes)
        if tag=='a':
            self.anchor={'href':attrs.get('href',''), 'text':''}; self.links.append(self.anchor)
            if self.parts and self.anchor['href'].startswith('journey-'):self.parts[-1].append(self.anchor['href'])
    def handle_endtag(self, tag):
        if tag=='a':self.anchor=None
    def handle_data(self, text):
        if self.anchor is not None:self.anchor['text']+=text
hub = Page((OUT/'index.html').read_text())
assert len(hub.parts) == 3
for part, (identity, region, style) in zip(hub.parts, expected):
    assert part == ['journey-'+identity+'.html']
    source = (OUT/('journey-'+identity+'.html')).read_text()
    page = Page(source)
    assert len(page.messages) == 1 and style in page.messages[0]
    assert any(a['href']=='reading/?text='+identity for a in page.links)
    assert 'not an original message or a direct quotation' in source
    assert not any(re.search(r'[\u0590-\u05ff]', a['text']) for a in page.links if a['href'].startswith('https://'))
for text in reading['texts']:
    sentences = [reading['sentences'][n] for n in text['ids']]
    full = ' '.join(s['en'] for s in sentences)
    expected_text = main if text['id'] == 'school-calendars' else next(s['en'] for s in data['stories'] if s['id'] == text['id'])
    assert full == expected_text
    cues = json.loads((OUT/'reading/assets'/f"{text['id']}.cues.json").read_text())
    assert full == cues['text']
    assert hashlib.sha256((OUT/'reading'/text['audio']).read_bytes()).hexdigest() == text['sha256'] == cues['sha256']
    assert [w for s in sentences for w in s['timings']] == cues['words']
    for sentence in sentences:
        assert sentence['he'] and sentence['start'] < sentence['end']
        assert [w['word'] for w in sentence['timings']] == sentence['en'].split()
        assert all(w['he'] for w in sentence['words'])
pdf = PdfReader(OUT/'files/unit2-workbook.pdf')
assert len(pdf.pages) == 6
for number, label in [(1, 'WhatsApp'), (3, 'Email'), (4, 'Instagram')]:
    assert label in pdf.pages[number].extract_text()
report = dict(main_words=len(main.split()), messages=3, regions=3, formats=['WhatsApp', 'Email', 'Instagram'], reading_texts=4,
              sentences=len(reading['sentences']), reading_parts=sum(len(t['pages']) for t in reading['texts']),
              words=reading['wordCount'], matched_recordings=4, workbook_pages=6, errors=[])
(ROOT/'tools/unit-2/revision-qa-report.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report))
