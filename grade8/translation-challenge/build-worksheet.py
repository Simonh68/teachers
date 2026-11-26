#!/usr/bin/env python3
"""Build the two-page companion worksheet and separate teacher key.

Run from any directory. The only content source is the adjacent data.json.
Dependencies: ReportLab, pypdf and the system FriBidi library. Hebrew and
English fonts are embedded; no network service is used during generation.
"""
from __future__ import annotations

import argparse
import ctypes
import ctypes.util
import json
from pathlib import Path

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from pypdf import PdfReader


HERE = Path(__file__).resolve().parent
PUBLIC_URL = "https://simonh68.github.io/teachers/grade8/translation-challenge/"
PAGE_IDS = [[1, 2, 15, 16, 24, 25, 35], [36, 39, 43, 48, 52, 55, 70]]
W, H = A4
MARGIN = 34
RIGHT = W - MARGIN
WIDTH = W - 2 * MARGIN
INK = colors.HexColor("#172A3A")
MUTED = colors.HexColor("#536570")
LINE = colors.HexColor("#B9C5CC")
PALE = colors.HexColor("#F3F6F8")
ACCENT = colors.HexColor("#216A77")


def load_fonts() -> None:
    font_dir = Path("/usr/share/fonts/truetype/dejavu")
    for name, file in [("Body", "DejaVuSans.ttf"), ("Bold", "DejaVuSans-Bold.ttf")]:
        path = font_dir / file
        if not path.exists():
            raise RuntimeError(f"Required readable Hebrew/English font missing: {path}")
        pdfmetrics.registerFont(TTFont(name, str(path)))


class Bidi:
    """Use the system Unicode bidi implementation, not a naive string reversal."""

    def __init__(self) -> None:
        lib_path = ctypes.util.find_library("fribidi")
        if not lib_path:
            raise RuntimeError("The system FriBidi library is required for Hebrew text.")
        self.lib = ctypes.CDLL(lib_path)
        self.lib.fribidi_get_bidi_type.argtypes = [ctypes.c_uint32]
        self.lib.fribidi_get_bidi_type.restype = ctypes.c_uint32
        self.lib.fribidi_log2vis.argtypes = [
            ctypes.POINTER(ctypes.c_uint32), ctypes.c_int,
            ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint32),
            ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,
        ]
        self.lib.fribidi_log2vis.restype = ctypes.c_uint8

    def display(self, text: str) -> str:
        if not text:
            return text
        inp = (ctypes.c_uint32 * len(text))(*map(ord, text))
        out = (ctypes.c_uint32 * len(text))()
        direction = ctypes.c_uint32(self.lib.fribidi_get_bidi_type(ord("א")))
        self.lib.fribidi_log2vis(inp, len(text), ctypes.byref(direction), out, None, None, None)
        return "".join(map(chr, out))


BIDI: Bidi


def is_hebrew(text: str) -> bool:
    return any("\u0590" <= ch <= "\u05ff" for ch in text)


def visual(text: str) -> str:
    return BIDI.display(text) if is_hebrew(text) else text


def text_width(text: str, size: float, font: str = "Body") -> float:
    return pdfmetrics.stringWidth(visual(text), font, size)


def wrap(text: str, width: float, size: float, font: str = "Body") -> list[str]:
    """Wrap logical text before bidi so each printed Hebrew line has correct order."""
    lines: list[str] = []
    for paragraph in str(text).split("\n"):
        words = paragraph.split()
        line = ""
        for word in words:
            candidate = f"{line} {word}".strip()
            if line and text_width(candidate, size, font) > width:
                lines.append(line)
                line = word
            else:
                line = candidate
        lines.append(line)
    return lines or [""]


def draw_text(c: canvas.Canvas, text: str, x: float, y: float, size: float = 12.5,
              font: str = "Body", rtl: bool | None = None, color=INK) -> None:
    c.setFont(font, size)
    c.setFillColor(color)
    rtl = is_hebrew(text) if rtl is None else rtl
    if rtl:
        c.drawRightString(x, y, visual(text))
    else:
        c.drawString(x, y, text)


def draw_lines(c: canvas.Canvas, lines: list[str], x: float, y: float,
               size: float, leading: float, rtl: bool, font: str = "Body", color=INK) -> float:
    for line in lines:
        draw_text(c, line, x, y, size, font, rtl, color)
        y -= leading
    return y


def qr(c: canvas.Canvas, x: float, y: float, size: float = 67) -> None:
    code = QrCodeWidget(PUBLIC_URL, barLevel="M")
    x0, y0, x1, y1 = code.getBounds()
    drawing = Drawing(size, size, transform=[size / (x1 - x0), 0, 0, size / (y1 - y0), 0, 0])
    drawing.add(code)
    renderPDF.draw(drawing, c, x, y)
    c.linkURL(PUBLIC_URL, (x, y, x + size, y + size), relative=0, thickness=0)


