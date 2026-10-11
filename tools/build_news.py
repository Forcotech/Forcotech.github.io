#!/usr/bin/env python3
# © Silent Engineering di Romolo Vicari – ForCoTech
"""Baut den News-Bereich der Visitenkarte aus news/posts.json.

Neuer Beitrag:
  1. Bild nach img/news/<name>.webp legen
  2. Eintrag in news/posts.json ergänzen (slug, date, image, de/en: title, alt, teaser)
  3. Text als HTML-Fragment in news/_src/<slug>.de.html und news/_src/<slug>.en.html
  4. status auf "online" setzen und  python3 tools/build_news.py  ausführen

Erzeugt bzw. aktualisiert:
  - Vorschau der 3 neuesten Beiträge auf index.html und en/index.html (zwischen NEWS-Markern)
  - Übersichten news/index.html und en/news/index.html
  - Beitragsseiten news/<slug>/ und en/news/<slug>/
  - sitemap.xml und den News-Abschnitt in llms.txt

Option --alle nimmt auch Entwürfe mit (nur für lokale Vorschau, nicht veröffentlichen).
"""
import html, json, re, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://forcotech.github.io"
ALLE = "--alle" in sys.argv

T = {
    "de": {
        "lang": "de", "home": "/", "news": "/news/", "other": "en",
        "h_pre": "News und", "h_acc": "Analysen",
        "sub": "Projekte, Messungen und Hintergründe aus der Auslegung unserer Schallhauben.",
        "all": "Alle Beiträge", "back": "Alle Beiträge", "skip": "Zum Inhalt",
        "nav": [("#leistungen", "Leistungen"), ("#hsa3", "HSA3"), ("#technik", "Technik"),
                ("/news/", "News"), ("#ueber-uns", "Über uns"), ("#kontakt", "Kontakt")],
        "cfg": ("https://forcotech.github.io/konfigurator/", "Konfigurator"),
        "nav_label": "Hauptnavigation", "home_label": "ForCoTech Startseite",
        "title_list": "News und Analysen – ForCoTech Schallhauben",
        "desc_list": "News und Analysen von ForCoTech: Projekte, Messungen und Hintergründe zu Schallhauben für Wärmepumpen, Kälteanlagen, VRF und PV-Wechselrichter.",
        "cta_h": "Projekt anfragen",
        "cta_p": "Schicken Sie uns Gerätetyp, Anzahl und Aufstellort – oder holen Sie sich direkt einen Richtpreis im Konfigurator.",
        "cta_b": "Zum Konfigurator", "privacy": "Datenschutz", "other_name": "English",
        "empty": "Hier erscheinen in Kürze unsere ersten Beiträge.",
        "months": None, "locale": "de_DE",
    },
    "en": {
        "lang": "en", "home": "/en/", "news": "/en/news/", "other": "de",
        "h_pre": "News and", "h_acc": "analyses",
        "sub": "Projects, measurements and background from the design of our acoustic enclosures.",
        "all": "All posts", "back": "All posts", "skip": "Skip to content",
        "nav": [("#services", "Applications"), ("#hsa3", "HSA3"), ("#technology", "Technology"),
                ("/en/news/", "News"), ("#about", "About us"), ("#contact", "Contact")],
        "cfg": ("https://forcotech.github.io/konfigurator/en/", "Configurator"),
        "nav_label": "Main navigation", "home_label": "ForCoTech home",
        "title_list": "News and analyses – ForCoTech acoustic enclosures",
        "desc_list": "News and analyses from ForCoTech: projects, measurements and background on acoustic enclosures for heat pumps, chillers, VRF and PV inverters.",
        "cta_h": "Request a project",
        "cta_p": "Send us the unit type, quantity and location – or get a budget price straight from the configurator.",
        "cta_b": "Open configurator", "privacy": "Privacy", "other_name": "Deutsch",
        "empty": "Our first posts will appear here shortly.",
        "months": None, "locale": "en_GB",
    },
}
LOGO_ALT = "ForCoTech – Stop Noise · Enjoy Silence · Improve Efficiency – Engineered with Absora Technology"
FOOT = "© {y} Silent Engineering di Romolo Vicari · Via Trento 22 · 23875 Osnago (LC) · {it} · P.IVA IT03833150133 · {al} ABSORA GmbH, Berlin"

e = html.escape


def fmt(d):
    y, m, dd = d.split("-")
    return f"{dd}.{m}.{y}"


def url(lang, slug=None):
    base = T[lang]["news"]
    return base + (slug + "/" if slug else "")


def load():
    posts = json.loads((ROOT / "news/posts.json").read_text(encoding="utf-8"))
    posts = [p for p in posts if ALLE or p.get("status") == "online"]
    return sorted(posts, key=lambda p: p["date"], reverse=True)


