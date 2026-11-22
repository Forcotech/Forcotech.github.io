#!/usr/bin/env python3
# © Silent Engineering di Romolo Vicari – ForCoTech
"""Italienische (it/) und spanische (es/) Fassung der Firmenseite – erzeugt aus den englischen Seiten.

Wie beim Konfigurator ist die englische Seite die Vorlage: Die fertig gebauten EN-Seiten werden gelesen, ihre Texte
(Absätze, Überschriften, Listen, Bildtexte, alt/title/aria-label, Meta-Beschreibung, JSON-LD) über die Wörterbücher
tools/sprachen/it.json bzw. es.json übersetzt. Kopf, Navigation, Anfrageformular und Fuß kommen wie bei allen
Unterseiten aus tools/build_news.py (page()), die Startseite zusätzlich aus tools/startseite_anfrage.py.

Seiten (Stufe 1, 22.11.2026): Startseite, Technik, IoT, Impressum, Datenschutz. Weitere Seiten in PAGES ergänzen.
Grafiken, Zeichnungen und Videos mit Text bleiben vorerst in der englischen Fassung.

Aufruf (nach den Builds der EN-Seiten, vor tools/build_news.py):
    python3 tools/build_sprachen.py            # baut it/… und es/…
    python3 tools/build_sprachen.py --report   # zusätzlich tools/sprachen/missing-<lang>.json (nicht einchecken)
Die erzeugten Seiten nicht von Hand ändern – Texte im Wörterbuch korrigieren und das Skript erneut ausführen.
"""
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_news as bn  # noqa: E402
import startseite_anfrage as sa  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
HERE = ROOT / "tools" / "sprachen"
LANGS = ("it", "es")

# EN-Pfad → Pfad je Sprache (auch für das Umschreiben von Links)
PATHS = bn.IT_ES
# Alle Sprachfassungen je Seite (für hreflang und Sprachumschalter)
ALTS = {
    "/en/technology/": {"de": "/technik/", "en": "/en/technology/", "fr": "/fr/technique/"},
    "/en/iot/": {"de": "/iot/", "en": "/en/iot/", "fr": "/fr/iot/"},
    "/en/legal-notice/": {"de": "/impressum/", "en": "/en/legal-notice/", "fr": "/fr/mentions-legales/"},
    "/en/privacy/": {"de": "/datenschutz/", "en": "/en/privacy/", "fr": "/fr/confidentialite/"},
}
TYP = {"/en/iot/": "iot"}  # Vorauswahl im Anfrageformular
NO_CTA = {"/en/legal-notice/", "/en/privacy/"}

INLINE = {"a", "b", "i", "em", "strong", "sub", "sup", "br", "span", "small", "code", "abbr", "time", "u", "s", "mark"}
ATTRS = ("alt", "title", "aria-label", "placeholder")
MISSING = {}


def load(lang):
    d = json.loads((HERE / f"{lang}.json").read_text(encoding="utf-8"))
    return {k: v for k, v in d.items() if not k.startswith("//")}


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def look(d, key, page):
    k = norm(key)
    if not re.search(r"[A-Za-z]{2}", re.sub(r"<[^>]+>|&\w+;", "", k)):
        return None
    if k in d:
        return d[k]
    MISSING.setdefault(k, set()).add(page)
    return None


def tr_attrs(tag, d, page):
    def rep(m):
        name, val = m.group(1), m.group(2)
        raw = html.unescape(val)
        if raw.startswith(("http", "/", "#", "data:")):
            return m.group(0)
        r = look(d, raw, page)
        return m.group(0) if r is None else f' {name}="{html.escape(r, quote=True)}"'
    tag = re.sub(r'\s(%s)="([^"]*)"' % "|".join(ATTRS), rep, tag)
    if tag.startswith("<meta") and re.search(r'name="description"|property="og:(title|description)"', tag):
        tag = re.sub(r'\scontent="([^"]*)"', lambda m: (lambda r: m.group(0) if r is None else f' content="{html.escape(r, quote=True)}"')(look(d, html.unescape(m.group(1)), page)), tag)
    return tag


def tr_jsonld(s, d, page):
    def walk(o):
        if isinstance(o, dict):
            return {k: (v if k in ("@id", "@type", "@context", "url", "email", "vatID", "sameAs", "image", "logo") else walk(v)) for k, v in o.items()}
        if isinstance(o, list):
            return [walk(x) for x in o]
        if isinstance(o, str):
            r = look(d, o, page)
            return o if r is None else r
        return o
    return json.dumps(walk(json.loads(s)), ensure_ascii=False)