def header(c: canvas.Canvas, page: int, teacher: bool) -> float:
    title = "Grade 8 | Teacher Key" if teacher else "Grade 8 | Translation Challenge"
    draw_text(c, title, MARGIN, H - 45, 20, "Bold", False)
    subtitle = "מפתח תשובות למורה" if teacher else "דף תרגול מלווה למצגת"
    draw_text(c, subtitle, RIGHT - 83, H - 69, 14, "Bold", True, ACCENT)
    qr(c, RIGHT - 67, H - 92)
    draw_text(c, "סרקו לפתיחת המצגת", RIGHT, H - 106, 8.7, "Body", True, MUTED)
    if teacher:
        draw_text(c, "תשובות אפשריות ל־14 הפריטים שבדף התרגול", RIGHT, H - 119, 11.2, "Body", True)
    else:
        draw_text(c, "שם: ____________________    כיתה: ________    תאריך: ____________",
                  RIGHT, H - 119, 10.8, "Body", True)
    instruction = (
        "קבלו גם תרגומים תקינים אחרים ששומרים על המשמעות ועל המבנה הנלמד."
        if teacher else
        "תרגמו או הקיפו תשובה אחת. מספר הפריט תואם למספר האתגר במצגת."
    )
    draw_text(c, instruction, RIGHT, H - 136, 10.1, "Body", True)
    c.setStrokeColor(ACCENT)
    c.setLineWidth(1)
    c.line(MARGIN, H - 146, RIGHT, H - 146)
    return H - 156


def level_label(item: dict) -> str:
    level = str(item.get("level", "")).lower()
    return {"easy": "קל", "low": "קל", "core": "רמת כיתה ח׳", "medium": "רמת כיתה ח׳",
            "hard": "מאתגר", "high": "מאתגר", "challenge": "מאתגר"}.get(level, level)


def options(item: dict) -> list[dict]:
    return list(item.get("options") or [])


def task_label(item: dict) -> str:
    if options(item):
        return "בחירה"
    return "תרגום לאנגלית" if item.get("sourceLang") == "he" else "תרגום לעברית"


def layout_item(item: dict, teacher: bool) -> dict:
    prompt_size = 12.1 if teacher else 12.7
    prompt_lines = wrap(item["prompt"], WIDTH - 20, prompt_size)
    cue_lines = wrap(str(item["cueHe"]), WIDTH - 20, 9.7) if item.get("cueHe") else []
    structure = {"prompt_lines": prompt_lines, "prompt_size": prompt_size, "cue_lines": cue_lines}
    height = 21 + len(prompt_lines) * 16
    height += len(cue_lines) * 13
    if teacher:
        answer = str(item["answer"])
        answer_lines = wrap(answer, WIDTH - 20, 12.7, "Bold")
        explanation = str(item.get("explanationHe") or "")
        explanation_lines = wrap(explanation, WIDTH - 20, 9.6)
        structure.update(answer_lines=answer_lines, explanation_lines=explanation_lines)
        height += 4 + len(answer_lines) * 16 + len(explanation_lines) * 12 + 7
    elif options(item):
        opt_rows = []
        for i, option in enumerate(options(item)):
            text = str(option["text"])
            opt_rows.append((chr(65 + i), wrap(text, WIDTH - 46, 11.4), is_hebrew(text)))
        structure["option_rows"] = opt_rows
        height += 3 + sum(len(row[1]) * 14.2 for row in opt_rows) + 8
    else:
        height += 37
    structure["height"] = height
    return structure


