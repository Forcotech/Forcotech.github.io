#!/usr/bin/env python3
"""Prüfung der Firmenseite www.forcotech.com vor dem Veröffentlichen – wenige Sekunden, ohne Browser, ohne Netz.

Prüft alle ausgelieferten HTML-Seiten (ohne _src/ und tools/):
- interne Links und Bilder/Medien/Downloads zeigen auf vorhandene Dateien (Links auf /konfigurator/… werden übersprungen,
  der Konfigurator ist ein eigenes Repository),
- jede Seite hat <title>, Meta-Beschreibung und lang-Attribut,
- hreflang-Verweise zeigen auf vorhandene Seiten,
- jeder Eintrag in sitemap.xml existiert,
- keine eingebetteten Bilder (data:image) und kein Python-Cache im Repository.

    python3 tools/check.py      # Exitcode 1 bei Fehlern
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "www.forcotech.com"
SKIP_DIRS = {".git", ".github", "tools", "_src", "__pycache__"}

errors, notes = [], []


def pages():
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT)
        if SKIP_DIRS.intersection(rel.parts):
            continue
        yield p, rel


def resolve(ref, page):
    """Interne Adresse → Datei im Repository; None für externe Adressen und den Konfigurator."""
    ref = ref.strip()
    if not ref or ref.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return None
    u = urlsplit(ref)
    if u.scheme in ("http", "https") or ref.startswith("//"):
        if u.netloc.lower() != DOMAIN:
            return None
    elif u.scheme:
        return None
    path = unquote(u.path)
    if not path:
        return None
    if path.startswith("/konfigurator"):
        return None
    target = (ROOT / path.lstrip("/")) if path.startswith("/") else (page.parent / path)
    if path.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target


def check_pages():
    n = 0
    for p, rel in pages():
        n += 1
        s = p.read_text(encoding="utf-8", errors="replace")
        redirect = 'http-equiv="refresh"' in s.lower()
        if "data:image/" in s:
            errors.append(f"{rel}: eingebettetes Bild (data:image) – als Datei in img/ ablegen")
        if not redirect and rel.as_posix() != "404.html":
            if not re.search(r"<title>\s*\S", s):
                errors.append(f"{rel}: <title> fehlt")
            if not re.search(r'<meta\s+name="description"\s+content="\s*\S', s):
                notes.append(f"{rel}: Meta-Beschreibung fehlt")
            if not re.search(r"<html[^>]*\blang=", s):
                errors.append(f"{rel}: lang-Attribut fehlt")
        for attr, ref in re.findall(r'\b(href|src|poster|data-src)="([^"]*)"', s):
            if "{" in ref or "${" in ref or "'" in ref or "+" in ref:
                continue
            t = resolve(ref, p)
            if t is not None and not t.exists():
                errors.append(f"{rel}: {attr} zeigt ins Leere: {ref}")
        for ref in re.findall(r'srcset="([^"]*)"', s):
            for part in ref.split(","):
                u = part.strip().split(" ")[0]
                t = resolve(u, p)
                if t is not None and not t.exists():
                    errors.append(f"{rel}: srcset zeigt ins Leere: {u}")
        for ref in re.findall(r'url\((["\']?)([^)"\']+)\1\)', s):
            t = resolve(ref[1], p)
            if t is not None and not t.exists():
                errors.append(f"{rel}: url() zeigt ins Leere: {ref[1]}")
    print(f"Seiten: {n} geprüft")


def check_css():
    css = ROOT / "style.css"
    if css.exists():
        for _, ref in re.findall(r'url\((["\']?)([^)"\']+)\1\)', css.read_text(encoding="utf-8")):
            t = resolve(ref, css)
            if t is not None and not t.exists():
                errors.append(f"style.css: url() zeigt ins Leere: {ref}")


def check_sitemap():
    sm = ROOT / "sitemap.xml"
    if not sm.exists():
        errors.append("sitemap.xml fehlt")
        return
    locs = re.findall(r"<loc>([^<]+)</loc>", sm.read_text(encoding="utf-8"))
    alts = re.findall(r'hreflang="[^"]+"\s+href="([^"]+)"', sm.read_text(encoding="utf-8"))
    for u in locs + alts:
        t = resolve(u, sm)
        if t is not None and not t.exists():
            errors.append(f"sitemap.xml: Seite fehlt: {u}")
    print(f"Sitemap: {len(locs)} Adressen geprüft")


def check_repo():
    ignoriert = "__pycache__" in ((ROOT / ".gitignore").read_text() if (ROOT / ".gitignore").exists() else "")
    for d in ([] if ignoriert else ROOT.rglob("__pycache__")):
        if ".git" not in d.parts:
            notes.append(f"{d.relative_to(ROOT)}: Python-Cache gehört nicht ins Repository (.gitignore)")
    if not (ROOT / "CNAME").exists() or (ROOT / "CNAME").read_text().strip() != DOMAIN:
        errors.append(f"CNAME fehlt oder ist nicht {DOMAIN} – sonst ist die Domain weg")


def main():
    check_repo()
    check_pages()
    check_css()
    check_sitemap()
    for n in notes:
        print("HINWEIS ", n)
    for e in errors:
        print("FEHLER  ", e)
    print("OK – keine Fehler." if not errors else f"{len(errors)} Fehler.")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