def translate(h, d, page):
    """Text-Abschnitte (Text mit Inline-Tags zwischen Block-Tags) und Attribute übersetzen."""
    out, run = [], []

    def flush():
        if not run:
            return
        seg = "".join(run)
        run.clear()
        if not re.search(r"[A-Za-z]{2}", re.sub(r"<[^>]+>", "", seg)):
            out.append(seg)
            return
        r = look(d, seg, page)
        if r is None:
            out.append(seg)
        else:
            lead = re.match(r"\s*", seg).group(0)
            trail = re.search(r"\s*$", seg).group(0)
            out.append(lead + r + trail)
    pos = 0
    for m in re.finditer(r"<script[^>]*>.*?</script>|<style[^>]*>.*?</style>|<!--.*?-->|<[^>]+>", h, re.S):
        text = h[pos:m.start()]
        if text:
            run.append(text)
        tag = m.group(0)
        pos = m.end()
        if tag.startswith("<script"):
            flush()
            mm = re.match(r"(<script[^>]*ld\+json[^>]*>)(.*)</script>", tag, re.S)
            out.append(mm.group(1) + tr_jsonld(mm.group(2), d, page) + "</script>" if mm else tag)
            continue
        if tag.startswith(("<style", "<!--")):
            flush()
            out.append(tag)
            continue
        name = re.match(r"</?([a-zA-Z0-9]+)", tag)
        name = name.group(1).lower() if name else ""
        tag = tr_attrs(tag, d, page)
        if name in INLINE:
            run.append(tag)
        else:
            flush()
            out.append(tag)
    if h[pos:]:
        run.append(h[pos:])
    flush()
    return "".join(out)


def links(s, lang):
    for en, t in sorted(PATHS.items(), key=lambda x: -len(x[0])):
        s = re.sub(r'href="(?:https://www\.forcotech\.com)?' + re.escape(en) + r'(#[^"]*)?"', lambda m: f'href="{t[lang]}{m.group(1) or ""}"', s)
    s = s.replace("https://www.forcotech.com/konfigurator/en/", f"https://www.forcotech.com/konfigurator/{lang}/")
    return s


def subpage(en_path, lang, d):
    src = (ROOT / en_path[1:] / "index.html").read_text(encoding="utf-8")
    title = html.unescape(re.search(r"<title>(.*?)</title>", src, re.S).group(1))
    desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', src).group(1))
    main = re.search(r'<main id="main">\n?(.*)</main>', src, re.S).group(1)
    main = re.sub(r'\n?<section id="anfrage">.*?</section>\s*$', "", main, flags=re.S)  # Formular kommt aus page()
    head = "".join(re.findall(r'<script type="application/ld\+json">.*?</script>', src.split("</head>")[0], re.S))
    page = en_path
    t_title, t_desc = look(d, title, page) or title, look(d, desc, page) or desc
    main = links(translate(main, d, page), lang)
    head = translate(head, d, page) if head else ""
    alts = dict(ALTS[en_path])
    alts.update({k: v for k, v in ((l, PATHS[en_path][l]) for l in LANGS)})
    out = bn.page(lang, t_title, t_desc, alts, main, extra_head=head, cta=en_path not in NO_CTA, typ=TYP.get(en_path))
    bn.write(PATHS[en_path][lang][1:] + "index.html", out)
    print(f"{PATHS[en_path][lang]}index.html", len(out))


