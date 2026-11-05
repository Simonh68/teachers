"""Attach anonymous counters only to published, catalogued HTML materials."""
import html
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

root = Path("public").resolve()
tracked = set()
for manifest in sorted((root / "data").glob("grade*.json")):
    for item in json.loads(manifest.read_text())["materials"]:
        url = urlsplit(item["url"])
        if url.scheme or url.netloc or url.path.startswith("/"):
            continue
        path = (root / unquote(url.path)).resolve()
        if not path.is_relative_to(root):
            continue
        if path.is_dir():
            path = path / "index.html"
        if path.suffix.lower() not in {".html", ".htm"} or not path.is_file() or path in tracked:
            continue
        source = path.read_text(encoding="utf-8")
        index = source.lower().rfind("</body>")
        if index < 0:
            index = source.lower().rfind("</html>")
        if index < 0:
            index = len(source)
        attribute = html.escape("/teachers/" + url.path, quote=True)
        tag = f'<script defer src="https://englishfornoar.co.il/teacher-visits.js" data-material="{attribute}"></script>'
        path.write_text(source[:index] + tag + source[index:], encoding="utf-8")
        tracked.add(path)
print(f"Connected {len(tracked)} catalogue pages.")
if not tracked:
    raise SystemExit("No catalogue pages found")
