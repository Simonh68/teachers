#!/usr/bin/env python3
"""Create Simon's approved Grade 9 reading and writing worksheet."""
from __future__ import annotations

import ctypes
import ctypes.util
import json
import argparse
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from pypdf import PdfReader

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent / 'grade9-noise-and-school-trips.pdf')
parser.add_argument('--preview-dir', type=Path, default=None, help='Optional directory for layout validation metadata.')
args = parser.parse_args()
OUTPUT = args.output.resolve()
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
PREVIEW = args.preview_dir
FONT_ROOT = Path('/usr/share/fonts/truetype/noto')
for name, filename in [
    ('Body', 'NotoSans-Regular.ttf'),
    ('Bold', 'NotoSans-Bold.ttf'),
]:
    pdfmetrics.registerFont(TTFont(name, str(FONT_ROOT / filename)))
pdfmetrics.registerFont(TTFont('Hebrew', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))

_fribidi = ctypes.CDLL(ctypes.util.find_library('fribidi'))
_fribidi.fribidi_get_bidi_type.argtypes = [ctypes.c_uint32]
_fribidi.fribidi_get_bidi_type.restype = ctypes.c_uint32
_fribidi.fribidi_log2vis.argtypes = [
    ctypes.POINTER(ctypes.c_uint32), ctypes.c_int,
    ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint32),
    ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,
]
_fribidi.fribidi_log2vis.restype = ctypes.c_uint8


def rtl(text: str) -> str:
    """Apply Unicode bidi using FriBidi; keep numeric spans in reading order."""
    logical = (ctypes.c_uint32 * len(text))(*map(ord, text))
    visual = (ctypes.c_uint32 * (len(text) + 1))()
    direction = ctypes.c_uint32(_fribidi.fribidi_get_bidi_type(ord('א')))
    if not _fribidi.fribidi_log2vis(logical, len(text), ctypes.byref(direction), visual, None, None, None):
        raise RuntimeError('FriBidi failed')
    return ''.join(chr(visual[i]) for i in range(len(text)))


PARAGRAPHS = [
    'Imagine trying to read a story while chairs move across the floor and students talk around you. You may read the same sentence several times without understanding it. Noise can make it difficult to concentrate, which means keeping your attention on what you are doing. This problem can affect students in both public and private schools.',
    'Noise may come from inside or outside the classroom. Talking, moving furniture and loud fans can disturb a lesson. Traffic and building work nearby can also make it hard to hear the teacher. When students miss important instructions, they may make mistakes even when they understand the subject.',
    'Some people think that private schools are always quieter than public schools. However, the type of school is not enough to tell us how noisy it is. A small private school next to a busy road may be noisier than a large public school on a quiet street. The number of students in a room and their behavior also make a difference.',
    'Noise does not affect every student in the same way. Some can work with quiet sounds around them, while others need more silence. The activity also matters. During a test, students usually need quiet. During group work, however, talking helps students share ideas. A completely silent classroom is therefore not always the best place to learn.',
    'Schools can take simple steps to reduce noise. They can put soft covers under chair legs and close windows during noisy activities outside. Teachers can also agree on clear rules with their classes, such as speaking one at a time. Both public and private schools should provide quiet spaces for students who need them.',
]

W, H = A4
LEFT, RIGHT = 43, W - 43
WIDTH = RIGHT - LEFT
NAVY = HexColor('#24384b')
INK = HexColor('#151b21')
GRAY = HexColor('#626b73')
RULE = HexColor('#a4aab1')
c = canvas.Canvas(str(OUTPUT), pagesize=A4, pageCompression=1)
c.setTitle('Grade 9 - Too Much Noise at School / School Trips')
c.setAuthor('Simon - English Learning Materials')
c.setSubject('Module C-style reading and writing practice: 7 reading questions and a 70-90-word writing task')


def text_line(text, x, baseline, size=12, font='Body', color=INK):
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawString(x, baseline, text)


def wrapped(text, y, size=12, leading=16, font='Body', x=LEFT, width=WIDTH, color=INK):
    lines = simpleSplit(text, font, size, width)
    for line in lines:
        text_line(line, x, y, size, font, color)
        y -= leading
    return y


def hebrew(text, y, size=10.5):
    c.setFillColor(INK)
    c.setFont('Hebrew', size)
    c.drawRightString(RIGHT, y, rtl(text))


def rule(y, x1=LEFT, x2=RIGHT, width=.55, color=RULE):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y, x2, y)


def answer_lines(y, count=1, spacing=21):
    for _ in range(count):
        rule(y)
        y -= spacing
    return y


def footer(number):
    rule(35, width=.4)
    text_line('GRADE 9  |  READING AND WRITING PRACTICE', LEFT, 22, 8, 'Body', GRAY)
    c.setFont('Body', 8)
    c.setFillColor(GRAY)
    c.drawRightString(RIGHT, 22, f'{number} / 2')


def section(title, y):
    text_line(title, LEFT, y, 12, 'Bold', NAVY)
    return y - 22


def question(number, text, y, size=11.4, leading=15):
    # A hanging indent makes the seven question numbers easy to locate.
    text_line(f'{number}.', LEFT, y, size, 'Bold')
    return wrapped(text, y, size=size, leading=leading, font='Bold', x=LEFT+18, width=WIDTH-18)