def home(lang, d):
    src = (ROOT / "en/index.html").read_text(encoding="utf-8")
    # Blöcke, die IT/ES nicht hat oder die anders entstehen
    src = re.sub(r"<!-- AUFBAU:START.*?<!-- AUFBAU:END -->\n?", "", src, flags=re.S)
    src = re.sub(r"<!-- NEWS:START.*?<!-- NEWS:END -->\n?", "", src, flags=re.S)
    src = re.sub(r'<section id="contact">.*?</section>', '<section id="contact"></section>', src, flags=re.S)
    src = re.sub(r'<h1>.*?</h1>\s*<p class="lead">.*?</p>', "<h1></h1>\n      <p class=\"lead\"></p>", src, count=1, flags=re.S)
    s = links(translate(src, d, "/en/"), lang)
    L = bn.T[lang]
    s = s.replace('<html lang="en">', f'<html lang="{lang}">', 1)
    s = s.replace('content="en_GB"', f'content="{L["locale"]}"')
    s = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{bn.SITE}/{lang}/">', s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{bn.SITE}/{lang}/">', s, count=1)
    alts = {"de": "/", "en": "/en/", "fr": "/fr/", "it": "/it/", "es": "/es/"}
    hl = "\n".join(f'<link rel="alternate" hreflang="{k}" href="{bn.SITE}{v}">' for k, v in alts.items())
    hl += f'\n<link rel="alternate" hreflang="x-default" href="{bn.SITE}/">'
    s = re.sub(r'(?:<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?)+', hl + "\n", s, count=1)
    s = s.replace('"inLanguage":"en"', f'"inLanguage":"{lang}"').replace('"inLanguage": "en"', f'"inLanguage": "{lang}"')
    # Kopf: Navigation und Sprachumschalter wie auf den Unterseiten
    nav = "\n      ".join(f'<a class="opt" href="{h if h.startswith("/") else L["home"] + h}">{n}</a>' for h, n in L["nav"])
    switch = "\n      ".join(f'<a class="lang" href="{alts[k]}" lang="{k}" hreflang="{k}">{k.upper()}</a>' for k in bn.LANGS if k != lang)
    s = re.sub(r'(<nav class="nav"[^>]*>).*?(</nav>)', lambda m: f'{m.group(1)}\n      {nav}\n      <a class="cta" href="{L["cfg"][0]}">{L["cfg"][1]}</a>\n      {switch}\n    {m.group(2)}', s, count=1, flags=re.S)
    s = re.sub(r'<a class="logo" href="[^"]*" aria-label="[^"]*">', f'<a class="logo" href="{L["home"]}" aria-label="{L["home_label"]}">', s, count=1)
    # Fuß: Rechtliches und Sprachen
    foot_lang = " · ".join(f'<a href="{alts[k]}" lang="{k}">{bn.LANG_NAME[k]}</a>' for k in bn.LANGS if k != lang)
    it, al = bn.COUNTRY[lang]
    s = re.sub(r"(<footer>.*?<span>)©.*?(</span>)", lambda m: m.group(1) + bn.FOOT.format(y=bn.date.today().year, it=it, al=al) + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'(<footer>.*?<span>©.*?</span>\s*<span>).*?(</span>)', lambda m: m.group(1) + f'<a href="{L["imprint_url"]}">{L["imprint"]}</a> · <a href="{L["privacy_url"]}">{L["privacy"]}</a> · {foot_lang}' + m.group(2), s, count=1, flags=re.S)
    out = ROOT / lang / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(s, encoding="utf-8")
    print(f"/{lang}/index.html", len(s))


def update_homes():
    """DE/EN/FR-Startseiten (Handseiten): IT und ES in hreflang, Sprachumschalter und Fuß ergänzen (wiederholbar)."""
    for f, up in (("index.html", ""), ("en/index.html", "../"), ("fr/index.html", "../")):
        p = ROOT / f
        s = p.read_text(encoding="utf-8")
        o = s
        for lg in LANGS:
            if f'hreflang="{lg}" href="{bn.SITE}/{lg}/"' not in s:
                s = s.replace('<link rel="alternate" hreflang="x-default"',
                              f'<link rel="alternate" hreflang="{lg}" href="{bn.SITE}/{lg}/">\n<link rel="alternate" hreflang="x-default"', 1)
            if f'class="lang" href="{up}{lg}/"' not in s:
                last = list(re.finditer(r'\n(\s*)<a class="lang" [^>]*>[A-Z]{2}</a>', s))[-1]
                s = s[:last.end()] + f'\n{last.group(1)}<a class="lang" href="{up}{lg}/" lang="{lg}" hreflang="{lg}">{lg.upper()}</a>' + s[last.end():]
            if f'lang="{lg}">{bn.LANG_NAME[lg]}</a>' not in s:
                m = list(re.finditer(r'<footer>.*?(<a href="[^"]*" lang="[a-z]{2}">[^<]+</a>)(</span>)', s, re.S))[-1]
                s = s[:m.end(1)] + f' · <a href="{up}{lg}/" lang="{lg}">{bn.LANG_NAME[lg]}</a>' + s[m.end(1):]
        if s != o:
            p.write_text(s, encoding="utf-8")


def main():
    update_homes()
    for lang in LANGS:
        MISSING.clear()
        d = load(lang)
        home(lang, d)
        for p in ALTS:
            subpage(p, lang, d)
        if "--report" in sys.argv:
            (HERE / f"missing-{lang}.json").write_text(json.dumps(sorted(MISSING), ensure_ascii=False, indent=0), encoding="utf-8")
            print(f"{lang}: {len(MISSING)} Texte ohne Übersetzung → tools/sprachen/missing-{lang}.json")
    sa.main()  # Claim und Anfrageformular der Startseiten (auch IT/ES)


if __name__ == "__main__":
    main()