def item_card(c: canvas.Canvas, item: dict, top: float, height: float, layout: dict, teacher: bool) -> None:
    c.setFillColor(PALE)
    c.roundRect(MARGIN, top - 15, WIDTH, 16, 3, stroke=0, fill=1)
    label = f"אתגר {item['id']}  |  {level_label(item)}  |  {task_label(item)}"
    draw_text(c, label, RIGHT - 7, top - 10.5, 9.2, "Bold", True, MUTED)
    y = top - 32
    src_rtl = item.get("sourceLang") == "he"
    y = draw_lines(c, layout["prompt_lines"], RIGHT - 10 if src_rtl else MARGIN + 10,
                   y, layout["prompt_size"], 16, src_rtl)
    if layout["cue_lines"]:
        y = draw_lines(c, layout["cue_lines"], RIGHT - 10, y + 1, 9.7, 13, True, "Body", MUTED)
    if teacher:
        y -= 3
        answer_rtl = is_hebrew(str(item["answer"]))
        y = draw_lines(c, layout["answer_lines"], RIGHT - 10 if answer_rtl else MARGIN + 10,
                       y, 12.7, 16, answer_rtl, "Bold", ACCENT)
        if layout["explanation_lines"]:
            draw_lines(c, layout["explanation_lines"], RIGHT - 10, y - 1, 9.6, 12, True, "Body", MUTED)
    elif options(item):
        y -= 2
        for letter, lines, rtl in layout["option_rows"]:
            if rtl:
                draw_text(c, f"{letter}.", RIGHT - 26, y, 10.5, "Bold", False, MUTED)
                draw_lines(c, lines, RIGHT - 38, y, 11.4, 14.2, True)
            else:
                draw_text(c, f"{letter}.", MARGIN + 10, y, 10.5, "Bold", False, MUTED)
                draw_lines(c, lines, MARGIN + 31, y, 11.4, 14.2, False)
            y -= len(lines) * 14.2
    else:
        c.setStrokeColor(LINE)
        c.setLineWidth(0.55)
        c.line(MARGIN + 10, y - 5, RIGHT - 10, y - 5)
        c.line(MARGIN + 10, y - 22, RIGHT - 10, y - 22)


def footer(c: canvas.Canvas, page: int, teacher: bool) -> None:
    draw_text(c, PUBLIC_URL, MARGIN, 43, 8.2, "Body", False, MUTED)
    c.linkURL(PUBLIC_URL, (MARGIN, 40, RIGHT, 52), relative=0, thickness=0)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.55)
    c.line(MARGIN, 35, RIGHT, 35)
    draw_text(c, "TEACHER KEY" if teacher else "14 SELECTED CHALLENGES", MARGIN, 21, 8, "Bold", False, MUTED)
    draw_text(c, f"עמוד {page} מתוך 2", RIGHT, 21, 9, "Body", True, MUTED)


def build(path: Path, by_id: dict[int, dict], teacher: bool) -> None:
    c = canvas.Canvas(str(path), pagesize=A4, pageCompression=1)
    c.setTitle("Grade 8 Translation Challenge - Teacher Key" if teacher else "Grade 8 Translation Challenge - Companion Worksheet")
    c.setAuthor("Simon | Teachers")
    c.setSubject("14 selected challenges, matched by ID to the interactive Grade 8 presentation")
    for page_num, ids in enumerate(PAGE_IDS, 1):
        top = header(c, page_num, teacher)
        items = [by_id[i] for i in ids]
        layouts = [layout_item(item, teacher) for item in items]
        gap = 7
        required = sum(layout["height"] for layout in layouts) + gap * (len(items) - 1)
        available = top - 48
        if required > available:
            raise RuntimeError(f"Page {page_num} {'key' if teacher else 'worksheet'} overflows: {required:.1f} > {available:.1f} points")
        extra_each = (available - required) / len(items)
        for item, layout in zip(items, layouts):
            height = layout["height"] + extra_each
            item_card(c, item, top, height, layout, teacher)
            top -= height + gap
        footer(c, page_num, teacher)
        c.showPage()
    c.save()
    reader = PdfReader(path)
    assert len(reader.pages) == 2, f"Expected two A4 pages in {path.name}"
    for page in reader.pages:
        assert abs(float(page.mediabox.width) - W) < 0.1
        assert abs(float(page.mediabox.height) - H) < 0.1
    print(f"Created {path}: 2 A4 pages, {path.stat().st_size:,} bytes")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=HERE / "data.json")
    parser.add_argument("--outdir", type=Path, default=HERE)
    args = parser.parse_args()
    data = json.loads(args.data.read_text(encoding="utf-8"))
    by_id = {int(item["id"]): item for round_ in data["rounds"] for item in round_["items"]}
    expected = [i for page in PAGE_IDS for i in page]
    assert len(set(expected)) == 14
    assert all(i in by_id for i in expected), "Missing selected challenge in data.json"
    for i in expected:
        assert by_id[i].get("sourceLang") in {"he", "en"}
        if options(by_id[i]):
            assert sum(bool(o.get("correct")) for o in options(by_id[i])) == 1
    global BIDI
    BIDI = Bidi()
    load_fonts()
    args.outdir.mkdir(parents=True, exist_ok=True)
    build(args.outdir / "worksheet.pdf", by_id, teacher=False)
    build(args.outdir / "answer-key.pdf", by_id, teacher=True)
    print("Source challenge IDs:", PAGE_IDS)


if __name__ == "__main__":
    main()