def body(slug, lang):
    f = ROOT / f"news/_src/{slug}.{lang}.html"
    return f.read_text(encoding="utf-8").strip() if f.exists() else ""


def card(p, lang, h="h3", lazy=True):
    t = p[lang]
    teaser = f'<p>{e(t["teaser"])}</p>' if t.get("teaser") else ""
    return (f'<article class="ncard"><a href="{url(lang, p["slug"])}">'
            f'<img src="/{p["image"]}" width="522" height="313" alt="{e(t["alt"])}"{' loading="lazy"' if lazy else ""}>'
            f'<time datetime="{p["date"]}">{fmt(p["date"])}</time>'
            f'<{h}>{e(t["title"])}</{h}>{teaser}</a></article>')


def teaser_section(posts, lang):
    L = T[lang]
    if not posts:
        return ""
    cards = "\n      ".join(card(p, lang) for p in posts[:3])
    more = f'<p class="nmore"><a href="{L["news"]}">{L["all"]} →</a></p>'
    return f"""<section id="news">
  <div class="wrap">
    <h2 class="nh">{L["h_pre"]} <span>{L["h_acc"]}</span></h2>
    <div class="ngrid">
      {cards}
    </div>
    {more}
  </div>
</section>"""


def page(lang, title, desc, canon, alt_url, main, og_image=None, extra_head=""):
    L = T[lang]
    nav = "\n      ".join(
        f'<a class="opt" href="{h if h.startswith("/") else L["home"] + h}">{n}</a>' for h, n in L["nav"])
    other = T[L["other"]]
    og = f'<meta property="og:image" content="{SITE}/{og_image}">' if og_image else ""
    it, al = ("Italien", "in Allianz mit") if lang == "de" else ("Italy", "in alliance with")
    return f"""<!doctype html>
<!-- © Silent Engineering di Romolo Vicari, Osnago (LC), Italien – Alle Rechte vorbehalten. -->
<!-- Automatisch erzeugt mit tools/build_news.py – Änderungen in news/posts.json bzw. news/_src/ vornehmen. -->
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<link rel="canonical" href="{SITE}{canon}">
<link rel="alternate" hreflang="{lang}" href="{SITE}{canon}">
<link rel="alternate" hreflang="{L['other']}" href="{SITE}{alt_url}">
<meta property="og:type" content="{'article' if og_image else 'website'}">
<meta property="og:site_name" content="ForCoTech">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{canon}">
{og}
<meta property="og:locale" content="{L['locale']}">
<link rel="icon" href="/img/forcotech-logo.png">
<link rel="stylesheet" href="/style.css">
{extra_head}
</head>
<body>
<a class="skip" href="#main">{L["skip"]}</a>
<header class="top">
  <div class="wrap">
    <a class="logo" href="{L['home']}" aria-label="{L['home_label']}"><img src="/img/forcotech-logo.png" width="415" height="231" alt="{LOGO_ALT}"></a>
    <nav class="nav" aria-label="{L['nav_label']}">
      {nav}
      <a class="cta" href="{L['cfg'][0]}">{L['cfg'][1]}</a>
      <a class="lang" href="{alt_url}" lang="{L['other']}" hreflang="{L['other']}">{L['other'].upper()}</a>
    </nav>
  </div>
</header>

<main id="main">
{main}
<section>
  <div class="wrap">
    <div class="contact">
      <div>
        <h2>{L["cta_h"]}</h2>
        <p>{L["cta_p"]}</p>
        <div class="btns" style="margin-top:18px"><a class="btn" href="{L['cfg'][0]}">{L["cta_b"]}</a><a class="btn" href="mailto:info@forcotech.com">info@forcotech.com</a></div>
      </div>
      <address><b>Silent Engineering di Romolo Vicari</b><br>ForCoTech · Silent-Mode<br>Via Trento 22 · 23875 Osnago (LC) · {it}<br>E-Mail: <a href="mailto:info@forcotech.com">info@forcotech.com</a></address>
    </div>
  </div>
</section>
</main>

<footer>
  <div class="wrap">
    <span>{FOOT.format(y=date.today().year, it=it, al=al)}</span>
    <span><a href="https://silent-mode.com/datenschutz">{L["privacy"]}</a> · <a href="{alt_url}" lang="{L['other']}">{L["other_name"]}</a></span>
  </div>
</footer>
</body>
</html>
"""


def write(rel, text):
    f = ROOT / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text, encoding="utf-8")