def options(items, y):
    for letter, item in zip('abcd', items):
        y = wrapped(f'{letter}.  {item}', y, size=11.4, leading=15.2, x=LEFT+18, width=WIDTH-18)
    return y


# PAGE 1
text_line('GRADE 9', LEFT, H-41, 10, 'Bold', NAVY)
c.setFont('Body', 10)
c.setFillColor(GRAY)
c.drawRightString(RIGHT, H-41, 'Reading and Writing Practice')
rule(H-51, color=NAVY, width=.8)
text_line('Name:', LEFT, H-72, 10)
rule(H-75, LEFT+34, LEFT+210)
text_line('Class:', LEFT+230, H-72, 10)
rule(H-75, LEFT+264, LEFT+330)
text_line('Date:', LEFT+350, H-72, 10)
rule(H-75, LEFT+380, RIGHT)

text_line('TOO MUCH NOISE AT SCHOOL', LEFT, H-108, 18, 'Bold', NAVY)
hebrew('קראו את הטקסט וענו באנגלית על שאלות 1-7.', H-130, 10.5)
y = H-154
for index, para in zip(['I','II','III','IV','V'], PARAGRAPHS):
    text_line(index, LEFT, y, 11, 'Bold', NAVY)
    y = wrapped(para, y, size=12, leading=16.15, x=LEFT+22, width=WIDTH-22)
    y -= 8

y = section('Reading Comprehension', y-3)
y = question(1, 'What problem is presented in paragraph I? Choose the correct answer.', y)
y -= 3
y = options([
    'Students do not have enough time to read.',
    'Noise can make it difficult for students to concentrate.',
    'Students prefer studying outside the classroom.',
    'Schools give students too many instructions.',
], y)
y -= 10
y = question(2, 'Why may students make mistakes even when they understand the subject? (Paragraph II)', y)
y = answer_lines(y-6, count=2, spacing=21)
page1_bottom = y+21
if page1_bottom < 48:
    raise RuntimeError(f'Page 1 exceeds safe area: {page1_bottom:.1f}')
footer(1)
c.showPage()

# PAGE 2
text_line('READING COMPREHENSION - CONTINUED', LEFT, H-42, 12, 'Bold', NAVY)
rule(H-52, color=NAVY, width=.8)
y = H-77
y = question(3, 'Why might a small private school be noisier than a large public school? (Paragraph III)', y)
y = answer_lines(y-6, count=2, spacing=20)
y -= 2
y = question(4, 'When do students usually need a quiet classroom? (Paragraph IV)', y)
y = answer_lines(y-6, count=1, spacing=21)
y -= 2
y = question(5, 'Complete the sentence according to paragraph IV.', y)
y = wrapped('Talking during group work can be useful because', y-2, size=11.6, leading=15, x=LEFT+18, width=WIDTH-18)
y = answer_lines(y-7, count=1, spacing=21)
y -= 2
y = question(6, 'Give TWO ways schools can reduce noise. (Paragraph V)', y)
y = answer_lines(y-6, count=2, spacing=20)
y -= 2
y = question(7, 'What is the main message of the text? Choose the correct answer.', y)
y -= 3
y = options([
    'Every lesson should be completely silent.',
    'Private schools always offer better places to study.',
    'Schools should reduce disturbing noise and allow useful discussion.',
    'Only noise from outside the classroom needs to be reduced.',
], y)

y -= 7
rule(y, color=NAVY, width=.7)
y -= 22
y = section('Writing - School Trips: Near or Far?', y)
hebrew('כתבו חיבור באנגלית בהיקף 70-90 מילים. הציגו את העדפתכם, תנו שני נימוקים והוסיפו דוגמה.', y+3, size=10.1)
y -= 19
y = wrapped('Which do you prefer: school trips to places near your school or school trips to places far away?', y, size=11.6, leading=15.4, font='Bold')
y = wrapped('Give TWO reasons for your choice and include an example.', y-3, size=11.4, leading=15.4)
y -= 5

# Twelve generous full-width lines are reserved for 70-90 words.
writing_top = y
writing_line_count = 12
writing_spacing = 23
y = answer_lines(y, count=writing_line_count, spacing=writing_spacing)
page2_bottom = y+writing_spacing
if page2_bottom < 48:
    raise RuntimeError(f'Page 2 exceeds safe area: {page2_bottom:.1f}')
footer(2)
c.save()

reader = PdfReader(str(OUTPUT))
assert len(reader.pages) == 2
metadata = {
    'output': str(OUTPUT),
    'pages': len(reader.pages),
    'page_size': 'A4',
    'reading_words': len(' '.join(PARAGRAPHS).split()),
    'writing_lines': writing_line_count,
    'writing_line_spacing_pt': writing_spacing,
    'writing_area_height_pt': writing_top-page2_bottom,
    'last_answer_rule_page1_pt': round(page1_bottom, 1),
    'last_answer_rule_page2_pt': round(page2_bottom, 1),
    'question_count': 7,
    'body_font_pt': 12,
}
if PREVIEW is not None:
    PREVIEW.mkdir(parents=True, exist_ok=True)
    (PREVIEW/'layout-checks.json').write_text(json.dumps(metadata, indent=2))
print(json.dumps(metadata, indent=2))
