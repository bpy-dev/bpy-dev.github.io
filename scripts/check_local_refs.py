#!/usr/bin/env python3
"""Fail when deployable HTML/CSS references a missing local file."""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

SKIP_SCHEMES = {"http", "https", "mailto", "tel", "data", "javascript"}
CSS_URL = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.I)


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.values: list[str] = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        for key in ("href", "src", "poster"):
            value = values.get(key)
            if value:
                self.values.append(value)
        srcset = values.get("srcset")
        if srcset:
            self.values.extend(item.strip().split()[0] for item in srcset.split(","))


def is_local(value: str) -> bool:
    parsed = urlparse(value)
    return not parsed.scheme and not parsed.netloc and bool(parsed.path)


def resolve(root: Path, source: Path, value: str) -> Path:
    path = unquote(urlparse(value).path)
    if path.startswith("/"):
        return root / path.lstrip("/")
    return source.parent / path


def collect(root: Path) -> list[tuple[Path, str]]:
    references: list[tuple[Path, str]] = []
    for html in sorted(root.rglob("*.html")):
        if ".git" in html.parts:
            continue
        parser = References()
        parser.feed(html.read_text(encoding="utf-8"))
        references.extend((html, value) for value in parser.values if is_local(value))
    for css in sorted(root.rglob("*.css")):
        if ".git" in css.parts:
            continue
        for _, value in CSS_URL.findall(css.read_text(encoding="utf-8")):
            if is_local(value):
                references.append((css, value))
    return references


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    missing = []
    references = collect(root)
    for source, value in references:
        target = resolve(root, source, value)
        if target.is_dir():
            target = target / "index.html"
        if not target.exists():
            missing.append((source.relative_to(root), value))
    for source, value in missing:
        print(f"MISSING {source}: {value}")
    print(f"Checked {len(references)} local references; {len(missing)} missing local references")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