def build():
    posts = load()
    other_of = {"de": "en", "en": "de"}

    for lang in ("de", "en"):
        L = T[lang]
        # Übersicht
        if posts:
            grid = "\n      ".join(card(p, lang, "h2", lazy=i > 2) for i, p in enumerate(posts))
            grid = f'<div class="ngrid">\n      {grid}\n    </div>'
        else:
            grid = f'<p class="sub">{L["empty"]}</p>'
        main = f"""<section class="nlist">
  <div class="wrap">
    <h1 class="nh">{L["h_pre"]} <span>{L["h_acc"]}</span></h1>
    <p class="sub">{L["sub"]}</p>
    {grid}
  </div>
</section>"""
        write(url(lang)[1:] + "index.html",
              page(lang, L["title_list"], L["desc_list"], url(lang), url(other_of[lang]), main))

        # Beitragsseiten
        for p in posts:
            t = p[lang]
            desc = t.get("teaser") or t["title"]
            ld = json.dumps({
                "@context": "https://schema.org", "@type": "BlogPosting", "headline": t["title"],
                "datePublished": p["date"], "dateModified": p.get("updated", p["date"]),
                "inLanguage": lang, "image": f"{SITE}/{p['image']}", "mainEntityOfPage": SITE + url(lang, p["slug"]),
                "author": {"@type": "Person", "name": "Romolo Vicari"},
                "publisher": {"@id": f"{SITE}/#org", "@type": "Organization", "name": "Silent Engineering di Romolo Vicari",
                              "logo": {"@type": "ImageObject", "url": f"{SITE}/img/forcotech-logo.png"}},
            }, ensure_ascii=False)
            content = body(p["slug"], lang)
            main = f"""<article class="npost">
  <div class="wrap">
    <p class="nback"><a href="{url(lang)}">← {L["back"]}</a></p>
    <time datetime="{p["date"]}">{fmt(p["date"])}</time>
    <h1>{e(t["title"])}</h1>
    <figure><img src="/{p["image"]}" width="522" height="313" alt="{e(t["alt"])}" fetchpriority="high"></figure>
    <div class="nbody">
{content}
    </div>
  </div>
</article>"""
            write(url(lang, p["slug"])[1:] + "index.html",
                  page(lang, f'{t["title"]} – ForCoTech', desc, url(lang, p["slug"]),
                       url(other_of[lang], p["slug"]), main, og_image=p["image"],
                       extra_head=f'<script type="application/ld+json">{ld}</script>'))

        # Startseite
        home = ROOT / ("index.html" if lang == "de" else "en/index.html")
        s = home.read_text(encoding="utf-8")
        block = "<!-- NEWS:START (automatisch, tools/build_news.py) -->\n" + teaser_section(posts, lang) + "\n<!-- NEWS:END -->"
        s, n = re.subn(r"<!-- NEWS:START.*?<!-- NEWS:END -->", block, s, flags=re.S)
        if n != 1:
            sys.exit(f"NEWS-Marker in {home} nicht gefunden")
        home.write_text(s, encoding="utf-8")

    # Sitemap
    today = date.today().isoformat()
    def u(loc, alt, alang, lm):
        return (f'  <url><loc>{SITE}{loc}</loc><lastmod>{lm}</lastmod>'
                f'<xhtml:link rel="alternate" hreflang="{alang}" href="{SITE}{alt}"/></url>')
    lines = [u("/", "/en/", "en", today), u("/en/", "/", "de", today),
             u("/news/", "/en/news/", "en", today), u("/en/news/", "/news/", "de", today)]
    for p in posts:
        lm = p.get("updated", p["date"])
        lines += [u(url("de", p["slug"]), url("en", p["slug"]), "en", lm),
                  u(url("en", p["slug"]), url("de", p["slug"]), "de", lm)]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
          + "\n".join(lines) + "\n</urlset>\n")

    # llms.txt
    f = ROOT / "llms.txt"
    s = f.read_text(encoding="utf-8")
    items = "\n".join(f'- [{p["en"]["title"]}]({SITE}{url("en", p["slug"])}) ({p["date"]}, Deutsch: {SITE}{url("de", p["slug"])})' for p in posts)
    block = f"<!-- NEWS:START -->\n## News and analyses\n- [News (Deutsch)]({SITE}/news/) · [News (English)]({SITE}/en/news/)\n{items}\n<!-- NEWS:END -->"
    if "<!-- NEWS:START -->" in s:
        s = re.sub(r"<!-- NEWS:START -->.*?<!-- NEWS:END -->", block, s, flags=re.S)
    else:
        s = s.rstrip() + "\n\n" + block + "\n"
    f.write_text(s, encoding="utf-8")
    print(f"{len(posts)} Beitrag/Beiträge gebaut" + (" (inkl. Entwürfe)" if ALLE else ""))


if __name__ == "__main__":
    build()
